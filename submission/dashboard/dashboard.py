from submission.dashboard.partikulasi_polusi.Korelasi_partikulasi_polusi_semua_kota import load_data, page_partilukalasi_polusi_harian, page_partilukalasi_polusi_mingguan, page_partilukalasi_polusi_bulanan, page_partilukalasi_polusi_tahunan
import streamlit as st

# Load data
dataframes = load_data()

# Get list of cities from data
kota_list = list(dataframes.keys())

# Streamlit navigation
st.sidebar.title("Analisis Partikulasi Polusi")
page = st.sidebar.selectbox("Pilih Halaman", ["Polusi Harian", "Polusi Mingguan", "Polusi Bulanan", "Polusi Tahunan"])

# Display pages based on selection
if page == "Polusi Harian":
    page_partilukalasi_polusi_harian(dataframes, kota_list)
elif page == "Polusi Mingguan":
    page_partilukalasi_polusi_mingguan(dataframes, kota_list)
elif page == "Polusi Bulanan":
    page_partilukalasi_polusi_bulanan(dataframes, kota_list)
elif page == "Polusi Tahunan":
    page_partilukalasi_polusi_tahunan(dataframes, kota_list)
