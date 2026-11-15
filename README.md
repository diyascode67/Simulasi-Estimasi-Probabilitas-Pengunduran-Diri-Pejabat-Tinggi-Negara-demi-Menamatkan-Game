[English](README.en.md) | **Bahasa Indonesia**

# Probabilitas Pengunduran Diri demi Menamatkan GTA VI

Simulasi Monte Carlo untuk naskah ilmiah satir **"Estimasi Probabilitas Pengunduran Diri Pejabat Tinggi Negara demi Menamatkan Gim Dunia Terbuka Berbiaya Besar: Pendekatan Waktu-hingga-Tamat, Biaya Peluang, dan Simulasi Monte Carlo"**.

Repositori ini memuat kode yang menghasilkan seluruh angka, tabel, dan gambar pada naskah, sehingga hasilnya dapat direproduksi.

> **Catatan keterbukaan (parodi).** Naskah ini adalah karya satir bergaya jurnal ilmiah. Subjek (W) adalah tokoh hipotetis dari "Republik Antah-Berantah" dan tidak merujuk pada pejabat nyata mana pun. Metode statistik, perhitungan, tanggal rilis, data durasi gim, dan sitasi bersifat nyata dan dapat ditelusuri; yang bercanda hanya premisnya. Seluruh angka adalah **estimasi berbasis asumsi model, bukan probabilitas empiris**.

## Ringkasan

Seorang wakil presiden hipotetis (W) menimbang untuk mundur demi menamatkan *Grand Theft Auto VI*. Model memisahkan dua lapis keputusan:

1. **Keputusan rasional menurut model** (*P*<sub>D</sub>): apakah mundur memang memangkas waktu tamat hingga di bawah toleransi bocoran cerita (τ).
2. **Realisasi** (π): peluang keputusan itu benar-benar dieksekusi setelah melewati hambatan institusional, politik, dan sosial.

Probabilitas akhir: **P = P<sub>D</sub> · E[π]**.

### Hasil utama

| Besaran | Nilai |
|---|---|
| Median waktu tamat, tetap menjabat | 17,6 minggu |
| Median waktu tamat, mundur | 1,47 minggu (sekitar 10 hari) |
| *P*<sub>D</sub> (keputusan rasional) | 0,7133 (interval Wilson 95%: 0,7126–0,7139) |
| *P* (pengunduran diri terealisasi) | 0,71% |
| Interval kredibel 95% untuk *P* | 0,018%–2,60% |
| Rentang *P* pada seluruh skenario sensitivitas | 0,40%–0,92% |

Hasil akhir terutama ditentukan oleh hambatan institusional (π), bukan oleh panjang gim. Di antara parameter durasi, yang paling berpengaruh adalah fraksi waktu luang (*f*), jam bermain per minggu (*G*<sub>0</sub>), dan toleransi bocoran cerita (τ).

## Pertanyaan penelitian

- **PP1.** Berapa lama W menamatkan GTA VI jika tetap menjabat dibandingkan jika mundur?
- **PP2.** Seberapa besar probabilitas keputusan mundur memenuhi kriteria rasional model (*P*<sub>D</sub>)?
- **PP3.** Seberapa besar probabilitas keputusan itu terealisasi (*P*), dan parameter mana yang paling menentukannya?

## Isi repositori

| Berkas | Keterangan |
|---|---|
| `simulation_gta_vi.py` | Skrip simulasi tunggal: kalibrasi, simulasi utama, verifikasi analitik, sensitivitas, dan pembuatan gambar |
| `Paper_Probabilitas_Pengunduran_Diri_GTA_VI_update.docx` | Naskah lengkap (versi terbaru) |
| `output_gta_vi/` | Gambar dan hasil numerik dari simulasi penuh; dibuat ulang otomatis saat skrip dijalankan (lihat bagian Keluaran) |
| `requirements.txt` | Daftar pustaka Python yang dibutuhkan |
| `LICENSE` | Teks lengkap lisensi CC BY 4.0 |

## Cara menjalankan

### Prasyarat

- Python 3.10 atau lebih baru (diuji pada Python 3.12)
- NumPy, SciPy, dan Matplotlib (diuji pada NumPy 2.5, SciPy 1.18, Matplotlib 3.11)

```bash
pip install -r requirements.txt
```

### Jalankan simulasi penuh

```bash
python simulation_gta_vi.py
```

Pengaturan bawaan: 2.000.000 iterasi utama, 1.000.000 iterasi per skenario sensitivitas, 10.000 replikasi pengambilan ulang sampel, dan 500.000 sampel π. Benih acak tetap (`20261119`), sehingga hasilnya sama setiap kali dijalankan.

### Jalankan versi cepat (untuk uji coba)

Jumlah iterasi dapat diubah lewat variabel lingkungan:

```bash
GTA_N_MAIN=100000 GTA_N_SENS=50000 python simulation_gta_vi.py
```

| Variabel lingkungan | Fungsi | Bawaan |
|---|---|---|
| `GTA_N_MAIN` | Iterasi simulasi utama | 2.000.000 |
| `GTA_N_SENS` | Iterasi per skenario sensitivitas | 1.000.000 |
| `GTA_N_BOOT` | Replikasi pengambilan ulang sampel (rasio durasi) | 10.000 |
| `GTA_N_PACT` | Sampel π untuk interval kredibel | 500.000 |

