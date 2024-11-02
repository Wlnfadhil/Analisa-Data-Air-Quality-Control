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
def partikulasi_polusi_tahunan(df, year):
    filtered_df = df.query('year == @year')

    result = (
        filtered_df.groupby(['year'])
        .agg(avg_PM25=('PM2.5', 'mean'), avg_PM10=('PM10', 'mean'))
        .reset_index()
    )

    result['avg_PM25'] = result['avg_PM25'].round()
    result['avg_PM10'] = result['avg_PM10'].round()

    return result


# Tabs untuk analisis per periode waktu
tab1, tab2, tab3 = st.tabs(["Mingguan", "Bulanan", "Tahunan"])

with tab1:
    with st.form(key='_form_tahunan'):
        st.header("Analisis Partikulasi Polusi Tahunan")

        kota_list = list(dataframes.keys())
        selected_kota = st.selectbox("Pilih Kota", kota_list)

        if st.form_submit_button("Analisis Tahunan"):
            df = dataframes[selected_kota]
            hasil_kualitas_udara = pd.DataFrame()
            for tahun in range(2013, 2018):
                hasil_kualitas_udara_tahun = partikulasi_polusi_tahunan(df, tahun)
                hasil_kualitas_udara = pd.concat([hasil_kualitas_udara, hasil_kualitas_udara_tahun])

            # Menambahkan kolom kategori berdasarkan PM10
            hasil_kualitas_udara['kategori'] = hasil_kualitas_udara['avg_PM10'].apply(kategori_pm10)

            # Visualisasi hasil tahunan
            fig = px.bar(hasil_kualitas_udara, x='year', y=['avg_PM25', 'avg_PM10'],
                         title=f"Kualitas Udara di {selected_kota} dari 2013 hingga 2017",
                         labels={'value': 'Kadar Polutan (μg/m³)', 'year': 'Tahun'},
                         color='kategori',  # Menggunakan kategori untuk pewarnaan
                         color_discrete_map={
                             "Baik": 'green',
                             "Sedang": 'blue',
                             "Tidak Sehat": 'orange',
                             "Sangat Tidak Sehat": 'red',
                             "Berbahaya": 'black'
                         })  # Menggunakan peta warna yang ditentukan
            fig.update_yaxes(range=[0, 420])
            fig.update_xaxes(tickvals=[2013, 2014, 2015, 2016, 2017])
            st.plotly_chart(fig)

            # Menulis keterangan menggunakan magic write tentang keadaan polusi
            st.write("Dari tahun 2013 hingga 2017, kualitas udara di {} telah mengalami variasi. Tahun-tahun tertentu menunjukkan kualitas udara yang tidak sehat dan sangat tidak sehat, sedangkan tahun lainnya menunjukkan kualitas udara yang sedang dan baik. Hal ini menunjukkan pentingnya pengawasan dan pengendalian polusi udara untuk meningkatkan kualitas hidup masyarakat.".format(selected_kota))


