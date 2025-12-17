import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Web App Analisis Data", layout="wide")

# =====================
# Sidebar
# =====================
st.sidebar.title("📊 Analisis Data")
menu = st.sidebar.selectbox(
    "Pilih Menu",
    ["Upload Data", "Ringkasan Data", "Statistik Deskriptif", "Visualisasi", "Missing Value"]
)

# =====================
# Upload Data
# =====================
if menu == "Upload Data":
    st.title("📂 Upload Dataset")
    file = st.file_uploader("Upload file CSV", type=["csv"])

    if file is not None:
        df = pd.read_csv(file)
        st.session_state["data"] = df
        st.success("Data berhasil di-upload!")
        st.dataframe(df.head())
    else:
        st.info("Silakan upload file CSV untuk memulai analisis.")

# =====================
# Ringkasan Data
# =====================
elif menu == "Ringkasan Data":
    st.title("📋 Ringkasan Data")
    if "data" in st.session_state:
        df = st.session_state["data"]
        st.write("Jumlah Baris dan Kolom:")
        st.write(df.shape)

        st.write("Tipe Data:")
        st.write(df.dtypes)

        st.write("Preview Data:")
        st.dataframe(df.head())
    else:
        st.warning("Data belum di-upload.")

# =====================
# Statistik Deskriptif
# =====================
elif menu == "Statistik Deskriptif":
    st.title("📈 Statistik Deskriptif")
    if "data" in st.session_state:
        df = st.session_state["data"]
        st.write("Statistik Deskriptif:")
        st.dataframe(df.describe())
    else:
        st.warning("Data belum di-upload.")

# =====================
# Visualisasi
# =====================
elif menu == "Visualisasi":
    st.title("📊 Visualisasi Data")
    if "data" in st.session_state:
        df = st.session_state["data"]
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

        if len(numeric_cols) > 0:
            col = st.selectbox("Pilih Kolom Numerik", numeric_cols)

            fig, ax = plt.subplots()
            ax.hist(df[col].dropna())
            ax.set_title(f"Histogram {col}")
            ax.set_xlabel(col)
            ax.set_ylabel("Frekuensi")
            st.pyplot(fig)
        else:
            st.info("Tidak ada kolom numerik untuk divisualisasikan.")
    else:
        st.warning("Data belum di-upload.")

# =====================
# Missing Value
# =====================
elif menu == "Missing Value":
    st.title("❓ Analisis Missing Value")
    if "data" in st.session_state:
        df = st.session_state["data"]
        missing = df.isnull().sum()
        st.write("Jumlah Missing Value per Kolom:")
        st.dataframe(missing)
    else:
        st.warning("Data belum di-upload.")


