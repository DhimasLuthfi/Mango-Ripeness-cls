"""Mango Ripeness Classifier - Streamlit Web Application.

Classifies mango ripeness stages using an Ultralytics YOLOv8-cls model.
Image processing and inference pipelines operate strictly in-memory with defensive error handling.
"""

from typing import Dict, Any, Optional
import os
import numpy as np
from PIL import Image, UnidentifiedImageError
import streamlit as st
from ultralytics import YOLO

# -----------------------------------------------------------------------------
# Metadata & Ripeness Stage Definitions
# -----------------------------------------------------------------------------
STAGE_METADATA = {
    0: {
        "title": "Stage 0 (Unripe)",
        "badge": "🟢 Unripe",
        "color": "#28a745",
        "characteristics": "Hard green skin, firm texture, and acidic/sour taste. Ideal for pickling or rujak.",
        "storage": "Store at ambient room temperature to encourage natural ripening."
    },
    1: {
        "title": "Stage 1 (Early Ripe)",
        "badge": "🟡 Early Ripe",
        "color": "#ffc107",
        "characteristics": "Predominantly green skin with faint yellowish undertones. Ripening has initiated.",
        "storage": "Keep in a well-ventilated dry space; usually ripens fully within 2-3 days."
    },
    2: {
        "title": "Stage 2 (Partially Ripe)",
        "badge": "🟠 Partially Ripe",
        "color": "#fd7e14",
        "characteristics": "Even blend of green and yellow hues. Flesh is moderately yielding with pleasant sweetness.",
        "storage": "Ready for eating if slightly tangy fruit is preferred, or allow 1 more day."
    },
    3: {
        "title": "Stage 3 (Ripe)",
        "badge": "🔴 Ripe",
        "color": "#dc3545",
        "characteristics": "Vibrant golden-yellow or reddish blush, soft texture, rich aroma, and peak natural sweetness.",
        "storage": "Peak ripeness. Consume immediately or refrigerate to preserve freshness."
    }
}

# -----------------------------------------------------------------------------
# 1. Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Mango Ripeness Classifier",
    page_icon="🥭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. Model Loading & Caching Pipeline
# -----------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_yolo_model(weights_path: str = "best.pt") -> Optional[YOLO]:
    """Loads and caches the YOLOv8 classification model into RAM.

    Args:
        weights_path: Path to the trained .pt weight file.

    Returns:
        YOLO: Instantiated model object, or None if loading fails.
    """
    if not os.path.exists(weights_path):
        st.error(
            f"Model weights file `{weights_path}` not found. "
            "Please ensure `best.pt` is placed in the project root directory."
        )
        return None

    try:
        model = YOLO(weights_path)
        return model
    except Exception as exc:
        st.error(
            f"Failed to load YOLOv8 model from `{weights_path}`: {exc}. "
            "Please verify that the checkpoint is a valid PyTorch weights file."
        )
        return None


# -----------------------------------------------------------------------------
# 3. Image Preprocessing Pipeline
# -----------------------------------------------------------------------------
def preprocess_image(image: Image.Image) -> Optional[np.ndarray]:
    """Preprocesses a PIL Image into an RGB NumPy array entirely in-memory.

    Args:
        image: User-provided PIL Image from file uploader or camera.

    Returns:
        np.ndarray: Image array formatted as RGB (H, W, 3), or None on error.
    """
    try:
        # Convert any color format (RGBA, Grayscale, etc.) to 3-channel RGB
        rgb_image = image.convert("RGB")
        img_array = np.array(rgb_image)
        return img_array
    except UnidentifiedImageError:
        st.error("Uploaded file is not a valid or recognizable image.")
        return None
    except Exception as exc:
        st.error(f"Image preprocessing failed: {exc}")
        return None


# -----------------------------------------------------------------------------
# 4. Inference & Probability Parsing Pipeline
# -----------------------------------------------------------------------------
def predict_ripeness(model: YOLO, img_array: np.ndarray) -> Optional[Dict[str, Any]]:
    """Executes model inference and parses classification metrics.

    Args:
        model: Loaded YOLOv8 classification model instance.
        img_array: Preprocessed RGB image matrix.

    Returns:
        dict: Top-1 index, label, confidence, and full probability map.
    """
    try:
        # Run inference in silent mode
        results = model.predict(source=img_array, verbose=False)
        if not results:
            st.error("Model returned an empty prediction result.")
            return None

        result = results[0]
        probs = result.probs

        # Extract Top-1 metrics
        top1_index = int(probs.top1)
        raw_label = result.names.get(top1_index, f"Stage_{top1_index}")
        top1_confidence = float(probs.top1conf.item()) * 100.0

        # Retrieve structured stage details
        meta = STAGE_METADATA.get(top1_index, {
            "title": raw_label,
            "badge": raw_label,
            "characteristics": "Standard stage classification.",
            "storage": "Store properly according to preferences."
        })

        # Parse probability distribution for all 4 target classes
        raw_probs = probs.data.tolist()
        class_distribution = []
        for idx, prob_val in enumerate(raw_probs):
            class_name = result.names.get(idx, f"Stage_{idx}")
            stage_info = STAGE_METADATA.get(idx, {"badge": class_name})
            class_distribution.append({
                "index": idx,
                "label": class_name,
                "badge": stage_info.get("badge", class_name),
                "probability": float(prob_val),
                "percentage": float(prob_val) * 100.0
            })

        return {
            "top1_index": top1_index,
            "top1_label": raw_label,
            "badge": meta["badge"],
            "characteristics": meta["characteristics"],
            "storage": meta["storage"],
            "confidence": top1_confidence,
            "distribution": class_distribution
        }
    except Exception as exc:
        st.error(f"An error occurred during model inference: {exc}")
        return None


