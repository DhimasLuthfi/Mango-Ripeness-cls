"""Mango Ripeness Classifier - Main Streamlit Entry Point.

Orchestrates YOLOv8-cls model inference logic (model.py) and the bespoke
MangoSense full-width visual design system (ui.py).
"""

from typing import Optional
from PIL import Image
import streamlit as st

from model import load_yolo_model, preprocess_image, predict_ripeness
from ui import (
    inject_custom_css,
    render_navbar,
    render_hero_left,
    render_card_top,
    render_security_footnote,
    render_prediction_hero_card,
    render_clean_probability_bars,
    render_steps_section,
    render_footer,
)

# -----------------------------------------------------------------------------
# 1. Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="MangoSense – Deteksi Kematangan Mangga",
    page_icon="🥭",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# -----------------------------------------------------------------------------
# 2. Main Application Flow
# -----------------------------------------------------------------------------
def main():
    """Main execution orchestrator."""
    # Inject Google Fonts, organic background shapes, and custom styling
    inject_custom_css()

    # Top Navigation Bar
    render_navbar()

    # Initialize YOLOv8 classification model (with @st.cache_resource)
    model = load_yolo_model("best.pt")
    if model is None:
        st.stop()

    # Two-Column Hero & Floating Card Grid
    col_hero, col_card = st.columns([1.05, 1.0], gap="large")

    with col_hero:
        render_hero_left()

    selected_image: Optional[Image.Image] = None

    with col_card:
        # Floating White Card Container with Golden Corner Flourish
        st.markdown('<div class="ms-card-wrapper">', unsafe_allow_html=True)
        render_card_top()

        # Method Selector Tabs
        method = st.radio(
            "Metode Input:",
            options=[" Unggah File Citra", " Ambil via Kamera"],
            horizontal=True,
            label_visibility="collapsed"
        )

        st.markdown('<span class="ms-lbl">Pilih foto buah mangga</span>', unsafe_allow_html=True)

        if method == " Unggah File Citra":
            uploaded_file = st.file_uploader(
                "Pilih file foto buah mangga",
                type=["jpg", "jpeg", "png"],
                label_visibility="collapsed",
                help="Format: JPG, JPEG, atau PNG. Maksimal 10 MB."
            )
            if uploaded_file is not None:
                try:
                    selected_image = Image.open(uploaded_file)
                except Exception as exc:
                    st.error(f"Format gambar tidak didukung: {exc}")
        else:
            camera_file = st.camera_input(
                "Arahkan kamera ke buah mangga",
                label_visibility="collapsed"
            )
            if camera_file is not None:
                try:
                    selected_image = Image.open(camera_file)
                except Exception as exc:
                    st.error(f"Gagal mengakses kamera: {exc}")

        # CTA Button "Analisis Kematangan"
        analyze_clicked = st.button(
            "Analisis Kematangan",
            disabled=(selected_image is None)
        )

        render_security_footnote()
        st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================================
    # FULL-WIDTH RESULT DASHBOARD (Gambar di Kiri, Penjelasan di Kanan)
    # =========================================================================
    if selected_image is not None:
        with st.spinner("Model sedang menganalisis tingkat kematangan..."):
            img_array = preprocess_image(selected_image)
            prediction = None
            if img_array is not None:
                prediction = predict_ripeness(model, img_array)

        if prediction is not None:
            # Standalone Section Title with Ample Spacing
            st.markdown(
                '<div class="ms-res-header-container">'
                '<span class="ms-res-header-badge">HASIL ANALISIS AI</span>'
                '<h2 class="ms-res-title-lg">Laporan Identifikasi Kematangan Mangga</h2>'
                '</div>',
                unsafe_allow_html=True
            )

            # Two Independent Padded Box Columns (Gambar di Kiri, Penjelasan di Kanan)
            col_res_img, col_res_info = st.columns([1.0, 1.15], gap="large")

            with col_res_img:
                st.markdown(
                    '<div class="ms-image-card">'
                    '<span class="ms-image-card-title">FOTO CITRA TERANALISIS</span>',
                    unsafe_allow_html=True
                )
                st.image(
                    selected_image,
                    caption=f"Resolusi: {selected_image.width} × {selected_image.height} px",
                    use_column_width=True
                )
                st.markdown('</div>', unsafe_allow_html=True)

            with col_res_info:
                st.markdown('<div class="ms-analytics-card">', unsafe_allow_html=True)

                # 1. Top-1 Prediction Banner Card with Tips
                render_prediction_hero_card(prediction)

                # 2. Confidence Metric Card
                st.metric(
                    label="Tingkat Keyakinan (Confidence Score)",
                    value=f"{prediction['confidence']:.2f}%"
                )

                # 3. Low Confidence Warning Safeguard (< 50%)
                if prediction["confidence"] < 50.0:
                    st.warning(
                        "⚠️ **Perhatian (Keyakinan < 50%)**: Tingkat keyakinan model rendah. "
                        "Objek mungkin bukan mangga, foto buram, atau pencahayaan kurang optimal."
                    )

                # 4. Clean Probability Bars for all 4 stages
                st.markdown(
                    '<div style="margin-top:20px;margin-bottom:12px;font-weight:700;color:var(--ink);">'
                    'Distribusi Probabilitas Tiap Kelas:'
                    '</div>',
                    unsafe_allow_html=True
                )
                render_clean_probability_bars(prediction["distribution"])

                st.markdown('</div>', unsafe_allow_html=True)

    # Three Simple Steps Section
    render_steps_section()

    # MangoSense Dark Footer
    render_footer()


if __name__ == "__main__":
    main()