Angka pada naskah berasal dari pengaturan bawaan. Versi cepat hanya untuk memeriksa bahwa skrip berjalan, dan angkanya akan sedikit berbeda.

## Keluaran

Skrip membuat folder `output_gta_vi/` berisi:

| Berkas | Isi | Pada naskah |
|---|---|---|
| `fig1.png` | Durasi historis judul Rockstar dan estimasi GTA VI | Gambar 1 |
| `fig2.png` | Distribusi waktu tamat (tetap menjabat vs mundur) | Gambar 2 |
| `fig3.png` | Diagram tornado sensitivitas satu-per-satu | Gambar 3 |
| `res.json` | Seluruh hasil numerik (probabilitas, persentil, sensitivitas, korelasi Spearman) | Tabel 4–6 dan teks |

## Model singkat

```
H        ~ LogNormal(ln M, σ_H²)            jam yang dibutuhkan
T_tinggal = H / (G0 · f)                    waktu tamat jika tetap menjabat
T_mundur  = H / (G0 · k)                    waktu tamat jika mundur
T~_tinggal = T_tinggal / ρ                  waktu tamat yang dipersepsikan W
D = 1  jika  T~_tinggal > τ  dan  T_mundur < τ
P = Pr(D = 1) · E[π],   π ~ Beta(1; 99)
```

### Parameter dasar

| Simbol | Arti | Nilai dasar | Status |
|---|---|---|---|
| *M* | Median jam tamat cerita utama GTA VI | 52,85 jam | Data/literatur |
| σ<sub>H</sub> | Dispersi logaritmik durasi | 0,35 | Asumsi |
| *G*<sub>0</sub> | Rerata jam bermain per minggu | 12 jam | Data/literatur |
| *f* | Fraksi *G*<sub>0</sub> saat menjabat | 0,25 | Asumsi |
| *k* | Pengali *G*<sub>0</sub> setelah mundur | 3,0 | Asumsi |
| τ | Toleransi bocoran cerita | 6 minggu | Asumsi |
| ρ | Rasio waktu aktual terhadap prediksi (kekeliruan perencanaan) | 1,637 | Data/literatur |
| π | Probabilitas bertindak | Beta(1; 99), rerata 0,01 | Asumsi |

Parameter berstatus **asumsi** tidak memiliki dasar empiris langsung karena peristiwa yang dimodelkan bersifat hipotetis. Nilainya diuji pada rentang lebar di analisis sensitivitas.

## Verifikasi dan analisis

- **Verifikasi analitik.** Kondisi pertama pada kriteria *D* mengikuti sebaran lognormal sehingga probabilitasnya dapat dihitung tertutup sebagai Φ(μ/σ); hasilnya dibandingkan dengan simulasi (0,7526 analitik vs 0,7524 simulasi).
- **Tiga jenis interval, tiga sumber ketidakpastian.** Interval Wilson untuk galat Monte Carlo *P*<sub>D</sub>; interval kepercayaan hasil pengambilan ulang sampel untuk rasio durasi; interval kredibel untuk *P* yang hanya mencerminkan ketidakpastian π.
- **Sensitivitas satu-per-satu** untuk tujuh parameter (nilai rendah dan tinggi), ditambah skenario E[π] dari 0,001 sampai 0,10 dan korelasi peringkat Spearman.

## Keterbatasan

- Parameter perilaku adalah asumsi, bukan hasil pengukuran.
- Analisis sensitivitas bersifat satu-per-satu sehingga tidak menangkap interaksi antarparameter; analisis sensitivitas global dapat dilakukan pada penelitian lanjutan.
- Bentuk perkalian *P* = *P*<sub>D</sub> · E[π] mengasumsikan π tidak bergantung pada parameter durasi.
- Tidak ada pengujian empiris terhadap perilaku pejabat nyata.

## Referensi utama

Becker (1965) tentang alokasi waktu; Buehler dkk. (1994, 2010) dan Kahneman & Tversky (1979) tentang kekeliruan perencanaan; Simon (1955) tentang rasionalitas terbatas; Limpert dkk. (2001) dan Aitchison & Brown (1957) tentang sebaran lognormal; Metropolis & Ulam (1949), Law (2007), dan Rubinstein & Kroese (2017) tentang simulasi Monte Carlo; Saltelli dkk. (2008) dan Spearman (1904) tentang analisis sensitivitas. Daftar lengkap ada pada naskah.

## Cara mengutip

```
Aditiya, D. (2026). Estimasi probabilitas pengunduran diri pejabat tinggi negara
demi menamatkan gim dunia terbuka berbiaya besar: Pendekatan waktu-hingga-tamat,
biaya peluang, dan simulasi Monte Carlo [Pracetak, belum ditelaah sejawat].
```

## Lisensi

Hak cipta © 2026 Diyas Aditiya.

Naskah, kode, dan seluruh isi repositori ini dilisensikan di bawah [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/); teks lengkap ada pada berkas [LICENSE](LICENSE). Anda bebas membagikan dan mengadaptasi materi ini untuk tujuan apa pun, termasuk komersial, selama mencantumkan atribusi yang sesuai kepada penulis.

## Kontak

Diyas Aditiya, Program Studi Teknik Industri, diyasgraphs@gmail.com
