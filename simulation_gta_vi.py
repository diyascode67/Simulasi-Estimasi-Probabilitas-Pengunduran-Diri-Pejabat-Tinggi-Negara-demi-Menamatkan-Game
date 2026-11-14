"""
Estimasi Probabilitas Pengunduran Diri demi Menamatkan GTA VI
Kode simulasi untuk lampiran paper.

Model diselaraskan dengan naskah:
- H, f, k, dan tau dimodelkan dengan distribusi lognormal.
- f menggunakan median 0.25 dan simpangan baku logaritmik 0.50.
- Simulasi utama: 2.000.000 iterasi.
- Analisis sensitivitas: 1.000.000 iterasi per skenario.
- Bootstrap rasio historis: 10.000 replikasi.

Dependensi:
    numpy
    scipy
    matplotlib

Jalankan:
    python simulation_gta_vi.py

Untuk uji cepat:
    GTA_N_MAIN=100000 GTA_N_SENS=50000 python simulation_gta_vi.py
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from scipy.stats import spearmanr


# ============================================================
# 1. KONFIGURASI
# ============================================================

SEED = 20261119

# Environment variables hanya untuk memudahkan uji cepat.
# Nilai default tetap mengikuti naskah paper.
N = int(os.getenv("GTA_N_MAIN", "2000000"))
N_SENS = int(os.getenv("GTA_N_SENS", "1000000"))
N_BOOT = int(os.getenv("GTA_N_BOOT", "10000"))
N_PACT = int(os.getenv("GTA_N_PACT", "500000"))

OUTPUT_DIR = Path("output_gta_vi")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

if min(N, N_SENS, N_BOOT, N_PACT) <= 0:
    raise ValueError("Semua jumlah iterasi harus lebih besar dari nol.")

plt.rcParams["font.family"] = "DejaVu Serif"
plt.rcParams["font.size"] = 10


# ============================================================
# 2. DATA HISTORIS
# ============================================================

titles = [
    "GTA III",
    "GTA Vice City",
    "GTA San Andreas",
    "GTA IV",
    "GTA V",
    "Red Dead Redemption",
    "Red Dead Redemption 2",
]

years = [2001, 2002, 2004, 2008, 2013, 2010, 2018]

main_story = np.array(
    [15.5, 18.0, 30.5, 27.5, 31.5, 17.5, 50.5],
    dtype=float,
)

main_plus_extra = np.array(
    [21.0, 25.5, 46.0, 40.5, 53.0, 26.5, 86.5],
    dtype=float,
)

if len(titles) != len(years) or len(main_story) != len(main_plus_extra):
    raise ValueError("Panjang data historis tidak konsisten.")

if np.any(main_story <= 0) or np.any(main_plus_extra <= 0):
    raise ValueError("Durasi historis harus bernilai positif.")

ratio = main_story / main_plus_extra
rbar = float(ratio.mean())
rsd = float(ratio.std(ddof=1))

# Estimasi pengembang untuk satu permainan penuh GTA VI.
DEVELOPER_ESTIMATE = 80.0

# Median durasi cerita utama GTA VI hasil kalibrasi.
M_MEDIAN = rbar * DEVELOPER_ESTIMATE


# ============================================================
# 3. PARAMETER MODEL DASAR
# ============================================================

base: dict[str, float] = {
    "M": M_MEDIAN,             # Median durasi permainan (jam)
    "sH": 0.35,                # Dispersi logaritmik H
    "G0": 12.0,                # Jam bermain per minggu
    "f": 0.25,                 # Median fraksi waktu luang saat menjabat
    "sf": 0.50,                # Dispersi logaritmik f
    "k": 3.0,                  # Median pengali waktu setelah mundur
    "sk": 0.40,                # Dispersi logaritmik k
    "tau": 6.0,                # Median toleransi spoiler (minggu)
    "st": 0.60,                # Dispersi logaritmik tau
    "rho": 55.5 / 33.9,        # Faktor planning fallacy
    "a": 1.0,                  # Parameter alpha distribusi Beta untuk p_act
    "b": 99.0,                 # Parameter beta distribusi Beta untuk p_act
}


# ============================================================
# 4. VALIDASI PARAMETER
# ============================================================

def validate_parameters(parameters: dict[str, float]) -> None:
    """Memastikan seluruh parameter model valid."""
    required = (
        "M", "sH", "G0", "f", "sf", "k",
        "sk", "tau", "st", "rho", "a", "b",
    )

    for key in required:
        if key not in parameters:
            raise KeyError(f"Parameter {key!r} tidak ditemukan.")
        value = parameters[key]
        if not np.isfinite(value) or value <= 0:
            raise ValueError(
                f"Parameter {key} harus positif dan bernilai finite."
            )

    if not 0 < parameters["f"] < 1:
        raise ValueError("Median f harus berada di antara 0 dan 1.")


validate_parameters(base)


# ============================================================
# 5. FUNGSI SIMULASI MONTE CARLO
# ============================================================

def draw(
    n: int,
    parameters: dict[str, float],
    rng: np.random.Generator,
) -> dict[str, np.ndarray]:
    """
    Menghasilkan sampel Monte Carlo untuk seluruh variabel model.

    Semua parameter H, f, k, dan tau menggunakan parameterisasi
    lognormal dengan median exp(mu_log) dan sigma logaritmik.
    """
    if n <= 0:
        raise ValueError("Jumlah sampel harus lebih besar dari nol.")

    validate_parameters(parameters)

    # Durasi penyelesaian permainan.
    H = rng.lognormal(
        mean=np.log(parameters["M"]),
        sigma=parameters["sH"],
        size=n,
    )

    # Fraksi waktu luang saat masih menjabat.
    # Dipertahankan lognormal agar konsisten dengan formulasi analitik
    # dan hasil yang dilaporkan dalam naskah.
    f = rng.lognormal(
        mean=np.log(parameters["f"]),
        sigma=parameters["sf"],
        size=n,
    )

    # Pengali jam bermain setelah pengunduran diri.
    k = rng.lognormal(
        mean=np.log(parameters["k"]),
        sigma=parameters["sk"],
        size=n,
    )

    # Toleransi terhadap spoiler.
    tau = rng.lognormal(
        mean=np.log(parameters["tau"]),
        sigma=parameters["st"],
        size=n,
    )

    # Waktu penyelesaian ketika tetap menjabat.
    T_stay = H / (parameters["G0"] * f)

    # Waktu penyelesaian setelah mengundurkan diri.
    T_withdraw = H / (parameters["G0"] * k)

    # Waktu penyelesaian yang dipersepsikan setelah koreksi
    # planning fallacy.
    T_perceived = T_stay / parameters["rho"]

    # Kriteria keputusan:
    # (1) waktu persepsian saat menjabat melebihi toleransi spoiler;
    # (2) waktu setelah mundur lebih kecil dari toleransi spoiler.
    condition_1 = T_perceived > tau
    condition_2 = T_withdraw < tau
    decision = condition_1 & condition_2

    return {
        "H": H,
        "f": f,
        "k": k,
        "tau": tau,
        "T_stay": T_stay,
        "T_withdraw": T_withdraw,
        "T_perceived": T_perceived,
        "condition_1": condition_1,
        "condition_2": condition_2,
        "decision": decision,
    }


# ============================================================
# 6. SIMULASI UTAMA
# ============================================================

rng = np.random.default_rng(SEED)
sim = draw(N, base, rng)

H = sim["H"]
f = sim["f"]
k = sim["k"]
tau = sim["tau"]

T_stay = sim["T_stay"]
T_withdraw = sim["T_withdraw"]
T_perceived = sim["T_perceived"]

condition_1 = sim["condition_1"]
condition_2 = sim["condition_2"]
decision = sim["decision"]

# Probabilitas keputusan mundur berdasarkan dua kriteria model.
P_D = float(decision.mean())

# Probabilitas tindakan aktual memiliki prior Beta(1, 99).
p_act_mean = base["a"] / (base["a"] + base["b"])

# Nilai harapan probabilitas pengunduran diri terealisasi.
P_final_expected = P_D * p_act_mean

# Simulasi Bernoulli tambahan menggunakan nilai harapan p_act.
# Ini mengestimasi nilai harapan, bukan ketidakpastian prior global.
act_rng = np.random.default_rng(SEED + 10)
act = act_rng.random(N) < p_act_mean
P_final_simulated = float((decision & act).mean())

# Standard error Monte Carlo untuk estimasi P_D.
P_D_mc_se = float(np.sqrt(P_D * (1.0 - P_D) / N))


# ============================================================
# 7. INTERVAL KREDIBEL PENGUNDURAN DIRI TEREALISASI
# ============================================================

# p_act diperlakukan sebagai satu probabilitas global yang tidak pasti.
# Sampel Beta ditransformasikan dengan mengalikan P_D.
pact_rng = np.random.default_rng(SEED + 20)
p_act_draws = pact_rng.beta(
    base["a"],
    base["b"],
    size=N_PACT,
)

P_final_draws = P_D * p_act_draws

P_final_low, P_final_median, P_final_high = np.percentile(
    P_final_draws,
    [2.5, 50.0, 97.5],
)


# ============================================================
# 8. KONDISI KEPUTUSAN DAN VERIFIKASI ANALITIK
# ============================================================

P1_simulated = float(condition_1.mean())
P2_simulated = float(condition_2.mean())

# Karena H, f, dan tau dimodelkan lognormal independen,
# log(T_perceived / tau) berdistribusi normal.
mu_1 = (
    np.log(base["M"])
    - np.log(base["G0"])
    - np.log(base["f"])
    - np.log(base["rho"])
    - np.log(base["tau"])
)

sigma_1 = np.sqrt(
    base["sH"] ** 2
    + base["sf"] ** 2
    + base["st"] ** 2
)

# P(T_perceived > tau) = Phi(mu_1 / sigma_1).
# Menggunakan scipy.special.ndtr untuk CDF normal standar.
from scipy.special import ndtr

P1_analytic = float(ndtr(mu_1 / sigma_1))

# Untuk kondisi kedua:
# log(T_withdraw / tau) berdistribusi normal.
mu_2 = (
    np.log(base["M"])
    - np.log(base["G0"])
    - np.log(base["k"])
    - np.log(base["tau"])
)

sigma_2 = np.sqrt(
    base["sH"] ** 2
    + base["sk"] ** 2
    + base["st"] ** 2
)

# P(T_withdraw < tau) = Phi(-mu_2 / sigma_2).
P2_analytic = float(ndtr(-mu_2 / sigma_2))

assert np.all(decision == (condition_1 & condition_2))
assert np.all(H > 0)
assert np.all(f > 0)
assert np.all(k > 0)
assert np.all(tau > 0)


# ============================================================
# 9. STATISTIK WAKTU PENYELESAIAN
# ============================================================

def quantiles(values: np.ndarray) -> np.ndarray:
    """Menghitung persentil 2,5; 50; dan 97,5."""
    return np.percentile(values, [2.5, 50.0, 97.5])


statistics = {
    "H": quantiles(H),
    "T_stay": quantiles(T_stay),
    "T_perceived": quantiles(T_perceived),
    "T_withdraw": quantiles(T_withdraw),
}

P_stay_over_8 = float((T_stay > 8).mean())
P_stay_over_52 = float((T_stay > 52).mean())
median_withdraw_days = float(np.median(T_withdraw) * 7)


# ============================================================
# 10. ANALISIS SENSITIVITAS
# ============================================================

def calculate_PD_for(
    parameter_name: str | None = None,
    parameter_value: float | None = None,
    seed: int = 7,
) -> float:
    """
    Menghitung P(D) untuk satu skenario sensitivitas.

    Seed yang sama digunakan pada setiap skenario agar perbandingan
    lebih stabil melalui common random numbers.
    """
    parameters = dict(base)

    if parameter_name is not None:
        if parameter_value is None:
            raise ValueError("Nilai parameter harus diberikan.")
        parameters[parameter_name] = float(parameter_value)

    local_rng = np.random.default_rng(seed)
    result = draw(N_SENS, parameters, local_rng)
    return float(result["decision"].mean())


P_D_sensitivity_baseline = calculate_PD_for()

# Rentang parameter mengikuti Tabel 4 pada naskah.
sensitivity_parameters = {
    "Median jam tamat M (jam)": ("M", 40.0, 80.0),
    "Dispersi logaritmik sigma H": ("sH", 0.20, 0.60),
    "Jam bermain per minggu G0": ("G0", 8.45, 26.56),
    "Fraksi waktu luang f": ("f", 0.10, 0.50),
    "Toleransi spoiler tau (minggu)": ("tau", 3.0, 12.0),
    "Faktor planning fallacy rho": ("rho", 1.0, 2.0),
}

sensitivity_rows: list[dict[str, Any]] = []

for name, (parameter, low_value, high_value) in sensitivity_parameters.items():
    P_low = calculate_PD_for(parameter, low_value)
    P_high = calculate_PD_for(parameter, high_value)

    sensitivity_rows.append(
        {
            "name": name,
            "parameter": parameter,
            "low_value": low_value,
            "high_value": high_value,
            "PD_low": P_low,
            "PD_high": P_high,
        }
    )


# ============================================================
# 11. SENSITIVITAS PROBABILITAS BERTINDAK
# ============================================================

p_act_sensitivity_values = [0.001, 0.005, 0.010, 0.050, 0.100]

p_act_sensitivity_rows = [
    {
        "E_p_act": value,
        "P_final": P_D_sensitivity_baseline * value,
    }
    for value in p_act_sensitivity_values
]


# ============================================================
# 12. KORELASI PERINGKAT SPEARMAN
# ============================================================

# Margin laten kondisi pertama:
# ln(T_perceived) - ln(tau).
margin_1 = np.log(T_perceived / tau)

# Margin laten kondisi kedua:
# ln(tau) - ln(T_withdraw).
margin_2 = np.log(tau / T_withdraw)

sample_size = min(200_000, N)

spearman_results = {
    "tau_condition1": float(
        spearmanr(
            tau[:sample_size],
            margin_1[:sample_size],
        ).statistic
    ),
    "f_condition1": float(
        spearmanr(
            f[:sample_size],
            margin_1[:sample_size],
        ).statistic
    ),
    "H_condition1": float(
        spearmanr(
            H[:sample_size],
            margin_1[:sample_size],
        ).statistic
    ),
}


# ============================================================
# 13. BOOTSTRAP RASIO HISTORIS
# ============================================================

bootstrap_rng = np.random.default_rng(SEED + 1)

bootstrap_means = np.empty(N_BOOT, dtype=float)

for i in range(N_BOOT):
    bootstrap_sample = bootstrap_rng.choice(
        ratio,
        size=len(ratio),
        replace=True,
    )
    bootstrap_means[i] = bootstrap_sample.mean()

ratio_ci_low, ratio_ci_high = np.percentile(
    bootstrap_means,
    [2.5, 97.5],
)

M_bootstrap_interval = (
    ratio_ci_low * DEVELOPER_ESTIMATE,
    ratio_ci_high * DEVELOPER_ESTIMATE,
)


# ============================================================
# 14. INTERVAL KEPERCAYAAN WILSON UNTUK P_D
# ============================================================

z_value = 1.96
n_value = N
p_hat = P_D

denominator = 1.0 + (z_value**2 / n_value)

wilson_center = (
    p_hat + (z_value**2 / (2.0 * n_value))
) / denominator

wilson_half_width = (
    z_value
    * np.sqrt(
        (p_hat * (1.0 - p_hat) / n_value)
        + (z_value**2 / (4.0 * n_value**2))
    )
    / denominator
)

wilson_low = wilson_center - wilson_half_width
wilson_high = wilson_center + wilson_half_width


# ============================================================
# 15. FIGURE 1: PERBANDINGAN DURASI HISTORIS
# ============================================================

fig, ax = plt.subplots(figsize=(9, 4.5))

x = np.arange(len(titles) + 1)
labels = titles + ["GTA VI\n(estimasi pengembang)"]

ax.bar(
    x[:-1] - 0.2,
    main_story,
    0.4,
    label="Cerita utama",
    color="#4a6fa5",
)

ax.bar(
    x[:-1] + 0.2,
    main_plus_extra,
    0.4,
    label="Utama + ekstra",
    color="#c9a227",
)

ax.bar(
    x[-1],
    DEVELOPER_ESTIMATE,
    0.4,
    label="Estimasi pengembang",
    color="#b5412b",
    hatch="//",
)

ax.axhline(
    M_MEDIAN,
    color="#4a6fa5",
    linestyle="--",
    linewidth=1,
)

ax.text(
    0.02,
    M_MEDIAN + 2,
    f"Estimasi median cerita utama M = {M_MEDIAN:.2f} jam",
    color="#4a6fa5",
    fontsize=8,
)

ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=8)
ax.set_ylabel("Durasi (jam)")
ax.set_title("Durasi Permainan Historis Rockstar")
ax.legend(fontsize=8, frameon=False)
ax.spines[["top", "right"]].set_visible(False)

fig.tight_layout()
fig.savefig(OUTPUT_DIR / "fig1.png", dpi=220)
plt.close(fig)


# ============================================================
# 16. FIGURE 2: DISTRIBUSI WAKTU PENYELESAIAN
# ============================================================

fig, ax = plt.subplots(figsize=(8, 4.5))

bins = np.logspace(
    np.log10(0.3),
    np.log10(400),
    80,
)

plot_n = min(500_000, N)

ax.hist(
    T_stay[:plot_n],
    bins=bins,
    alpha=0.65,
    label="Tetap menjabat",
    density=True,
    color="#4a6fa5",
)

ax.hist(
    T_withdraw[:plot_n],
    bins=bins,
    alpha=0.65,
    label="Mengundurkan diri",
    density=True,
    color="#b5412b",
)

ax.set_xscale("log")

ax.axvline(
    np.median(T_stay),
    color="#4a6fa5",
    linestyle="--",
)

ax.axvline(
    np.median(T_withdraw),
    color="#b5412b",
    linestyle="--",
)

ax.set_xlabel("Waktu penyelesaian (minggu, skala logaritmik)")
ax.set_ylabel("Kepadatan probabilitas")
ax.set_title("Distribusi Waktu Penyelesaian")
ax.legend(fontsize=8, frameon=False)
ax.spines[["top", "right"]].set_visible(False)

fig.tight_layout()
fig.savefig(OUTPUT_DIR / "fig2.png", dpi=220)
plt.close(fig)


# ============================================================
# 17. FIGURE 3: TORNADO SENSITIVITY
# ============================================================

sorted_rows = sorted(
    sensitivity_rows,
    key=lambda row: abs(row["PD_high"] - row["PD_low"]),
)

fig, ax = plt.subplots(figsize=(8, 5))

for i, row in enumerate(sorted_rows):
    low_probability = row["PD_low"]
    high_probability = row["PD_high"]

    ax.barh(
        i,
        low_probability - P_D_sensitivity_baseline,
        left=P_D_sensitivity_baseline,
        color="#4a6fa5",
        height=0.55,
    )

    ax.barh(
        i,
        high_probability - P_D_sensitivity_baseline,
        left=P_D_sensitivity_baseline,
        color="#c9a227",
        height=0.55,
    )

ax.axvline(
    P_D_sensitivity_baseline,
    color="black",
    linewidth=0.9,
)

ax.set_yticks(range(len(sorted_rows)))
ax.set_yticklabels(
    [row["name"] for row in sorted_rows],
    fontsize=8,
)

ax.set_xlabel("Probabilitas keputusan mundur P(D)")
ax.set_title("Analisis Sensitivitas One-at-a-Time")
ax.set_xlim(0, 1)

ax.legend(
    handles=[
        Patch(color="#4a6fa5", label="Nilai parameter rendah"),
        Patch(color="#c9a227", label="Nilai parameter tinggi"),
    ],
    fontsize=8,
    frameon=False,
)

ax.spines[["top", "right"]].set_visible(False)

fig.tight_layout()
fig.savefig(OUTPUT_DIR / "fig3.png", dpi=220)
plt.close(fig)


# ============================================================
# 18. EKSPOR HASIL KE JSON
# ============================================================

results = {
    "metadata": {
        "seed": SEED,
        "iterations_main": N,
        "iterations_sensitivity_per_scenario": N_SENS,
        "bootstrap_iterations": N_BOOT,
        "p_act_draws": N_PACT,
    },
    "historical": {
        "titles": titles,
        "years": years,
        "main_story_hours": main_story.tolist(),
        "main_plus_extra_hours": main_plus_extra.tolist(),
        "ratios": ratio.tolist(),
        "ratio_mean": rbar,
        "ratio_sd": rsd,
        "ratio_bootstrap_95_ci": [
            float(ratio_ci_low),
            float(ratio_ci_high),
        ],
        "M_median_hours": float(M_MEDIAN),
        "M_bootstrap_95_interval_hours": [
            float(M_bootstrap_interval[0]),
            float(M_bootstrap_interval[1]),
        ],
    },
    "probability": {
        "P_D": P_D,
        "P_D_monte_carlo_se": P_D_mc_se,
        "P_D_wilson_95_ci": [
            float(wilson_low),
            float(wilson_high),
        ],
        "P_final_expected": float(P_final_expected),
        "P_final_simulated": P_final_simulated,
        "P_final_credible_95_interval": [
            float(P_final_low),
            float(P_final_high),
        ],
        "p_act_prior_mean": float(p_act_mean),
    },
    "conditions": {
        "P_condition1_simulated": P1_simulated,
        "P_condition1_analytic": P1_analytic,
        "P_condition2_simulated": P2_simulated,
        "P_condition2_analytic": P2_analytic,
    },
    "parameters": base,
    "time_statistics": {
        key: [float(value) for value in values]
        for key, values in statistics.items()
    },
    "time_probabilities": {
        "P_T_stay_over_8_weeks": P_stay_over_8,
        "P_T_stay_over_52_weeks": P_stay_over_52,
        "median_T_withdraw_days": median_withdraw_days,
    },
    "sensitivity": sensitivity_rows,
    "p_act_sensitivity": p_act_sensitivity_rows,
    "spearman": spearman_results,
}

with (OUTPUT_DIR / "res.json").open("w", encoding="utf-8") as file:
    json.dump(
        results,
        file,
        indent=4,
        ensure_ascii=False,
    )


# ============================================================
# 19. RINGKASAN HASIL
# ============================================================

print("\n========== HISTORICAL DATA ==========")
print("Ratios:", np.round(ratio, 4))
print("Mean ratio:", round(rbar, 4))
print("SD ratio:", round(rsd, 4))
print("Estimated median game hours:", round(M_MEDIAN, 4))
print(
    "Bootstrap 95% interval for M:",
    np.round(M_bootstrap_interval, 4),
)

print("\n========== MAIN SIMULATION ==========")
print("P(D):", round(P_D, 6))
print("P(final) expected:", round(P_final_expected, 6))
print("P(final) simulated:", round(P_final_simulated, 6))
print("P(D) Monte Carlo SE:", round(P_D_mc_se, 8))
print("Wilson 95% CI:", wilson_low, wilson_high)

print("\n========== P_FINAL UNCERTAINTY ==========")
print("Mean p_act:", p_act_mean)
print("Median P_final:", P_final_median)
print("P_final 95% credible interval:", P_final_low, P_final_high)

print("\n========== CONDITIONS ==========")
print("P(T_perceived > tau), simulated:", P1_simulated)
print("P(T_perceived > tau), analytic:", P1_analytic)
print("P(T_withdraw < tau), simulated:", P2_simulated)
print("P(T_withdraw < tau), analytic:", P2_analytic)
print("P(D):", P_D)

print("\n========== TIME STATISTICS ==========")
for name, values in statistics.items():
    print(name, np.round(values, 3))

print("Mean T_stay:", T_stay.mean())
print("Mean T_withdraw:", T_withdraw.mean())
print("P(T_stay > 8 weeks):", P_stay_over_8)
print("P(T_stay > 52 weeks):", P_stay_over_52)
print("Median T_withdraw (days):", median_withdraw_days)

print("\n========== SENSITIVITY ==========")
for row in sensitivity_rows:
    print(
        row["name"],
        "| Low:", row["low_value"],
        "| P(D) low:", round(row["PD_low"], 5),
        "| High:", row["high_value"],
        "| P(D) high:", round(row["PD_high"], 5),
    )

print("Sensitivity baseline P(D):", P_D_sensitivity_baseline)

print("\n========== P_ACT SENSITIVITY ==========")
for row in p_act_sensitivity_rows:
    print(
        "E[p_act]:",
        row["E_p_act"],
        "| P_final:",
        row["P_final"],
    )

print("\n========== SPEARMAN ==========")
print(spearman_results)

print("\n====================================")
print("SIMULATION COMPLETED SUCCESSFULLY")
print("====================================")
print("Generated files:")
print("-", OUTPUT_DIR / "fig1.png")
print("-", OUTPUT_DIR / "fig2.png")
print("-", OUTPUT_DIR / "fig3.png")
print("-", OUTPUT_DIR / "res.json")
print("\nFinal P(D):", P_D)
print("Final P_final expected:", P_final_expected)
print(
    "Final P_final 95% CrI:",
    P_final_low,
    P_final_high,
)
print("====================================")
