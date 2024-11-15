import os
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# load page config
st.title("Korelasi Partikulasi Polusi Semua Kota 🏙️")
st.header("INFORMASI KONSENTRASI PARTIKULAT PM2.5 & PM10")
_KETERANGAN = """
Partikulat (PM2.5) adalah Partikel udara yang berukuran lebih kecil dari 2.5 mikron (mikrometer).
Nilai Ambang Batas (NAB) adalah Batas konsentrasi polusi udara yang diperbolehkan berada dalam udara ambien. NAB PM2.5 = 35 µgram/m3

Partikulat (PM10) adalah Partikel udara yang berukuran lebih kecil dari 10 mikron (mikrometer).
Nilai Ambang Batas (NAB) adalah Batas konsentrasi polusi udara yang diperbolehkan berada dalam udara ambien. NAB PM10 = 150 µgram/m³.
"""
st.write(_KETERANGAN)

# Membuat Metric untuk PM2.5 & PM10
col1, col2, col3, col4, col5 = st.columns(5)
col1.image("submission/img/icon/pm25/pm25-baik.webp", caption="BAIK: 0-15.5 μg/m³")
col2.image("submission/img/icon/pm25/pm25-sedang.webp", caption="SEDANG: 15.6 - 55.4 μg/m³")
col3.image("submission/img/icon/pm25/pm25-tidaksehat.webp", caption="TIDAK SEHAT: 55.5 - 150.4 μg/m³")
col4.image("submission/img/icon/pm25/pm25-sangattidaksehat.webp", caption="SANGAT TIDAK SEHAT: 150.5 - 250.4 μg/m³")
col5.image("submission/img/icon/pm25/pm25-berbahaya.webp", caption="BERBAHAYA: >250.4 μg/m³")

col1, col2, col3, col4, col5 = st.columns(5)
col1.image("submission/img/icon/pm10/pm10-baik.webp", caption="BAIK: 0-50 μg/m³")
col2.image("submission/img/icon/pm10/pm10-sedang.webp", caption="SEDANG: 51-150 μg/m³")
col3.image("submission/img/icon/pm10/pm10-tidaksehat.webp", caption="TIDAK SEHAT: 151-350 μg/m³")
col4.image("submission/img/icon/pm10/pm10-sangattidaksehat.webp", caption="SANGAT TIDAK SEHAT: 351-420 μg/m³")
col5.image("submission/img/icon/pm10/pm10-berbahaya.webp", caption="BERBAHAYA: >420 μg/m³")

# Load data
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

# Inisialisasi dataframes dengan memuat data
dataframes = load_data()

# Monthly pollution analysis
def partikulasi_polusi_bulanan(df, year, month):
    filtered_df = df.query('year == @year and month == @month')

    result = (
        filtered_df.groupby(['year', 'month'])
        .agg(avg_PM25=('PM2.5', 'mean'), avg_PM10=('PM10', 'mean'))
        .reset_index()
    )

    result['avg_PM25'] = result['avg_PM25'].round()
    result['avg_PM10'] = result['avg_PM10'].round()
    result['kategori_pm25_bulanan'] = result['avg_PM25'].apply(kategori_pm25)
    result['kategori_pm10_bulanan'] = result['avg_PM10'].apply(kategori_pm10)
    return result

# Yearly pollution analysis
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

# Fungsi untuk mendapatkan kategori kualitas udara PM2.5    
def kategori_pm25(pm25):
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
    
# Fungsi untuk mendapatkan kategori kualitas udara PM10    
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
    
# Tab Setup 
tab1, tab2 = st.tabs([ "Bulanan", "Tahunan"])

# Bulanan Analisis
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
        st.header(f"Konsentrasi PM2.5 dan PM10 Bulanan di Semua Kota pada Tahun {selected_year_bulanan} dan Bulan {selected_month_bulanan}")

        all_cities_data = []
        for city, df in dataframes.items():
            monthly_data = partikulasi_polusi_bulanan(df, selected_year_bulanan, selected_month_bulanan)
            monthly_data['location'] = city
            all_cities_data.append(monthly_data)

        all_cities_data = pd.concat(all_cities_data, ignore_index=True)
        
        # Membuat subplots dengan 1 baris dan 1 kolom untuk mengakomodasi 5 bar chart
        fig = make_subplots(rows=1, cols=1)

        # Menetapkan warna khusus untuk setiap kategori
        warna_khusus = {
            'PM2.5': 'red',      # Warna untuk PM2.5
            'PM10': 'green',     # Warna untuk PM10
            'SO2': 'blue',       # Warna untuk SO2
            'CO': 'orange',      # Warna untuk CO
            'NO2': 'purple',     # Warna untuk NO2
            'O3': 'cyan'         # Warna untuk O3
        }

        # Grafik bar chart untuk PM2.5, PM10, SO2, CO, NO2, dan O3 dalam satu frame
        fig.add_trace(
            go.Bar(
                x=all_cities_data['location'],
                y=all_cities_data['avg_PM25'],
                name='PM2.5',
                marker_color=warna_khusus['PM2.5'],  # Gunakan warna khusus untuk PM2.5
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
                marker_color=warna_khusus['PM10'],  # Gunakan warna khusus untuk PM10
                width=0.4,  # Lebar bar PM10
                offsetgroup=1,  # Offset untuk PM10
                hoverinfo='y+name'  # Menampilkan informasi saat dihover
            )
        )


        # Update layout untuk mempercantik plot
        fig.update_layout(
            height=500,
            title_text=f"Konsentrasi PM2.5, PM10, SO2, CO, NO2, dan O3 Bulanan di Semua Kota pada Tahun {selected_year_bulanan} dan Bulan {selected_month_bulanan}",
            barmode='group',  # Mengatur mode bar menjadi 'group' untuk menampilkan berdampingan
            xaxis_title="Kota",
            yaxis_title="Konsentrasi (µg/m³)",
            yaxis=dict(range=[0, 420])  # Mengatur rentang sumbu Y menjadi 0 hingga 420
        )

        # Tampilkan chart di Streamlit
        st.plotly_chart(fig, use_container_width=True)

        # Keterangan analisis
        rata_rata_pm25 = all_cities_data['avg_PM25'].mean()
        rata_rata_pm10 = all_cities_data['avg_PM10'].mean()
        kategori_pm25 = kategori_pm25(rata_rata_pm25)
        kategori_pm10 = kategori_pm10(rata_rata_pm10)

        st.write(f"Rata-rata konsentrasi PM2.5 untuk seluruh kota pada tahun {selected_year_bulanan}  bulan {selected_month_bulanan} adalah {rata_rata_pm25:.2f} µg/m³, termasuk dalam kategori {kategori_pm25}.")
        st.write(f"Rata-rata konsentrasi PM10 untuk seluruh kota pada tahun {selected_year_bulanan}  bulan {selected_month_bulanan} adalah {rata_rata_pm10:.2f} µg/m³, termasuk dalam kategori {kategori_pm10}.")

