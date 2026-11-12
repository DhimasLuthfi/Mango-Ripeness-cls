"""Mango Ripeness Classification Model Engine.

Handles YOLOv8-cls model loading with caching, in-memory image preprocessing,
and prediction probability extraction.
"""

from typing import Dict, Any, Optional
import os
import numpy as np
from PIL import Image, UnidentifiedImageError
import streamlit as st
from ultralytics import YOLO

# -----------------------------------------------------------------------------
# Ripeness Stage Metadata Definitions
# -----------------------------------------------------------------------------
STAGE_MAPPING = {
    0: {
        "name": "Stage 0: Mentah (Unripe)",
        "badge": "Mentah",
        "color": "#5e8c55",
        "description": "Hijau & keras",
        "tip": "Buah masih hijau pekat dan keras. Cocok untuk rujak atau simpan beberapa hari lagi di suhu ruang.",
    },
    1: {
        "name": "Stage 1: Mulai Matang (Early Ripe)",
        "badge": "Mulai Matang",
        "color": "#8fae3f",
        "description": "Semburat kuning samar",
        "tip": "Buah mulai mengalami pematangan dengan rona kuning tipis. Simpan di tempat sejuk berventilasi.",
    },
    2: {
        "name": "Stage 2: Setengah Matang (Partially Ripe)",
        "badge": "Setengah Matang",
        "color": "#d8a31f",
        "description": "Kuning & hijau seimbang",
        "tip": "Perpaduan warna hijau dan kuning merata dengan aroma manis lembut. Sudah nikmat dikonsumsi jika suka rasa asam-manis segar.",
    },
    3: {
        "name": "Stage 3: Matang Penuh (Ripe)",
        "badge": "Matang",
        "color": "#e8742c",
        "description": "Kuning & siap makan",
        "tip": "Buah matang sempurna dengan warna kuning keemasan/oranye, tekstur lembut, aroma harum, dan rasa manis maksimal.",
    },
}


# -----------------------------------------------------------------------------
# Model Caching & Loading Pipeline
# -----------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_yolo_model(weights_path: str = "best.pt") -> Optional[YOLO]:
    """Loads and caches the YOLOv8 classification model into RAM.

    Args:
        weights_path: Path to the trained weights file.

    Returns:
        YOLO: Instantiated model object, or None if loading fails.
    """
    if not os.path.exists(weights_path):
        st.error(
            f"Model weights file `{weights_path}` not found. "
            "Please ensure `best.pt` is in the project root directory."
        )
        return None

    try:
        model = YOLO(weights_path)
        return model
    except Exception as exc:
        st.error(f"Failed to load YOLOv8 model from `{weights_path}`: {exc}")
        return None


# -----------------------------------------------------------------------------
# Image Preprocessing Pipeline (100% In-Memory RAM)
# -----------------------------------------------------------------------------
def preprocess_image(image: Image.Image) -> Optional[np.ndarray]:
    """Preprocesses a PIL Image into an RGB NumPy array in memory.

    Args:
        image: User-provided PIL Image.

    Returns:
        np.ndarray: Image array formatted as RGB, or None on error.
    """
    try:
        rgb_image = image.convert("RGB")
        return np.array(rgb_image)
    except UnidentifiedImageError:
        st.error("Uploaded file is not a valid image.")
        return None
    except Exception as exc:
        st.error(f"Image preprocessing failed: {exc}")
        return None


# -----------------------------------------------------------------------------
# Inference & Probability Parsing Pipeline
# -----------------------------------------------------------------------------
def predict_ripeness(model: YOLO, img_array: np.ndarray) -> Optional[Dict[str, Any]]:
    """Runs model inference and parses classification metrics.

    Args:
        model: Loaded YOLOv8 classification model.
        img_array: Preprocessed RGB image matrix.

    Returns:
        dict: Top-1 index, label, confidence, and 4-stage probability list.
    """
    try:
        results = model.predict(source=img_array, verbose=False)
        if not results:
            st.error("Model returned an empty prediction result.")
            return None

        result = results[0]
        probs = result.probs

        top1_index = int(probs.top1)
        top1_conf = float(probs.top1conf.item()) * 100.0

        stage_meta = STAGE_MAPPING.get(top1_index, {
            "name": result.names.get(top1_index, f"Stage_{top1_index}"),
            "badge": f"Stage {top1_index}",
            "color": "#d8a31f",
            "tip": "Ripeness stage detected.",
        })

        raw_probs = probs.data.tolist()
        distribution = []
        for idx in range(len(STAGE_MAPPING)):
            prob_val = raw_probs[idx] if idx < len(raw_probs) else 0.0
            meta = STAGE_MAPPING.get(idx, {
                "name": f"Stage_{idx}",
                "badge": f"Stage {idx}",
                "color": "#5e8c55"
            })
            distribution.append({
                "index": idx,
                "name": meta["name"],
                "badge": meta["badge"],
                "color": meta["color"],
                "probability": float(prob_val),
                "percentage": float(prob_val) * 100.0,
            })

        return {
            "top1_index": top1_index,
            "top1_name": stage_meta["name"],
            "top1_badge": stage_meta["badge"],
            "top1_color": stage_meta["color"],
            "top1_tip": stage_meta["tip"],
            "confidence": top1_conf,
            "distribution": distribution,
        }
    except Exception as exc:
        st.error(f"Inference error: {exc}")
        return None

