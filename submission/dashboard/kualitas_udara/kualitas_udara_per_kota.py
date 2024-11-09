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

        # Menetapkan warna khusus untuk setiap kategori
        warna_khusus = {
            'PM2.5': 'red',      # Warna untuk PM2.5
            'PM10': 'green',     # Warna untuk PM10
            'SO2': 'blue',       # Warna untuk SO2
            'CO': 'orange',      # Warna untuk CO
            'NO2': 'purple',     # Warna untuk NO2
            'O3': 'cyan'         # Warna untuk O3
        }

        # Menetapkan warna default
        default_color = 'gray'  # Anda bisa memilih warna default yang diinginkan

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

        fig.add_trace(
            go.Bar(
                x=all_cities_data['location'],
                y=all_cities_data['avg_SO2'],
                name='SO2',
                marker_color=warna_khusus['SO2'],  # Gunakan warna khusus untuk SO2
                width=0.4,  # Lebar bar SO2
                offsetgroup=2,  # Offset untuk SO2
                hoverinfo='y+name'  # Menampilkan informasi saat dihover
            )
        )

        fig.add_trace(
            go.Bar(
                x=all_cities_data['location'],
                y=all_cities_data['avg_CO'],
                name='CO',
                marker_color=warna_khusus['CO'],  # Gunakan warna khusus untuk CO
                width=0.4,  # Lebar bar CO
                offsetgroup=3,  # Offset untuk CO
                hoverinfo='y+name'  # Menampilkan informasi saat dihover
            )
        )

        fig.add_trace(
            go.Bar(
                x=all_cities_data['location'],
                y=all_cities_data['avg_NO2'],
                name='NO2',
                marker_color=warna_khusus['NO2'],  # Gunakan warna khusus untuk NO2
                width=0.4,  # Lebar bar NO2
                offsetgroup=4,  # Offset untuk NO2
                hoverinfo='y+name'  # Menampilkan informasi saat dihover
            )
        )

        fig.add_trace(
            go.Bar(
                x=all_cities_data['location'],
                y=all_cities_data['avg_O3'],
                name='O3',
                marker_color=warna_khusus.get('O3', default_color),  # Gunakan warna khusus untuk O3 atau warna default
                width=0.4,  # Lebar bar O3
                offsetgroup=5,  # Offset untuk O3
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

        # Inisialisasi keterangan dengan nilai default
        keterangan_pm25 = "Keterangan tidak tersedia."
        keterangan_pm10 = "Keterangan tidak tersedia."
        # ... inisialisasi untuk SO2, CO, NO2, O3 jika diperlukan ...

        # Logika untuk menentukan keterangan PM2.5
        if kategori_pm25 == "BAIK":
            keterangan_pm25 = f"Rata-rata konsentrasi PM2.5 untuk seluruh kota adalah {rata_rata_pm25:.2f} µg/m³, yang termasuk dalam kategori {kategori_pm25}. Kualitas udara sangat baik dan tidak berbahaya bagi kesehatan."
        elif kategori_pm25 == "SEDANG":
            keterangan_pm25 = f"Rata-rata konsentrasi PM2.5 untuk seluruh kota adalah {rata_rata_pm25:.2f} µg/m³, yang termasuk dalam kategori {kategori_pm25}. Kualitas udara masih aman, namun perlu diawasi untuk mencegah peningkatan polusi."
        elif kategori_pm25 == "TIDAK SEHAT":
            keterangan_pm25 = f"Rata-rata konsentrasi PM2.5 untuk seluruh kota adalah {rata_rata_pm25:.2f} µg/m³, yang termasuk dalam kategori {kategori_pm25}. Kualitas udara tidak sehat dan perlu pengurangan aktivitas yang menyebabkan polusi."
        elif kategori_pm25 == "BERBAHAYA":
            keterangan_pm25 = f"Rata-rata konsentrasi PM2.5 untuk seluruh kota adalah {rata_rata_pm25:.2f} µg/m³, yang termasuk dalam kategori {kategori_pm25}. Udara berbahaya dan tindakan pencegahan perlu dilakukan segera."
        elif kategori_pm25 == "SANGAT BERBAHAYA":
            keterangan_pm25 = f"Rata-rata konsentrasi PM2.5 untuk seluruh kota adalah {rata_rata_pm25:.2f} µg/m³, yang termasuk dalam kategori {kategori_pm25}. Situasi sangat berbahaya dan tindakan darurat diperlukan."

        # Pastikan untuk melakukan hal yang sama untuk kategori lainnya
        # Misalnya untuk PM10, SO2, CO, NO2, O3

        # Tampilkan keterangan
        st.write(keterangan_pm25)

        if kategori_pm10 == "BAIK":
            keterangan_pm10 = f"Rata-rata konsentrasi PM10 untuk seluruh kota pada tahun {selected_year_bulanan} bulan {selected_month_bulanan} adalah {rata_rata_pm10:.2f} µg/m³, yang termasuk dalam kategori {kategori_pm10}. Kualitas udara sangat baik dan tidak berbahaya bagi kesehatan."
        elif kategori_pm10 == "SEDANG":
            keterangan_pm10 = f"Rata-rata konsentrasi PM10 untuk seluruh kota pada tahun {selected_year_bulanan} bulan {selected_month_bulanan} adalah {rata_rata_pm10:.2f} µg/m³, yang termasuk dalam kategori {kategori_pm10}. Kualitas udara masih aman, namun perlu diawasi untuk mencegah peningkatan polusi."
        elif kategori_pm10 == "TIDAK SEHAT":
            keterangan_pm10 = f"Rata-rata konsentrasi PM10 untuk seluruh kota pada tahun {selected_year_bulanan} bulan {selected_month_bulanan} adalah {rata_rata_pm10:.2f} µg/m³, yang termasuk dalam kategori {kategori_pm10}. Kualitas udara tidak sehat dan perlu pengurangan aktivitas yang menyebabkan polusi."
        elif kategori_pm10 == "BERBAHAYA":
            keterangan_pm10 = f"Rata-rata konsentrasi PM10 untuk seluruh kota pada tahun {selected_year_bulanan} bulan {selected_month_bulanan} adalah {rata_rata_pm10:.2f} µg/m³, yang termasuk dalam kategori {kategori_pm10}. Udara berbahaya dan tindakan pencegahan perlu dilakukan segera."
        elif kategori_pm10 == "SANGAT BERBAHAYA":
            keterangan_pm10 = f"Rata-rata konsentrasi PM10 untuk seluruh kota pada tahun {selected_year_bulanan} bulan {selected_month_bulanan} adalah {rata_rata_pm10:.2f} µg/m³, yang termasuk dalam kategori {kategori_pm10}. Situasi sangat berbahaya dan tindakan darurat diperlukan."

        st.write(keterangan_pm10)

        # Analisis untuk SO2, NO2, CO, O3
        rata_rata_so2 = all_cities_data['avg_SO2'].mean()
        rata_rata_no2 = all_cities_data['avg_NO2'].mean()
        rata_rata_co = all_cities_data['avg_CO'].mean()
        rata_rata_o3 = all_cities_data['avg_O3'].mean()

        kategori_so2 = kategori_so2(rata_rata_so2)
        kategori_no2 = kategori_no2(rata_rata_no2)
        kategori_co = kategori_co(rata_rata_co)
        kategori_o3 = kategori_o3(rata_rata_o3)

        if kategori_so2 == "BAIK":
            keterangan_so2 = f"Rata-rata konsentrasi SO2 untuk seluruh kota pada tahun {selected_year_bulanan} bulan {selected_month_bulanan} adalah {rata_rata_so2:.2f} µg/m³, yang termasuk dalam kategori {kategori_so2}. Kualitas udara sangat baik dan tidak berbahaya bagi kesehatan."
        elif kategori_so2 == "SEDANG":
            keterangan_so2 = f"Rata-rata konsentrasi SO2 untuk seluruh kota pada tahun {selected_year_bulanan} bulan {selected_month_bulanan} adalah {rata_rata_so2:.2f} µg/m³, yang termasuk dalam kategori {kategori_so2}. Kualitas udara masih aman, namun perlu diawasi untuk mencegah peningkatan polusi."
        elif kategori_so2 == "TIDAK SEHAT":
            keterangan_so2 = f"Rata-rata konsentrasi SO2 untuk seluruh kota pada tahun {selected_year_bulanan} bulan {selected_month_bulanan} adalah {rata_rata_so2:.2f} µg/m³, yang termasuk dalam kategori {kategori_so2}. Kualitas udara tidak sehat dan perlu pengurangan aktivitas yang menyebabkan polusi."
        elif kategori_so2 == "BERBAHAYA":
            keterangan_so2 = f"Rata-rata konsentrasi SO2 untuk seluruh kota pada tahun {selected_year_bulanan} bulan {selected_month_bulanan} adalah {rata_rata_so2:.2f} µg/m³, yang termasuk dalam kategori {kategori_so2}. Udara berbahaya dan tindakan pencegahan perlu dilakukan segera."
        elif kategori_so2 == "SANGAT BERBAHAYA":
            keterangan_so2 = f"Rata-rata konsentrasi SO2 untuk seluruh kota pada tahun {selected_year_bulanan} bulan {selected_month_bulanan} adalah {rata_rata_so2:.2f} µg/m³, yang termasuk dalam kategori {kategori_so2}. Situasi sangat berbahaya dan tindakan darurat diperlukan."

        if kategori_no2 == "BAIK":
            keterangan_no2 = f"Rata-rata konsentrasi NO2 untuk seluruh kota pada tahun {selected_year_bulanan} bulan {selected_month_bulanan} adalah {rata_rata_no2:.2f} µg/m³, yang termasuk dalam kategori {kategori_no2}. Kualitas udara sangat baik dan tidak berbahaya bagi kesehatan."
        elif kategori_no2 == "SEDANG":
            keterangan_no2 = f"Rata-rata konsentrasi NO2 untuk seluruh kota pada tahun {selected_year_bulanan} bulan {selected_month_bulanan} adalah {rata_rata_no2:.2f} µg/m³, yang termasuk dalam kategori {kategori_no2}. Kualitas udara masih aman, namun perlu diawasi untuk mencegah peningkatan polusi."
        elif kategori_no2 == "TIDAK SEHAT":
            keterangan_no2 = f"Rata-rata konsentrasi NO2 untuk seluruh kota pada tahun {selected_year_bulanan} bulan {selected_month_bulanan} adalah {rata_rata_no2:.2f} µg/m³, yang termasuk dalam kategori {kategori_no2}. Kualitas udara tidak sehat dan perlu pengurangan aktivitas yang menyebabkan polusi."
        elif kategori_no2 == "BERBAHAYA":
            keterangan_no2 = f"Rata-rata konsentrasi NO2 untuk seluruh kota pada tahun {selected_year_bulanan} bulan {selected_month_bulanan} adalah {rata_rata_no2:.2f} µg/m³, yang termasuk dalam kategori {kategori_no2}. Udara berbahaya dan tindakan pencegahan perlu dilakukan segera."
        elif kategori_no2 == "SANGAT BERBAHAYA":
            keterangan_no2 = f"Rata-rata konsentrasi NO2 untuk seluruh kota pada tahun {selected_year_bulanan} bulan {selected_month_bulanan} adalah {rata_rata_no2:.2f} µg/m³, yang termasuk dalam kategori {kategori_no2}. Situasi sangat berbahaya dan tindakan darurat diperlukan."

        if kategori_co == "BAIK":
            keterangan_co = f"Rata-rata konsentrasi CO untuk seluruh kota pada tahun {selected_year_bulanan} bulan {selected_month_bulanan} adalah {rata_rata_co:.2f} µg/m³, yang termasuk dalam kategori {kategori_co}. Kualitas udara sangat baik dan tidak berbahaya bagi kesehatan."
        elif kategori_co == "SEDANG":
            keterangan_co = f"Rata-rata konsentrasi CO untuk seluruh kota pada tahun {selected_year_bulanan} bulan {selected_month_bulanan} adalah {rata_rata_co:.2f} µg/m³, yang termasuk dalam kategori {kategori_co}. Kualitas udara masih aman, namun perlu diawasi untuk mencegah peningkatan polusi."
        elif kategori_co == "TIDAK SEHAT":
            keterangan_co = f"Rata-rata konsentrasi CO untuk seluruh kota pada tahun {selected_year_bulanan} bulan {selected_month_bulanan} adalah {rata_rata_co:.2f} µg/m³, yang termasuk dalam kategori {kategori_co}. Kualitas udara tidak sehat dan perlu pengurangan aktivitas yang menyebabkan polusi."
        elif kategori_co == "BERBAHAYA":
            keterangan_co = f"Rata-rata konsentrasi CO untuk seluruh kota pada tahun {selected_year_bulanan} bulan {selected_month_bulanan} adalah {rata_rata_co:.2f} µg/m³, yang termasuk dalam kategori {kategori_co}. Udara berbahaya dan tindakan pencegahan perlu dilakukan segera."
        elif kategori_co == "SANGAT BERBAHAYA":
            keterangan_co = f"Rata-rata konsentrasi CO untuk seluruh kota pada tahun {selected_year_bulanan} bulan {selected_month_bulanan} adalah {rata_rata_co:.2f} µg/m³, yang termasuk dalam kategori {kategori_co}. Situasi sangat berbahaya dan tindakan darurat diperlukan."

        if kategori_o3 == "BAIK":
            keterangan_o3 = f"Rata-rata konsentrasi O3 untuk seluruh kota pada tahun {selected_year_bulanan} bulan {selected_month_bulanan} adalah {rata_rata_o3:.2f} µg/m³, yang termasuk dalam kategori {kategori_o3}. Kualitas udara sangat baik dan tidak berbahaya bagi kesehatan."
        elif kategori_o3 == "SEDANG":
            keterangan_o3 = f"Rata-rata konsentrasi O3 untuk seluruh kota pada tahun {selected_year_bulanan} bulan {selected_month_bulanan} adalah {rata_rata_o3:.2f} µg/m³, yang termasuk dalam kategori {kategori_o3}. Kualitas udara masih aman, namun perlu diawasi untuk mencegah peningkatan polusi."
        elif kategori_o3 == "TIDAK SEHAT":
            keterangan_o3 = f"Rata-rata konsentrasi O3 untuk seluruh kota pada tahun {selected_year_bulanan} bulan {selected_month_bulanan} adalah {rata_rata_o3:.2f} µg/m³, yang termasuk dalam kategori {kategori_o3}. Kualitas udara tidak sehat dan perlu pengurangan aktivitas yang menyebabkan polusi."
        elif kategori_o3 == "BERBAHAYA":
            keterangan_o3 = f"Rata-rata konsentrasi O3 untuk seluruh kota pada tahun {selected_year_bulanan} bulan {selected_month_bulanan} adalah {rata_rata_o3:.2f} µg/m³, yang termasuk dalam kategori {kategori_o3}. Udara berbahaya dan tindakan pencegahan perlu dilakukan segera."
        elif kategori_o3 == "SANGAT BERBAHAYA":
            keterangan_o3 = f"Rata-rata konsentrasi O3 untuk seluruh kota pada tahun {selected_year_bulanan} bulan {selected_month_bulanan} adalah {rata_rata_o3:.2f} µg/m³, yang termasuk dalam kategori {kategori_o3}. Situasi sangat berbahaya dan tindakan darurat diperlukan."

        st.write(keterangan_so2)
        st.write(keterangan_no2)
        st.write(keterangan_co)
        st.write(keterangan_o3)
