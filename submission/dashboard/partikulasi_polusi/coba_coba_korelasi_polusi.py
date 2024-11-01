# import library
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import os

# navbar page config
st.set_page_config(
    page_title="Korelasi Partikulasi Polusi",
    page_icon="🌫️",
)

# load data
def load_data():
    current_dir = os.getcwd()
    csv_files = [f"PRSA_Data_{city}_20130301-20170228.csv" for city in ["Aotizhongxin", "Changping", "Dingling", "Dongsi", "Guanyuan", "Gucheng", "Huairou", "Nongzhanguan", "Shunyi", "Tiantan", "Wanliu", "Wanshouxigong"]]

    dataframes = {}
    for csv_file in csv_files:
        file_path = os.path.join(current_dir, "submission/data", csv_file)
        df = pd.read_csv(file_path)
        location = csv_file.split('_')[2]
        dataframes[location] = df
    return dataframes  

dataframes = load_data()

# Filter functions for various periods
def korelasi_partikulasi_polusi_harian(df, year, month):
    filtered_df = df[(df['year'] == year) & (df['month'] == month)]
    return filtered_df

def korelasi_partikulasi_polusi_mingguan(df, year, month):
    filtered_df = df[(df['year'] == year) & (df['month'] == month)]
    return filtered_df

def korelasi_partikulasi_polusi_bulanan(df, year, month):
    filtered_df = df[(df['year'] == year) & (df['month'] == month)]
    return filtered_df

def korelasi_partikulasi_polusi_tahunan(df, year):
    filtered_df = df[df['year'] == year]
    return filtered_df

# Fungsi untuk mendapatkan kategori kualitas udara
def get_kategori(pm25):
    if pm25 <= 15.5:
        return 'Baik'
    elif 15.5 < pm25 <= 55.4:
        return 'Sedang'
    elif 55.5 < pm25 <= 150.4:
        return 'Tidak Sehat'
    elif 150.5 < pm25 <= 250.4:
        return 'Sangat Tidak Sehat'
    else:
        return 'Berbahaya'

def get_kategori_pm10(pm10):
    if pm10 <= 50:
        return 'Baik'
    elif 51 <= pm10 <= 150:
        return 'Sedang'
    elif 151 <= pm10 <= 350:
        return 'Tidak Sehat'
    elif 351 <= pm10 <= 420:
        return 'Sangat Tidak Sehat'
    else:
        return 'Berbahaya'

st.title("Analisis Korelasi Partikulasi Polusi")  # Pastikan judul ditampilkan dengan benar

# Sidebar input
with st.sidebar:
    selected_year = st.selectbox("Pilih Tahun", options=["2013", "2014", "2015", "2016", "2017"], index=0)
    selected_period = st.selectbox("Pilih Periode", ["Harian", "Mingguan", "Bulanan", "Tahunan"])

    if selected_period in ["Harian", "Mingguan", "Bulanan"]:
        selected_month = st.number_input(
            "Bulan", 
            min_value=3 if selected_year == "2013" else 1, 
            max_value=12 if selected_year != "2017" else 2, 
            value=3
        )
    


