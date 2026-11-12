"""MangoSense UI & Design Components.

Contains custom CSS styles, HTML layout templates, and frontend visual renderers
replicating the bespoke MangoSense visual design language.
"""

from typing import Dict, Any, List
from PIL import Image
import streamlit as st

# -----------------------------------------------------------------------------
# MangoSense Bespoke Design System CSS
# -----------------------------------------------------------------------------
CUSTOM_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=DM+Serif+Display:ital@0;1&display=swap" rel="stylesheet">

<style>
:root {
  --bg: #f8f7ef;
  --paper: #ffffff;
  --ink: #17402c;
  --muted: #5d6f64;
  --line: #e3e8dc;
  --leaf: #eef3e7;
  --leaf-2: #e4ecdc;
  --gold: #d4922a;
  --gold-dark: #b9791a;
  --c1: #5e8c55;
  --c2: #d8a31f;
  --c3: #e8742c;
  --serif: 'DM Serif Display', Georgia, serif;
  --sans: 'DM Sans', system-ui, sans-serif;
}

/* Base Body & Streamlit Overrides */
.stApp {
  background: var(--bg) !important;
  color: var(--ink) !important;
  font-family: var(--sans) !important;
  overflow-x: hidden;
}

/* Background Decorative Shapes */
.stApp::before {
  content: "";
  position: fixed;
  width: 320px;
  height: 320px;
  background: var(--leaf);
  left: -130px;
  top: 240px;
  border-radius: 50%;
  z-index: 0;
  pointer-events: none;
}
.stApp::after {
  content: "";
  position: fixed;
  width: 360px;
  height: 360px;
  border: 56px solid rgba(216,163,31,.12);
  right: -150px;
  top: 100px;
  border-radius: 50%;
  z-index: 0;
  pointer-events: none;
}

/* Remove Streamlit default blank headers and footer */
#MainMenu, header[data-testid="stHeader"], footer, div[data-testid="stToolbar"] {
  display: none !important;
}

.block-container {
  max-width: 1240px !important;
  padding-top: 1.5rem !important;
  padding-bottom: 2.5rem !important;
  padding-left: 2rem !important;
  padding-right: 2rem !important;
  position: relative;
  z-index: 1;
}

/* Typography */
h1, h2, h3, .brand, .serif {
  font-family: var(--serif) !important;
  font-weight: 400 !important;
  color: var(--ink) !important;
}

/* Navbar */
.ms-navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 76px;
  border-bottom: 1px solid var(--line);
  margin-bottom: 36px;
}
.ms-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  font-family: var(--serif);
  font-size: 1.65rem;
  color: var(--ink);
  text-decoration: none;
}
.ms-nav-links {
  display: flex;
  gap: 32px;
  font-size: 0.95rem;
}
.ms-nav-links a {
  color: var(--muted);
  text-decoration: none;
  font-weight: 500;
  padding: 6px 0;
  border-bottom: 2px solid transparent;
}
.ms-nav-links a.active {
  color: var(--ink);
  font-weight: 600;
  border-bottom: 2px solid var(--gold);
}
.ms-tag {
  border: 1px solid var(--line);
  background: #fff;
  border-radius: 99px;
  padding: 4px 14px;
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  color: var(--muted);
}

/* Hero Section (Left Column) */
.ms-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--leaf);
  border: 1px solid var(--leaf-2);
  border-radius: 99px;
  padding: 6px 16px;
  font-size: 0.74rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #2f5a3f;
  margin-bottom: 18px;
}
.ms-pill::before {
  content: "";
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--gold);
}

.ms-hero-title {
  font-size: clamp(2.6rem, 5.2vw, 4.1rem);
  line-height: 1.05;
  letter-spacing: -0.015em;
  margin: 16px 0 22px;
  color: var(--ink);
}
.ms-hero-title em {
  color: var(--gold);
  font-style: italic;
}

.ms-lead {
  font-size: 1.12rem;
  color: var(--muted);
  max-width: 32em;
  line-height: 1.85;
}

