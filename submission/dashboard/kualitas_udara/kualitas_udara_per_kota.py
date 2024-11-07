# import semua library yang diperlukan
import streamlit as st
import numpy as np
import pandas as pd
import os
from plotly.subplots import make_subplots
import plotly.graph_objects as go  # Add this line to import go

# load page config
st.title("Tingkat Polusi Per Kota ")
st.header("Informasi")

# load dataset
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
        df = pd.read_csv(file_path)
        location = csv_file.split('_')[2]
        dataframes[location] = df
    return dataframes

dataframes = load_data()

# code engine kualitas udara per kota
def load_data():
    current_dir = os.getcwd()
    cities = [
        "Aotizhongxin", "Changping", "Dingling", "Dongsi", 
        "Guanyuan", "Gucheng", "Huairou", "Nongzhanguan", 
        "Shunyi", "Tiantan", "Wanliu", "Wanshouxigong"
    ]

    dataframes = {city: None for city in cities}  # Membuat dictionary dengan kota sebagai kunci

    for city in cities:
        csv_file = f"PRSA_Data_{city}_20130301-20170228.csv"
        file_path = os.path.join(current_dir, "submission/data", csv_file)
        df = pd.read_csv(file_path)
        dataframes[city] = df
    return dataframes
dataframes = load_data()

# Fungsi untuk menentukan kategori PM2.5 dan PM10
def kategori_pm25(value):
    if value <= 50:
        return 'Baik'
    elif value <= 100:
        return 'Sedang'
    elif value <= 150:
        return 'Tidak Sehat'
    else:
        return 'Berbahaya'

def kategori_pm10(value):
    if value <= 50:
        return 'Baik'
    elif value <= 100:
        return 'Sedang'
    elif value <= 150:
        return 'Tidak Sehat'
    else:
        return 'Berbahaya'
    
def kategori_co(co):
    if co <= 4000:
        return 'BAIK'
    elif 4000 < co <= 8000:
        return 'SEDANG'
    elif 8000 < co <= 15000:
        return 'TIDAK SEHAT'
    elif 15000 < co <= 30000:
        return 'BERBAHAYA'
    else:
        return 'SANGAT BERBAHAYA'

def kategori_no2(value):
    if value <= 80:
        return "BAIK"
    elif value <= 200:
        return "SEDANG"
    elif value <= 1130:
        return "TIDAK SEHAT"
    elif value <= 2260:
        return "SANGAT TIDAK SEHAT"
    else:
        return "BERBAHAYA"
    
def kategori_o3(value):
    if value <= 4000:
        return "BAIK"
    elif value <= 8000:
        return "SEDANG"
    elif value <= 15000:
        return "TIDAK SEHAT"
    elif value <= 30000:
        return "SANGAT TIDAK SEHAT"
    else:
        return "BERBAHAYA"

# Memperbaiki indentasi di sini
def kategori_so2(value):
    if value <= 52:
        return "BAIK"
    elif value <= 180:
        return "SEDANG"
    elif value <= 400:
        return "TIDAK SEHAT"
    elif value <= 800:
        return "SANGAT TIDAK SEHAT"
    else:
        return "BERBAHAYA"   

# Kualitas Udara Bulanan
def kualitas_Udara_bulanan(df, year, month):
    filtered_df = df.query('year == @year and month == @month')
    result = (
        filtered_df.groupby(['year', 'month'])
        .agg(
            avg_PM25=('PM2.5', 'mean'),
            avg_PM10=('PM10', 'mean'),
            avg_SO2=('SO2', 'mean'),
            avg_NO2=('NO2', 'mean'),
            avg_CO=('CO', 'mean'),
            avg_O3=('O3', 'mean')
        )
    )
    
    # Pembulatan hasil rata-rata
    result['avg_PM25'] = result['avg_PM25'].round()
    result['avg_PM10'] = result['avg_PM10'].round()
    result['avg_SO2'] = result['avg_SO2'].round()
    result['avg_NO2'] = result['avg_NO2'].round()
    result['avg_CO'] = result['avg_CO'].round()
    result['avg_O3'] = result['avg_O3'].round()

    # Menambahkan kategori untuk setiap polutan
    result['kategori_pm25_bulanan'] = result['avg_PM25'].apply(kategori_pm25)
    result['kategori_pm10_bulanan'] = result['avg_PM10'].apply(kategori_pm10)
    result['kategori_co'] = result['avg_CO'].apply(kategori_co)
    result['kategori_no2'] = result['avg_NO2'].apply(kategori_no2)
    result['kategori_o3'] = result['avg_O3'].apply(kategori_o3)
    result['kategori_so2'] = result['avg_SO2'].apply(kategori_so2)

    return result