# Analisa Per Tahun 
with tab2:
    with st.form(key='_form_tahunan'):
        selected_year_tahunan = st.number_input("Pilih Tahun", min_value=2013, max_value=2017, step=1)
        submit_button_tahunan = st.form_submit_button(label='Analisa Tahunan')

    if submit_button_tahunan:
        st.header(f"Konsentrasi PM2.5 dan PM10 Tahunan di Semua Kota pada Tahun {selected_year_tahunan}")

        all_cities_data = []
        for city, df in dataframes.items():
            annual_data = partikulasi_polusi_tahunan(df, selected_year_tahunan)
            annual_data['location'] = city
            all_cities_data.append(annual_data)

        all_cities_data = pd.concat(all_cities_data, ignore_index=True)

        # Creating the plot
        fig = make_subplots(rows=1, cols=1)

        # Define color mapping
        warna_kategori = {
            "Baik": 'green',
            "Sedang": 'blue',
            "Tidak Sehat": 'orange',
            "Sangat Tidak Sehat": 'red',
            "Berbahaya": 'black'
        }

        # Plotting PM2.5
        fig.add_trace(
            go.Bar(
                x=all_cities_data['location'],
                y=all_cities_data['avg_PM25'],
                name='PM2.5',
                marker_color=[warna_kategori[kategori_pm25(pm)] for pm in all_cities_data['avg_PM25']],
                width=0.4,
                offsetgroup=0
            )
        )

        # Plotting PM10
        fig.add_trace(
            go.Bar(
                x=all_cities_data['location'],
                y=all_cities_data['avg_PM10'],
                name='PM10',
                marker_color=[warna_kategori[kategori_pm10(pm)] for pm in all_cities_data['avg_PM10']],
                width=0.4,
                offsetgroup=1
            )
        )

        # Update layout
        fig.update_layout(
            height=500,
            title_text=f"Konsentrasi PM2.5 dan PM10 Tahunan di Semua Kota pada Tahun {selected_year_tahunan}",
            barmode='group',
            xaxis_title="Kota",
            yaxis_title="Konsentrasi (µg/m³)",
            yaxis=dict(range=[0, 420])
        )

        # Display chart
        st.plotly_chart(fig, use_container_width=True)

        # Display average analysis
        rata_rata_pm25 = all_cities_data['avg_PM25'].mean()
        rata_rata_pm10 = all_cities_data['avg_PM10'].mean()
        kategori_pm25_tahunan = kategori_pm25(rata_rata_pm25)
        kategori_pm10_tahunan = kategori_pm10(rata_rata_pm10)

        st.write(f"Rata-rata konsentrasi PM2.5 untuk seluruh kota pada tahun {selected_year_tahunan} adalah {rata_rata_pm25:.2f} µg/m³, termasuk dalam kategori {kategori_pm25_tahunan}. PM2.5 adalah partikel udara halus yang dapat masuk jauh ke dalam paru-paru dan menyebabkan berbagai masalah kesehatan. Paparan tinggi terhadap PM2.5 dalam jangka panjang dapat meningkatkan risiko penyakit jantung, paru-paru, dan berbagai gangguan pernapasan.")
        st.write(f"Rata-rata konsentrasi PM10 untuk seluruh kota pada tahun {selected_year_tahunan} adalah {rata_rata_pm10:.2f} µg/m³, termasuk dalam kategori {kategori_pm10_tahunan}. PM10 adalah partikel udara yang lebih besar dari PM2.5, namun masih cukup kecil untuk terhirup dan dapat menyebabkan iritasi pada saluran pernapasan atas. Pengendalian PM10 penting untuk mengurangi dampak langsung polusi udara terhadap kesehatan.")

        st.write("Dari tahun ke tahun, kualitas udara di kota-kota dengan tingkat polusi tertinggi serta untuk masing-masing kota telah mengalami variasi. Tahun-tahun tertentu menunjukkan kualitas udara yang tidak sehat dan sangat tidak sehat, sedangkan tahun lainnya menunjukkan kualitas udara yang sedang dan baik. Hal ini menunjukkan pentingnya pengawasan dan pengendalian polusi udara untuk meningkatkan kualitas hidup masyarakat.")



