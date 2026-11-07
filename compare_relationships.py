import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("=" * 45)
print("       CARDIOLAB")
print("  CORRELATION COMPARISON")
print("=" * 45)

# Generate reproducible simulated data
rng = np.random.default_rng(42)

number_of_athletes = 100

# Generate resting heart rates
resting_hr = rng.normal(68, 8, number_of_athletes)

# Standardize the resting heart rates
standardized_hr = (
    resting_hr - resting_hr.mean()
) / resting_hr.std()

# Create three different relationships

# 1. Positive relationship
positive_recovery = (
    25 + 5 * standardized_hr
    + rng.normal(0, 2, number_of_athletes)
)

# 2. Negative relationship
negative_recovery = (
    25 - 5 * standardized_hr
    + rng.normal(0, 2, number_of_athletes)
)

# 3. No designed relationship
no_relationship = (
    25 + rng.normal(0, 5, number_of_athletes)
)

# Organize the data
df = pd.DataFrame({
    "Resting_HR": resting_hr,
    "Positive": positive_recovery,
    "Negative": negative_recovery,
    "No_Relationship": no_relationship
})

# Calculate correlations
positive_r = df["Resting_HR"].corr(df["Positive"])
negative_r = df["Resting_HR"].corr(df["Negative"])
no_r = df["Resting_HR"].corr(df["No_Relationship"])

print("\nCORRELATION RESULTS")
print("-" * 35)

print(f"Positive correlation: {positive_r:.3f}")
print(f"Negative correlation: {negative_r:.3f}")
print(f"No designed relationship: {no_r:.3f}")

# Create three graphs
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

relationships = [
    ("Positive Relationship", "Positive", positive_r),
    ("Negative Relationship", "Negative", negative_r),
    ("No Designed Relationship", "No_Relationship", no_r)
]

for ax, (title, column, correlation) in zip(
    axes, relationships
):
    x = df["Resting_HR"]
    y = df[column]

    ax.scatter(x, y)

    # Calculate regression line
    slope, intercept = np.polyfit(x, y, 1)

    predicted = slope * x + intercept

    ax.plot(x, predicted)

    ax.set_title(f"{title}\nr = {correlation:.3f}")
    ax.set_xlabel("Resting HR (BPM)")
    ax.set_ylabel("Recovery (BPM)")
    ax.grid(True)

fig.suptitle(
    "CARDIOLAB: Comparing Statistical Relationships"
)

plt.tight_layout()

plt.savefig("relationship_comparison.png")
plt.show()

print("\nComparison complete!")