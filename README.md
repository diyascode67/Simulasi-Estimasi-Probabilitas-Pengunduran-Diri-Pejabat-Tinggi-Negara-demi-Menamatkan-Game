# Estimating the Probability of Resigning to Finish GTA VI

A Monte Carlo simulation study exploring a hypothetical question: what is the probability that a vice president would resign from office to finish *Grand Theft Auto VI*?

This project models the trade-off between time availability while holding public office and the increased gaming time potentially available after resignation.

## Research Overview

The simulation uses historical playtime data from seven Rockstar Games titles to calibrate the estimated main-story completion time of GTA VI. It incorporates the planning fallacy through a correction factor based on Buehler, Griffin, and Ross (1994).

The model evaluates two conditions:

1. Whether the perceived completion time while remaining in office exceeds the acceptable spoiler-tolerance period.
2. Whether the completion time after resignation falls within that period.

A resignation decision is considered feasible when both conditions are satisfied.

## Methodology

- **Simulation method:** Monte Carlo
- **Main simulation:** 2,000,000 iterations
- **Sensitivity analysis:** 1,000,000 iterations per scenario
- **Bootstrap:** 10,000 replications
- **Random seed:** 20261119
- **Distributions:** Lognormal and Beta
- **Statistical analysis:** Spearman rank correlation and sensitivity analysis

## Technologies

- Python
- NumPy
- SciPy
- Matplotlib

## Installation

Install the required dependencies:

```bash
pip install numpy scipy matplotlib
```

## Usage

Run the simulation:

```bash
python simulation_gta_vi.py
```

For a quicker test run:

```bash
GTA_N_MAIN=100000 GTA_N_SENS=50000 python simulation_gta_vi.py
```

## Output

The simulation generates an `output_gta_vi/` directory containing:

- `fig1.png` – Historical Rockstar game duration comparison.
- `fig2.png` – Distribution of estimated completion times.
- `fig3.png` – One-at-a-time sensitivity analysis.
- `res.json` – Numerical simulation results and model parameters.

## Disclaimer

This project is a hypothetical quantitative modeling exercise. All behavioral parameters are explicit modeling assumptions rather than empirical measurements of an actual political figure.

The results should be interpreted as outputs of the specified model, not as predictions of real-world political behavior.

## Reproducibility

The random seed and simulation parameters are specified in the source code to support reproducibility.

## License

See the repository license for usage and redistribution terms.
