"""Mango Ripeness Classifier - Streamlit Web Application.

A professional computer vision interface to classify mango ripeness stages
using an Ultralytics YOLOv8-cls model.
"""

from typing import Dict, Any, Optional
import os
import numpy as np
from PIL import Image, UnidentifiedImageError
import streamlit as st
from ultralytics import YOLO

# -----------------------------------------------------------------------------
# 1. Page Configuration & Ripeness Stage Definitions
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Mango Ripeness Classifier",
    page_icon="🥭",
    layout="centered",
    initial_sidebar_state="collapsed"
)

STAGE_MAPPING = {
    0: {
        "name": "Stage_0 (Unripe)",
        "badge": "🟢 Stage 0 (Unripe)",
        "description": "Hard green skin, firm texture, and acidic/sour taste.",
    },
    1: {
        "name": "Stage_1 (Early Ripe)",
        "badge": "🟡 Stage 1 (Early Ripe)",
        "description": "Green skin with slight yellowish undertones.",
    },
    2: {
        "name": "Stage_2 (Partially Ripe)",
        "badge": "🟠 Stage 2 (Partially Ripe)",
        "description": "Evenly mixed green and yellow hues with developing sweetness.",
    },
    3: {
        "name": "Stage_3 (Ripe)",
        "badge": "🔴 Stage 3 (Ripe)",
        "description": "Rich golden-yellow or reddish blush, soft, aromatic, and sweet.",
    },
}


# -----------------------------------------------------------------------------
# 2. Model Loading & Caching Pipeline
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
# 3. Image Preprocessing & Display Helpers
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


def render_image_responsive(image: Image.Image, caption: str = "") -> None:
    """Renders image responsively supporting all Streamlit versions."""
    st.image(image, caption=caption, use_column_width=True)


# -----------------------------------------------------------------------------
# 4. Inference & Probability Parsing Pipeline
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
            "description": "Ripeness stage detected.",
        })

        raw_probs = probs.data.tolist()
        distribution = []
        for idx in range(len(STAGE_MAPPING)):
            prob_val = raw_probs[idx] if idx < len(raw_probs) else 0.0
            meta = STAGE_MAPPING.get(idx, {"name": f"Stage_{idx}", "badge": f"Stage {idx}"})
            distribution.append({
                "index": idx,
                "name": meta["name"],
                "badge": meta["badge"],
                "probability": float(prob_val),
                "percentage": float(prob_val) * 100.0,
            })

        return {
            "top1_index": top1_index,
            "top1_name": stage_meta["name"],
            "top1_badge": stage_meta["badge"],
            "top1_description": stage_meta["description"],
            "confidence": top1_conf,
            "distribution": distribution,
        }
    except Exception as exc:
        st.error(f"Inference error: {exc}")
        return None


# -----------------------------------------------------------------------------
# 5. UI Layout & Main Application
# -----------------------------------------------------------------------------
def main():
    """Builds and executes the Streamlit dashboard layout."""
    # 1. Model Initialization
    model = load_yolo_model("best.pt")
    if model is None:
        st.stop()

    # 2. Header & System Description
    st.title("🥭 Mango Ripeness Classifier")
    st.markdown(
        """
        Sistem cerdas identifikasi fase kematangan buah mangga secara *real-time* berbasis **YOLOv8-cls**.
        
        **Kategori Fase Kematangan:**
        * **Stage 0 (Unripe):** Mangga mentah berwarna hijau pekat dan padat.
        * **Stage 1 (Early Ripe):** Mangga mulai matang dengan semburat kekuningan samar.
        * **Stage 2 (Partially Ripe):** Mangga setengah matang dengan perpaduan hijau dan kuning seimbang.
        * **Stage 3 (Ripe):** Mangga matang penuh dengan warna kuning keemasan/oranye dan aroma harum.
        """
    )
    st.divider()

    # 3. Dual Input Method Selection
    input_method = st.radio(
        "Pilih Metode Pengambilan Gambar:",
        options=["Unggah File Citra", "Ambil Foto via Kamera"],
        horizontal=True,
    )

    selected_image: Optional[Image.Image] = None

    if input_method == "Unggah File Citra":
        uploaded_file = st.file_uploader(
            "Pilih foto buah mangga (format JPG, JPEG, atau PNG)...",
            type=["jpg", "jpeg", "png"],
            help="Pastikan pencahayaan cukup dan buah mangga berada di fokus utama.",
        )
        if uploaded_file is not None:
            try:
                selected_image = Image.open(uploaded_file)
            except Exception as exc:
                st.error(f"Gagal memuat file gambar: {exc}")
    else:
        camera_file = st.camera_input("Arahkan kamera ke buah mangga dan ambil foto...")
        if camera_file is not None:
            try:
                selected_image = Image.open(camera_file)
            except Exception as exc:
                st.error(f"Gagal memproses gambar dari kamera: {exc}")

    # 4. Results & Metrics Display (Empty State Guard)
    if selected_image is not None:
        st.divider()
        col_preview, col_metrics = st.columns([1, 1], gap="medium")

        with col_preview:
            st.subheader("Foto Citra Input")
            render_image_responsive(
                selected_image,
                caption=f"Target Analisis ({selected_image.width} × {selected_image.height} px)",
            )

        with col_metrics:
            st.subheader("Hasil Analisis & Metrik")
            with st.spinner("Model sedang menganalisis tingkat kematangan..."):
                img_array = preprocess_image(selected_image)
                prediction = None
                if img_array is not None:
                    prediction = predict_ripeness(model, img_array)

            if img_array is not None and prediction is not None:
                # Primary Top-1 Prediction Card
                st.success(f"**Klasifikasi Utama:** {prediction['top1_badge']}")
                st.metric(
                    label="Tingkat Keyakinan (Confidence Score)",
                    value=f"{prediction['confidence']:.2f}%",
                )

                # Low Confidence Threshold Alert (< 50%)
                if prediction["confidence"] < 50.0:
                    st.warning(
                        "⚠️ **Perhatian (Keyakinan < 50%)**: Tingkat keyakinan model rendah. "
                        "Objek mungkin bukan mangga, foto buram, atau pencahayaan kurang optimal."
                    )

                # Characteristics Note
                st.caption(f"ℹ️ **Karakteristik:** {prediction['top1_description']}")

                # 4-Stage Probability Distribution
                st.write("##### Distribusi Probabilitas 4 Tahapan:")
                for item in prediction["distribution"]:
                    col_name, col_pct = st.columns([3, 1])
                    with col_name:
                        st.write(f"- **{item['name']}**")
                    with col_pct:
                        st.write(f"**{item['percentage']:.2f}%**")
                    st.progress(float(item["probability"]))

    # 5. Footer & System Metadata
    st.divider()
    st.caption("Dikembangkan menggunakan Ultralytics YOLOv8 & Streamlit. Pemrosesan citra 100% in-memory.")


if __name__ == "__main__":
    main()