# -----------------------------------------------------------------------------
# 5. UI Layout & Application Entry Point
# -----------------------------------------------------------------------------
def render_sidebar():
    """Renders informative sidebar details and ripeness legend."""
    with st.sidebar:
        st.header("🥭 Ripeness Guide")
        st.caption("Reference guide for mango ripeness grading stages:")

        for idx, info in STAGE_METADATA.items():
            st.markdown(f"**{info['badge']}**")
            st.caption(f"{info['characteristics']}")
            st.write("")

        st.divider()
        st.markdown("### ⚙️ System Details")
        st.markdown(
            """
            - **Model**: YOLOv8-cls
            - **Framework**: Streamlit & Ultralytics
            - **Data Handling**: 100% In-Memory (RAM)
            - **Target Classes**: 4 Ripeness Stages
            """
        )


def main():
    """Main application execution pipeline."""
    render_sidebar()

    # Load model with caching
    model = load_yolo_model("best.pt")
    if model is None:
        st.stop()

    # Header section
    st.title("🥭 Mango Ripeness Classifier")
    st.markdown(
        "Real-time, automated mango ripeness identification powered by **YOLOv8-cls**. "
        "Upload an image or capture a live photo to inspect ripeness grading and confidence metrics."
    )
    st.divider()

    # Interactive input method selection
    input_tab1, input_tab2 = st.tabs(["📁 Upload Image", "📸 Camera Input"])
    selected_image: Optional[Image.Image] = None

    with input_tab1:
        uploaded_file = st.file_uploader(
            "Select a mango photo (JPG, JPEG, PNG):",
            type=["jpg", "jpeg", "png"],
            help="For best accuracy, ensure good lighting and center a single mango."
        )
        if uploaded_file is not None:
            try:
                selected_image = Image.open(uploaded_file)
            except Exception as exc:
                st.error(f"Unable to read image file: {exc}")

    with input_tab2:
        camera_file = st.camera_input("Point camera at the mango and take a photo:")
        if camera_file is not None:
            try:
                selected_image = Image.open(camera_file)
            except Exception as exc:
                st.error(f"Unable to read camera input: {exc}")

    # Empty State display when no image is loaded
    if selected_image is None:
        st.info("💡 **Awaiting Image Input**: Please upload a mango photograph or snap a picture using the camera above.")
        return

    # Two-Column Results Display
    st.divider()
    col_preview, col_analytics = st.columns([1, 1], gap="large")

    with col_preview:
        st.subheader("Target Preview")
        st.image(
            selected_image,
            caption=f"Source Image ({selected_image.width} × {selected_image.height} px)",
            use_column_width=True
        )

    with col_analytics:
        st.subheader("Classification Analytics")
        with st.spinner("Analyzing ripeness..."):
            img_array = preprocess_image(selected_image)
            prediction = None
            if img_array is not None:
                prediction = predict_ripeness(model, img_array)

        if img_array is not None and prediction is not None:
            # Primary Top-1 Result Card
            st.success(f"**Identified Stage:** {prediction['badge']}")
            
            st.metric(
                label="Confidence Score",
                value=f"{prediction['confidence']:.2f}%",
                help="Top-1 class prediction probability."
            )

            # Safeguard: Low Confidence Warning (< 50%)
            if prediction["confidence"] < 50.0:
                st.warning(
                    "⚠️ **Low Confidence Detection (< 50%)**: "
                    "The model has reduced certainty. The target may not be a mango, "
                    "or the photo might suffer from blurriness, extreme shadows, or heavy background noise."
                )

            # Stage Characteristics & Storage Advice Callout
            with st.expander("ℹ️ Stage Details & Storage Advice", expanded=True):
                st.write(f"**Characteristics:** {prediction['characteristics']}")
                st.write(f"**Storage Tip:** {prediction['storage']}")

            # Probability Distribution for all 4 classes
            st.write("##### Probability Distribution Across Stages")
            for item in prediction["distribution"]:
                col_label, col_val = st.columns([3, 1])
                with col_label:
                    st.write(f"**{item['badge']}**")
                with col_val:
                    st.write(f"`{item['percentage']:.2f}%`")
                st.progress(item["probability"])

    st.divider()
    st.caption("Engineered with Ultralytics YOLOv8 & Streamlit Community Cloud. In-memory processing guarantees data privacy.")


if __name__ == "__main__":
    main()
