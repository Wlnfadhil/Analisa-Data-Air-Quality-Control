import streamlit as st
import pandas as pd
import os
import plotly.express as px

# Title and Header
st.title("Kualitas Udara: SO2 🌫️")
st.header("INFORMASI KONSENTRASI SO2 📰")
_KETERANGAN = """
Sulfur Dioksida (SO2) adalah salah satu spesies dari gas-gas oksida sulfur (SOx). Gas ini sangat mudah terlarut dalam air, memiliki bau namun tidak berwarna. SO2 dan gas-gas oksida sulfur lainnya terbentuk saat terjadi pembakaran bahan bakar fosil yang mengandung sulfur. Sulfur sendiri terdapat dalam hampir semua material mentah yang belum diolah seperti minyak mentah, batu bara, dan bijih-bijih yang mengandung metal seperti alumunium, tembaga, seng, timbal, dan besi. Di daerah perkotaan, yang menjadi sumber sulfur utama adalah kegiatan pembangkit tenaga listrik, terutama yang menggunakan batu bara ataupun minyak diesel sebagai bahan bakarnya, juga gas buang dari kendaraan yang menggunakan diesel dan industri-industri yang menggunakan bahan bakar batu bara dan minyak mentah. Pencemaran oleh sulfur oksida terutama disebabkan oleh dua komponen sulfur bentuk gas yang tidak berwarna, yaitu sulfur dioksida (SO2) dan Sulfur trioksida (SO3), dan keduanya disebut sulfur oksida (SOx). Sulfur dioksida mempunyai karakteristik bau yang tajam dan tidak mudah terbakar di udara, sedangkan sulfur trioksida merupakan komponen yang tidak reaktif.
   
"""
st.write(_KETERANGAN)
if st.button('Informasi Dampak Pencemaran SO2'):
    st.subheader("Dampak Pencemaran SO2")
    st.subheader("Dampak Pencemaran SO2 pada Kesehatan")
    st.write("🏥")

    st.write("Gas SO2 telah lama dikenal sebagai gas yang dapat menyebabkan iritasi pada sistem pernafasan, seperti pada selaput lendir hidung, tenggorokan, dan saluran udara di paru-paru. Efek kesehatan ini menjadi lebih buruk pada penderita asma. Disamping itu, SO2 terkonversi di udara menjadi pencemar sekunder seperti aerosol sulfat.")
    st.write("Aerosol yang dihasilkan sebagai pencemar sekunder umumnya mempunyai ukuran yang sangat halus sehingga dapat terhisap ke dalam sistem pernafasan bawah. Aerosol sulfat yang masuk ke dalam saluran pernafasan dapat menyebabkan dampak kesehatan yang lebih berat daripada partikel-partikel lainnya karena mempunyai sifat korosif dan karsinogen. Oleh karena gas SO2 berpotensi untuk menghasilkan aerosol sulfat sebagai pencemar sekunder, kasus peningkatan angka kematian karena kegagalan pernafasan terutama pada orang tua dan anak-anak sering berhubungan dengan konsentrasi SO2 dan partikulat secara bersamaan (Harrop, 2002).")
    st.write("Dalam bentuk gas, SO2 dapat menyebabkan iritasi pada paru-paru yang menyebabkan timbulnya kesulitan bernafas, terutama pada kelompok orang yang sensitive seperti orang berpenyakit asma, anak-anak, dan lansia. SO2 juga mampu bereaksi dengan senyawa kimia lain membentuk partikel sulfat yang jika terhirup dapat terakumulasi di paru-paru dan menyebabkan kesulitan bernapas, penyakit pernapasan, dan bahkan kematian (EPA, 2007).")

    st.subheader("Lingkungan 🌿")
    st.write("Tingginya kadar SO2 di udara merupakan salah satu penyebab terjadinya hujan asam. Hujan asam disebabkan oleh belerang (sulfur) yang merupakan pengotor dalam bahan bakar fosil serta nitrogen di udara yang bereaksi dengan oksigen membentuk sulfur dioksida dan nitrogen oksida. Zat-zat ini berdifusi ke atmosfer dan bereaksi dengan air untuk membentuk asam sulfat dan asam nitrat yang mudah larut sehingga jatuh bersama air hujan. Air hujan yang asam tersebut akan meningkatkan kadar keasaman tanah dan air permukaan yang terbukti berbahaya bagi kehidupan ikan dan tanaman")
    st.write("Kelebihan zat asam pada danau akan mengakibatkan sedikitnya species yang bertahan. Jenis Plankton dan invertebrate merupakan makhluk yang paling pertama mati akibat pengaruh pengasaman. Apa yang terjadi jika didanau memiliki pH dibawah 5, lebih dari 75 % dari spesies ikan akan hilang (Anonim, 2002). Ini disebabkan oleh pengaruh rantai makanan, yang secara signifikan berdampak pada keberlangsungan suatu ekosistem. Tidak semua danau yang terkena hujan asam akan menjadi pengasaman, dimana telah ditemukan jenis batuan dan tanah yang dapat membantu menetralkan keasaman.")
    st.write("Selain menyebabkan hujan asam, SO2 juga dapat mengurangi jarak pandang karena gas maupun partikel SO2 mampu menyerap cahaya sehingga menimbulkan kabut..")

    st.subheader("Dampak Pencemaran SO2 terhadap Tanaman 🌳")
    st.write("Sulfur dioksida juga berbahaya bagi tanaman. Adanya gas ini pada konsentrasi tinggi dapat membunuh jaringan pada daun. Pinggiran daun dan daerah diantara tulang-tulang daun rusak. Secara kronis SO2 menyebabkan terjadi")

