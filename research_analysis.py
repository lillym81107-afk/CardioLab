import pandas as pd
import numpy as np
from scipy.stats import pearsonr

print("=" * 50)
print("          CARDIOLAB RESEARCH")
print("       STATISTICAL REPORT")
print("=" * 50)

# Generate reproducible simulated data
rng = np.random.default_rng(42)

n = 100

resting_hr = rng.normal(68, 8, n)
standardized_hr = (
    resting_hr - resting_hr.mean()
) / resting_hr.std()

positive = 25 + 5 * standardized_hr + rng.normal(0, 2, n)
negative = 25 - 5 * standardized_hr + rng.normal(0, 2, n)
random = 25 + rng.normal(0, 5, n)

datasets = {
    "Positive": positive,
    "Negative": negative,
    "No Relationship": random
}

results = []

for name, recovery in datasets.items():

    correlation, p_value = pearsonr(
        resting_hr,
        recovery
    )

    r_squared = correlation ** 2

    if p_value < 0.05:
        significance = "Statistically significant"
    else:
        significance = "Not statistically significant"

    results.append({
        "Relationship": name,
        "Correlation": round(correlation, 3),
        "R_squared": round(r_squared, 3),
        "P_value": round(p_value, 4),
        "Result": significance
    })

report = pd.DataFrame(results)

print("\nRESEARCH RESULTS")
print(report.to_string(index=False))

report.to_csv("research_report.csv", index=False)

print("\nResearch report saved!")