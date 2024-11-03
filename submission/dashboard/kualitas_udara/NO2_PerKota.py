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

# Function to calculate NO2 category
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



# Function to calculate NO2 daily analysis
def no2_harian(df, year, month, day_start, day_end):
    df_filtered = df[(df['year'] == int(year)) & (df['month'] == int(month)) & (df['day'] >= day_start) & (df['day'] <= day_end)]
    if df_filtered.empty:
        return None  # Mengembalikan None jika tidak ada data yang cocok
    result = df_filtered.groupby(['year', 'month', 'day']).agg(avg_NO2=('NO2', 'mean')).reset_index()
    result['kategori_no2'] = result['avg_NO2'].apply(kategori_no2)
    
    # Define color mapping based on categories
    color_map = {
        "BAIK": "green",
        "SEDANG": "blue",
        "TIDAK SEHAT": "orange",
        "SANGAT TIDAK SEHAT": "red",
        "BERBAHAYA": "black"
    }
    
    return result  # Pastikan untuk mengembalikan DataFrame yang valid

# Function to calculate NO2 weekly analysis

def no2_mingguan(df, year, month):
    filtered_df = df.query('year == @year and month == @month')
    if filtered_df.empty:
        return None  # Mengembalikan None jika tidak ada data yang cocok
    if filtered_df['day'].apply(lambda x: isinstance(x, int)).all():
        filtered_df['week'] = filtered_df['day'].apply(lambda x: (x - 1) // 7 + 1)
    result = filtered_df.groupby(['year', 'month', 'week']).agg(avg_NO2=('NO2', 'mean')).reset_index()
    result['avg_NO2'] = result['avg_NO2'].round()
    
    # Memisahkan kategori dan warna
    result['kategori_no2'] = result['avg_NO2'].apply(kategori_no2)
    result['warna_kategori'] = result['kategori_no2'].map({
        "BAIK": "green",
        "SEDANG": "blue",
        "TIDAK SEHAT": "orange",
        "SANGAT TIDAK SEHAT": "red",
        "BERBAHAYA": "black"
    })
    
    return result

# Function to calculate NO2 monthly analysis
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

# Function to calculate NO2 yearly analysis
def no2_tahunan(df, year):
    filtered_df = df.query('year == @year')
    result = filtered_df.groupby('year').agg(avg_NO2=('NO2', 'mean')).reset_index()
    result['avg_NO2'] = result['avg_NO2'].round()
    result['kategori_no2_tahunan'] = result['avg_NO2'].apply(kategori_no2)
    return result

# Tab setup
tab1, tab2, tab3, tab4 = st.tabs(["Harian","Mingguan", "Bulanan", "Tahunan"])   

# Tab 1 Harian
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
        st.header(f"Konsentrasi NO2 Harian di {selected_city_harian}")
        filtered_data = no2_harian(dataframes[selected_city_harian], selected_year_harian, selected_month_harian, 1, 31)
        if filtered_data is not None:
            filtered_data['kategori_no2'] = filtered_data['avg_NO2'].apply(kategori_no2)
            st.vega_lite_chart({
                "layer": [
                    {
                        "mark": "area",
                        "encoding": {
                            "x": {"field": "day", "type": "quantitative", "axis": {"title": "Hari"}},
                            "y": {"field": "avg_NO2", "type": "quantitative", "axis": {"title": "NO2 (µg/m³)", "scale": {"domain": [0, 2260]}}},
                            "color": {
                                "field": "kategori_no2",
                                "type": "nominal",
                                "scale": {
                                    "domain": ["BAIK", "SEDANG", "TIDAK SEHAT", "SANGAT TIDAK SEHAT", "BERBAHAYA"],
                                    "range": ["green", "blue", "orange", "red", "black"]
                                },
                                "legend": {"title": "Kategori NO2"}
                            },
                            "tooltip": [
                                {"field": "day", "type": "quantitative", "title": "Hari"},
                                {"field": "avg_NO2", "type": "quantitative", "title": "NO2 (µg/m³)"},
                                {"field": "kategori_no2", "type": "nominal", "title": "Kategori NO2"}
                            ]
                        }
                    },
                    {
                        "mark": "line",
                        "encoding": {
                            "x": {"field": "day", "type": "quantitative"},
                            "y": {"field": "avg_NO2", "type": "quantitative"},
                            "color": {"value": "white"}
                        }
                    }
                ],
                "title": f"Konsentrasi NO2 di {selected_city_harian}",
                "data": {"values": filtered_data.to_dict("records")}
            })
            rata_rata_harian = filtered_data['avg_NO2'].mean()
            kategori_rata_rata = kategori_no2(rata_rata_harian)
            keterangan = f"Rata-rata konsentrasi NO2 harian di {selected_city_harian} pada bulan {selected_month_harian} tahun {selected_year_harian} adalah {rata_rata_harian:.2f} µg/m³, yang termasuk dalam kategori {kategori_rata_rata}."
            st.write(keterangan)

# Tab 2 Mingguan       
with tab2:
    with st.form(key='_form_mingguan'):
        selected_city_mingguan = st.selectbox("Pilih Kota", list(dataframes.keys()))
        selected_year_mingguan = st.number_input("Pilih Tahun", min_value=2013, max_value=2017, step=1)
        if selected_year_mingguan == 2013:
            selected_month_mingguan = st.number_input("Pilih Bulan", min_value=3, max_value=12, value=3)
        elif selected_year_mingguan == 2017:
            selected_month_mingguan = st.number_input("Pilih Bulan", min_value=1, max_value=2, value=1)
        else:
            selected_month_mingguan = st.number_input("Pilih Bulan", min_value=1, max_value=12, value=1)
        if st.form_submit_button(label='Analisa Mingguan'):
            df = dataframes[selected_city_mingguan]
            hasil_kualitas_udara = no2_mingguan(df, selected_year_mingguan, selected_month_mingguan)
            if hasil_kualitas_udara is not None:
                fig = px.bar(hasil_kualitas_udara,
                              x='week',
                              y='avg_NO2',
                              color='kategori_no2',
                              color_discrete_map={
                                  "BAIK": "green",
                                  "SEDANG": "blue",
                                  "TIDAK SEHAT": "orange",
                                  "SANGAT TIDAK SEHAT": "red",
                                  "BERBAHAYA": "black"
                              },
                              labels={"week": "Minggu", "avg_NO2": "Rata-rata NO2 (μg/m³)"},
                              title="Rata-rata Mingguan NO2"
                              )
                st.plotly_chart(fig, use_container_width=True)
                for index, row in hasil_kualitas_udara.iterrows():
                    kategori = kategori_no2(row['avg_NO2'])
                    st.write(f"Minggu ke-{int(row['week'])}: Kadar NO2 rata-rata adalah {row['avg_NO2']} μg/m³, termasuk ke dalam kategori polusi {kategori}. Maka dari itu, perlu perbaikan kualitas udara supaya warga dapat hidup lebih sehat.")
# tab 3 bulanan
with tab3:
    with st.form(key='_form_bulanan'):
        selected_city_bulanan = st.selectbox("Pilih Kota", list(dataframes.keys()))
        selected_year_bulanan = st.number_input("Pilih Tahun", min_value=2013, max_value=2017, step=1)
        submit_button_bulanan = st.form_submit_button(label='Analisa Bulanan')

    if submit_button_bulanan:
        st.header(f"Konsentrasi NO2 Bulanan di {selected_city_bulanan} pada Tahun {selected_year_bulanan}")
        filtered_data = no2_bulanan(dataframes[selected_city_bulanan], selected_year_bulanan)

        fig = px.bar(
            filtered_data, x='month', y='avg_NO2', color='kategori_no2_bulanan', color_discrete_map={
                "BAIK": "green", 
                "SEDANG": "blue", 
                "TIDAK SEHAT": "orange", 
                "SANGAT TIDAK SEHAT": "red", 
                "BERBAHAYA": "black"
            },
            title=f"Analisis NO2 Bulanan di {selected_city_bulanan} pada Tahun {selected_year_bulanan}",
            labels={'avg_NO2': 'Kadar NO2 (μg/m³)', 'month': 'Bulan'}
        )
        fig.update_layout(yaxis=dict(range=[0, 150]))
        st.plotly_chart(fig, use_container_width=True)
        for index, row in filtered_data.iterrows():
            kategori = kategori_no2(row['avg_NO2'])
            st.write(f"Bulan ke-{int(row['month'])}: Kadar NO2 rata-rata adalah {row['avg_NO2']} μg/m³, termasuk ke dalam kategori polusi {kategori}. Maka dari itu, kualitas udara perlu perbaikan supaya warga dapat hidup lebih sehat.")

# Tab 4 Tahunan
with tab4:
    with st.form(key='_form_tahunan'):
        st.header("Analisis NO2 Tahunan")
        kota_list = list(dataframes.keys())
        selected_kota = st.selectbox("Pilih Kota", kota_list)
        if st.form_submit_button("Analisis Tahunan"):
            df = dataframes[selected_kota]
            hasil_kualitas_udara = pd.DataFrame()
            for tahun in range(2013, 2018):
                hasil_kualitas_udara_tahun = no2_tahunan(df, tahun)
                hasil_kualitas_udara = pd.concat([hasil_kualitas_udara, hasil_kualitas_udara_tahun])
            
            hasil_kualitas_udara['kategori'] = hasil_kualitas_udara['avg_NO2'].apply(kategori_no2)
            fig = px.bar(hasil_kualitas_udara, x='year', y='avg_NO2', color='kategori',
                         title=f"Kualitas Udara di {selected_kota} dari 2013 hingga 2017",
                         labels={'avg_NO2': 'Kadar Polutan (μg/m³)', 'year': 'Tahun'},
                         color_discrete_map={
                             "BAIK": 'green',
                             "SEDANG": 'blue',
                             "TIDAK SEHAT": 'orange',
                             "SANGAT TIDAK SEHAT": 'red',
                             "BERBAHAYA": 'black'
                         })
            st.plotly_chart(fig, use_container_width=True)
            keterangan = ""
            if hasil_kualitas_udara['kategori'].iloc[0] == "BAIK":
                keterangan = "Dari tahun 2013 hingga 2017, kadar NO2 di {} telah menunjukkan kualitas udara yang baik. Hal ini menunjukkan bahwa pengawasan dan pengendalian polusi udara telah efektif dalam meningkatkan kualitas hidup masyarakat.".format(selected_kota)
            elif hasil_kualitas_udara['kategori'].iloc[0] == "SEDANG":
                keterangan = "Dari tahun 2013 hingga 2017, kadar NO2 di {} telah menunjukkan kualitas udara yang sedang. Oleh karena itu, perlu dilakukan upaya peningkatan kualitas udara untuk mencapai kategori baik.".format(selected_kota)
            elif hasil_kualitas_udara['kategori'].iloc[0] == "TIDAK SEHAT":
                keterangan = "Dari tahun 2013 hingga 2017, kadar NO2 di {} telah menunjukkan kualitas udara yang tidak sehat. Hal ini menunjukkan bahwa pengawasan dan pengendalian polusi udara masih belum efektif dalam meningkatkan kualitas hidup masyarakat.".format(selected_kota)
            else:
                keterangan = "Dari tahun 2013 hingga 2017, kadar NO2 di {} telah menunjukkan kualitas udara yang sangat tidak sehat atau berbahaya. Oleh karena itu, perlu dilakukan upaya peningkatan kualitas udara yang lebih serius untuk mencapai kategori baik.".format(selected_kota)
            st.write(keterangan)