# membuat metric
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric(label="BAIK", value="0-52 μg/m³")
col2.metric(label="SEDANG", value="52-180 μg/m³")
col3.metric(label="TIDAK SEHAT", value="400 μg/m³")
col4.metric(label="SANGAT TIDAK SEHAT", value="800 μg/m³")
col5.metric(label="BERBAHAYA", value="1200 μg/m³")

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

# function untuk menghitung kategori SO2
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

# Mengkategorikan Warna
color_map = {
    "BAIK": "green",
    "SEDANG": "blue",
    "TIDAK SEHAT": "orange",
    "SANGAT TIDAK SEHAT": "red",
    "BERBAHAYA": "black"
}

# function untuk menghitung rata-rata SO2 harian
def so2_harian(df, year, month, day_start, day_end):
    df_filtered = df[(df['year'] == int(year)) & (df['month'] == int(month)) & (df['day'] >= day_start) & (df['day'] <= day_end)]
    result = df_filtered.groupby(['year', 'month', 'day']).agg(avg_SO2=('SO2', 'mean')).reset_index()
    result['avg_SO2'] = result['avg_SO2'].round()
    result['kategori_so2'] = result['avg_SO2'].apply(kategori_so2)
    return result

# function untuk menghitung rata_rata SO2 mingguan
def so2_mingguan(df, year, month):
    filtered_df = df.query('year == @year and month == @month')

    filtered_df['week'] = filtered_df['day'].apply(lambda x: (x - 1) // 7 + 1)

    result = (
        filtered_df.groupby(['year', 'month', 'week'])
        .agg(avg_SO2=('SO2', 'mean'))
        .reset_index()
    )
    result['avg_SO2'] = result['avg_SO2'].round()
    result['kategori_so2'] = result['avg_SO2'].apply(kategori_so2)
    return result

# function untuk menghitung rata-rata SO2 bulanan
def so2_bulanan(df, year):
    filtered_df = df[df['year'] == year]
    result = (
        filtered_df.groupby('month')
        .agg(avg_SO2=('SO2', 'mean'))
        .reset_index()
    )
    result['avg_SO2'] = result['avg_SO2'].round()
    result['kategori_so2'] = result['avg_SO2'].apply(kategori_so2)
    result['kategori_so2_bulanan'] = result['avg_SO2'].apply(kategori_so2)
    return result

# function untuk menghitung rata-rata SO2 tahunan
def so2_tahunan(df, year):
    filtered_df = df[df['year'] == year]
    result = (
        filtered_df.groupby('year')
        .agg(avg_SO2=('SO2', 'mean'))
        .reset_index()
    )
    result['avg_SO2'] = result['avg_SO2'].round()
    result['kategori_so2'] = result['avg_SO2'].apply(kategori_so2)
    result['kategori_so2_tahunan'] = result['avg_SO2'].apply(kategori_so2)
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
        st.header(f"Konsentrasi SO2 Harian di {selected_city_harian}")
        filtered_data = so2_harian(dataframes[selected_city_harian], selected_year_harian, selected_month_harian, 1, 31)
        filtered_data['kategori_so2'] = filtered_data['avg_SO2'].apply(kategori_so2)
        st.vega_lite_chart(
            {
                "layer": [
                    {
                        "mark": "bar",
                        "encoding": {
                            "x": {"field": "day", "type": "ordinal", "axis": {"title": "Hari"}},
                            "y": {"field": "avg_SO2", "type": "quantitative", "axis": {"title": "SO2 (ppb)", "scale": {"domain": [0, 400]}}},
                            "color": {
                                "field": "kategori_so2",
                                "type": "nominal",
                                "scale": {
                                    "domain": ["BAIK", "SEDANG", "TIDAK SEHAT", "SANGAT TIDAK SEHAT", "BERBAHAYA"],
                                    "range": ["green", "blue", "orange", "red", "black"]
                                },
                                "legend": {"title": "Kategori SO2"}
                            },
                            "tooltip": [
                                {"field": "day", "type": "ordinal", "title": "Hari"},
                                {"field": "avg_SO2", "type": "quantitative", "title": "SO2 (ppb)"},
                                {"field": "kategori_so2", "type": "nominal", "title": "Kategori SO2"}
                            ]
                        }
                    }
                ],
                "title": f"Konsentrasi SO2 di {selected_city_harian}",
                "data": {"values": filtered_data.to_dict("records")}
            }
        )
        rata_rata_harian = filtered_data['avg_SO2'].mean()
        kategori_rata_rata = kategori_so2(rata_rata_harian)
        if kategori_rata_rata == "BAIK":
            keterangan = f"Rata-rata konsentrasi SO2 harian di {selected_city_harian} pada bulan {selected_month_harian} tahun {selected_year_harian} adalah {rata_rata_harian:.2f} ppb, yang termasuk dalam kategori {kategori_rata_rata}. Kualitas udara di kota ini sangat baik dan tidak berbahaya bagi kesehatan."
        elif kategori_rata_rata == "SEDANG":
            keterangan = f"Rata-rata konsentrasi SO2 harian di {selected_city_harian} pada bulan {selected_month_harian} tahun {selected_year_harian} adalah {rata_rata_harian:.2f} ppb, yang termasuk dalam kategori {kategori_rata_rata}. Kualitas udara di kota ini sedang dan perlu diawasi untuk mencegah penurunan kualitas udara."
        elif kategori_rata_rata == "TIDAK SEHAT":
            keterangan = f"Rata-rata konsentrasi SO2 harian di {selected_city_harian} pada bulan {selected_month_harian} tahun {selected_year_harian} adalah {rata_rata_harian:.2f} ppb, yang termasuk dalam kategori {kategori_rata_rata}. Kualitas udara di kota ini tidak sehat dan perlu diambil tindakan untuk mengurangi polusi."
        elif kategori_rata_rata == "SANGAT TIDAK SEHAT":
            keterangan = f"Rata-rata konsentrasi SO2 harian di {selected_city_harian} pada bulan {selected_month_harian} tahun {selected_year_harian} adalah {rata_rata_harian:.2f} ppb, yang termasuk dalam kategori {kategori_rata_rata}. Kualitas udara di kota ini sangat tidak sehat dan perlu diambil tindakan darurat untuk mengurangi polusi."
        elif kategori_rata_rata == "BERBAHAYA":
            keterangan = f"Rata-rata konsentrasi SO2 harian di {selected_city_harian} pada bulan {selected_month_harian} tahun {selected_year_harian} adalah {rata_rata_harian:.2f} ppb, yang termasuk dalam kategori {kategori_rata_rata}. Kualitas udara di kota ini sangat berbahaya bagi kesehatan dan perlu diambil tindakan segera untuk mengurangi polusi."
        st.write(keterangan)

# Tab 2 Mingguan
with tab2:
    with st.form(key='_form_mingguan'):
        selected_city_mingguan = st.selectbox("Pilih Kota", list(dataframes.keys()))
        selected_year_mingguan = st.number_input("Pilih Tahun", min_value=2013, max_value=2017, step=1, value=2013)
        selected_month_mingguan = st.number_input("Pilih Bulan", min_value=3, max_value=12, step=1, value=3)
        submit_button_mingguan = st.form_submit_button(label='Analisa Mingguan')
    if submit_button_mingguan:
        df = dataframes[selected_city_mingguan]
        df['day'] = df['day'].astype(int)
        hasil_kualitas_udara = so2_mingguan(df, selected_year_mingguan, selected_month_mingguan)
        
        fig = px.bar(
            hasil_kualitas_udara, x='week', y='avg_SO2', color='avg_SO2',
            color_discrete_map={
                "BAIK": "green", 
                "SEDANG": "blue", 
                "TIDAK SEHAT": "orange", 
                "SANGAT TIDAK SEHAT": "red", 
                "BERBAHAYA": "black"
            },
            title=f"Kualitas Udara Mingguan di {selected_city_mingguan} pada {selected_month_mingguan}/{selected_year_mingguan}",
            labels={'avg_SO2': 'Kadar SO2 (ppb)', 'week': 'Minggu'}
        )
        fig.update_layout(yaxis=dict(range=[0, 200]))
        st.plotly_chart(fig)

        # Keterangan untuk tiap minggu
        for index, row in hasil_kualitas_udara.iterrows():
            kategori = kategori_so2(row['avg_SO2'])
            if kategori == "BAIK":
                keterangan = f"Minggu ke-{int(row['week'])}: Kadar SO2 rata-rata adalah {row['avg_SO2']} ppb, yang termasuk dalam kategori {kategori}. Kualitas udara di kota ini sangat baik dan tidak berbahaya bagi kesehatan."
            elif kategori == "SEDANG":
                keterangan = f"Minggu ke-{int(row['week'])}: Kadar SO2 rata-rata adalah {row['avg_SO2']} ppb, yang termasuk dalam kategori {kategori}. Kualitas udara di kota ini sedang dan perlu diawasi untuk mencegah penurunan kualitas udara."
            elif kategori == "TIDAK SEHAT":
                keterangan = f"Minggu ke-{int(row['week'])}: Kadar SO2 rata-rata adalah {row['avg_SO2']} ppb, yang termasuk dalam kategori {kategori}. Kualitas udara di kota ini tidak sehat dan perlu diambil tindakan untuk mengurangi polusi."
            elif kategori == "SANGAT TIDAK SEHAT":
                keterangan = f"Minggu ke-{int(row['week'])}: Kadar SO2 rata-rata adalah {row['avg_SO2']} ppb, yang termasuk dalam kategori {kategori}. Kualitas udara di kota ini sangat tidak sehat dan perlu diambil tindakan darurat untuk mengurangi polusi."
            elif kategori == "BERBAHAYA":
                keterangan = f"Minggu ke-{int(row['week'])}: Kadar SO2 rata-rata adalah {row['avg_SO2']} ppb, yang termasuk dalam kategori {kategori}. Kualitas udara di kota ini sangat berbahaya bagi kesehatan dan perlu diambil tindakan segera untuk mengurangi polusi."
            st.write(keterangan)

# Tab 3 Bulanan
with tab3:
    with st.form(key='_form_bulanan'):
        selected_city_bulanan = st.selectbox("Pilih Kota", list(dataframes.keys()))
        selected_year_bulanan = st.number_input("Pilih Tahun", min_value=2013, max_value=2017, step=1)
        submit_button_bulanan = st.form_submit_button(label='Analisa Bulanan')
    if submit_button_bulanan:
        st.header(f"Konsentrasi SO2 Bulanan di {selected_city_bulanan} pada Tahun {selected_year_bulanan}")
        filtered_data = so2_bulanan(dataframes[selected_city_bulanan], selected_year_bulanan)
        
        fig = px.bar(filtered_data, x='month', y='avg_SO2', color='kategori_so2_bulanan',
                     color_discrete_map={
                         "BAIK": "green", "SEDANG": "blue", "TIDAK SEHAT": "orange", "SANGAT TIDAK SEHAT": "red", "BERBAHAYA": "black"
                     })
        fig.update_layout(title=f"Konsentrasi SO2 Bulanan di {selected_city_bulanan} pada Tahun {selected_year_bulanan}")
        fig.update_yaxes(range=[0, 200])
        fig.update_layout(height=420, xaxis_title="Bulan", yaxis_title="SO2 (ppb)", xaxis=dict(tickmode='linear', tick0=1, dtick=1), yaxis=dict(range=[0, 800]))
        # Mengubah sumbu x menjadi nama bulan
        fig.update_xaxes(ticktext=['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'])
        st.plotly_chart(fig, use_container_width=True)
        # Keterangan untuk tiap bulan
        for index, row in filtered_data.iterrows():
            kategori = kategori_so2(row['avg_SO2'])
            if kategori == "BAIK":
                keterangan = f"Bulan ke-{int(row['month'])}: Kadar SO2 rata-rata adalah {row['avg_SO2']} ppb, yang termasuk dalam kategori {kategori}. Kualitas udara di kota ini sangat baik dan tidak berbahaya bagi kesehatan."
            elif kategori == "SEDANG":
                keterangan = f"Bulan ke-{int(row['month'])}: Kadar SO2 rata-rata adalah {row['avg_SO2']} ppb, yang termasuk dalam kategori {kategori}. Kualitas udara di kota ini sedang dan perlu diawasi untuk mencegah penurunan kualitas udara."
            elif kategori == "TIDAK SEHAT":
                keterangan = f"Bulan ke-{int(row['month'])}: Kadar SO2 rata-rata adalah {row['avg_SO2']} ppb, yang termasuk dalam kategori {kategori}. Kualitas udara di kota ini tidak sehat dan perlu diambil tindakan untuk mengurangi polusi."
            elif kategori == "SANGAT TIDAK SEHAT":
                keterangan = f"Bulan ke-{int(row['month'])}: Kadar SO2 rata-rata adalah {row['avg_SO2']} ppb, yang termasuk dalam kategori {kategori}. Kualitas udara di kota ini sangat tidak sehat dan perlu diambil tindakan darurat untuk mengurangi polusi."
            elif kategori == "BERBAHAYA":
                keterangan = f"Bulan ke-{int(row['month'])}: Kadar SO2 rata-rata adalah {row['avg_SO2']} ppb, yang termasuk dalam kategori {kategori}. Kualitas udara di kota ini sangat berbahaya bagi kesehatan dan perlu diambil tindakan segera untuk mengurangi polusi."
            st.write(keterangan)

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
                hasil_kualitas_udara_tahun = so2_tahunan(df, tahun)
                hasil_kualitas_udara = pd.concat([hasil_kualitas_udara, hasil_kualitas_udara_tahun])
            hasil_kualitas_udara['kategori'] = hasil_kualitas_udara['avg_SO2'].apply(kategori_so2)
            fig = px.bar(hasil_kualitas_udara, x='year', y='avg_SO2',
                         title=f"Kualitas Udara di {selected_kota} dari 2013 hingga 2017",
                         labels={'avg_SO2': 'Kadar SO2 (ppb)', 'year': 'Tahun'},
                         color='kategori',  # Menggunakan kategori untuk pewarnaan
                         color_discrete_map={
                             "BAIK": 'green',
                             "SEDANG": 'blue',
                             "TIDAK SEHAT": 'orange',
                             "SANGAT TIDAK SEHAT": 'red',
                             "BERBAHAYA": 'black'
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
            elif "SANGAT TIDAK SEHAT" in kategori_tahunan:
                keterangan = f"Dari tahun 2013 hingga 2017, kualitas udara di {selected_kota} telah mengalami variasi. Tahun-tahun tertentu menunjukkan kualitas udara yang sangat tidak sehat dan perlu diambil tindakan darurat."
            elif "BERBAHAYA" in kategori_tahunan:
                keterangan = f"Dari tahun 2013 hingga 2017, kualitas udara di {selected_kota} telah mengalami variasi. Tahun-tahun tertentu menunjukkan kualitas udara yang sangat berbahaya bagi kesehatan dan perlu diambil tindakan segera."
            st.write(keterangan)
