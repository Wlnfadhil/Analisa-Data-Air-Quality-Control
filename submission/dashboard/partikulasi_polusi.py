import os
import pandas as pd
import streamlit as st
import plotly.express as px
# Load data
def load_data():
    current_dir = os.getcwd()
    csv_files = [
        "PRSA_Data_Aotizhongxin_20130301-20170228.csv",
        "PRSA_Data_Changping_20130301-20170228.csv",
        "PRSA_Data_Dingling_20130301-20170228.csv",
        "PRSA_Data_Dongsi_20130301-20170228.csv",
        "PRSA_Data_Guanyuan_20130301-20170228.csv",
        "PRSA_Data_Gucheng_20130301-20170228.csv",
        "PRSA_Data_Huairou_20130301-20170228.csv",
        "PRSA_Data_Nongzhanguan_20130301-20170228.csv",
        "PRSA_Data_Shunyi_20130301-20170228.csv",
        "PRSA_Data_Tiantan_20130301-20170228.csv",
        "PRSA_Data_Wanliu_20130301-20170228.csv",
        "PRSA_Data_Wanshouxigong_20130301-20170228.csv"
    ]

    dataframes = {}
    for csv_file in csv_files:
        file_path = os.path.join(current_dir, "submission/data", csv_file)  # Adjust directory if necessary
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            location = csv_file.split('_')[2]
            dataframes[location] = df
        else:
            st.error(f"File {csv_file} not found at {file_path}")
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