/* 4 Ripeness Classes Cards */
.ms-classes-t {
  margin: 36px 0 12px;
  font-size: 0.76rem;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--muted);
  display: flex;
  justify-content: space-between;
}
.ms-classes-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  list-style: none;
  padding: 0;
  margin: 0;
}
.ms-class-item {
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 14px 12px;
  box-shadow: 0 2px 10px rgba(23,64,44,.04);
}
.ms-class-item .r {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.ms-class-item .dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}
.ms-class-item .n {
  font-family: var(--serif);
  font-size: 0.82rem;
  color: #8a978f;
}
.ms-class-item b {
  display: block;
  font-size: 0.88rem;
  line-height: 1.3;
  color: var(--ink);
}
.ms-class-item small {
  color: var(--muted);
  font-size: 0.74rem;
  line-height: 1.2;
  display: block;
  margin-top: 2px;
}
.ms-class-item .m {
  height: 4px;
  border-radius: 9px;
  background: rgba(0,0,0,.06);
  margin-top: 10px;
  overflow: hidden;
}
.ms-class-item .m i {
  display: block;
  height: 100%;
  border-radius: 9px;
}

/* Right Card & Corner Flourish */
.ms-card-wrapper {
  position: relative;
  background: var(--paper);
  border-radius: 28px;
  padding: 32px;
  box-shadow: 0 24px 60px -20px rgba(23,64,44,.22), 0 2px 8px rgba(23,64,44,.05);
  border: 1px solid var(--line);
}
.ms-card-wrapper::before {
  content: "";
  position: absolute;
  top: -12px;
  left: -12px;
  width: 58px;
  height: 58px;
  border-top: 3px solid rgba(212, 146, 42, 0.6);
  border-left: 3px solid rgba(212, 146, 42, 0.6);
  border-top-left-radius: 30px;
  pointer-events: none;
}

.ms-card-h {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 22px;
}
.ms-eyebrow {
  font-size: 0.74rem;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--gold-dark);
}
.ms-card-h2 {
  font-size: 1.75rem;
  line-height: 1.2;
  margin-top: 6px;
  color: var(--ink);
}
.ms-step {
  flex: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--leaf);
  display: grid;
  place-items: center;
  font-size: 0.85rem;
  font-weight: 600;
  color: #2f5a3f;
}

/* Method Radio Buttons inside Card */
div[data-testid="stRadio"] > div[role="radiogroup"] {
  display: grid !important;
  grid-template-columns: 1fr 1fr !important;
  gap: 12px !important;
  background: transparent !important;
  padding: 0 !important;
  margin-bottom: 20px !important;
}
div[data-testid="stRadio"] label {
  display: flex !important;
  align-items: center !important;
  justify-content: flex-start !important;
  background: #ffffff !important;
  border: 1px solid var(--line) !important;
  border-radius: 14px !important;
  padding: 14px 16px !important;
  cursor: pointer !important;
  transition: all 0.2s ease !important;
}
div[data-testid="stRadio"] label:hover {
  border-color: var(--c1) !important;
}
div[data-testid="stRadio"] label > div:first-child {
  display: none !important;
}
div[data-testid="stRadio"] label[data-checked="true"],
div[data-testid="stRadio"] label:has(input:checked) {
  background: var(--leaf) !important;
  border-color: var(--c1) !important;
}
div[data-testid="stRadio"] label p {
  color: var(--ink) !important;
  font-weight: 600 !important;
  font-size: 0.92rem !important;
  margin: 0 !important;
}

.ms-lbl {
  display: block;
  font-weight: 600;
  font-size: 0.92rem;
  margin-bottom: 10px;
  color: var(--ink);
}

/* File Uploader Custom Styling */
div[data-testid="stFileUploader"] section {
  border: 1.5px dashed #c5d0bf !important;
  background: #fbfcf8 !important;
  border-radius: 18px !important;
  min-height: 190px !important;
  padding: 24px !important;
  text-align: center !important;
  transition: 0.2s ease !important;
}
div[data-testid="stFileUploader"] section:hover {
  border-color: var(--c1) !important;
  background: var(--leaf) !important;
}
div[data-testid="stFileUploader"] section * {
  color: #17402c !important;
}
div[data-testid="stFileUploader"] section span {
  color: #17402c !important;
  font-weight: 500 !important;
}
div[data-testid="stFileUploader"] section small {
  color: #5d6f64 !important;
}
div[data-testid="stFileUploader"] button {
  background: var(--ink) !important;
  border-radius: 99px !important;
  padding: 8px 22px !important;
  border: 0 !important;
  font-weight: 600 !important;
  font-size: 0.88rem !important;
}
div[data-testid="stFileUploader"] button * {
  color: #ffffff !important;
}

