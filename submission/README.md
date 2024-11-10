# Dashboard Analisis Kualitas Udara dan Partikulasi Polusi

Proyek ini merupakan dashboard interaktif yang dikembangkan menggunakan Streamlit untuk menganalisis kualitas udara dan partikulasi polusi di berbagai kota. Aplikasi ini membantu pengguna memahami tren dan korelasi antara berbagai indikator kualitas udara seperti PM2.5, PM10, CO, NO2, O3, dan SO2.

## Fitur Utama
- **Analisis Kualitas Udara Per Kota**: Menampilkan data dan visualisasi untuk berbagai indikator kualitas udara di setiap kota.
- **Partikulasi Polusi**: Analisis partikulasi seperti PM2.5 dan PM10 serta korelasinya di berbagai kota.
- **Visualisasi Interaktif**: Grafik dan diagram interaktif menggunakan Plotly dan Streamlit untuk pengalaman pengguna yang lebih baik.

## Struktur Direktori
- **submission/**: Direktori utama proyek.
  - **dashboard/**: Direktori aplikasi dashboard.
    - **dashboard.py**: File utama aplikasi dashboard.
    - **kualitas_udara/**: Direktori modul analisis kualitas udara.
      - **CO_Perkota.py**: Modul analisis CO per kota.
      - **kualitas_udara_per_kota.py**: Modul analisis kualitas udara per kota.
      - **NO2_PerKota.py**: Modul analisis NO2 per kota.
      - **O3_Perkota.py**: Modul analisis O3 per kota.
      - **SO2_Perkota.py**: Modul analisis SO2 per kota.
    - **partikulasi_polusi/**: Direktori modul analisis partikulasi polusi.
      - **Korelasi_partikulasi_polusi_semua_kota.py**: Modul analisis korelasi partikulasi polusi di semua kota.
      - **PM10_Perkota.py**: Modul analisis PM10 per kota.
      - **PM2.5_PerKota.py**: Modul analisis PM2.5 per kota.

## Cara Menjalankan Aplikasi Secara Lokal
1. **Kloning repositori ini**:
   ```bash
   git clone <URL_REPOSITORI>
   cd <NAMA_FOLDER_PROYEK>
2. Instal dependensi: Pastikan Python 3.x telah diinstal di sistem Anda.
   ```bash
   pip install -r requirements.txt
3. Jalankan aplikasi Streamlit:
   ```bash
   streamlit run submission/dashboard/dashboard.py
4. Buka aplikasi di browser: Aplikasi akan terbuka secara otomatis di http://localhost:8501/ atau alamat port yang ditampilkan di terminal.

## Akses Aplikasi Online
Aplikasi ini dapat diakses secara online melalui tautan berikut: [Dashboard Analisis Kualitas Udara dan Partikulasi Polusi](https://iehhbd9ktqxnzqn4gz75cq.streamlit.app/)

## Dependensi Utama
- streamlit
- pandas
- numpy
- plotly
- matplotlib

## Catatan
Pastikan data CSV yang diperlukan sudah diatur di folder submission/data agar aplikasi dapat memuat data dengan benar.

## Kontribusi
Kontribusi sangat dihargai. Silakan fork repositori ini dan ajukan pull request untuk perbaikan atau fitur baru.

## Lisensi
Proyek ini dilisensikan di bawah MIT License.

README ini mencakup deskripsi proyek, fitur, struktur direktori, panduan untuk menjalankan aplikasi, dan tautan akses online. Jangan lupa untuk mengganti `<URL_REPOSITORI>` dan `<NAMA_FOLDER_PROYEK>` sesuai kebutuhan.
