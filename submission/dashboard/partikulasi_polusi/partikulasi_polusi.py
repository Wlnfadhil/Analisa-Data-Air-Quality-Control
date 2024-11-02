import os
import pandas as pd
import streamlit as st
import plotly.express as px

# load page config
st.set_page_config(
    page_title="Partikulasi Polusi",
    page_icon="🌫️",
)

# Load data
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

# Daily pollution analysis
def partikulasi_polusi_harian(df, year, month, day_start, day_end):
    filtered_df = df.query('year == @year and month == @month and day >= @day_start and day <= @day_end')

    result = (
        filtered_df.groupby(['year', 'month', 'day'])
        .agg(avg_PM25=('PM2.5', 'mean'), avg_PM10=('PM10', 'mean'))
        .reset_index()
    )

    result['avg_PM25'] = result['avg_PM25'].round()
    result['avg_PM10'] = result['avg_PM10'].round()

    return result

# Weekly pollution analysis
def partikulasi_polusi_mingguan(df, year, month):
    filtered_df = df.query('year == @year and month == @month')

    filtered_df['week'] = filtered_df['day'].apply(lambda x: (x - 1) // 7 + 1)

    result = (
        filtered_df.groupby(['year', 'month', 'week'])
        .agg(avg_PM25=('PM2.5', 'mean'), avg_PM10=('PM10', 'mean'))
        .reset_index()
    )

    result['avg_PM25'] = result['avg_PM25'].round()
    result['avg_PM10'] = result['avg_PM10'].round()

    return result

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

# membuat side bar 
with st.sidebar:
    selected_kota = st.selectbox("Pilih Kota", list(dataframes.keys()))
    if selected_kota:
        selected_year = st.selectbox("Pilih Tahun", options=["2013", "2014", "2015", "2016", "2017"], index=0)
        if selected_year:
            selected_period = st.selectbox("Pilih Periode", ["Harian", "Mingguan", "Bulanan", "Tahunan"])
            if selected_period == "Harian":
                page_partilukalasi_polusi_harian(dataframes, kota_list)
            elif selected_period == "Mingguan":
                page_partilukalasi_polusi_mingguan(dataframes, kota_list)
            elif selected_period == "Bulanan":
                page_partilukalasi_polusi_bulanan(dataframes, kota_list)
            elif selected_period == "Tahunan":
                page_partilukalasi_polusi_tahunan(dataframes, kota_list)

# Function for daily pollution analysis page
def page_partilukalasi_polusi_harian(dataframes, kota_list):
    st.header("Analisis Partikulasi Polusi Harian")

    selected_kota = st.selectbox("Pilih Kota", kota_list)
    selected_year = st.number_input("Tahun", min_value=2013, max_value=2017, value=2013)

    if selected_year == 2013:
        selected_month = st.number_input("Bulan", min_value=3, max_value=12, value=3)
    elif selected_year == 2017:
        selected_month = st.number_input("Bulan", min_value=1, max_value=2, value=1)
    else:
        selected_month = st.number_input("Bulan", min_value=1, max_value=12, value=1)

    selected_day_start = st.number_input("Hari Mulai", min_value=1, max_value=31, value=1)
    selected_day_end = st.number_input("Hari Akhir", min_value=1, max_value=31, value=31)

    if st.button("Analisis"):
        df = dataframes[selected_kota]
        df['day'] = df['day'].astype(int)

        hasil_kualitas_udara = partikulasi_polusi_harian(df, selected_year, selected_month, selected_day_start, selected_day_end)

        st.write("Hasil Kualitas Udara Harian:")
        st.dataframe(hasil_kualitas_udara)

        # Visualisasi hasil dengan Plotly
        fig = px.line(hasil_kualitas_udara, x='day', y=['avg_PM25', 'avg_PM10'],
                      title=f"Kualitas Udara di {selected_kota} pada {selected_month}/{selected_year}",
                      labels={'value': 'Kadar Polutan (μg/m³)', 'day': 'Hari'})
        st.plotly_chart(fig)

# Function for weekly pollution analysis page
def page_partilukalasi_polusi_mingguan(dataframes, kota_list):
    st.header("Analisis Partikulasi Polusi Mingguan")

    selected_kota = st.selectbox("Pilih Kota", kota_list)
    selected_year = st.number_input("Tahun", min_value=2013, max_value=2017, value=2013)

    if selected_year == 2013:
        selected_month = st.number_input("Bulan", min_value=3, max_value=12, value=3)
    elif selected_year == 2017:
        selected_month = st.number_input("Bulan", min_value=1, max_value=2, value=1)
    else:
        selected_month = st.number_input("Bulan", min_value=1, max_value=12, value=1)

    if st.button("Analisis Mingguan"):
        df = dataframes[selected_kota]
        df['day'] = df['day'].astype(int)

        hasil_kualitas_udara = partikulasi_polusi_mingguan(df, selected_year, selected_month)

        st.write("Hasil Kualitas Udara Mingguan:")
        st.dataframe(hasil_kualitas_udara)

        # Visualisasi hasil dengan Plotly
        fig = px.line(hasil_kualitas_udara, x='week', y=['avg_PM25', 'avg_PM10'],
                      title=f"Kualitas Udara Mingguan di {selected_kota} pada {selected_month}/{selected_year}",
                      labels={'value': 'Kadar Polutan (μg/m³)', 'week': 'Minggu'})
        st.plotly_chart(fig)

# Function for monthly pollution analysis page
def page_partilukalasi_polusi_bulanan(dataframes, kota_list):
    st.header("Analisis Partikulasi Polusi Bulanan")

    selected_kota = st.selectbox("Pilih Kota", kota_list)
    selected_year = st.number_input("Tahun", min_value=2013, max_value=2017, value=2013)

    if selected_year == 2013:
        selected_month = st.number_input("Bulan", min_value=3, max_value=12, value=3)
    elif selected_year == 2017:
        selected_month = st.number_input("Bulan", min_value=1, max_value=2, value=1)
    else:
        selected_month = st.number_input("Bulan", min_value=1, max_value=12, value=1)

    if st.button("Analisis Bulanan"):
        df = dataframes[selected_kota]
        hasil_kualitas_udara = partikulasi_polusi_bulanan(df, selected_year, selected_month)

        st.write(f"Hasil Kualitas Udara di {selected_kota} pada {selected_month}/{selected_year}:")
        st.dataframe(hasil_kualitas_udara)

        # Visualisasi hasil bulanan
        fig = px.bar(hasil_kualitas_udara, x='month', y=['avg_PM25', 'avg_PM10'],
                     title=f"Kualitas Udara di {selected_kota} pada {selected_month}/{selected_year}",
                     labels={'value': 'Kadar Polutan (μg/m³)', 'month': 'Bulan'})
        st.plotly_chart(fig)

# Function for yearly pollution analysis page
def page_partilukalasi_polusi_tahunan(dataframes, kota_list):
    st.header("Analisis Partikulasi Polusi Tahunan")

    selected_kota = st.selectbox("Pilih Kota", kota_list)
    selected_year = st.number_input("Tahun", min_value=2013, max_value=2017, value=2013)

    if st.button("Analisis Tahunan"):
        df = dataframes[selected_kota]
        hasil_kualitas_udara = partikulasi_polusi_tahunan(df, selected_year)

        st.write(f"Hasil Kualitas Udara di {selected_kota} pada {selected_year}:")
        st.dataframe(hasil_kualitas_udara)

        # Visualisasi hasil tahunan
        fig = px.bar(hasil_kualitas_udara, x='year', y=['avg_PM25', 'avg_PM10'],
                     title=f"Kualitas Udara di {selected_kota} pada {selected_year}",
                     labels={'value': 'Kadar Polutan (μg/m³)', 'year': 'Tahun'})
        st.plotly_chart(fig)
# metrik 
def page_metrik(dataframes, kota_list):
    st.header("Metrik Kualitas Udara")

    selected_kota = st.selectbox("Pilih Kota", kota_list)
    selected_year = st.number_input("Tahun", min_value=2013, max_value=2017, value=2013)

    if selected_year == 2013:
        selected_month = st.number_input("Bulan", min_value=3, max_value=12, value=3)
    elif selected_year == 2017:
        selected_month = st.number_input("Bulan", min_value=1, max_value=2, value=1)
    else:
        selected_month = st.number_input("Bulan", min_value=1, max_value=12, value=1)

    if st.button("Tampilkan Metrik"):
        df = dataframes[selected_kota]

        # Harian
        hasil_kualitas_udara_harian = partikulasi_polusi_harian(df, selected_year, selected_month, 1, 31)
        avg_PM25_harian = hasil_kualitas_udara_harian['avg_PM25'].mean()
        avg_PM10_harian = hasil_kualitas_udara_harian['avg_PM10'].mean()

        # Mingguan
        hasil_kualitas_udara_mingguan = partikulasi_polusi_mingguan(df, selected_year, selected_month)
        avg_PM25_mingguan = hasil_kualitas_udara_mingguan['avg_PM25'].mean()
        avg_PM10_mingguan = hasil_kualitas_udara_mingguan['avg_PM10'].mean()

        # Bulanan
        hasil_kualitas_udara_bulanan = partikulasi_polusi_bulanan(df, selected_year, selected_month)
        avg_PM25_bulanan = hasil_kualitas_udara_bulanan['avg_PM25'].mean()
        avg_PM10_bulanan = hasil_kualitas_udara_bulanan['avg_PM10'].mean()

        # Tahunan
        hasil_kualitas_udara_tahunan = partikulasi_polusi_tahunan(df, selected_year)
        avg_PM25_tahunan = hasil_kualitas_udara_tahunan['avg_PM25'].mean()
        avg_PM10_tahunan = hasil_kualitas_udara_tahunan['avg_PM10'].mean()

        col1, col2 = st.columns(2)
        col1.metric("PM 2.5 Harian", f"{avg_PM25_harian:.2f} μg/m³", f"{selected_kota} - {selected_month}/{selected_year}")
        col2.metric("PM10 Harian", f"{avg_PM10_harian:.2f} μg/m³", f"{selected_kota} - {selected_month}/{selected_year}")

        col1, col2 = st.columns(2)
        col1.metric("PM 2.5 Mingguan", f"{avg_PM25_mingguan:.2f} μg/m³", f"{selected_kota} - {selected_month}/{selected_year}")
        col2.metric("PM10 Mingguan", f"{avg_PM10_mingguan:.2f} μg/m³", f"{selected_kota} - {selected_month}/{selected_year}")

        col1, col2 = st.columns(2)
        col1.metric("PM 2.5 Bulanan", f"{avg_PM25_bulanan:.2f} μg/m³", f"{selected_kota} - {selected_month}/{selected_year}")
        col2.metric("PM10 Bulanan", f"{avg_PM10_bulanan:.2f} μg/m³", f"{selected_kota} - {selected_month}/{selected_year}")

        col1, col2 = st.columns(2)
        col1.metric("PM 2.5 Tahunan", f"{avg_PM25_tahunan:.2f} μg/m³", f"{selected_kota} - {selected_year}")
        col2.metric("PM10 Tahunan", f"{avg_PM10_tahunan:.2f} μg/m³", f"{selected_kota} - {selected_year}")


# Main function to run the app
def main():
    st.title("Analisis Data Kualitas Udara")
    dataframes = load_data()
    kota_list = list(dataframes.keys())

    st.sidebar.title("Navigasi")
    app_mode = st.sidebar.selectbox("Pilih Mode Analisis", ("Analisis Harian", "Analisis Mingguan", "Analisis Bulanan", "Analisis Tahunan"))

    if app_mode == "Analisis Harian":
        page_partilukalasi_polusi_harian(dataframes, kota_list)
    elif app_mode == "Analisis Mingguan":
        page_partilukalasi_polusi_mingguan(dataframes, kota_list)
    elif app_mode == "Analisis Bulanan":
        page_partilukalasi_polusi_bulanan(dataframes, kota_list)
    elif app_mode == "Analisis Tahunan":
        page_partilukalasi_polusi_tahunan(dataframes, kota_list)

if __name__ == "__main__":
    main()
