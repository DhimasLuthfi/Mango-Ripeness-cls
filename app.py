import streamlit as st
from PIL import Image
import numpy as np
from ultralytics import YOLO

# 1. Konfigurasi Halaman Web
st.set_page_config(
    page_title="Klasifikasi Kematangan Mangga",
    page_icon="🥭",
    layout="centered"
)

# 2. Caching Pemuatan Model YOLOv8-cls
@st.cache_resource
def load_yolo_model():
    # Memuat bobot hasil training Kaggle
    return YOLO("best.pt")

model = load_yolo_model()

# 3. Header & Deskripsi
st.title("🥭 Mango Ripeness Classifier")
st.markdown(
    """
    Sistem identifikasi fase kematangan buah mangga secara *real-time* berbasis **YOLOv8-cls**.
    
    Kategori fase kematangan:
    * **Stage 0:** Unripe (Mentah)
    * **Stage 1:** Early Ripe (Mulai Matang)
    * **Stage 2:** Partially Ripe (Setengah Matang)
    * **Stage 3:** Ripe (Matang Penuh)
    """
)
st.write("---")

# 4. Pilihan Metode Input Citra
metode_input = st.radio(
    "Pilih Metode Pengambilan Gambar:",
    ("Unggah File Citra", "Gunakan Kamera (Real-Time)"),
    horizontal=True
)

gambar_terpilih = None

if metode_input == "Unggah File Citra":
    file_unggah = st.file_uploader(
        "Pilih file foto mangga (format JPG, JPEG, atau PNG)...",
        type=["jpg", "jpeg", "png"]
    )
    if file_unggah is not None:
        gambar_terpilih = Image.open(file_unggah)
else:
    file_kamera = st.camera_input("Arahkan kamera ke buah mangga dan ambil foto...")
    if file_kamera is not None:
        gambar_terpilih = Image.open(file_kamera)

# 5. Eksekusi Inferensi dan Visualisasi Hasil
if gambar_terpilih is not None:
    st.write("---")
    col1, col2 = st.columns([1, 1], gap="medium")

    with col1:
        st.subheader("Foto Mangga")
        st.image(gambar_terpilih, use_container_width=True)

    with col2:
        st.subheader("Hasil Analisis")
        with st.spinner("Model sedang memproses citra..."):
            # Konversi gambar ke format array RGB
            img_rgb = np.array(gambar_terpilih.convert("RGB"))
            
            # Prediksi menggunakan model YOLO
            hasil_prediksi = model.predict(img_rgb, verbose=False)[0]
            
            top1_index = hasil_prediksi.probs.top1
            kelas_terpilih = hasil_prediksi.names[top1_index]
            confidence = hasil_prediksi.probs.top1conf.item() * 100

            # Kartu Metrik Prediksi Utama
            st.success(f"**Hasil:** {kelas_terpilih}")
            st.metric(label="Tingkat Keyakinan (Confidence)", value=f"{confidence:.2f}%")

        # Visualisasi Distribusi Probabilitas Seluruh Kelas
        st.write("##### Probabilitas Tiap Kategori:")
        daftar_probabilitas = hasil_prediksi.probs.data.tolist()
        nama_semua_kelas = hasil_prediksi.names

        for idx, nilai_prob in enumerate(daftar_probabilitas):
            label_kelas = nama_semua_kelas[idx]
            persentase = nilai_prob * 100
            st.write(f"- **{label_kelas}**: {persentase:.1f}%")
            st.progress(float(nilai_prob))

st.write("---")
st.caption("Dikembangkan menggunakan Ultralytics YOLOv8 & Streamlit.")