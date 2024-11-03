# Import Library
import streamlit as st
import pandas as pd
import os
import plotly.express as px

# Title and Header
st.title("Kualitas Udara: O3 🌐")
st.header("INFORMASI KONSENTRASI O3 🌿")
_KETERANGAN_O3 = """
Ozon (O3) adalah gas yang terbentuk dari tiga atom oksigen, memiliki warna biru pucat, dan bau khas yang tajam. Di lapisan stratosfer, ozon berperan penting sebagai pelindung dari sinar ultraviolet (UV) yang berbahaya. Namun, ozon di permukaan bumi (troposfer) menjadi polutan yang dapat merusak kesehatan manusia dan lingkungan.

Ozon permukaan terutama terbentuk melalui reaksi kimia antara nitrogen dioksida (NO2) dan senyawa organik volatil (VOC) di bawah pengaruh sinar matahari. Peningkatan ozon umumnya terjadi di wilayah perkotaan, seiring dengan aktivitas kendaraan bermotor dan pembakaran bahan bakar fosil dari industri. Menurut Badan Perlindungan Lingkungan AS (EPA), paparan ozon dapat menyebabkan iritasi saluran pernapasan, mengurangi fungsi paru-paru, serta memperburuk penyakit pernapasan kronis seperti asma dan bronkitis.

Ozon adalah salah satu komponen utama dalam pembentukan kabut asap (smog) yang mengurangi visibilitas dan kualitas udara di kota besar. Konsentrasi ozon tinggi dalam jangka panjang dapat berdampak buruk bagi kesehatan manusia dan mengancam vegetasi serta ekosistem. (Sumber: EPA, 2023; WHO, 2022)
"""

st.write(_KETERANGAN_O3)

# membuat metric
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric(label="BAIK", value="0-4000 μg/m³")
col2.metric(label="SEDANG", value="8000 μg/m³")
col3.metric(label="TIDAK SEHAT", value="15000 μg/m³")
col4.metric(label="SANGAT TIDAK SEHAT", value="30000 μg/m³")
col5.metric(label="BERBAHAYA", value="45000 μg/m³")

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

# function untuk menghitung kategori O3
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
    
# Kategori Warna 
color_map = {
    "BAIK": "green",
    "SEDANG": "blue",
    "TIDAK SEHAT": "orange",
    "SANGAT TIDAK SEHAT": "red",
    "BERBAHAYA": "black"
}

# function untuk menghitung rata-rata O3 harian
def o3_harian(df, year, month, day_start, day_end):
    df_filtered = df[(df['year'] == int(year)) & (df['month'] == int(month)) & (df['day'] >= day_start) & (df['day'] <= day_end)]
    result = df_filtered.groupby(['year', 'month', 'day']).agg(avg_O3=('O3', 'mean')).reset_index()
    result['avg_O3'] = result['avg_O3'].round()
    result['kategori_o3'] = result['avg_O3'].apply(kategori_o3)
    return result

