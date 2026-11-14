# Estimasi Probabilitas Pengunduran Diri untuk Menamatkan GTA VI
### Monte Carlo Simulation of a Hypothetical Resignation Decision

---

## 🇮🇩 Bahasa Indonesia

### Deskripsi Proyek

Proyek ini merupakan simulasi Monte Carlo untuk mengestimasi probabilitas seorang wakil presiden hipotetis mengundurkan diri dari jabatannya demi menyelesaikan permainan *Grand Theft Auto VI (GTA VI)*.

Model ini membandingkan waktu yang tersedia untuk bermain jika tetap menjabat dengan waktu yang tersedia setelah mengundurkan diri. Simulasi menggunakan distribusi lognormal untuk memodelkan durasi permainan, koreksi *planning fallacy* berdasarkan penelitian Buehler dkk. (1994), serta analisis sensitivitas untuk mengevaluasi pengaruh berbagai parameter terhadap hasil akhir.

Penelitian ini bersifat hipotetis dan menggunakan sejumlah asumsi perilaku yang dinyatakan secara eksplisit.

### Metodologi

Simulasi menggunakan beberapa pendekatan statistik:

- **Monte Carlo Simulation:** Menghasilkan 2.000.000 iterasi untuk estimasi utama.
- **Lognormal Distribution:** Memodelkan ketidakpastian durasi penyelesaian permainan.
- **Planning Fallacy Correction:** Mengoreksi estimasi waktu berdasarkan rasio waktu aktual terhadap prediksi.
- **Sensitivity Analysis:** Menguji perubahan hasil berdasarkan variasi parameter model.
- **Bootstrap Analysis:** Mengevaluasi ketidakpastian rasio durasi permainan berdasarkan data historis.

### Teknologi yang Digunakan

- Python
- NumPy
- SciPy
- Matplotlib

### Instalasi

Pastikan Python telah terpasang, kemudian instal dependensi:

```bash
pip install numpy scipy matplotlib
```

### Menjalankan Sim