# Tab Setup 
tab1, tab2 = st.tabs([ "Bulanan", "Tahunan"])
with tab1:
    with st.form(key='_form_bulanan'):
        selected_year_bulanan = st.number_input("Pilih Tahun", min_value=2013, max_value=2017, step=1)
        if selected_year_bulanan == 2013:
            selected_month_bulanan = st.number_input("Pilih Bulan", min_value=3, max_value=12, step=1)
        elif selected_year_bulanan == 2017:
            selected_month_bulanan = st.number_input("Pilih Bulan", min_value=1, max_value=2, step=1)
        else:
            selected_month_bulanan = st.number_input("Pilih Bulan", min_value=1, max_value=12, step=1)
        submit_button_bulanan = st.form_submit_button(label='Analisa Bulanan')

    if submit_button_bulanan:
        st.header(f"Konsentrasi PM2.5, PM10, SO2, NO2, CO, O3 Bulanan di Semua Kota pada Tahun {selected_year_bulanan} dan Bulan {selected_month_bulanan}")

        all_cities_data = []
        for city, df in dataframes.items():
            # Apply the new analysis function to get air quality data for the selected year and month
            monthly_data = kualitas_Udara_bulanan(df, selected_year_bulanan, selected_month_bulanan)
            monthly_data['location'] = city
            all_cities_data.append(monthly_data)

        all_cities_data = pd.concat(all_cities_data, ignore_index=True)
        
        # Membuat subplots dengan 1 baris dan 2 kolom
        fig = make_subplots(rows=1, cols=1)

        # Tambahkan konfigurasi warna kategori
        warna_kategori = {
            "Baik": 'green',
            "Sedang": 'blue',
            "Tidak Sehat": 'orange',
            "Sangat Tidak Sehat": 'red',
            "Berbahaya": 'black'
        }

        # Grafik bar chart untuk PM2.5 dan PM10 dalam satu frame
        fig.add_trace(
            go.Bar(
                x=all_cities_data['location'],
                y=all_cities_data['avg_PM25'],
                name='PM2.5',
                marker_color=[warna_kategori[kategori] for kategori in all_cities_data['kategori_pm25_bulanan']],
                width=0.4,  # Lebar bar PM2.5
                offsetgroup=0,  # Offset untuk PM2.5
                hoverinfo='y+name'  # Menampilkan informasi saat dihover
            )
        )

        fig.add_trace(
            go.Bar(
                x=all_cities_data['location'],
                y=all_cities_data['avg_PM10'],
                name='PM10',
                marker_color=[warna_kategori[kategori] for kategori in all_cities_data['kategori_pm10_bulanan']],
                width=0.4,  # Lebar bar PM10
                offsetgroup=1,  # Offset untuk PM10
                hoverinfo='y+name'  # Menampilkan informasi saat dihover
            )
        )

        # Update layout untuk mempercantik plot
        fig.update_layout(
            height=500,
            title_text=f"Konsentrasi PM2.5 dan PM10 Bulanan di Semua Kota pada Tahun {selected_year_bulanan} dan Bulan {selected_month_bulanan}",
            barmode='group',  # Mengatur mode bar menjadi 'group' untuk menampilkan berdampingan
            xaxis_title="Kota",
            yaxis_title="Konsentrasi (µg/m³)",
            yaxis=dict(range=[0, 420])  # Mengatur rentang sumbu Y menjadi 0 hingga 420
        )

        # Tampilkan chart di Streamlit
        st.plotly_chart(fig, use_container_width=True)

        # Keterangan analisis untuk PM2.5 dan PM10
        rata_rata_pm25 = all_cities_data['avg_PM25'].mean()
        rata_rata_pm10 = all_cities_data['avg_PM10'].mean()
        kategori_pm25 = kategori_pm25(rata_rata_pm25)
        kategori_pm10 = kategori_pm10(rata_rata_pm10)

        st.write(f"Rata-rata konsentrasi PM2.5 untuk seluruh kota pada tahun {selected_year_bulanan} bulan {selected_month_bulanan} adalah {rata_rata_pm25:.2f} µg/m³, termasuk dalam kategori {kategori_pm25}.")
        st.write(f"Rata-rata konsentrasi PM10 untuk seluruh kota pada tahun {selected_year_bulanan} bulan {selected_month_bulanan} adalah {rata_rata_pm10:.2f} µg/m³, termasuk dalam kategori {kategori_pm10}.")

        # Analisis untuk SO2, NO2, CO, O3
        rata_rata_so2 = all_cities_data['avg_SO2'].mean()
        rata_rata_no2 = all_cities_data['avg_NO2'].mean()
        rata_rata_co = all_cities_data['avg_CO'].mean()
        rata_rata_o3 = all_cities_data['avg_O3'].mean()

        st.write(f"Rata-rata konsentrasi SO2 untuk seluruh kota pada tahun {selected_year_bulanan} bulan {selected_month_bulanan} adalah {rata_rata_so2:.2f} µg/m³.")
        st.write(f"Rata-rata konsentrasi NO2 untuk seluruh kota pada tahun {selected_year_bulanan} bulan {selected_month_bulanan} adalah {rata_rata_no2:.2f} µg/m³.")
        st.write(f"Rata-rata konsentrasi CO untuk seluruh kota pada tahun {selected_year_bulanan} bulan {selected_month_bulanan} adalah {rata_rata_co:.2f} µg/m³.")
        st.write(f"Rata-rata konsentrasi O3 untuk seluruh kota pada tahun {selected_year_bulanan} bulan {selected_month_bulanan} adalah {rata_rata_o3:.2f} µg/m³.")
