# import semua library yang diperlukan
import streamlit as st
import numpy as np
import pandas as pd
import os
import time
import plotly.express as px

# load dataset
st.title("🪟 Kualitas Udara: CO")
st.header("🔍 INFORMASI KONSENTRASI GAS CO")

_KETERANGAN = """
🌫️ **CO (Karbon Monoksida): Gas Tak Terlihat yang Berbahaya**

Gas CO adalah zat tak berwarna, tak berbau, dan tak berasa, tapi sangat berbahaya. Gas ini muncul akibat pembakaran tidak sempurna dari bahan bakar fosil, seperti bensin dan gas alam. 
"""
st.write(_KETERANGAN)
if st.button('Informasi Dampak Pencemaran CO'):
    st.subheader("Dampak Pencemaran CO")
    st.subheader("Dampak Pencemaran CO pada Kesehatan")
    st.write("🏥")

    st.write("CO bisa menempel pada hemoglobin dalam darah lebih kuat dibandingkan oksigen. Ini mengurangi asupan oksigen dalam tubuh, memicu sakit kepala hingga masalah serius pada jantung, bahkan berisiko mematikan. Karena CO tak terdeteksi oleh indra kita, gas ini dikenal sebagai ancaman yang “silen.”")

    st.write("Paparan singkat CO dapat menyebabkan sakit kepala, pusing, mual. Sementara paparan jangka panjang dapat meningkatkan risiko penyakit jantung, paru-paru, dan kanker.")

    st.subheader("Lingkungan 🌿")
    st.write("CO berkontribusi pada perubahan iklim.")

    st.subheader("Cara Mengurangi Paparan CO")
    st.write("Batasi penggunaan kendaraan pribadi.")
    st.write("Rawat alat pembakaran seperti kompor.")
    st.write("Tanam pohon untuk menyerap polutan.")

# buat metric
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric(label="BAIK", value="0-4000 μg/m³")
col2.metric(label="SEDANG", value="4000-8000 μg/m³")
col3.metric(label="TIDAK SEHAT", value="8000-15000 μg/m³")
col4.metric(label="BERBAHAYA", value="15000-30000 μg/m³")
col5.metric(label="SANGAT BERBAHAYA", value=">30000 μg/m³")

# Function to load air quality data files
def load_data():
    current_dir = os.getcwd()
    csv_files = [f"PRSA_Data_{city}_20130301-20170228.csv" for city in ["Aotizhongxin", "Changping", "Dingling", "Dongsi", "Guanyuan", "Gucheng", "Huairou", "Nongzhanguan", "Shunyi", "Tiantan", "Wanliu", "Wanshouxigong"]]
    dataframes = {}
    for csv_file in csv_files:
        file_path = os.path.join(current_dir, "submission/data", csv_file)
        df = pd.read_csv(file_path, encoding='utf-8')
        location = csv_file.split('_')[2]
        dataframes[location] = df
    return dataframes

dataframes = load_data()

# Fungsi untuk menentukan kategori CO dengan konsistensi kapitalisasi
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
    
   # Mengkategorikan Warna
color_map = {
    "BAIK": "green",
    "SEDANG": "blue",
    "TIDAK SEHAT": "orange",
    "SANGAT TIDAK SEHAT": "red",
    "BERBAHAYA": "black"
} 
# co harian
def co_harian(df, year, month, day_start, day_end):
    filtered_df = df.query('year == @year and month == @month and day >= @day_start and day <= @day_end')

    result = (
        filtered_df.groupby(['year', 'month', 'day'])
        .agg(avg_CO=('CO', 'mean'))
        .reset_index()
    )

    result['avg_CO'] = result['avg_CO'].round()

    return result