/* Action Button (.cta) */
div[data-testid="stButton"] button {
  width: 100% !important;
  margin-top: 16px !important;
  padding: 16px !important;
  border: 0 !important;
  border-radius: 14px !important;
  background: var(--ink) !important;
  color: #fff !important;
  font-weight: 600 !important;
  font-size: 1rem !important;
  transition: 0.2s !important;
  box-shadow: 0 8px 20px -8px rgba(23,64,44,.5) !important;
}
div[data-testid="stButton"] button:hover {
  background: #0f2d1e !important;
  color: #fff !important;
}

/* Security Note */
.ms-note {
  display: flex;
  gap: 8px;
  justify-content: center;
  align-items: center;
  margin-top: 14px;
  font-size: 0.78rem;
  color: var(--muted);
}
.ms-note svg {
  width: 14px;
  height: 14px;
}

/* =========================================================================
   PADDED FULL-WIDTH RESULT DASHBOARD
   ========================================================================= */
.ms-res-header-container {
  margin-top: 52px;
  margin-bottom: 26px;
}

.ms-res-header-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--leaf);
  border: 1px solid var(--leaf-2);
  border-radius: 99px;
  padding: 6px 16px;
  font-size: 0.74rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #2f5a3f;
  margin-bottom: 8px;
}

.ms-res-title-lg {
  font-family: var(--serif);
  font-size: 2.3rem;
  color: var(--ink);
  line-height: 1.15;
  margin: 6px 0 0;
}

/* Left Image Box (Padded Card) */
.ms-image-card {
  background: #ffffff;
  border: 1px solid var(--line);
  border-radius: 26px;
  padding: 24px;
  box-shadow: 0 16px 40px -15px rgba(23,64,44,.12);
  margin-bottom: 24px;
}
.ms-image-card-title {
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--gold-dark);
  margin-bottom: 16px;
  display: block;
}

/* Right Analytics Box (Padded Card) */
.ms-analytics-card {
  background: #ffffff;
  border: 1px solid var(--line);
  border-radius: 26px;
  padding: 32px 36px;
  box-shadow: 0 16px 40px -15px rgba(23,64,44,.12);
  margin-bottom: 24px;
}

.ms-prediction-hero {
  display: flex;
  align-items: center;
  gap: 16px;
  background: #fbfcf8;
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 20px 24px;
  margin-bottom: 20px;
}
.ms-prediction-hero .dot-lg {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  flex: none;
}
.ms-prediction-hero h3 {
  font-family: var(--serif);
  font-size: 2rem;
  margin: 0;
  line-height: 1.1;
  color: var(--ink);
}
.ms-prediction-hero .tagline {
  color: var(--muted);
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-weight: 700;
  display: block;
  margin-bottom: 3px;
}

.ms-tip-box {
  background: var(--leaf);
  border-left: 4px solid var(--gold);
  border-radius: 12px;
  padding: 16px 20px;
  color: var(--ink);
  font-size: 0.94rem;
  line-height: 1.6;
  margin-bottom: 20px;
}

/* Metric Widget Styling with Padding */
div[data-testid="stMetric"] {
  background: #fbfcf8 !important;
  border: 1px solid var(--line) !important;
  border-radius: 16px !important;
  padding: 16px 22px !important;
  margin-bottom: 20px !important;
}
div[data-testid="stMetric"] label {
  color: var(--muted) !important;
  font-weight: 700 !important;
  font-size: 0.8rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.08em !important;
}
div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
  color: var(--ink) !important;
  font-family: var(--serif) !important;
  font-size: 2.2rem !important;
}

/* Clean Probability Rows */
.ms-prob-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  padding: 4px 0;
  margin-bottom: 12px;
  font-size: 0.88rem;
}
.ms-prob-name {
  width: 140px;
  font-weight: 600;
  color: var(--ink);
  flex: none;
}
.ms-prob-track {
  flex: 1;
  height: 9px;
  background: var(--leaf-2);
  border-radius: 9px;
  overflow: hidden;
}
.ms-prob-fill {
  display: block;
  height: 100%;
  border-radius: 9px;
  transition: width 0.6s ease;
}
.ms-prob-num {
  width: 52px;
  text-align: right;
  font-weight: 700;
  color: var(--ink);
  flex: none;
}

