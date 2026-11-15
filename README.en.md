**English** | [Bahasa Indonesia](README.md)

# Probability of Resignation to Finish GTA VI

Monte Carlo simulation for the satirical research manuscript **"Estimating the Probability That a High-Ranking State Official Resigns to Finish a High-Budget Open-World Game: A Time-to-Completion, Opportunity Cost, and Monte Carlo Simulation Approach"** (original title in Indonesian).

This repository contains the code that produces every number, table, and figure in the manuscript, so the results can be reproduced.

> **Disclosure (parody).** This manuscript is satire written in the style of a scientific journal article. The subject (W) is a hypothetical figure from the "Republic of Antah-Berantah" and does not refer to any real official. The statistical methods, calculations, release dates, game-duration data, and citations are real and traceable; only the premise is a joke. All figures are **model-based estimates under stated assumptions, not empirical probabilities**.

## Summary

A hypothetical vice president (W) considers resigning in order to finish *Grand Theft Auto VI*. The model separates two layers of the decision:

1. **Rational decision under the model** (*P*<sub>D</sub>): whether resigning actually cuts the completion time below W's spoiler tolerance (τ).
2. **Realization** (π): the probability that the decision is actually carried out after passing institutional, political, and social barriers.

Final probability: **P = P<sub>D</sub> · E[π]**.

### Main results

| Quantity | Value |
|---|---|
| Median completion time, stays in office | 17.6 weeks |
| Median completion time, resigns | 1.47 weeks (about 10 days) |
| *P*<sub>D</sub> (rational decision) | 0.7133 (95% Wilson interval: 0.7126–0.7139) |
| *P* (resignation realized) | 0.71% |
| 95% credible interval for *P* | 0.018%–2.60% |
| Range of *P* across all sensitivity scenarios | 0.40%–0.92% |

The final result is driven mainly by institutional barriers (π), not by the length of the game. Among the duration parameters, the most influential are the free-time fraction (*f*), weekly playing hours (*G*<sub>0</sub>), and spoiler tolerance (τ).

## Research questions

- **RQ1.** How long does W take to finish GTA VI if he stays in office compared with if he resigns?
- **RQ2.** How likely is the resignation decision to satisfy the model's rationality criterion (*P*<sub>D</sub>)?
- **RQ3.** How likely is that decision to be realized (*P*), and which parameters determine it most?

## Repository contents

| File | Description |
|---|---|
| `simulation_gta_vi.py` | Single simulation script: calibration, main simulation, analytical verification, sensitivity analysis, and figure generation |
| `Paper_Probabilitas_Pengunduran_Diri_GTA_VI_update.docx` | Full manuscript (latest version, in Indonesian) |
| `output_gta_vi/` | Figures and numerical results from the full simulation; regenerated automatically when the script runs (see Outputs) |
| `requirements.txt` | Required Python packages |
| `LICENSE` | Full text of the CC BY 4.0 license |

## How to run

### Requirements

- Python 3.10 or newer (tested on Python 3.12)
- NumPy, SciPy, and Matplotlib (tested with NumPy 2.5, SciPy 1.18, Matplotlib 3.11)

```bash
pip install -r requirements.txt
```

### Run the full simulation

```bash
python simulation_gta_vi.py
```

Defaults: 2,000,000 main iterations, 1,000,000 iterations per sensitivity scenario, 10,000 bootstrap replicates, and 500,000 draws of π. The random seed is fixed (`20261119`), so results are identical on every run.

### Run a quick version (for testing)

The number of iterations can be changed through environment variables:

```bash
GTA_N_MAIN=100000 GTA_N_SENS=50000 python simulation_gta_vi.py
```

| Environment variable | Purpose | Default |
|---|---|---|
| `GTA_N_MAIN` | Main simulation iterations | 2,000,000 |
| `GTA_N_SENS` | Iterations per sensitivity scenario | 1,000,000 |
| `GTA_N_BOOT` | Bootstrap replicates (duration ratio) | 10,000 |
| `GTA_N_PACT` | Draws of π for the credible interval | 500,000 |

The numbers in the manuscript come from the default settings. The quick version only checks that the script runs, and its numbers will differ slightly.

