# import semua library yang diperlukan
import streamlit as st
import numpy as np
import pandas as pd
import os

# load page config
st.set_page_config(
    page_title="Kualitas Udara Per Kota",
    page_icon="https://w7.pngwing.com/pngs/597/667/png-transparent-computer-icons-air-quality-index-air-pollution-others.png",
)

st.title("Kualitas Udara Per Kota")

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
# kualitas udara harian
def kualitas_udara_harian(df, year, month, day_start, day_end):
    filtered_df = df[(df['year'] == year) & (df['month'] == month) & (df['day'].between(day_start, day_end))]
    result = filtered_df.groupby(['year', 'month', 'day']).agg(
        avg_PM25=('PM2.5', 'mean'), 
        avg_PM10=('PM10', 'mean'), 
        avg_NO2=('NO2', 'mean'), 
        avg_CO=('CO', 'mean'),
        avg_O3=('O3', 'mean'),
    ).reset_index()
    return result
# kualitas udara mingguan
def kualitas_udara_mingguan(df, year, week_start, week_end):
    filtered_df = df[(df['year'] == year) & (df['week'].between(week_start, week_end))]
    result = filtered_df.groupby(['year', 'week']).agg(
        avg_PM25=('PM2.5', 'mean'), 
        avg_PM10=('PM10', 'mean'), 
        avg_NO2=('NO2', 'mean'), 
        avg_CO=('CO', 'mean'),
        avg_O3=('O3', 'mean'),
    ).reset_index()
    return result

# kualitas udara bulanan
def kualitas_udara_bulanan(df, year, month_start, month_end):
    filtered_df = df[(df['year'] == year) & (df['month'].between(month_start, month_end))]
    result = filtered_df.groupby(['year', 'month']).agg(
        avg_PM25=('PM2.5', 'mean'), 
        avg_PM10=('PM10', 'mean'), 
        avg_NO2=('NO2', 'mean'), 
        avg_CO=('CO', 'mean'),
        avg_O3=('O3', 'mean'),
    ).reset_index()
    return result

# kualitas udara tahunan
def kualitas_udara_tahunan(df, year):
    filtered_df = df[df['year'] == year]
    result = filtered_df.groupby(['year']).agg(
        avg_PM25=('PM2.5', 'mean'), 
        avg_PM10=('PM10', 'mean'), 
        avg_NO2=('NO2', 'mean'), 
        avg_CO=('CO', 'mean'),
        avg_O3=('O3', 'mean'),
    ).reset_index()
    return result

# end code engine kualitas udara per kota

# membuat sidebar
with st.sidebar:
    selected_city = st.selectbox("Pilih Kota", list(dataframes.keys()))
    selected_year = st.selectbox("Pilih Tahun", options=["2013", "2014", "2015", "2016", "2017"], index=0)

    if selected_city and selected_year:
