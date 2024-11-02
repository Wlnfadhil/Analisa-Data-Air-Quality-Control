# import library
import streamlit as st
import os
import pandas as pd
import plotly.express as px

# Header
st.title("Partikulasi Polusi: 🏭")
st.header("INFORMASI KONSENTRASI PARTIKULAT PM2.5")
_KETERANGAN = """
Partikulat (PM2.5) adalah Partikel udara yang berukuran lebih kecil dari 2.5 mikron (mikrometer).

Nilai Ambang Batas (NAB) adalah Batas konsentrasi polusi udara yang diperbolehkan berada dalam udara ambien. NAB PM2.5 = 35 µgram/m3.
"""
st.write(_KETERANGAN)
# metrik
col1, col2, col3, col4, col5 = st.columns(5)
col1.image("submission/img/icon/pm25/pm25-baik.webp", caption="BAIK: 0-15.5 μg/m³")
col2.image("submission/img/icon/pm25/pm25-sedang.webp", caption="SEDANG: 15.6 - 55.4 μg/m³")
col3.image("submission/img/icon/pm25/pm25-tidaksehat.webp", caption="TIDAK SEHAT: 55.5 - 150.4 μg/m³")
col4.image("submission/img/icon/pm25/pm25-sangattidaksehat.webp", caption="SANGAT TIDAK SEHAT: 150.5 - 250.4 μg/m³")
col5.image("submission/img/icon/pm25/pm25-berbahaya.webp", caption="BERBAHAYA: >250.4 μg/m³")

# load data
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

# Partikulasi Polusi PM 2.5 Harian
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

# Partikulasi Polusi PM 2.5 Mingguan
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

# Partikulasi Polusi PM 2.5 Bulanan

def partikulasi_polusi_bulanan(df, year):
    filtered_df = df[df['year'] == year]
    result = (
        filtered_df.groupby('month')
        .agg(avg_PM25=('PM2.5', 'mean'), avg_PM10=('PM10', 'mean'))
        .reset_index()
    )
    result['avg_PM25'] = result['avg_PM25'].round()
    result['avg_PM10'] = result['avg_PM10'].round()
    result['kategori_pm25_bulanan'] = result['avg_PM25'].apply(kategori_pm25)
    return result

# Partikulasi Polusi PM 2.5 Tahunan

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


# Fungsi untuk mendapatkan kategori kualitas udara
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

# membuat Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Harian","Mingguan", "Bulanan", "Tahunan"])

# Tab 1 Partikulasi Polusi PM 2.5 Harian
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
        st.header(f"Konsentrasi PM2.5 Harian di {selected_city_harian}")
        filtered_data = partikulasi_polusi_harian(dataframes[selected_city_harian], selected_year_harian, selected_month_harian, 1, 31)
        filtered_data['kategori_pm25'] = filtered_data['avg_PM25'].apply(kategori_pm25)
        st.vega_lite_chart(
            {
                "layer": [
                    {
                        "mark": "area",
                        "encoding": {
                            "x": {"field": "day", "type": "quantitative", "axis": {"title": "Hari"}},
                            "y": {"field": "avg_PM25", "type": "quantitative", "axis": {"title": "PM2.5 (µg/m³)", "scale": {"domain": [0, 300]}}},
                            "color": {
                                "field": "kategori_pm25",
                                "type": "nominal",
                                "scale": {
                                    "domain": ["Baik", "Sedang", "Tidak Sehat", "Sangat Tidak Sehat", "Berbahaya"],
                                    "range": ["green", "blue", "orange", "red", "black"]
                                },
                                "legend": {"title": "Kategori PM2.5"}
                            },
                            "tooltip": [
                                {"field": "day", "type": "quantitative", "title": "Hari"},
                                {"field": "avg_PM25", "type": "quantitative", "title": "PM2.5 (µg/m³)"},
                                {"field": "kategori_pm25", "type": "nominal", "title": "Kategori PM2.5"}
                            ]
                        }
                    },
                    {
                        "mark": "line",
                        "encoding": {
                            "x": {"field": "day", "type": "quantitative"},
                            "y": {"field": "avg_PM25", "type": "quantitative"},
                            "color": {"value": "white"}
                        }
                    }
                ],
                "title": f"Konsentrasi PM2.5 di {selected_city_harian}",
                "data": {"values": filtered_data.to_dict("records")}
            }
        )
        rata_rata_harian = filtered_data['avg_PM25'].mean()
        kategori_rata_rata = kategori_pm25(rata_rata_harian)
        keterangan = f"Rata-rata konsentrasi PM2.5 harian di {selected_city_harian} pada bulan {selected_month_harian} tahun {selected_year_harian} adalah {rata_rata_harian:.2f} µg/m³, yang termasuk dalam kategori {kategori_rata_rata}."
        st.write(keterangan)

# Tab 2 Partikulasi Polusi PM 2.5 Mingguan
with tab2:
    with st.form(key='_form_mingguan'):
        selected_city_mingguan = st.selectbox("Pilih Kota", list(dataframes.keys()))
        selected_year_mingguan = st.number_input("Pilih Tahun", min_value=2013, max_value=2017, step=1)
        if selected_year_mingguan == 2013:
            selected_month_mingguan = st.number_input("Pilih Bulan", min_value=3, max_value=12, step=1)
        elif selected_year_mingguan == 2017:
            selected_month_mingguan = st.number_input("Pilih Bulan", min_value=1, max_value=2, step=1)
        else:
            selected_month_mingguan = st.number_input("Pilih Bulan", min_value=1, max_value=12, step=1)
        submit_button_mingguan = st.form_submit_button(label='Analisa Mingguan')
    if submit_button_mingguan:
        df = dataframes[selected_city_mingguan]
        df['day'] = df['day'].astype(int)

        hasil_kualitas_udara = partikulasi_polusi_mingguan(df, selected_year_mingguan, selected_month_mingguan)

        fig = px.bar(
            hasil_kualitas_udara, x='week', y='avg_PM25', color='avg_PM25',
            color_discrete_map={
                "Baik": "green", 
                "Sedang": "blue", 
                "Tidak Sehat": "orange", 
                "Sangat Tidak Sehat": "red", 
                "Berbahaya": "black"
            },
            title=f"Kualitas Udara Mingguan di {selected_city_mingguan} pada {selected_month_mingguan}/{selected_year_mingguan}",
            labels={'avg_PM25': 'Kadar PM2.5 (μg/m³)', 'week': 'Minggu'}
        )
        fig.update_layout(yaxis=dict(range=[0, 300]))
        st.plotly_chart(fig)

        # Keterangan untuk tiap minggu
        for index, row in hasil_kualitas_udara.iterrows():
            kategori = kategori_pm25(row['avg_PM25'])
            st.write(f"Minggu ke-{int(row['week'])}: Kadar PM2.5 rata-rata adalah {row['avg_PM25']} μg/m³, termasuk ke dalam kategori polusi {kategori}.")

# Tab 3 Partikulasi Polusi PM 2.5 Bulanan
with tab3:
    with st.form(key='_from_bulanan'):
        selected_city_bulanan = st.selectbox("Pilih Kota", list(dataframes.keys()))
        selected_year_bulanan = st.number_input("Pilih Tahun", min_value=2013, max_value=2017, step=1)
        submit_button_bulanan = st.form_submit_button(label='Analisa Bulanan')

    if submit_button_bulanan:
        st.header(f"Konsentrasi PM2.5 Bulanan di {selected_city_bulanan} pada Tahun {selected_year_bulanan}")
        filtered_data = partikulasi_polusi_bulanan(dataframes[selected_city_bulanan], selected_year_bulanan)

        fig = px.bar(filtered_data, x='month', y='avg_PM25', color='kategori_pm25_bulanan',
                     color_discrete_map={
                         "Baik": "green", "Sedang": "blue", "Tidak Sehat": "orange", "Sangat Tidak Sehat": "red", "Berbahaya": "black"
                     })
        fig.update_layout(title=f"Konsentrasi PM2.5 Bulanan di {selected_city_bulanan} pada Tahun {selected_year_bulanan}")
        fig.update_yaxes(range=[0, 300])
        fig.update_layout(height=420, xaxis_title="Bulan", yaxis_title="PM2.5 (µg/m³)", xaxis=dict(tickmode='linear', tick0=1, dtick=1), yaxis=dict(range=[0, 300]))
        # Mengubah sumbu x menjadi nama bulan
        fig.update_xaxes(ticktext=['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'])
        st.plotly_chart(fig, use_container_width=True)

        # Hasil analisis per bulan
        for index, row in filtered_data.iterrows():
            kategori_bulanan = kategori_pm25(row['avg_PM25'])
            st.write(f"Bulan {row['month']}: Kadar PM2.5 rata-rata adalah {row['avg_PM25']} μg/m³, termasuk ke dalam kategori polusi ({kategori_bulanan}).")

# Tab 4 Partikulasi Polusi PM 2.5 Tahunan
with tab4:
    with st.form(key='_form_tahunan'):
        st.header("Analisis Partikulasi Polusi Tahunan")
        kota_list = list(dataframes.keys())
        selected_kota = st.selectbox("Pilih Kota", kota_list, key='selectbox_tahunan')
        if st.form_submit_button("Analisis Tahunan"):
            df = dataframes[selected_kota]
            hasil_kualitas_udara = pd.DataFrame()
            for tahun in range(2013, 2018):
                hasil_kualitas_udara_tahun = partikulasi_polusi_tahunan(df, tahun)
                hasil_kualitas_udara = pd.concat([hasil_kualitas_udara, hasil_kualitas_udara_tahun])
            
            hasil_kualitas_udara['kategori'] = hasil_kualitas_udara['avg_PM25'].apply(kategori_pm25)

            fig = px.bar(hasil_kualitas_udara, x='year', y='avg_PM25',
                         title=f"Kualitas Udara di {selected_kota} dari 2013 hingga 2017",
                         labels={'avg_PM25': 'Kadar PM2.5 (μg/m³)', 'year': 'Tahun'},
                         color='kategori',  # Menggunakan kategori untuk pewarnaan
                         color_discrete_map={
                             "Baik": 'green',
                             "Sedang": 'blue',
                             "Tidak Sehat": 'orange',
                             "Sangat Tidak Sehat": 'red',
                             "Berbahaya": 'black'
                         })  # Menggunakan peta warna yang ditentukan
            fig.update_yaxes(range=[0, 300])
            fig.update_xaxes(tickvals=[2013, 2014, 2015, 2016, 2017])
            st.plotly_chart(fig)

            # Menulis keterangan menggunakan magic write tentang keadaan polusi
            st.write("Dari tahun 2013 hingga 2017, kualitas udara di {} telah mengalami variasi. Tahun-tahun tertentu menunjukkan kualitas udara yang tidak sehat dan sangat tidak sehat, sedangkan tahun lainnya menunjukkan kualitas udara yang sedang dan baik. Hal ini menunjukkan pentingnya pengawasan dan pengendalian polusi udara untuk meningkatkan kualitas hidup masyarakat.".format(selected_kota))
