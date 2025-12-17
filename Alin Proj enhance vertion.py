# enhanced_streamlit_app.py
# Combines Matrix Transformations + Image Processing (Blur, Sharpen, Background Removal)
# Bilingual UI: English / Bahasa Indonesia

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image, ImageFilter

# =====================
# Language Dictionary
# =====================
LANG = {
    "English": {
        "title": "Matrix & Image Processing Playground",
        "desc": "Matrix transformations for 2D points and basic image processing features.",
        "matrix_tab": "Matrix Transformations",
        "image_tab": "Image Processing",
        "team_tab": "Developer Team",
        "upload_image": "Upload an image",
        "blur": "Blur",
        "sharpen": "Sharpen",
        "bg_remove": "Background Removal (simple)",
        "apply": "Apply",
        "download": "Download Result",
    },
    "Indonesia": {
        "title": "Aplikasi Transformasi Matriks & Pengolahan Citra",
        "desc": "Transformasi matriks 2D dan fitur dasar pengolahan citra.",
        "matrix_tab": "Transformasi Matriks",
        "image_tab": "Pengolahan Citra",
        "team_tab": "Tim Pengembang",
        "upload_image": "Unggah gambar",
        "blur": "Blur",
        "sharpen": "Pertajam",
        "bg_remove": "Hapus Latar Belakang (sederhana)",
        "apply": "Terapkan",
        "download": "Unduh Hasil",
    }
}

# =====================
# Page Config
# =====================
st.set_page_config(page_title="Matrix & Image Processing", layout="wide")

lang_choice = st.sidebar.selectbox("Language / Bahasa", ["English", "Indonesia"])
T = LANG[lang_choice]

st.title(T["title"])
st.markdown(T["desc"])

# =====================
# Tabs
# =====================
mat_tab, img_tab, team_tab = st.tabs([T["matrix_tab"], T["image_tab"], T["team_tab"]])

# =====================
# MATRIX TAB (simplified reuse)
# =====================
with mat_tab:
    st.subheader(T["matrix_tab"])
    pts_text = st.text_area("Input points (x,y)", "0,0\n1,0\n1,1\n0,1")
    angle = st.number_input("Rotation angle (deg)", value=30.0)
    run = st.button(T["apply"], key="matrix")

    pts = []
    for ln in pts_text.splitlines():
        try:
            x, y = ln.split(',')
            pts.append([float(x), float(y)])
        except:
            pass
    pts = np.array(pts)

    if run and len(pts) > 0:
        rad = np.deg2rad(angle)
        R = np.array([[np.cos(rad), -np.sin(rad)], [np.sin(rad), np.cos(rad)]])
        new_pts = pts @ R.T

        fig, ax = plt.subplots()
        ax.plot(*pts.T, 'o-', label='Original')
        ax.plot(*new_pts.T, 'o-', label='Rotated')
        ax.legend(); ax.grid(True)
        st.pyplot(fig)

# =====================
# IMAGE PROCESSING TAB
# =====================
with img_tab:
    st.subheader(T["image_tab"])
    img_file = st.file_uploader(T["upload_image"], type=["jpg", "png"])

    if img_file:
        img = Image.open(img_file).convert("RGB")
        st.image(img, caption="Original", use_container_width=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            blur_btn = st.button(T["blur"])
        with col2:
            sharp_btn = st.button(T["sharpen"])
        with col3:
            bg_btn = st.button(T["bg_remove"])

        result = img

        if blur_btn:
            result = img.filter(ImageFilter.BLUR)
        if sharp_btn:
            result = img.filter(ImageFilter.SHARPEN)
        if bg_btn:
            # Simple background removal using threshold (educational purpose)
            arr = np.array(img)
            gray = np.mean(arr, axis=2)
            mask = gray > 240
            arr[mask] = [255, 255, 255]
            result = Image.fromarray(arr)

        st.image(result, caption="Result", use_container_width=True)

        buf = BytesIO()
        result.save(buf, format="PNG")
        st.download_button(T["download"], buf.getvalue(), "processed.png", "image/png")

# =====================
# DEVELOPER TEAM TAB
# =====================
with team_tab:
    st.subheader(T["team_tab"])

    st.markdown("""
    **Project Lead: Artjuna**  
    Focus: Streamlit Cloud deployment and testing

    **Member: Gievara **  
    Focus: Matrix computation, image processing logic (Python, NumPy, PIL)

    **member: Riski**  
    Focus: Streamlit UI, bilingual interface, usability

    **Member: Helena**  
    Focus: User guide, Streamlit Cloud deployment, testing
    """)

    st.info("This project is designed for Industrial Engineering students as an educational web application.")
