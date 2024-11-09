import streamlit as st
from streamlit_option_menu import option_menu
import os

# Page configuration
st.set_page_config(page_title="Dashboard Navigasi", page_icon="📊")

# Sidebar navigation
with st.sidebar:
    selected = option_menu(
        menu_title="Navigasi Utama",
        options=["Home", "Kualitas Udara", "Partikulasi Polusi"],
        icons=["house", "cloud", "bar-chart"],
        menu_icon="cast",
        default_index=0,
    )

# Display content based on the selected menu
if selected == "Home":
    st.title("Selamat Datang di Dashboard Utama")
    st.write("Gunakan navigasi di samping untuk memilih analisis data yang diinginkan.")

elif selected == "Kualitas Udara":
    selected_submenu = option_menu(
        menu_title="Submenu Kualitas Udara",
        options=["CO Per Kota", "Kualitas Udara Per Kota", "NO2 Per Kota", "O3 Per Kota", "SO2 Per Kota"],
        icons=["cloud", "bar-chart", "bar-chart", "bar-chart", "bar-chart"],
        menu_icon="cloud",
        default_index=0,
    )
    
    if selected_submenu == "CO Per Kota":
        st.write("Menampilkan data CO per kota")
        exec(open("submission/dashboard/kualitas_udara/CO_Perkota.py", encoding='utf-8').read())

    elif selected_submenu == "Kualitas Udara Per Kota":
        st.write("Menampilkan kualitas udara per kota")
        exec(open("submission/dashboard/kualitas_udara/kualitas_udara_per_kota.py").read())

    elif selected_submenu == "NO2 Per Kota":
        st.write("Menampilkan data NO2 per kota")
        exec(open("submission/dashboard/kualitas_udara/NO2_PerKota.py").read())

    elif selected_submenu == "O3 Per Kota":
        st.write("Menampilkan data O3 per kota")
        exec(open("submission/dashboard/kualitas_udara/O3_Perkota.py", encoding='utf-8').read())

    elif selected_submenu == "SO2 Per Kota":
        st.write("Menampilkan data SO2 per kota")
        exec(open("submission/dashboard/kualitas_udara/SO2_Perkota.py", encoding='utf-8').read())

elif selected == "Partikulasi Polusi":
    selected_submenu = option_menu(
        menu_title="Submenu Partikulasi Polusi",
        options=["Korelasi Partikulasi Polusi Semua Kota", "PM10 Per Kota", "PM2.5 Per Kota"],
        icons=["graph-up", "chart-bar", "chart-line"],
        menu_icon="graph-up",
        default_index=0,
    )
    
    if selected_submenu == "Korelasi Partikulasi Polusi Semua Kota":
        st.write("Menampilkan korelasi partikulasi polusi semua kota")
        exec(open("submission/dashboard/partikulasi_polusi/Korelasi_partikulasi_polusi_semua_kota.py", encoding='utf-8').read())

    elif selected_submenu == "PM10 Per Kota":
        st.write("Menampilkan data PM10 per kota")
        exec(open("submission/dashboard/partikulasi_polusi/PM10_Perkota.py", encoding='utf-8').read())

    elif selected_submenu == "PM2.5 Per Kota":
        st.write("Menampilkan data PM2.5 per kota")
        exec(open("submission/dashboard/partikulasi_polusi/PM2.5_PerKota.py", encoding='utf-8').read())
