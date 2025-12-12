# Laporan Proyek Akhir: Data Visualisation Competition 2025
**Tema:** Communicate the Co-Benefits of Climate Action  
**Nama Pengembang:** Restu Firmansyah  
**Target Audiens:** Pemerintah Lokal, Pembuat Kebijakan, dan Masyarakat Umum  

---

## 1. Latar Belakang

Perubahan iklim sering kali hanya dipandang sebagai masalah emisi karbon (CO2) yang abstrak dan jauh dari kehidupan sehari-hari. Padahal, tindakan mitigasi iklim membawa **manfaat tambahan (co-benefits)** yang nyata dan langsung dirasakan oleh masyarakat, seperti peningkatan kualitas udara, kesehatan yang lebih baik, penghematan biaya energi, dan pengurangan kemacetan.

Kompetisi "The Data Lab Data Visualisation Competition 2025" menantang peserta untuk memvisualisasikan data dari **UK Co-Benefits Atlas** agar dapat mengubah cara pandang audiens terhadap aksi iklim, dari sekadar "beban biaya" menjadi "peluang investasi" yang menguntungkan secara ekonomi dan sosial.

## 2. Tujuan

Tujuan dari pengembangan dashboard **"The Hidden Value of Climate Action"** ini adalah:
1.  **Mengungkap Nilai Tersembunyi:** Memvisualisasikan nilai moneter (£) dari berbagai manfaat tambahan aksi iklim yang sering terabaikan.
2.  **Mendukung Pengambilan Keputusan:** Memberikan alat bagi pemerintah lokal untuk membandingkan area mana yang paling membutuhkan intervensi dan manfaat apa yang paling potensial.
3.  **Edukasi Interaktif:** Membuat data ekonomi yang kompleks menjadi mudah dipahami melalui visualisasi naratif dan interaktif (seperti *gamification* visual).

## 3. Deskripsi Dataset

Aplikasi ini menggunakan dataset **UK Co-Benefits Atlas (Level 3 Data)** yang mencakup proyeksi manfaat ekonomi dari aksi iklim di berbagai wilayah (Data Zones) di Inggris, khususnya area Glasgow.

*   **Dimensi Waktu:** Proyeksi tahun 2025 hingga 2050 (Rentang 25 tahun).
*   **Variabel Utama (Co-Benefits):** Dataset ini mencakup 11 kategori manfaat, antara lain:
    *   🏃 **Active Travel:** Manfaat kesehatan dari berjalan kaki & bersepeda.
    *   💨 **Air Quality:** Penghematan biaya kesehatan akibat udara bersih.
    *   🚦 **Congestion:** Pengurangan kerugian ekonomi akibat macet.
    *   🏥 **Health:** Penurunan biaya NHS (Layanan Kesehatan).
    *   🔊 **Noise:** Peningkatan kualitas hidup akibat berkurangnya polusi suara.
    *   🏠 **Fuel Poverty:** Penghematan tagihan energi rumah tangga.
*   **Geospasial:** Data dikelompokkan berdasarkan Kode Area (Small Area Code) dan Otoritas Lokal (Local Authority).

## 4. Fitur Utama & Interpretasi Visualisasi

Dashboard ini dirancang dengan pendekatan *"Scrollytelling"* dan interaktivitas tingkat tinggi. Berikut adalah fitur unggulan dan cara interpretasinya:

### A. Animated Nightingale Rose Chart ("The Flower of Benefits") 🌺
*   **Deskripsi:** Grafik visual berbentuk bunga yang mekar, di mana setiap kelopak mewakili satu jenis manfaat (co-benefit).
*   **Interpretasi:**
    *   **Panjang Kelopak:** Menunjukkan besarnya nilai ekonomi (£).
    *   **Animasi Mekar:** Menunjukkan akumulasi manfaat dari tahun 2025 ke 2050.
    *   **Insight:** Pengguna dapat langsung melihat sektor mana yang memberikan kontribusi terbesar (kelopak paling panjang) tanpa harus membaca angka tabel yang rumit.

### B. Neon Sankey Diagram ("Value Flow Analysis") 🌊
*   **Deskripsi:** Diagram alur yang memetakan hubungan dari kategori besar (seperti Kesehatan, Lingkungan) ke dampak spesifiknya.
*   **Fitur:** Menggunakan gaya estetika *Neon* untuk kontras tinggi.
*   **Interpretasi:**
    *   **Ketebalan Aluran:** Menunjukkan proporsi kontribusi.
    *   **Insight:** Membantu audiens memahami "Dari mana uang itu datang?". Misalnya, audiens bisa melihat bahwa investasi di "Transportasi" ternyata mengalir deras ke "Penghematan Biaya Kesehatan".

### C. The Co-Benefit Race (Motion Bubble Chart) 🏎️
*   **Deskripsi:** Grafik animasi di mana ikon Emoji (🏃, 💨, 🚦) bergerak melintasi layar.
*   **Sumbu X (Posisi):** Total Nilai Manfaat (Kekayaan).
*   **Sumbu Y (Ketinggian):** Tingkat Pertumbuhan (Growth Rate).
*   **Interpretasi:**
    *   **Siapa di Depan (Kanan)?** Benefit dengan nilai ekonomi terbesar (Juara Bertahan).
    *   **Siapa di Atas?** Benefit yang sedang tumbuh paling cepat (Pendatang Baru Potensial).
    *   **Insight:** Membedakan antara manfaat yang sudah *jenuh* vs manfaat yang sedang *berkembang pesat*.

### D. Time-Lapse Bar Race ⏳
*   **Deskripsi:** Grafik batang yang "berbalapan" naik turun seiring berjalannya tahun.
*   **Interpretasi:** Memperlihatkan perubahan ranking prioritas. Benefit yang di tahun 2025 mungkin nomor 5, bisa jadi naik ke nomor 1 di tahun 2040. Ini krusial untuk perencanaan jangka panjang.

### E. Interactive Geospatial Map 🗺️
*   **Deskripsi:** Peta korolet (Choropleth Map) interaktif yang diwarnai berdasarkan intensitas manfaat total per area.
*   **Interpretasi:**
    *   **Warna Gelap/Terang:** Menunjukkan konsentrasi nilai manfaat. Area yang lebih terang/mencolok memiliki potensi penghematan ekonomi tertinggi dari aksi iklim.
    *   **Insight:** Pemerintah dapat menargetkan investasi ke zona-zona prioritas ini.

## 5. Manfaat Aplikasi

1.  **Transparansi Anggaran:** Membuktikan bahwa anggaran iklim bukan biaya hangus, melainkan investasi yang kembali dalam bentuk kesehatan dan produktivitas.
2.  **Efisiensi Kebijakan:** Membantu pemerintah memilih kebijakan dengan *Return on Investment (ROI)* sosial tertinggi.
3.  **Public Engagement:** Meningkatkan dukungan publik terhadap proyek hijau karena mereka paham manfaat langsungnya bagi dompet dan kesehatan mereka.

## 6. Teknologi

Aplikasi ini dibangun menggunakan teknologi *State-of-the-Art* dalam Data Science:
*   **Framework:** Streamlit (Python)
*   **Data Processing:** DuckDB (In-memory SQL untuk performa ultra-cepat)
*   **Visualisasi:** Plotly Express & Graph Objects
*   **Deployment:** Streamlit Cloud (Dapat diakses 24/7)

---
**Tautan Aplikasi:** [https://climate-co-benefits-app.streamlit.app/](https://climate-co-benefits-app.streamlit.app/)  
**Repositori Kode:** GitHub - FirmanRcode/climate-co-benefits-app  