/* 3 Steps Section (.steps) */
.ms-steps {
  background: var(--leaf-2);
  margin-top: 50px;
  border-radius: 20px;
  padding: 30px 40px;
}
.ms-steps-wrap {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}
.ms-steps h2 {
  font-size: 1.4rem;
  margin: 0;
  color: var(--ink);
}
.ms-steps ol {
  display: flex;
  gap: 48px;
  list-style: none;
  margin: 0;
  padding: 0;
}
.ms-steps li {
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 500;
  font-size: 0.95rem;
  color: var(--ink);
}
.ms-steps li span {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: #fff;
  display: grid;
  place-items: center;
  font-family: var(--serif);
  font-size: 0.85rem;
  color: var(--gold-dark);
  flex: none;
}

/* Footer */
.ms-footer {
  background: var(--ink);
  color: #cdddd1;
  margin-top: 40px;
  border-radius: 20px;
  padding: 30px 40px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.85rem;
}
.ms-footer .brand {
  color: #fff;
  font-size: 1.35rem;
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}

/* Responsive adjustments */
@media (max-width: 960px) {
  .ms-classes-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .ms-steps-wrap {
    flex-direction: column;
    align-items: flex-start;
  }
  .ms-steps ol {
    flex-wrap: wrap;
    gap: 20px;
  }
  .ms-footer {
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }
}
</style>
"""


# -----------------------------------------------------------------------------
# Modular UI Renderers
# -----------------------------------------------------------------------------
def inject_custom_css() -> None:
    """Injects Google Fonts, decorative background shapes, and custom CSS."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_navbar() -> None:
    """Renders the MangoSense top navigation bar."""
    st.markdown(
        '<header><div class="ms-navbar">'
        '<a class="ms-brand" href="#deteksi">'
        '<svg viewBox="0 0 32 32" style="width:28px;height:28px;display:inline-block;vertical-align:middle;">'
        '<path d="M16 2c8 2 14 8 14 15 0 7-6 13-14 13S2 24 2 17C2 10 8 4 16 2z" fill="#e8a63a"/>'
        '<path d="M9 24c4-1 8-5 13-13M14 19c-1-3 0-6 2-8M17 16c3 0 5 1 6 3" stroke="#17402c" stroke-width="1.8" fill="none" stroke-linecap="round"/>'
        '</svg> MangoSense</a>'
        '<nav class="ms-nav-links" aria-label="Navigasi utama">'
        '<a href="#deteksi" class="active">Deteksi</a>'
        '<a href="#cara-kerja">Cara Kerja</a>'
        '</nav>'
        '<span class="ms-tag">VISKOM</span>'
        '</div></header>',
        unsafe_allow_html=True
    )


def render_hero_left() -> None:
    """Renders the hero header and 4 classification cards."""
    st.markdown(
        '<section aria-labelledby="judul" id="deteksi">'
        '<span class="ms-pill">Teknologi AI untuk hasil panen</span>'
        '<h1 class="ms-hero-title" id="judul">Kenali kematangan<br>mangga dengan<br><em>lebih mudah.</em></h1>'
        '<p class="ms-lead">Unggah citra buah mangga dan biarkan model deep learning kami mengenali tingkat kematangannya dalam hitungan detik.</p>'
        '<div class="ms-classes-t"><span>Kelas yang dapat diprediksi</span><span>4 Kategori</span></div>'
        '<ul class="ms-classes-grid">'
        '<li class="ms-class-item"><div class="r"><span class="dot" style="background:var(--c1)"></span><span class="n">01</span></div><b>Mentah</b><small>Hijau &amp; keras</small><div class="m"><i style="background:var(--c1);width:55%;"></i></div></li>'
        '<li class="ms-class-item"><div class="r"><span class="dot" style="background:#8fae3f"></span><span class="n">02</span></div><b>Mulai Matang</b><small>Semburat kuning</small><div class="m"><i style="background:#8fae3f;width:70%;"></i></div></li>'
        '<li class="ms-class-item"><div class="r"><span class="dot" style="background:var(--c2)"></span><span class="n">03</span></div><b>Setengah Matang</b><small>Mulai menguning</small><div class="m"><i style="background:var(--c2);width:85%;"></i></div></li>'
        '<li class="ms-class-item"><div class="r"><span class="dot" style="background:var(--c3)"></span><span class="n">04</span></div><b>Matang</b><small>Kuning &amp; siap makan</small><div class="m"><i style="background:var(--c3);width:100%;"></i></div></li>'
        '</ul></section>',
        unsafe_allow_html=True
    )