# function untuk menghitung rata-rata O3 mingguan
def o3_mingguan(df, year, month):
    filtered_df = df.query('year == @year and month == @month')

    filtered_df['week'] = filtered_df['day'].apply(lambda x: (x - 1) // 7 + 1)

    result = (
        filtered_df.groupby(['year', 'month', 'week'])
        .agg(avg_O3=('O3', 'mean'))
        .reset_index()
    )
    result['avg_O3'] = result['avg_O3'].round()
    result['kategori_o3'] = result['avg_O3'].apply(kategori_o3)
    return result

# function untuk menghitung rata-rata O3 bulanan
def o3_bulanan(df, year):
    filtered_df = df[df['year'] == year]
    result = (
        filtered_df.groupby('month')
        .agg(avg_O3=('O3', 'mean'))
        .reset_index()
    )
    result['avg_O3'] = result['avg_O3'].round()
    result['kategori_o3_bulanan'] = result['avg_O3'].apply(kategori_o3)
    return result

# function untuk menghitung rata-rata O3 tahunan
def o3_tahunan(df, year):
    filtered_df = df[df['year'] == year]
    result = (
        filtered_df.groupby('year')
        .agg(avg_O3=('O3', 'mean'))
        .reset_index()
    )
    result['avg_O3'] = result['avg_O3'].round()
    result['kategori_o3_tahunan'] = result['avg_O3'].apply(kategori_o3)
    return result

# Tab setup
tab1, tab2, tab3, tab4 = st.tabs(["Harian","Mingguan", "Bulanan", "Tahunan"])

# Tab 1 Harian
with tab1:
    with st.form(key='_form_harian_o3'):
        selected_city_harian_o3 = st.selectbox("Pilih Kota", list(dataframes.keys()))
        selected_year_harian_o3 = st.number_input("Pilih Tahun", min_value=2013, max_value=2017, step=1)
        if selected_year_harian_o3 == 2013:
            selected_month_harian_o3 = st.number_input("Pilih Bulan", min_value=3, max_value=12, step=1)
        elif selected_year_harian_o3 == 2017:
            selected_month_harian_o3 = st.number_input("Pilih Bulan", min_value=1, max_value=2, step=1)
        else:
            selected_month_harian_o3 = st.number_input("Pilih Bulan", min_value=1, max_value=12, step=1)
        submit_button_harian_o3 = st.form_submit_button(label='Analisa Harian')
        
    if submit_button_harian_o3:
        st.header(f"Konsentrasi O3 Harian di {selected_city_harian_o3}")
        filtered_data_o3 = o3_harian(dataframes[selected_city_harian_o3], selected_year_harian_o3, selected_month_harian_o3, 1, 31)
        filtered_data_o3['kategori_o3'] = filtered_data_o3['avg_O3'].apply(kategori_o3)
        st.vega_lite_chart(
            {
                "layer": [
                    {
                        "mark": "bar",
                        "encoding": {
                            "x": {"field": "day", "type": "ordinal", "axis": {"title": "Hari"}},
                            "y": {"field": "avg_O3", "type": "quantitative", "axis": {"title": "O3 (ppm)", "scale": {"domain": [0, 120]}}},
                            "color": {
                                "field": "kategori_o3",
                                "type": "nominal",
                                "scale": {
                                    "domain": ["BAIK", "SEDANG", "TIDAK SEHAT", "BERBAHAYA", "SANGAT BERBAHAYA"],
                                    "range": ["green", "blue", "orange", "red", "black"]
                                },
                                "legend": {"title": "Kategori O3"}
                            },
                            "tooltip": [
                                {"field": "day", "type": "ordinal", "title": "Hari"},
                                {"field": "avg_O3", "type": "quantitative", "title": "O3 (ppm)"},
                                {"field": "kategori_o3", "type": "nominal", "title": "Kategori O3"}
                            ]
                        }
                    }
                ],
                "title": f"Konsentrasi O3 di {selected_city_harian_o3}",
                "data": {"values": filtered_data_o3.to_dict("records")}
            }
        )
        rata_rata_harian_o3 = filtered_data_o3['avg_O3'].mean()
        kategori_rata_rata_o3 = kategori_o3(rata_rata_harian_o3)
        if kategori_rata_rata_o3 == "BAIK":
            keterangan_o3 = f"Rata-rata konsentrasi O3 harian di {selected_city_harian_o3} pada bulan {selected_month_harian_o3} tahun {selected_year_harian_o3} adalah {rata_rata_harian_o3:.2f} ppm, yang termasuk dalam kategori {kategori_rata_rata_o3}. Kualitas udara di kota ini sangat baik dan tidak berbahaya bagi kesehatan."
        elif kategori_rata_rata_o3 == "SEDANG":
            keterangan_o3 = f"Rata-rata konsentrasi O3 harian di {selected_city_harian_o3} pada bulan {selected_month_harian_o3} tahun {selected_year_harian_o3} adalah {rata_rata_harian_o3:.2f} ppm, yang termasuk dalam kategori {kategori_rata_rata_o3}. Kualitas udara di kota ini sedang dan perlu diawasi untuk mencegah penurunan kualitas udara."
        elif kategori_rata_rata_o3 == "TIDAK SEHAT":
            keterangan_o3 = f"Rata-rata konsentrasi O3 harian di {selected_city_harian_o3} pada bulan {selected_month_harian_o3} tahun {selected_year_harian_o3} adalah {rata_rata_harian_o3:.2f} ppm, yang termasuk dalam kategori {kategori_rata_rata_o3}. Kualitas udara di kota ini tidak sehat dan perlu diambil tindakan untuk mengurangi polusi."
        elif kategori_rata_rata_o3 == "BERBAHAYA":
            keterangan_o3 = f"Rata-rata konsentrasi O3 harian di {selected_city_harian_o3} pada bulan {selected_month_harian_o3} tahun {selected_year_harian_o3} adalah {rata_rata_harian_o3:.2f} ppm, yang termasuk dalam kategori {kategori_rata_rata_o3}. Kualitas udara di kota ini berbahaya bagi kesehatan dan perlu diambil tindakan segera untuk mengurangi polusi."
        elif kategori_rata_rata_o3 == "SANGAT BERBAHAYA":
            keterangan_o3 = f"Rata-rata konsentrasi O3 harian di {selected_city_harian_o3} pada bulan {selected_month_harian_o3} tahun {selected_year_harian_o3} adalah {rata_rata_harian_o3:.2f} ppm, yang termasuk dalam kategori {kategori_rata_rata_o3}. Kualitas udara di kota ini sangat berbahaya bagi kesehatan dan perlu diambil tindakan darurat untuk mengurangi polusi."
        st.write(keterangan_o3)

# Tab 2 Mingguan
with tab2:
    with st.form(key='_form_mingguan_o3'):
        selected_city_mingguan_o3 = st.selectbox("Pilih Kota", list(dataframes.keys()))
        selected_year_mingguan_o3 = st.number_input("Pilih Tahun", min_value=2013, max_value=2017, step=1, value=2013)
        selected_month_mingguan_o3 = st.number_input("Pilih Bulan", min_value=3, max_value=12, step=1, value=3)
        submit_button_mingguan_o3 = st.form_submit_button(label='Analisa Mingguan')
    
    if submit_button_mingguan_o3:
        df = dataframes[selected_city_mingguan_o3]
        # Pastikan kolom 'day' bertipe integer
        if df['day'].dtype != 'int':
            df['day'] = df['day'].astype(int)
        
        hasil_kualitas_udara_o3 = o3_mingguan(df, selected_year_mingguan_o3, selected_month_mingguan_o3)
        
        fig = px.bar(
            hasil_kualitas_udara_o3, x='week', y='avg_O3', color='kategori_o3',
            color_discrete_map={
                "BAIK": "green", 
                "SEDANG": "blue", 
                "TIDAK SEHAT": "orange", 
                "BERBAHAYA": "red", 
                "SANGAT BERBAHAYA": "black"
            },
            title=f"Kualitas Udara Mingguan di {selected_city_mingguan_o3} pada Bulan {selected_month_mingguan_o3} Tahun {selected_year_mingguan_o3}",
            labels={"week": "Minggu", "avg_O3": "Rata-rata O3 (ppm)", "kategori_o3": "Kategori O3"}
        )
        st.plotly_chart(fig)

        
        # Menghasilkan interpretasi berdasarkan kategori
        rata_rata_mingguan_o3 = hasil_kualitas_udara_o3['avg_O3'].mean()
        kategori_rata_rata_o3 = kategori_o3(rata_rata_mingguan_o3)
        if kategori_rata_rata_o3 == "BAIK":
            keterangan_o3 = f"Rata-rata konsentrasi O3 mingguan di {selected_city_mingguan_o3} pada bulan {selected_month_mingguan_o3} tahun {selected_year_mingguan_o3} adalah {rata_rata_mingguan_o3:.2f} ppm, yang termasuk dalam kategori {kategori_rata_rata_o3}. Kualitas udara sangat baik dan tidak berbahaya bagi kesehatan."
        elif kategori_rata_rata_o3 == "SEDANG":
            keterangan_o3 = f"Rata-rata konsentrasi O3 mingguan di {selected_city_mingguan_o3} pada bulan {selected_month_mingguan_o3} tahun {selected_year_mingguan_o3} adalah {rata_rata_mingguan_o3:.2f} ppm, yang termasuk dalam kategori {kategori_rata_rata_o3}. Kualitas udara masih aman, namun perlu diawasi untuk mencegah peningkatan polusi."
        elif kategori_rata_rata_o3 == "TIDAK SEHAT":
            keterangan_o3 = f"Rata-rata konsentrasi O3 mingguan di {selected_city_mingguan_o3} pada bulan {selected_month_mingguan_o3} tahun {selected_year_mingguan_o3} adalah {rata_rata_mingguan_o3:.2f} ppm, yang termasuk dalam kategori {kategori_rata_rata_o3}. Kualitas udara tidak sehat dan perlu pengurangan aktivitas yang menyebabkan polusi."
        elif kategori_rata_rata_o3 == "BERBAHAYA":
            keterangan_o3 = f"Rata-rata konsentrasi O3 mingguan di {selected_city_mingguan_o3} pada bulan {selected_month_mingguan_o3} tahun {selected_year_mingguan_o3} adalah {rata_rata_mingguan_o3:.2f} ppm, yang termasuk dalam kategori {kategori_rata_rata_o3}. Udara berbahaya dan tindakan pencegahan perlu dilakukan segera."
        elif kategori_rata_rata_o3 == "SANGAT BERBAHAYA":
            keterangan_o3 = f"Rata-rata konsentrasi O3 mingguan di {selected_city_mingguan_o3} pada bulan {selected_month_mingguan_o3} tahun {selected_year_mingguan_o3} adalah {rata_rata_mingguan_o3:.2f} ppm, yang termasuk dalam kategori {kategori_rata_rata_o3}. Situasi sangat berbahaya dan tindakan darurat diperlukan."

        st.write(keterangan_o3)

# Tab 3 Bulanan
with tab3:
    with st.form(key='_form_bulanan_o3'):
        selected_city_bulanan_o3 = st.selectbox("Pilih Kota", list(dataframes.keys()))
        selected_year_bulanan_o3 = st.number_input("Pilih Tahun", min_value=2013, max_value=2017, step=1, value=2013)
        submit_button_bulanan_o3 = st.form_submit_button(label='Analisa Bulanan')

    if submit_button_bulanan_o3:
        df = dataframes[selected_city_bulanan_o3]
        hasil_kualitas_udara_o3_bulanan = o3_bulanan(df, selected_year_bulanan_o3)

        fig = px.bar(
            hasil_kualitas_udara_o3_bulanan, x='month', y='avg_O3', color='kategori_o3_bulanan',
            color_discrete_map={
                "BAIK": "green", 
                "SEDANG": "blue", 
                "TIDAK SEHAT": "orange", 
                "BERBAHAYA": "red", 
                "SANGAT BERBAHAYA": "black"
            },
            title=f"Kualitas Udara Bulanan di {selected_city_bulanan_o3} pada Tahun {selected_year_bulanan_o3}",
            labels={"month": "Bulan", "avg_O3": "O3 (ppm)"}
        )
        
        st.plotly_chart(fig)

        # Menampilkan rata-rata bulanan O3
        rata_rata_bulanan_o3 = hasil_kualitas_udara_o3_bulanan['avg_O3'].mean()
        kategori_rata_rata_bulanan_o3 = kategori_o3(rata_rata_bulanan_o3)
        if kategori_rata_rata_bulanan_o3 == "BAIK":
            keterangan_o3 = f"Rata-rata konsentrasi O3 bulanan di {selected_city_bulanan_o3} pada tahun {selected_year_bulanan_o3} adalah {rata_rata_bulanan_o3:.2f} ppm, yang termasuk dalam kategori {kategori_rata_rata_bulanan_o3}. Kualitas udara sangat baik dan tidak berbahaya bagi kesehatan."
        elif kategori_rata_rata_bulanan_o3 == "SEDANG":
            keterangan_o3 = f"Rata-rata konsentrasi O3 bulanan di {selected_city_bulanan_o3} pada tahun {selected_year_bulanan_o3} adalah {rata_rata_bulanan_o3:.2f} ppm, yang termasuk dalam kategori {kategori_rata_rata_bulanan_o3}. Kualitas udara masih aman, namun perlu diawasi untuk mencegah peningkatan polusi."
        elif kategori_rata_rata_bulanan_o3 == "TIDAK SEHAT":
            keterangan_o3 = f"Rata-rata konsentrasi O3 bulanan di {selected_city_bulanan_o3} pada tahun {selected_year_bulanan_o3} adalah {rata_rata_bulanan_o3:.2f} ppm, yang termasuk dalam kategori {kategori_rata_rata_bulanan_o3}. Kualitas udara tidak sehat dan perlu pengurangan aktivitas yang menyebabkan polusi."
        elif kategori_rata_rata_bulanan_o3 == "BERBAHAYA":
            keterangan_o3 = f"Rata-rata konsentrasi O3 bulanan di {selected_city_bulanan_o3} pada tahun {selected_year_bulanan_o3} adalah {rata_rata_bulanan_o3:.2f} ppm, yang termasuk dalam kategori {kategori_rata_rata_bulanan_o3}. Udara berbahaya dan tindakan pencegahan perlu dilakukan segera."
        elif kategori_rata_rata_bulanan_o3 == "SANGAT BERBAHAYA":
            keterangan_o3 = f"Rata-rata konsentrasi O3 bulanan di {selected_city_bulanan_o3} pada tahun {selected_year_bulanan_o3} adalah {rata_rata_bulanan_o3:.2f} ppm, yang termasuk dalam kategori {kategori_rata_rata_bulanan_o3}. Situasi sangat berbahaya dan tindakan darurat diperlukan."
        st.write(keterangan_o3)

# Tab 4 Tahunan
with tab4:
    with st.form(key='_form_tahunan'):
        st.header("Analisis Kualitas Udara Tahunan")
        kota_list = list(dataframes.keys())
        selected_kota = st.selectbox("Pilih Kota", kota_list, key='selectbox_tahunan')
        tahun = st.number_input("Pilih Tahun", min_value=2013, max_value=2017, step=1, key='tahun_tahunan')
        if st.form_submit_button("Analisis Tahunan"):
            df = dataframes[selected_kota]
            hasil_kualitas_udara = pd.DataFrame()
            for tahun in range(2013, 2018):
                hasil_kualitas_udara_tahun = o3_tahunan(df, tahun)
                hasil_kualitas_udara = pd.concat([hasil_kualitas_udara, hasil_kualitas_udara_tahun])
            hasil_kualitas_udara['kategori'] = hasil_kualitas_udara['avg_O3'].apply(kategori_o3)
            fig = px.bar(hasil_kualitas_udara, x='year', y='avg_O3',
                         title=f"Kualitas Udara di {selected_kota} dari 2013 hingga 2017",
                         labels={'avg_O3': 'Kadar O3 (ppm)', 'year': 'Tahun'},
                         color='kategori',  # Menggunakan kategori untuk pewarnaan
                         color_discrete_map={
                             "BAIK": 'green',
                             "SEDANG": 'blue',
                             "TIDAK SEHAT": 'orange',
                             "BERBAHAYA": 'red',
                             "SANGAT BERBAHAYA": 'black'
                         })  # Menggunakan peta warna yang ditentukan
            fig.update_yaxes(range=[0, 200])
            fig.update_xaxes(tickvals=[2013, 2014, 2015, 2016, 2017])
            st.plotly_chart(fig)
            # Menulis keterangan menggunakan magic write tentang keadaan polusi
            kategori_tahunan = hasil_kualitas_udara['kategori'].unique()
            if "BAIK" in kategori_tahunan:
                keterangan = f"Dari tahun 2013 hingga 2017, kualitas udara di {selected_kota} telah mengalami variasi. Tahun-tahun tertentu menunjukkan kualitas udara yang baik."
            elif "SEDANG" in kategori_tahunan:
                keterangan = f"Dari tahun 2013 hingga 2017, kualitas udara di {selected_kota} telah mengalami variasi. Tahun-tahun tertentu menunjukkan kualitas udara yang sedang dan perlu diawasi."
            elif "TIDAK SEHAT" in kategori_tahunan:
                keterangan = f"Dari tahun 2013 hingga 2017, kualitas udara di {selected_kota} telah mengalami variasi. Tahun-tahun tertentu menunjukkan kualitas udara yang tidak sehat dan perlu diambil tindakan."
            elif "BERBAHAYA" in kategori_tahunan:
                keterangan = f"Dari tahun 2013 hingga 2017, kualitas udara di {selected_kota} telah mengalami variasi. Tahun-tahun tertentu menunjukkan kualitas udara yang sangat berbahaya bagi kesehatan dan perlu diambil tindakan segera."
            elif "SANGAT BERBAHAYA" in kategori_tahunan:
                keterangan = f"Dari tahun 2013 hingga 2017, kualitas udara di {selected_kota} telah mengalami variasi. Tahun-tahun tertentu menunjukkan kualitas udara yang sangat berbahaya dan tindakan darurat diperlukan."
            st.write(keterangan)

