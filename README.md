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

### Menjalankan Simulasi

Jalankan program utama menggunakan:

```bash
python simulation_gta_vi.py
```

Untuk menjalankan simulasi dengan jumlah iterasi lebih kecil melalui PowerShell:

```powershell
$env:GTA_N_MAIN="100000"
$env:GTA_N_SENS="50000"
python simulation_gta_vi.py
```

### Output

Hasil simulasi akan disimpan dalam folder `output_gta_vi`, yang berisi:

| File | Deskripsi |
|---|---|
| `fig1.png` | Visualisasi hasil simulasi utama |
| `fig2.png` | Visualisasi analisis sensitivitas |
| `fig3.png` | Visualisasi analisis tambahan |
| `res.json` | Ringkasan hasil simulasi dalam format JSON |

### Reproducibility

Untuk menjaga konsistensi hasil, simulasi menggunakan random seed `20261119`. Jumlah iterasi dapat disesuaikan melalui environment variables yang tersedia.

### Catatan

Penelitian ini merupakan eksperimen pemodelan probabilistik hipotetis. Hasil simulasi tidak dimaksudkan untuk memprediksi atau menggambarkan keputusan pejabat publik yang sebenarnya.

---

## 🇬🇧 English

### Project Overview

This project presents a Monte Carlo simulation designed to estimate the probability of a hypothetical vice president resigning from office to finish *Grand Theft Auto VI (GTA VI)*.

The model compares the available gaming time under two scenarios: remaining in office and resigning. It incorporates a lognormal distribution to model game completion time, a *planning fallacy* correction based on Buehler et al. (1994), and sensitivity analysis to evaluate how different parameters influence the final results.

This research is hypothetical and relies on explicitly stated behavioral assumptions.

### Methodology

The simulation incorporates several statistical approaches:

- **Monte Carlo Simulation:** Performs 2,000,000 iterations for the main estimation.
- **Lognormal Distribution:** Models uncertainty in game completion time.
- **Planning Fallacy Correction:** Adjusts estimated completion time using the ratio of actual to predicted task duration.
- **Sensitivity Analysis:** Examines how variations in model parameters affect the results.
- **Bootstrap Analysis:** Evaluates uncertainty in game-duration ratios using historical data.

### Technologies

- Python
- NumPy
- SciPy
- Matplotlib

### Installation

Make sure Python is installed, then install the required dependencies:

```bash
pip install numpy scipy matplotlib
```

### Running the Simulation

Run the main simulation using:

```bash
python simulation_gta_vi.py
```

To run the simulation with a smaller number of iterations in PowerShell:

```powershell
$env:GTA_N_MAIN="100000"
$env:GTA_N_SENS="50000"
python simulation_gta_vi.py
```

### Output

Simulation results are saved in the `output_gta_vi` directory:

| File | Description |
|---|---|
| `fig1.png` | Main simulation visualization |
| `fig2.png` | Sensitivity analysis visualization |
| `fig3.png` | Additional analysis visualization |
| `res.json` | Simulation results summary in JSON format |

### Reproducibility

A random seed of `20261119` is used to ensure reproducibility. The number of iterations can be adjusted through the available environment variables.

### Disclaimer

This project is a hypothetical probabilistic modeling experiment. Its results are not intended to predict or represent the actual decisions of any public official.

---

**Author:** Diyas Aditiya  
**Institution:** Universitas Singaperbangsa Karawang
