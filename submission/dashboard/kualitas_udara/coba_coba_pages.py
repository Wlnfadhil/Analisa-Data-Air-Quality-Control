import streamlit as st
import pandas as pd
import os
import plotly.express as px

# Title and Header
st.title("Kualitas Udara: NO2, 🌀")
st.header("INFORMASI KONSENTRASI NO2")
_KETERANGAN = """
Nitrogen Dioxide (NO2) adalah gas beracun yang dapat menyebabkan efek kesehatan yang serius, terutama pada orang-orang yang memiliki masalah pernapasan seperti asma. NO2 dapat menyebabkan iritasi pada mata, hidung, dan tenggorokan, serta dapat memperburuk kondisi kesehatan jantung. Menurut Badan Perlindungan Lingkungan Amerika Serikat (EPA), konsentrasi NO2 yang tinggi dapat menyebabkan efek kesehatan yang serius, terutama pada anak-anak, orang tua, dan orang-orang yang memiliki masalah kesehatan. (Referensi: Google, EPA)
"""
st.write(_KETERANGAN)

# Metrics
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric(label="BAIK", value="0-80 μg/m³")
col2.metric(label="SEDANG", value="81-200 μg/m³")
col3.metric(label="TIDAK SEHAT", value="201-1130 μg/m³")
col4.metric(label="SANGAT TIDAK SEHAT", value="1131-2260 μg/m³")
col5.metric(label="BERBAHAYA", value=">2260 μg/m³")

# Function to load data
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

# Define NO2 category and color function
def kategori_no2(value):
    kategori_warna = {
        "BAIK": "green",
        "SEDANG": "blue",
        "TIDAK SEHAT": "orange",
        "SANGAT TIDAK SEHAT": "red",
        "BERBAHAYA": "black"
    }
    if value <= 80:
        kategori = "BAIK"
    elif value <= 200:
        kategori = "SEDANG"
    elif value <= 1130:
        kategori = "TIDAK SEHAT"
    elif value <= 2260:
        kategori = "SANGAT TIDAK SEHAT"
    else:
        kategori = "BERBAHAYA"
    return kategori, kategori_warna[kategori]

# Function for monthly NO2 analysis
def no2_bulanan(df, year):
    filtered_df = df[df['year'] == year]
    result = (
        filtered_df.groupby('month')
        .agg(avg_NO2=('NO2', 'mean'))
        .reset_index()
    )
    result['avg_NO2'] = result['avg_NO2'].round()
    result['kategori_no2_bulanan'] = result['avg_NO2'].apply(kategori_no2)
    return result

result = no2_bulanan(dataframes["Aotizhongxin"], 2013)
fig = px.bar(
    result, x='month', y='avg_NO2', color='kategori_no2_bulanan', color_discrete_map={
        "BAIK": "green", 
        "SEDANG": "blue", 
        "TIDAK SEHAT": "orange", 
        "SANGAT TIDAK SEHAT": "red", 
        "BERBAHAYA": "black"
    },
    title=f"Analisis NO2 Bulanan di Aotizhongxin pada Tahun 2013",
    labels={'avg_NO2': 'Kadar NO2 (μg/m³)', 'month': 'Bulan'}
)
fig.update_layout(yaxis=dict(range=[0, 150]))
st.plotly_chart(fig, use_container_width=True)
for index, row in result.iterrows():
    kategori, _ = kategori_no2(row['avg_NO2'])
    st.write(f"Bulan ke-{int(row['month'])}: Kadar NO2 rata-rata adalah {row['avg_NO2']} μg/m³, termasuk ke dalam kategori polusi {kategori}. Maka dari itu, kualitas udara perlu perbaikan supaya warga dapat hidup lebih sehat.")