## Outputs

The script creates an `output_gta_vi/` folder containing:

| File | Content | In the manuscript |
|---|---|---|
| `fig1.png` | Historical durations of Rockstar titles and the GTA VI estimate | Figure 1 |
| `fig2.png` | Distribution of completion time (stays vs resigns) | Figure 2 |
| `fig3.png` | One-at-a-time sensitivity (tornado) diagram | Figure 3 |
| `res.json` | All numerical results (probabilities, percentiles, sensitivity, Spearman correlations) | Tables 4–6 and text |

## Model in brief

```
H         ~ LogNormal(ln M, σ_H²)           hours needed to finish
T_stay     = H / (G0 · f)                   completion time if W stays in office
T_resign   = H / (G0 · k)                   completion time if W resigns
T~_stay    = T_stay / ρ                     completion time as perceived by W
D = 1  if  T~_stay > τ  and  T_resign < τ
P = Pr(D = 1) · E[π],   π ~ Beta(1, 99)
```

### Baseline parameters

| Symbol | Meaning | Baseline | Status |
|---|---|---|---|
| *M* | Median main-story hours of GTA VI | 52.85 h | Data/literature |
| σ<sub>H</sub> | Log-scale dispersion of duration | 0.35 | Assumption |
| *G*<sub>0</sub> | Mean playing hours per week | 12 h | Data/literature |
| *f* | Fraction of *G*<sub>0</sub> available while in office | 0.25 | Assumption |
| *k* | Multiplier of *G*<sub>0</sub> after resigning | 3.0 | Assumption |
| τ | Spoiler tolerance | 6 weeks | Assumption |
| ρ | Ratio of actual to predicted time (planning fallacy) | 1.637 | Data/literature |
| π | Probability of acting | Beta(1, 99), mean 0.01 | Assumption |

Parameters marked **assumption** have no direct empirical basis because the modeled event is hypothetical. Their values are tested over wide ranges in the sensitivity analysis.

## Verification and analysis

- **Analytical verification.** The first condition of the criterion *D* follows a lognormal distribution, so its probability has a closed form, Φ(μ/σ), which is compared with the simulation (0.7526 analytical vs 0.7524 simulated).
- **Three kinds of interval, three sources of uncertainty.** A Wilson interval for the Monte Carlo error of *P*<sub>D</sub>; a bootstrap confidence interval for the duration ratio; and a credible interval for *P* that reflects only the uncertainty in π.
- **One-at-a-time sensitivity** for seven parameters (low and high values), plus E[π] scenarios from 0.001 to 0.10 and Spearman rank correlations.

## Limitations

- Behavioral parameters are assumptions, not measurements.
- The sensitivity analysis is one-at-a-time, so it does not capture interactions between parameters; a global sensitivity analysis is left for future work.
- The product form *P* = *P*<sub>D</sub> · E[π] assumes π is independent of the duration parameters.
- There is no empirical test against the behavior of real officials.

## Key references

Becker (1965) on time allocation; Buehler et al. (1994, 2010) and Kahneman & Tversky (1979) on the planning fallacy; Simon (1955) on bounded rationality; Limpert et al. (2001) and Aitchison & Brown (1957) on the lognormal distribution; Metropolis & Ulam (1949), Law (2007), and Rubinstein & Kroese (2017) on Monte Carlo simulation; Saltelli et al. (2008) and Spearman (1904) on sensitivity analysis. The full list is in the manuscript.

## How to cite

```
Aditiya, D. (2026). Estimasi probabilitas pengunduran diri pejabat tinggi negara
demi menamatkan gim dunia terbuka berbiaya besar: Pendekatan waktu-hingga-tamat,
biaya peluang, dan simulasi Monte Carlo [Preprint, not peer reviewed].
```

## License

Copyright © 2026 Diyas Aditiya.

The manuscript, code, and all contents of this repository are licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/); the full text is in the [LICENSE](LICENSE) file. You are free to share and adapt this material for any purpose, including commercially, as long as you give appropriate credit to the author.

## Contact

Diyas Aditiya, Industrial Engineering Program, diyasgraphs@gmail.com
