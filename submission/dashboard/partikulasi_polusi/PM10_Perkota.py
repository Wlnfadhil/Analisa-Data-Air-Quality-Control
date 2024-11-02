import streamlit as st
import pandas as pd
import os
import plotly.express as px

# Title and header
st.title("Partikulasi Polusi: 🏭")
st.header("INFORMASI KONSENTRASI PARTIKULAT PM10")
_KETERANGAN = """
Partikulat (PM10) adalah Partikel udara yang berukuran lebih kecil dari 10 mikron (mikrometer).

Nilai Ambang Batas (NAB) adalah Batas konsentrasi polusi udara yang diperbolehkan berada dalam udara ambien. NAB PM10 = 150 µgram/m³.
"""
st.write(_KETERANGAN)

# Metrics
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("BAIK", "0-50 μg/m³", "👨")
col2.metric("SEDANG", "51 - 150 μg/m³", "😐")
col3.metric("TIDAK SEHAT", "151 - 350 μg/m³", "🤒")
col4.metric("SANGAT TIDAK SEHAT", "351-420 μg/m³", "🚨")
col5.metric("BERBAHAYA", "<420 μg/m³", "💀")

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

# PM10 category function
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

# Daily pollution analysis function
def partikulasi_polusi_harian(df, year, month, day_start, day_end):
    df = df[(df['year'] == int(year)) & (df['month'] == int(month)) & (df['day'] >= day_start) & (df['day'] <= day_end)]
    result = df.groupby(['year', 'month', 'day']).agg(avg_PM25=('PM2.5', 'mean'), avg_PM10=('PM10', 'mean')).reset_index()
    result['kategori_pm10'] = result['avg_PM10'].apply(kategori_pm10)
    return result.round({'avg_PM25': 0, 'avg_PM10': 0})