# Fungsi untuk menghitung CO mingguan
def co_mingguan(df, year, month):
    filtered_df = df.query('year == @year and month == @month')

    filtered_df['week'] = filtered_df['day'].apply(lambda x: (x - 1) // 7 + 1)

    result = (
        filtered_df.groupby(['year', 'month', 'week'])
        .agg(avg_CO=('CO', 'mean'))
        .reset_index()
    )
    result['avg_CO'] = result['avg_CO'].round()
    result['kategori_co'] = result['avg_CO'].apply(kategori_co)
    return result

# co bulanan
def co_bulanan(df, year):
    filtered_df = df[df['year'] == year]

    result = (
        filtered_df.groupby('month')
        .agg(avg_CO=('CO', 'mean'))
        .reset_index()
    )

    result['avg_CO'] = result['avg_CO'].round()
    result['kategori_co_bulanan'] = result['avg_CO'].apply(kategori_co)

    return result

# co tahunan

def co_tahunan(df, year):
    filtered_df = df[df['year'] == year]

    result = (
        filtered_df.groupby('year')
        .agg(avg_CO=('CO', 'mean'))
        .reset_index()
    )

    result['avg_CO'] = result['avg_CO'].round()

    return result

# membuat tabs
tab1, tab2, tab3, tab4 = st.tabs(["Harian", "Mingguan", "Bulanan", "Tahunan"])

# tab 1 co harian
with tab1:
    with st.form(key='_form_harian_co'):
        selected_city_harian_co = st.selectbox("Pilih Kota", list(dataframes.keys()))
        selected_year_harian_co = st.number_input("Pilih Tahun", min_value=2013, max_value=2017, step=1)
        if selected_year_harian_co == 2013:
            selected_month_harian_co = st.number_input("Pilih Bulan", min_value=3, max_value=12, step=1)
        elif selected_year_harian_co == 2017:
            selected_month_harian_co = st.number_input("Pilih Bulan", min_value=1, max_value=2, step=1)
        else:
            selected_month_harian_co = st.number_input("Pilih Bulan", min_value=1, max_value=12, step=1)
        submit_button_harian_co = st.form_submit_button(label='Analisa Harian')
        
    if submit_button_harian_co:
        st.header(f"Konsentrasi CO Harian di {selected_city_harian_co}")
        filtered_data_co = co_harian(dataframes[selected_city_harian_co], selected_year_harian_co, selected_month_harian_co, 1, 31)
        filtered_data_co['kategori_co'] = filtered_data_co['avg_CO'].apply(kategori_co)
        st.vega_lite_chart(
            {
                "layer": [
                    {
                        "mark": "bar",
                        "encoding": {
                            "x": {"field": "day", "type": "ordinal", "axis": {"title": "Hari"}},
                            "y": {"field": "avg_CO", "type": "quantitative", "axis": {"title": "CO (ppm)", "scale": {"domain": [0, 4000]}}},
                            "color": {
                                "field": "kategori_co",
                                "type": "nominal",
                                "scale": {
                                    "domain": ["BAIK", "SEDANG", "TIDAK SEHAT", "BERBAHAYA", "SANGAT BERBAHAYA"],
                                    "range": ["green", "blue", "orange", "red", "black"]
                                },
                                "legend": {"title": "Kategori CO"}
                            },
                            "tooltip": [
                                {"field": "day", "type": "ordinal", "title": "Hari"},
                                {"field": "avg_CO", "type": "quantitative", "title": "CO (ppm)"},
                                {"field": "kategori_co", "type": "nominal", "title": "Kategori CO"}
                            ]
                        }
                    }
                ],
                "title": f"Konsentrasi CO di {selected_city_harian_co}",
                "data": {"values": filtered_data_co.to_dict("records")}
            }
        )
        rata_rata_harian_co = filtered_data_co['avg_CO'].mean()
        kategori_rata_rata_co = kategori_co(rata_rata_harian_co)
        if kategori_rata_rata_co == "BAIK":
            keterangan_co = f"Rata-rata konsentrasi CO harian di {selected_city_harian_co} pada bulan {selected_month_harian_co} tahun {selected_year_harian_co} adalah {rata_rata_harian_co:.2f} ppm, yang termasuk dalam kategori {kategori_rata_rata_co}. Kualitas udara di kota ini sangat baik dan tidak berbahaya bagi kesehatan."
        elif kategori_rata_rata_co == "SEDANG":
            keterangan_co = f"Rata-rata konsentrasi CO harian di {selected_city_harian_co} pada bulan {selected_month_harian_co} tahun {selected_year_harian_co} adalah {rata_rata_harian_co:.2f} ppm, yang termasuk dalam kategori {kategori_rata_rata_co}. Kualitas udara di kota ini sedang dan perlu diawasi untuk mencegah penurunan kualitas udara."
        elif kategori_rata_rata_co == "TIDAK SEHAT":
            keterangan_co = f"Rata-rata konsentrasi CO harian di {selected_city_harian_co} pada bulan {selected_month_harian_co} tahun {selected_year_harian_co} adalah {rata_rata_harian_co:.2f} ppm, yang termasuk dalam kategori {kategori_rata_rata_co}. Kualitas udara di kota ini tidak sehat dan perlu diambil tindakan untuk mengurangi polusi."
        elif kategori_rata_rata_co == "BERBAHAYA":
            keterangan_co = f"Rata-rata konsentrasi CO harian di {selected_city_harian_co} pada bulan {selected_month_harian_co} tahun {selected_year_harian_co} adalah {rata_rata_harian_co:.2f} ppm, yang termasuk dalam kategori {kategori_rata_rata_co}. Kualitas udara di kota ini berbahaya bagi kesehatan dan perlu diambil tindakan segera untuk mengurangi polusi."
        elif kategori_rata_rata_co == "SANGAT BERBAHAYA":
            keterangan_co = f"Rata-rata konsentrasi CO harian di {selected_city_harian_co} pada bulan {selected_month_harian_co} tahun {selected_year_harian_co} adalah {rata_rata_harian_co:.2f} ppm, yang termasuk dalam kategori {kategori_rata_rata_co}. Kualitas udara di kota ini sangat berbahaya bagi kesehatan dan perlu diambil tindakan darurat untuk mengurangi polusi."
        st.write(keterangan_co)

# tab 2 co mingguan
with tab2:
    with st.form(key='_form_mingguan_co'):
        selected_city_mingguan_co = st.selectbox("Pilih Kota", list(dataframes.keys()))
        selected_year_mingguan_co = st.number_input("Pilih Tahun", min_value=2013, max_value=2017, step=1, value=2013)
        selected_month_mingguan_co = st.number_input("Pilih Bulan", min_value=3, max_value=12, step=1, value=3)
        submit_button_mingguan_co = st.form_submit_button(label='Analisa Mingguan')
    
    if submit_button_mingguan_co:
        df = dataframes[selected_city_mingguan_co]
        # Pastikan kolom 'day' bertipe integer
        if df['day'].dtype != 'int':
            df['day'] = df['day'].astype(int)
        
        hasil_kualitas_udara_co = co_mingguan(df, selected_year_mingguan_co, selected_month_mingguan_co)
        
        fig = px.bar(
            hasil_kualitas_udara_co, x='week', y='avg_CO', color='kategori_co',
            color_discrete_map={
                "BAIK": "green", 
                "SEDANG": "blue", 
                "TIDAK SEHAT": "orange", 
                "BERBAHAYA": "red", 
                "SANGAT BERBAHAYA": "black"
            },
            title=f"Kualitas Udara Mingguan di {selected_city_mingguan_co} pada Bulan {selected_month_mingguan_co} Tahun {selected_year_mingguan_co}",
            labels={"week": "Minggu", "avg_CO": "Rata-rata CO (ppm)", "kategori_co": "Kategori CO"}
        )
        st.plotly_chart(fig)

        
        # Menghasilkan interpretasi berdasarkan kategori
        rata_rata_mingguan_co = hasil_kualitas_udara_co['avg_CO'].mean()
        kategori_rata_rata_co = kategori_co(rata_rata_mingguan_co)
        if kategori_rata_rata_co == "BAIK":
            keterangan_co = f"Rata-rata konsentrasi CO mingguan di {selected_city_mingguan_co} pada bulan {selected_month_mingguan_co} tahun {selected_year_mingguan_co} adalah {rata_rata_mingguan_co:.2f} ppm, yang termasuk dalam kategori {kategori_rata_rata_co}. Kualitas udara sangat baik dan tidak berbahaya bagi kesehatan."
        elif kategori_rata_rata_co == "SEDANG":
            keterangan_co = f"Rata-rata konsentrasi CO mingguan di {selected_city_mingguan_co} pada bulan {selected_month_mingguan_co} tahun {selected_year_mingguan_co} adalah {rata_rata_mingguan_co:.2f} ppm, yang termasuk dalam kategori {kategori_rata_rata_co}. Kualitas udara masih aman, namun perlu diawasi untuk mencegah peningkatan polusi."
        elif kategori_rata_rata_co == "TIDAK SEHAT":
            keterangan_co = f"Rata-rata konsentrasi CO mingguan di {selected_city_mingguan_co} pada bulan {selected_month_mingguan_co} tahun {selected_year_mingguan_co} adalah {rata_rata_mingguan_co:.2f} ppm, yang termasuk dalam kategori {kategori_rata_rata_co}. Kualitas udara tidak sehat dan perlu pengurangan aktivitas yang menyebabkan polusi."
        elif kategori_rata_rata_co == "BERBAHAYA":
            keterangan_co = f"Rata-rata konsentrasi CO mingguan di {selected_city_mingguan_co} pada bulan {selected_month_mingguan_co} tahun {selected_year_mingguan_co} adalah {rata_rata_mingguan_co:.2f} ppm, yang termasuk dalam kategori {kategori_rata_rata_co}. Udara berbahaya dan tindakan pencegahan perlu dilakukan segera."
        elif kategori_rata_rata_co == "SANGAT BERBAHAYA":
            keterangan_co = f"Rata-rata konsentrasi CO mingguan di {selected_city_mingguan_co} pada bulan {selected_month_mingguan_co} tahun {selected_year_mingguan_co} adalah {rata_rata_mingguan_co:.2f} ppm, yang termasuk dalam kategori {kategori_rata_rata_co}. Situasi sangat berbahaya dan tindakan darurat diperlukan."

        st.write(keterangan_co)

# Tab 3 co bulanan
with tab3:
    with st.form(key='_form_bulanan_co'):
        selected_city_bulanan_co = st.selectbox("Pilih Kota", list(dataframes.keys()))
        selected_year_bulanan_co = st.number_input("Pilih Tahun", min_value=2013, max_value=2017, step=1, value=2013)
        submit_button_bulanan_co = st.form_submit_button(label='Analisa Bulanan')

    if submit_button_bulanan_co:
        df = dataframes[selected_city_bulanan_co]
        hasil_kualitas_udara_co_bulanan = co_bulanan(df, selected_year_bulanan_co)

        fig = px.bar(
            hasil_kualitas_udara_co_bulanan, x='month', y='avg_CO', color='kategori_co_bulanan',
            color_discrete_map={
                "BAIK": "green", 
                "SEDANG": "blue", 
                "TIDAK SEHAT": "orange", 
                "BERBAHAYA": "red", 
                "SANGAT BERBAHAYA": "black"
            },
            title=f"Kualitas Udara Bulanan di {selected_city_bulanan_co} pada Tahun {selected_year_bulanan_co}",
            labels={"month": "Bulan", "avg_CO": "CO (μg/m³)"}
        )
        
        st.plotly_chart(fig)

        # Menampilkan rata-rata bulanan CO
        rata_rata_bulanan_co = hasil_kualitas_udara_co_bulanan['avg_CO'].mean()
        kategori_rata_rata_bulanan_co = kategori_co(rata_rata_bulanan_co)
        st.write(f"Rata-rata konsentrasi CO bulanan di {selected_city_bulanan_co} pada tahun {selected_year_bulanan_co} adalah {rata_rata_bulanan_co:.2f} μg/m³, yang termasuk dalam kategori {kategori_rata_rata_bulanan_co}.")

# tab 4 co tahunan
with tab4:
    with st.form(key='_form_tahunan_co'):
        selected_city_tahunan_co = st.selectbox("Pilih Kota", list(dataframes.keys()))
        submit_button_tahunan_co = st.form_submit_button(label='Analisa Tahunan')

    if submit_button_tahunan_co:
        df = dataframes[selected_city_tahunan_co]
        hasil_kualitas_udara_co_tahunan = pd.concat([co_tahunan(df, year) for year in range(2013, 2018)])

        fig = px.bar(
            hasil_kualitas_udara_co_tahunan, x='year', y='avg_CO',
            title=f"Kualitas Udara Tahunan di {selected_city_tahunan_co}",
            labels={"year": "Tahun", "avg_CO": "CO (μg/m³)"}
        )
        
        st.plotly_chart(fig)

        # Menampilkan rata-rata tahunan CO
        rata_rata_tahunan_co = hasil_kualitas_udara_co_tahunan['avg_CO'].mean()
        kategori_rata_rata_tahunan_co = kategori_co(rata_rata_tahunan_co)
        st.write(f"Rata-rata konsentrasi CO tahunan di {selected_city_tahunan_co} dari tahun 2013 hingga 2017 adalah {rata_rata_tahunan_co:.2f} μg/m³, yang termasuk dalam kategori {kategori_rata_rata_tahunan_co}.")