# Analisis berdasarkan pilihan periode
if st.button("Analisis"):
    year = int(selected_year)
    month = int(selected_month) if selected_period != "Tahunan" else None

    if selected_period == "Harian":
        filtered_df = pd.concat([korelasi_partikulasi_polusi_harian(df, year, month) for df in dataframes.values()])
    elif selected_period == "Mingguan":
        filtered_df = pd.concat([korelasi_partikulasi_polusi_mingguan(df, year, month) for df in dataframes.values()])
    elif selected_period == "Bulanan":
        # Analisis bulanan tanpa menggunakan filtered_df
        monthly_data = pd.concat([korelasi_partikulasi_polusi_bulanan(df, year, month) for df in dataframes.values()])
        
        # Hitung rata-rata PM2.5 dan PM10 untuk setiap bulan
        monthly_avg_pm25 = monthly_data.groupby(['year', 'month'])['PM2.5'].mean().reset_index()
        monthly_avg_pm10 = monthly_data.groupby(['year', 'month'])['PM10'].mean().reset_index()

        # Gabungkan rata-rata PM2.5 dan PM10
        monthly_avg = pd.merge(monthly_avg_pm25, monthly_avg_pm10, on=['year', 'month'], suffixes=('_pm25', '_pm10'))

        # Membuat chart_data untuk visualisasi
        chart_data = {
            "col1": list(range(len(monthly_avg))),  # Indeks bulan
            "col2": monthly_avg['PM2.5'].tolist(),  # Rata-rata PM2.5
            "col3": monthly_avg['PM10'].tolist(),    # Rata-rata PM10
            "col4": np.random.rand(len(monthly_avg)),  # Data acak untuk kolom 4
            "col5": np.random.rand(len(monthly_avg))   # Data acak untuk kolom 5
        }

        # Mengonversi chart_data menjadi DataFrame
        chart_df = pd.DataFrame(chart_data)

        # Membuat bar chart untuk visualisasi
        fig = px.bar(chart_df, x='col1', y=['col2', 'col3', 'col4', 'col5'], 
                     title='Visualisasi Korelasi Partikulasi Polusi Bulanan', 
                     labels={'value': 'Kadar Polutan (μg/m³)', 'variable': 'Parameter'})
        st.plotly_chart(fig)

    elif selected_period == "Tahunan":
        filtered_df = pd.concat([korelasi_partikulasi_polusi_tahunan(df, year) for df in dataframes.values()])

    # Pastikan filtered_df didefinisikan sebelum digunakan
    if 'filtered_df' in locals() and not filtered_df.empty:
        # Plotting
        filtered_df['kategori'] = filtered_df['PM2.5'].apply(get_kategori)
        filtered_df['kategori_pm10'] = filtered_df['PM10'].apply(get_kategori_pm10)

        # Hitung rata-rata PM2.5 dan PM10 untuk setiap hari
        filtered_df['avg_pm25'] = filtered_df.groupby('day')['PM2.5'].transform('mean')
        filtered_df['avg_pm10'] = filtered_df.groupby('day')['PM10'].transform('mean')

        colors = {
            'Baik': 'green',
            'Sedang': 'blue',
            'Tidak Sehat': 'orange',
            'Sangat Tidak Sehat': 'red',
            'Berbahaya': 'black'
        }

        st.header(f"Korelasi Partikulasi Polusi di {selected_period} {selected_year}")

        # Buat subplot untuk setiap kota untuk PM2.5
        for city in dataframes.keys():
            fig, ax = plt.subplots(figsize=(12, 6))
            city_data = filtered_df[filtered_df['station'] == city]
            ax.plot(city_data['day'], city_data['PM2.5'], label=f'{city} PM2.5', color=colors[city_data['kategori'].iloc[0]], linestyle='-', marker='o')

            # Set label sumbu untuk PM2.5
            ax.set_title(f'Konsentrasi PM2.5 di {city}')
            ax.set_xlabel('Hari (1-31)')
            ax.set_ylabel('Konsentrasi PM2.5 (ug/m3)')
            ax.set_xlim(1, 31)  # Rentang hari
            ax.set_ylim(0, 400)  # Set batas sumbu y
            ax.legend()
            ax.grid(True)  # Menambahkan grid untuk visualisasi yang lebih baik
            st.pyplot(fig)

        # Buat subplot untuk setiap kota untuk PM10
        for city in dataframes.keys():
            fig, ax = plt.subplots(figsize=(12, 6))
            city_data = filtered_df[filtered_df['station'] == city]
            ax.plot(city_data['day'], city_data['PM10'], label=f'{city} PM10', color=colors[city_data['kategori_pm10'].iloc[0]], linestyle='--', marker='x')

            # Set label sumbu untuk PM10
            ax.set_title(f'Konsentrasi PM10 di {city}')
            ax.set_xlabel('Hari (1-31)')
            ax.set_ylabel('Konsentrasi PM10 (ug/m3)')
            ax.set_xlim(1, 31)  # Rentang hari
            ax.set_ylim(0, 900)  # Set batas sumbu y
            ax.legend()
            ax.grid(True)  # Menambahkan grid untuk visualisasi yang lebih baik
            st.pyplot(fig)