# Partikulasi Polusi Mingguan
def partikulasi_polusi_mingguan(df, year, month):
    filtered_df = df.query('year == @year and month == @month')
    
    if filtered_df.empty:
        st.error("No data available for the selected year and month.")
        return None
    
    filtered_df['day'] = filtered_df['day'].astype(int)  # Ensure 'day' is numeric
    filtered_df['week'] = filtered_df['day'].apply(lambda x: (x - 1) // 7 + 1)


    result = filtered_df.groupby(['year', 'month', 'week']).agg(avg_PM10=('PM10', 'mean')).reset_index()
    result['avg_PM10'] = result['avg_PM10'].round()
    
    return result

# Monthly pollution analysis function
def partikulasi_polusi_bulanan(df, year):
    filtered_df = df[df['year'] == year]
    result = (
        filtered_df.groupby('month')
        .agg(avg_PM25=('PM2.5', 'mean'), avg_PM10=('PM10', 'mean'))
        .reset_index()
    )
    result['avg_PM25'] = result['avg_PM25'].round()
    result['avg_PM10'] = result['avg_PM10'].round()
    result['kategori_pm10_bulanan'] = result['avg_PM10'].apply(kategori_pm10)
    return result

# Patikulasi Tahunan
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

# Tab setup
tab1, tab2, tab3, tab4 = st.tabs(["Harian","Mingguan", "Bulanan", "Tahunan"])

# Daily analysis tab
with tab1:
    with st.form(key='_form_harian'):
        selected_city_harian = st.selectbox("Pilih Kota", list(dataframes.keys()))
        selected_year_harian = st.number_input("Pilih Tahun", min_value=2013, max_value=2017, step=1)
        if selected_year_harian == 2013:
            selected_month_harian = st.number_input("Pilih Bulan", min_value=3, max_value=12, step=1)
        elif selected_year_harian == 2017:
            selected_month_harian = st.number_input("Pilih Bulan", min_value=1, max_value=2, step=1)
        else:
            selected_month_harian = st.number_input("Pilih Bulan", min_value=1, max_value=12, step=1)
        submit_button_harian = st.form_submit_button(label='Analisa Harian')

    if submit_button_harian:
        st.header(f"Konsentrasi PM10 Harian di {selected_city_harian}")
        filtered_data = partikulasi_polusi_harian(dataframes[selected_city_harian], selected_year_harian, selected_month_harian, 1, 31)
        filtered_data['kategori_pm10'] = filtered_data['avg_PM10'].apply(kategori_pm10)
        st.vega_lite_chart({
            "layer": [
                {
                    "mark": "area",
                    "encoding": {
                        "x": {"field": "day", "type": "quantitative", "axis": {"title": "Hari"}},
                        "y": {"field": "avg_PM10", "type": "quantitative", "axis": {"title": "PM10 (µg/m³)", "scale": {"domain": [0, 900]}}},
                        "color": {
                            "field": "kategori_pm10",
                            "type": "nominal",
                            "scale": {
                                "domain": ["Baik", "Sedang", "Tidak Sehat", "Sangat Tidak Sehat", "Berbahaya"],
                                "range": ["green", "blue", "orange", "red", "black"]
                            },
                            "legend": {"title": "Kategori PM10"}
                        },
                        "tooltip": [
                            {"field": "day", "type": "quantitative", "title": "Hari"},
                            {"field": "avg_PM10", "type": "quantitative", "title": "PM10 (µg/m³)"},
                            {"field": "kategori_pm10", "type": "nominal", "title": "Kategori PM10"}
                        ]
                    }
                },
                {
                    "mark": "line",
                    "encoding": {
                        "x": {"field": "day", "type": "quantitative"},
                        "y": {"field": "avg_PM10", "type": "quantitative"},
                        "color": {"value": "white"}
                    }
                }
            ],
            "title": f"Konsentrasi PM10 di {selected_city_harian}",
            "data": {"values": filtered_data.to_dict("records")}
        })
        rata_rata_harian = filtered_data['avg_PM10'].mean()
        kategori_rata_rata = kategori_pm10(rata_rata_harian)
        keterangan = f"Rata-rata konsentrasi PM10 harian di {selected_city_harian} pada bulan {selected_month_harian} tahun {selected_year_harian} adalah {rata_rata_harian:.2f} µg/m³, yang termasuk dalam kategori {kategori_rata_rata}."
        st.write(keterangan)
with tab2:
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
            fig.update_layout(yaxis=dict(range=[0, 420]))
            st.plotly_chart(fig)

            # Keterangan untuk tiap minggu
            for index, row in hasil_kualitas_udara.iterrows():
                kategori = kategori_pm10(row['avg_PM10'])
                st.write(f"Minggu ke-{int(row['week'])}: Kadar PM10 rata-rata adalah {row['avg_PM10']} μg/m³, termasuk ke dalam kategori polusi {kategori}.")
# Monthly analysis tab
with tab3:
    with st.form(key='_form_bulanan'):
        selected_city_bulanan = st.selectbox("Pilih Kota", list(dataframes.keys()))
        selected_year_bulanan = st.number_input("Pilih Tahun", min_value=2013, max_value=2017, step=1)
        submit_button_bulanan = st.form_submit_button(label='Analisa Bulanan')

    if submit_button_bulanan:
        st.header(f"Konsentrasi PM10 Bulanan di {selected_city_bulanan} pada Tahun {selected_year_bulanan}")
        filtered_data = partikulasi_polusi_bulanan(dataframes[selected_city_bulanan], selected_year_bulanan)
        fig = px.bar(
            filtered_data, 
            x='month', 
            y='avg_PM10', 
            color='kategori_pm10_bulanan',
            color_discrete_map={
                "Baik": "green", 
                "Sedang": "blue", 
                "Tidak Sehat": "orange", 
                "Sangat Tidak Sehat": "red", 
                "Berbahaya": "black"
            },
            title=f"Konsentrasi PM10 Bulanan di {selected_city_bulanan} pada Tahun {selected_year_bulanan}"
        )
        rata_rata_bulanan = filtered_data['avg_PM10'].mean()
        kategori_rata_rata = kategori_pm10(rata_rata_bulanan)
        keterangan = f"Rata-rata konsentrasi PM10 bulanan di {selected_city_bulanan} pada tahun {selected_year_bulanan} adalah {rata_rata_bulanan:.2f} µg/m³, yang termasuk dalam kategori {kategori_rata_rata}."
        st.write(keterangan)
        fig.update_layout(height=420, xaxis_title="Bulan", yaxis_title="PM10 (µg/m³)", xaxis=dict(tickmode='linear', tick0=1, dtick=1), yaxis=dict(range=[0, 420]))
        # Mengubah sumbu x menjadi nama bulan
        fig.update_xaxes(ticktext=['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'])
        st.plotly_chart(fig, use_container_width=True)
        # Hasil analisis per bulan
        for index, row in filtered_data.iterrows():
            kategori_bulanan = kategori_pm10(row['avg_PM10'])
            st.write(f"Bulan {row['month']}: Kadar PM10 rata-rata adalah {row['avg_PM10']} μg/m³,termasuk ke dalam kategori polusi ({kategori_bulanan}).")

with tab4:
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
