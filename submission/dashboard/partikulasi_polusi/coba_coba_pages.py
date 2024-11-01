import streamlit as st
import pandas as pd
import os
import plotly.express as px

# Title dan header
st.title("Partikulasi Polusi: 🏭")
st.header("INFORMASI KONSENTRASI PARTIKULAT PM10")
_KETERANGAN = """
Partikulat (PM10) adalah Partikel udara yang berukuran lebih kecil dari 10 mikron (mikrometer).

Nilai Ambang Batas (NAB) adalah Batas konsentrasi polusi udara yang diperbolehkan berada dalam udara ambien. NAB PM10 = 150 µgram/m3.
"""
st.write(_KETERANGAN)

# Metrik
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("BAIK", "0-50 μg/m³", "👨")
col2.metric("SEDANG", "51 - 150 μg/m³", "😐")
col3.metric("TIDAK SEHAT", "151 - 350 μg/m³", "🤒")
col4.metric("SANGAT TIDAK SEHAT", "351-420 μg/m³", "🚨")
col5.metric("BERBAHAYA", "<420 μg/m³", "💀")

# Fungsi untuk memuat data
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

# Fungsi kategori PM10
def kategori_pm10(value):
    if value <= 50:
        return "Baik"
    elif value <= 150:
        return "Sedang"
    elif value <= 350:
        return "Tidak Sehat"
    elif value <= 420:
        return "Sangat Tidak Sehat"
    else:
        return "Berbahaya"

# Fungsi untuk menghitung polusi mingguan (PM10 saja)
def partikulasi_polusi_mingguan(df, year, month):
    filtered_df = df.query('year == @year and month == @month')
    
    # Menghitung kolom 'week' berdasarkan tahun, bulan, dan hari
    filtered_df['week'] = pd.to_datetime(filtered_df[['year', 'month', 'day']]).dt.isocalendar().week
    
    result = filtered_df.groupby(['year', 'month', 'week']).agg(avg_PM10=('PM10', 'mean')).reset_index()
    result['avg_PM10'] = result['avg_PM10'].round()
    return result

# Tabs untuk analisis per periode waktu
tab1, tab2, tab3 = st.tabs(["Mingguan", "Bulanan", "Tahunan"])

with tab1:
    with st.form(key='_form_mingguan'):
        selected_city_mingguan = st.selectbox("Pilih Kota", list(dataframes.keys()))
        selected_year_mingguan = st.number_input("Tahun", min_value=2013, max_value=2017, value=2013)

        if selected_year_mingguan == 2013:
            selected_month_mingguan = st.number_input("Bulan", min_value=3, max_value=12, value=3)
        elif selected_year_mingguan == 2017:
            selected_month_mingguan = st.number_input("Bulan", min_value=1, max_value=2, value=1)
        else:
            selected_month_mingguan = st.number_input("Bulan", min_value=1, max_value=12, value=1)

        if st.form_submit_button("Analisis Mingguan"):
            df = dataframes[selected_city_mingguan]
            df['day'] = df['day'].astype(int)

            hasil_kualitas_udara = partikulasi_polusi_mingguan(df, selected_year_mingguan, selected_month_mingguan)


            # Visualisasi hasil dengan bar chart (PM10 saja) menggunakan warna untuk identifikasi
            fig = px.bar(
                hasil_kualitas_udara, x='week', y='avg_PM10', color='avg_PM10',
                color_discrete_map={
                    "Baik": "green", 
                    "Sedang": "blue", 
                    "Tidak Sehat": "orange", 
                    "Sangat Tidak Sehat": "red", 
                    "Berbahaya": "black"
                },
                title=f"Kualitas Udara Mingguan di {selected_city_mingguan} pada {selected_month_mingguan}/{selected_year_mingguan}",
                labels={'avg_PM10': 'Kadar PM10 (μg/m³)', 'week': 'Minggu'}
            )
            st.plotly_chart(fig)

            # Keterangan untuk tiap minggu
            for index, row in hasil_kualitas_udara.iterrows():
                kategori = kategori_pm10(row['avg_PM10'])
                st.write(f"Minggu ke-{int(row['week'])}: Kadar PM10 rata-rata adalah {row['avg_PM10']} μg/m³ ({kategori}).")
