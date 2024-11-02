import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots  # Pastikan ini diimpor
import os
from streamlit_option_menu import option_menu
from babel.numbers import format_currency

st.set_page_config(
    page_title="Partikulasi Polusi",
    page_icon="🏛️",
)

st.title("Korelasi Partikulasi Polusi Per Kota")

# Function to load air quality data files
def load_data():
    current_dir = os.getcwd()
    csv_files = [
        f"PRSA_Data_{city}_20130301-20170228.csv" for city in [
            "Aotizhongxin", "Changping", "Dingling", "Dongsi", 
            "Guanyuan", "Gucheng", "Huairou", "Nongzhanguan", 
            "Shunyi", "Tiantan", "Wanliu", "Wanshouxigong"
        ]
    ]

    dataframes = {}
    for csv_file in csv_files:
        file_path = os.path.join(current_dir, "submission/data", csv_file)
        df = pd.read_csv(file_path)  # Mengasumsikan file selalu ada
        location = csv_file.split('_')[2]
        dataframes[location] = df
    return dataframes

dataframes = load_data()
kota_list = list(dataframes.keys())

# Daily pollution analysis
def partikulasi_polusi_harian(df, year, month, day_start, day_end):
    df = df[(df['year'] == year) & (df['month'] == month) & (df['day'] >= day_start) & (df['day'] <= day_end)]
    result = df.groupby(['year', 'month', 'day']).agg(avg_PM25=('PM2.5', 'mean'), avg_PM10=('PM10', 'mean')).reset_index()
    return result.round({'avg_PM25': 0, 'avg_PM10': 0})

# Weekly pollution analysis
def partikulasi_polusi_mingguan(df, year, month):
    df = df[(df['year'] == year) & (df['month'] == month)]
    df['week'] = ((df['day'] - 1) // 7) + 1
    result = df.groupby(['year', 'month', 'week']).agg(avg_PM25=('PM2.5', 'mean'), avg_PM10=('PM10', 'mean')).reset_index()
    return result.round({'avg_PM25': 0, 'avg_PM10': 0})

# Monthly pollution analysis
def partikulasi_polusi_bulanan(df, year, month):
    df = df[(df['year'] == year) & (df['month'] == month)]
    result = df.groupby(['year', 'month']).agg(avg_PM25=('PM2.5', 'mean'), avg_PM10=('PM10', 'mean')).reset_index()
    return result.round({'avg_PM25': 0, 'avg_PM10': 0})

# Yearly pollution analysis
def partikulasi_polusi_tahunan(df, year):
    df = df[(df['year'] == year)]
    result = df.groupby(['year']).agg(avg_PM25=('PM2.5', 'mean'), avg_PM10=('PM10', 'mean')).reset_index()
    return result.round({'avg_PM25': 0, 'avg_PM10': 0})

# Sidebar with navigation menu
with st.sidebar:
    selected_year = st.selectbox("Pilih Tahun", options=["2013", "2014", "2015", "2016", "2017"], index=0)

    if selected_year:
        selected_period = st.selectbox("Pilih Periode", ["Harian", "Mingguan", "Bulanan", "Tahunan"])
        
        if selected_period == "Harian":
            # Tambahkan input untuk memilih bulan dan hari
            selected_month = st.number_input("Bulan", min_value=3 if selected_year == "2013" else 1, max_value=12 if selected_year != "2017" else 2, value=3)
            selected_day_start = st.number_input("Hari Mulai", min_value=1, max_value=31, value=1)
            selected_day_end = st.number_input("Hari Akhir", min_value=1, max_value=31, value=31)
        
        elif selected_period == "Mingguan":
            # Tambahkan input untuk memilih bulan
            selected_month = st.number_input("Bulan", min_value=3 if selected_year == "2013" else 1, max_value=12 if selected_year != "2017" else 2, value=3)
        
        elif selected_period == "Bulanan":
            # Tambahkan input untuk memilih bulan
            selected_month = st.number_input("Bulan", min_value=3 if selected_year == "2013" else 1, max_value=12 if selected_year != "2017" else 2, value=3)
        
        elif selected_period == "Tahunan":
            # Tidak perlu input tambahan untuk tahunan
            pass

# Display based on selected year and period
if selected_year:
    st.write(f"Analisis untuk tahun {selected_year} dan periode {selected_period}")
    
    # Jika periode harian, tampilkan rentang hari
    if selected_period == "Harian":
        st.write(f"Bulan: {selected_month}, Hari: {selected_day_start} hingga {selected_day_end}")
    elif selected_period == "Mingguan":
        st.write(f"Bulan: {selected_month}")
    elif selected_period == "Bulanan":
        st.write(f"Bulan: {selected_month}")
    elif selected_period == "Tahunan":
        st.write(f"Tahun: {selected_year}")

    if st.button("Analisis untuk Semua Kota"):
        all_results = []

        for kota, df in dataframes.items():
            # Pastikan kolom tahun, bulan, dan hari adalah integer untuk penyaringan
            df[['year', 'month', 'day']] = df[['year', 'month', 'day']].astype(int)
            
            # Lakukan analisis harian untuk setiap kota
            if selected_period == "Harian":
                hasil_kualitas_udara = partikulasi_polusi_harian(df, int(selected_year), selected_month, selected_day_start, selected_day_end)
            elif selected_period == "Mingguan":
                hasil_kualitas_udara = partikulasi_polusi_mingguan(df, int(selected_year), selected_month)
            elif selected_period == "Bulanan":
                hasil_kualitas_udara = partikulasi_polusi_bulanan(df, int(selected_year), selected_month)
            elif selected_period == "Tahunan":
                hasil_kualitas_udara = partikulasi_polusi_tahunan(df, int(selected_year))

            hasil_kualitas_udara['Kota'] = kota  # Tambahkan kolom nama kota
            all_results.append(hasil_kualitas_udara)

        # Gabungkan semua hasil menjadi satu DataFrame
        combined_results = pd.concat(all_results, ignore_index=True)

        # Mengurutkan hasil berdasarkan nilai PM2.5 dan PM10
        combined_results = combined_results.sort_values(by=['avg_PM25', 'avg_PM10'])

        # Pastikan DataFrame tidak kosong sebelum visualisasi
        if not combined_results.empty:
            # Visualisasikan hasil untuk PM2.5 dan PM10 dalam satu frame
            fig = make_subplots(rows=1, cols=2, subplot_titles=("PM2.5", "PM10"))

            # Grafik untuk PM2.5
            fig.add_trace(
                go.Bar(x=combined_results['Kota'], y=combined_results['avg_PM25'], name='PM2.5'),
                row=1, col=1
            )

            # Grafik untuk PM10
            fig.add_trace(
                go.Bar(x=combined_results['Kota'], y=combined_results['avg_PM10'], name='PM10'),
                row=1, col=2
            )

            # Memperbarui layout
            if selected_period == "Tahunan":
                fig.update_layout(title_text=f"Kualitas Udara pada {selected_year}", barmode='group')  # Hanya tahun
            else:
                fig.update_layout(title_text=f"Kualitas Udara pada {selected_year} dan Bulan {selected_month}", barmode='group')  # Tahun dan bulan

            st.plotly_chart(fig)
        else:
            st.warning("Tidak ada data untuk ditampilkan.")
