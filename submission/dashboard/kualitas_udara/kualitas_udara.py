# import semua library yang diperlukan
import streamlit as st
import numpy as np
import pandas as pd
import os

# load dataset
st.set_page_config(
    page_title="Kualitas Udara",
    page_icon="🧫",
)

st.title("Kualitas Udara")

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

# code engine kualitas udara 

# kualitas udara harian
def kualitas_udara_harian(df, year, month, day_start, day_end):
    filtered_df = df[(df['year'] == year) & (df['month'] == month) & (df['day'].between(day_start, day_end))]
    result = filtered_df.groupby(['year', 'month', 'day']).agg(
        avg_PM25=('PM2.5', 'mean'), 
        avg_PM10=('PM10', 'mean'), 
        avg_NO2=('NO2', 'mean'), 
        avg_CO=('CO', 'mean')
    ).reset_index()
    return result.round({'avg_PM25': 0, 'avg_PM10': 0, 'avg_NO2': 0, 'avg_CO': 0})

# kualitas udara mingguan 
def kualitas_udara_mingguan(df, year, month):
    df = df[(df['year'] == year) & (df['month'] == month)]
    df['week'] = ((df['day'] - 1) // 7) + 1
    result = df.groupby(['year', 'month', 'week']).agg(
        avg_PM25=('PM2.5', 'mean'), 
        avg_PM10=('PM10', 'mean'), 
        avg_NO2=('NO2', 'mean'), 
        avg_CO=('CO', 'mean')
    ).reset_index()
    return result.round({'avg_PM25': 0, 'avg_PM10': 0, 'avg_NO2': 0, 'avg_CO': 0})

# kualitas udara bulanan
def kualitas_udara_bulanan(df, year, month):
    df = df[(df['year'] == year) & (df['month'] == month)]
    result = df.groupby(['year', 'month']).agg(
        avg_PM25=('PM2.5', 'mean'), 
        avg_PM10=('PM10', 'mean'), 
        avg_NO2=('NO2', 'mean'), 
        avg_CO=('CO', 'mean')
    ).reset_index()
    return result.round({'avg_PM25': 0, 'avg_PM10': 0, 'avg_NO2': 0, 'avg_CO': 0})

# kualitas udara tahunan
def kualitas_udara_tahunan(df, year):
    df = df[(df['year'] == year)]
    result = df.groupby(['year']).agg(
        avg_PM25=('PM2.5', 'mean'), 
        avg_PM10=('PM10', 'mean'), 
        avg_NO2=('NO2', 'mean'), 
        avg_CO=('CO', 'mean')
    ).reset_index()
    return result.round({'avg_PM25': 0, 'avg_PM10': 0, 'avg_NO2': 0, 'avg_CO': 0})

# end code engine kualitas udara 

# membuat sidebar 
with st.sidebar:
    selected_year = st.selectbox("Pilih Tahun", options=["2013", "2014", "2015", "2016", "2017"], index=0)

    if selected_year:
        selected_period = st.selectbox("Pilih Periode", ["Harian", "Mingguan", "Bulanan", "Tahunan"])
        
        if selected_period == "Harian":
            selected_month = st.number_input("Bulan", min_value=3 if selected_year == "2013" else 1, max_value=12 if selected_year != "2017" else 2, value=3)
            selected_day_start = st.number_input("Hari Mulai", min_value=1, max_value=31, value=1)
            selected_day_end = st.number_input("Hari Akhir", min_value=1, max_value=31, value=31)

        elif selected_period in ["Mingguan", "Bulanan"]:
            selected_month = st.number_input("Bulan", min_value=3 if selected_year == "2013" else 1, max_value=12 if selected_year != "2017" else 2, value=3)

# end sidebar 

# Display based on selected year and period
if selected_year:
    st.write(f"Analisis untuk tahun {selected_year} dan periode {selected_period}")

    if selected_period == "Harian":
        st.write(f"Bulan: {selected_month}, Hari: {selected_day_start} hingga {selected_day_end}")

    if st.button("Analisis untuk Semua Kota"):
        all_results = []

        if selected_period == "Harian":
            for kota, df in dataframes.items():
                hasil_kualitas_udara = kualitas_udara_harian(df, int(selected_year), selected_month, selected_day_start, selected_day_end)
                hasil_kualitas_udara['Kota'] = kota  # Menambahkan kolom Kota
                all_results.append(hasil_kualitas_udara)

            # Menggabungkan semua hasil ke dalam satu DataFrame
            combined_results = pd.concat(all_results, ignore_index=True)

            # Visualisasi data harian
            for polusi in ['avg_PM25', 'avg_PM10', 'avg_NO2', 'avg_CO']:
                chart = st.vega_lite_chart(
                    {
                        "mark": "line",
                        "encoding": {
                            "x": {
                                "field": "day", 
                                "type": "temporal",
                                "title": "Tanggal"  # Menambahkan keterangan sumbu X
                            },
                            "y": {"field": polusi, "type": "quantitative"},
                            "color": {"field": "Kota", "type": "nominal"}
                        },
                        "datasets": {
                            "combined_results": combined_results,  # Menggunakan DataFrame gabungan
                        },
                        "data": {"name": "combined_results"},
                    }
                )
                st.write(f"Visualisasi {polusi} untuk Semua Kota")

        elif selected_period == "Mingguan":
            all_weekly_results = []

            for kota, df in dataframes.items():
                hasil_kualitas_udara = kualitas_udara_mingguan(df, int(selected_year), selected_month)
                hasil_kualitas_udara['Kota'] = kota  # Menambahkan kolom Kota
                all_weekly_results.append(hasil_kualitas_udara)

            # Menggabungkan semua hasil ke dalam satu DataFrame
            combined_weekly_results = pd.concat(all_weekly_results, ignore_index=True)

            # Visualisasi data mingguan
            st.subheader("Visualisasi Kualitas Udara Mingguan")
            for polusi in ['avg_PM25', 'avg_PM10', 'avg_NO2', 'avg_CO']:
                my_chart = st.vega_lite_chart(
                    {
                        "mark": "bar",
                        "encoding": {
                            "x": {
                                "field": "week", 
                                "type": "ordinal",
                                "title": "Minggu"  # Menambahkan keterangan sumbu X
                            },
                            "y": {
                                "field": polusi, 
                                "type": "quantitative",
                                "title": f"Kualitas Udara ({polusi})"  # Menambahkan keterangan sumbu Y
                            },
                            "color": {"field": "Kota", "type": "nominal"}
                        },
                        "datasets": {
                            "some_fancy_name": combined_weekly_results,  # <-- named dataset
                        },
                        "data": {"name": "some_fancy_name"},
                    }
                )
                st.write(f"Visualisasi {polusi} untuk Semua Kota")
                my_chart.add_rows(some_fancy_name=combined_weekly_results)

        elif selected_period == "Bulanan":
            all_monthly_results = []

            for kota, df in dataframes.items():
                hasil_kualitas_udara = kualitas_udara_bulanan(df, int(selected_year), selected_month)
                hasil_kualitas_udara['Kota'] = kota  # Menambahkan kolom Kota
                all_monthly_results.append(hasil_kualitas_udara)

            # Menggabungkan semua hasil ke dalam satu DataFrame
            combined_results = pd.concat(all_monthly_results, ignore_index=True)

            # Mengatur DataFrame untuk visualisasi
            combined_results_melted = combined_results.melt(id_vars=['Kota'], 
                                                             value_vars=['avg_PM25', 'avg_PM10', 'avg_NO2', 'avg_CO'],
                                                             var_name='Jenis Polusi', 
                                                             value_name='Nilai')

            # Visualisasi data bulanan menggunakan st.vega_lite_chart
            my_chart = st.vega_lite_chart(
                {
                    "mark": "bar",
                    "encoding": {
                        "x": {
                            "field": "Nilai", 
                            "type": "quantitative",
                            "title": "Nilai Kualitas Udara"  # Menambahkan keterangan sumbu X
                        },
                        "y": {
                            "field": "Kota", 
                            "type": "nominal",
                            "title": "Kota"  # Menambahkan keterangan sumbu Y
                        },
                        "color": {
                            "field": "Jenis Polusi", 
                            "type": "nominal",
                            "title": "Jenis Polusi"
                        }
                    },
                    "data": {
                        "values": combined_results_melted.to_dict(orient='records')  # Menggunakan data dari DataFrame
                    }
                }
            )

            st.write("Visualisasi Kualitas Udara Bulanan untuk Semua Kota")
            col1 , col2 , col3 , col4 = st.columns(4)

            # Menghitung nilai rata-rata untuk setiap jenis polusi
            pm25_value = combined_results_melted['Nilai'].loc[combined_results_melted['Jenis Polusi'] == 'avg_PM25'].mean()
            pm10_value = combined_results_melted['Nilai'].loc[combined_results_melted['Jenis Polusi'] == 'avg_PM10'].mean()
            co_value = combined_results_melted['Nilai'].loc[combined_results_melted['Jenis Polusi'] == 'avg_CO'].mean()

            # Menampilkan metrik untuk PM2.5
            if pm25_value <= 15:
                col1.metric("PM2.5", f"{pm25_value:.2f} μg/m³", "Baik")
            elif pm25_value <= 65:
                col1.metric("PM2.5", f"{pm25_value:.2f} μg/m³", "Sedang")
            elif pm25_value <= 150:
                col1.metric("PM2.5", f"{pm25_value:.2f} μg/m³", "Tidak Sehat")
            elif pm25_value <= 250:
                col1.metric("PM2.5", f"{pm25_value:.2f} μg/m³", "Sangat Tidak Sehat")
            else:
                col1.metric("PM2.5", f"{pm25_value:.2f} μg/m³", "Berbahaya")

            # Menampilkan metrik untuk PM10
            if pm10_value <= 50:
                col2.metric("PM10", f"{pm10_value:.2f} μg/m³", "Baik")
            elif pm10_value <= 150:
                col2.metric("PM10", f"{pm10_value:.2f} μg/m³", "Sedang")
            elif pm10_value <= 350:
                col2.metric("PM10", f"{pm10_value:.2f} μg/m³", "Tidak Sehat")
            elif pm10_value <= 421:
                col2.metric("PM10", f"{pm10_value:.2f} μg/m³", "Sangat Tidak Sehat")
            else:
                col2.metric("PM10", f"{pm10_value:.2f} μg/m³", "Sangat Berbahaya")

            # Menampilkan metrik untuk CO
            if co_value < 70:
                col4.metric("CO", f"{co_value:.2f} ppm", "Aman")
            elif co_value <= 150:
                col4.metric("CO", f"{co_value:.2f} ppm", "Berbahaya")
            else:
                col4.metric("CO", f"{co_value:.2f} ppm", "Mematikan")

            st.vega_lite_chart(my_chart, use_container_width=True)

        elif selected_period == "Tahunan":
            for kota, df in dataframes.items():
                hasil_kualitas_udara = kualitas_udara_tahunan(df, int(selected_year))
                hasil_kualitas_udara['Kota'] = kota  # Menambahkan kolom Kota
                all_results.append(hasil_kualitas_udara)

            # Menggabungkan semua hasil ke dalam satu DataFrame
            combined_results = pd.concat(all_results, ignore_index=True)

            # Visualisasi data tahunan menggunakan st.bar_chart
            st.bar_chart(combined_results.set_index('year')[['avg_PM25', 'avg_PM10', 'avg_NO2', 'avg_CO']])
            st.write("Visualisasi Kualitas Udara Tahunan untuk Semua Kota")