def render_card_top() -> None:
    """Renders the top title and step badge of the interactive card."""
    st.markdown(
        '<div class="ms-card-h">'
        '<div><div class="ms-eyebrow">Mulai deteksi</div>'
        '<h2 class="ms-card-h2">Pilih metode pengambilan gambar</h2></div>'
        '<span class="ms-step">01</span>'
        '</div>',
        unsafe_allow_html=True
    )


def render_security_footnote() -> None:
    """Renders the security and privacy reassurance footnote."""
    st.markdown(
        '<p class="ms-note">'
        '<svg viewBox="0 0 24 24" style="fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;">'
        '<rect x="5" y="11" width="14" height="9" rx="2"></rect><path d="M8 11V8a4 4 0 0 1 8 0v3"></path>'
        '</svg> Gambar Anda diproses dengan aman dan tidak disimpan (100% In-Memory RAM)'
        '</p>',
        unsafe_allow_html=True
    )


def render_prediction_hero_card(prediction: Dict[str, Any]) -> None:
    """Renders the prominent Top-1 prediction banner card."""
    html = (
        f'<div class="ms-prediction-hero">'
        f'<span class="dot-lg" style="background:{prediction["top1_color"]}"></span>'
        f'<div>'
        f'<span class="tagline">HASIL IDENTIFIKASI UTAMA</span>'
        f'<h3>{prediction["top1_badge"]}</h3>'
        f'</div>'
        f'</div>'
        f'<div class="ms-tip-box">'
        f'<b>Karakteristik &amp; Rekomendasi:</b><br>{prediction["top1_tip"]}'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_clean_probability_bars(distribution: List[Dict[str, Any]]) -> None:
    """Renders clean styled probability bars with zero markdown indentation issues."""
    rows = []
    for item in distribution:
        pct = round(item["percentage"], 1)
        row = (
            f'<div class="ms-prob-row">'
            f'<span class="ms-prob-name">{item["badge"]}</span>'
            f'<div class="ms-prob-track">'
            f'<i class="ms-prob-fill" style="width:{pct}%;background:{item["color"]};"></i>'
            f'</div>'
            f'<span class="ms-prob-num">{pct}%</span>'
            f'</div>'
        )
        rows.append(row)
    
    html = f'<div>{"".join(rows)}</div>'
    st.markdown(html, unsafe_allow_html=True)


def render_steps_section() -> None:
    """Renders the bottom 3-step guide section."""
    st.markdown(
        '<section class="ms-steps" id="cara-kerja">'
        '<div class="ms-steps-wrap">'
        '<h2>Cukup tiga langkah sederhana</h2>'
        '<ol>'
        '<li><span>01</span>Pilih foto mangga</li>'
        '<li><span>02</span>AI menganalisis citra</li>'
        '<li><span>03</span>Lihat hasil kematangan</li>'
        '</ol></div></section>',
        unsafe_allow_html=True
    )


def render_footer() -> None:
    """Renders the dark green MangoSense footer."""
    st.markdown(
        '<footer><div class="ms-footer" id="tentang">'
        '<a class="brand" href="#deteksi">'
        '<svg viewBox="0 0 32 32" style="width:26px;height:26px;fill:none;">'
        '<path d="M16 2c8 2 14 8 14 15 0 7-6 13-14 13S2 24 2 17C2 10 8 4 16 2z" fill="#e8a63a"/>'
        '<path d="M9 24c4-1 8-5 13-13M14 19c-1-3 0-6 2-8M17 16c3 0 5 1 6 3" stroke="#fff" stroke-width="1.8" fill="none" stroke-linecap="round"/>'
        '</svg> MangoSense</a>'
        '<span>Klasifikasi kematangan mangga berbasis deep learning YOLOv8-cls.</span>'
        '<span>&copy; 2025 MangoSense</span>'
        '</div></footer>',
        unsafe_allow_html=True
    )
