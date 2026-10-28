# OryzAI --- Sistem Pakar Diagnosis Hama dan Penyakit Padi

## 1. Deskripsi Sistem

OryzAI adalah aplikasi sistem pakar berbasis Python dan Streamlit untuk
membantu skrining awal hama dan penyakit tanaman padi. Sistem
menganalisis gejala yang dipilih pengguna menggunakan metode **Forward
Chaining** dan **Certainty Factor (CF)**, lalu menampilkan dugaan
diagnosis beserta penjelasan aturan yang digunakan.

OryzAI merupakan alat bantu skrining awal dan bukan pengganti diagnosis
dari pakar atau penyuluh pertanian.

## 2. Instalasi dan Menjalankan Aplikasi

Pastikan Python telah terpasang, lalu buka terminal pada folder proyek.

**Windows (PowerShell):**

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

**macOS/Linux:**

``` bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Setelah perintah dijalankan, buka alamat lokal yang ditampilkan
Streamlit pada browser, biasanya `http://localhost:8501`.

Untuk menjalankan pengujian:

``` bash
python -m unittest discover -s tests -v
```

## 3. Fitur Sistem

-   **Konsultasi diagnosis:** memilih gejala dan tingkat keyakinan
    berdasarkan kondisi tanaman.
-   **Forward Chaining:** mencocokkan gejala dengan aturan IF--THEN
    dalam basis pengetahuan.
-   **Certainty Factor:** menghitung skor dukungan untuk kandidat
    diagnosis.
-   **Penjelasan hasil:** menampilkan aturan yang aktif dan alasan di
    balik hasil diagnosis.
-   **Kamus penyakit dan hama:** mencari informasi terkait diagnosis dan
    gejala.
-   **Kelola aturan:** menambah, mengubah, dan menghapus aturan pada
    basis pengetahuan.
-   **Riwayat konsultasi:** melihat riwayat dan mengunduh data
    konsultasi.

## 4. Screenshot

### Beranda

![Beranda OryzAI](docs/screenshots/beranda.png)

### Konsultasi dan pemilihan gejala

![Halaman konsultasi OryzAI](docs/screenshots/konsultasi.png)

### Hasil diagnosis

![Hasil diagnosis OryzAI](docs/screenshots/hasil-diagnosis.png)

### Kamus penyakit dan hama

![Halaman kamus penyakit dan hama OryzAI](https://github.com/user-attachments/assets/9ec40719-a5e9-4552-a3bb-787b7a44d713)

### Kelola aturan

<img width="1277" height="593" alt="Halaman kelola aturan OryzAI" src="https://github.com/user-attachments/assets/79f2cfa3-0645-4cda-b935-a176bf4e1ce8" />

### Riwayat konsultasi

<img width="1266" height="427" alt="Halaman riwayat transaksi OryzAI" src="https://github.com/user-attachments/assets/94a16afd-cbdd-48aa-901b-4f2faa0da317" />

### Certainty Factor

<img width="1233" height="175" alt="Halaman Certainty Factor OryzAI" src="https://github.com/user-attachments/assets/7b991fdc-f8c9-4eff-879f-5318c40aac1a" />

### Forward Chaining

<img width="1231" height="301" alt="Halaman Forward Chaining 1 OryzAI" src="https://github.com/user-attachments/assets/680041fc-a5fe-4b26-be0a-1e3787e92b53" />

<img width="1233" height="382" alt="Halaman Forward Chaining 2 OryzAI" src="https://github.com/user-attachments/assets/967544c9-5467-40e9-8a81-270c391130ae" />

<img width="1266" height="547" alt="Halaman Forward Chaining 3 OryzAI" src="https://github.com/user-attachments/assets/0b2dd0af-0d98-44d6-a6bb-cbe25ed34226" />

