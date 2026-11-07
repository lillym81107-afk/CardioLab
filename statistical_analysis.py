import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("=" * 45)
print("       CARDIOLAB")
print("   STATISTICAL ANALYSIS")
print("=" * 45)

# Load our athlete dataset
df = pd.read_csv("athlete_data.csv")

# Select two variables
resting_hr = df["Resting_HR"]
recovery = df["Recovery_1_Min"]

# Calculate correlation
correlation = resting_hr.corr(recovery)

# Calculate linear regression
slope, intercept = np.polyfit(resting_hr, recovery, 1)

# Calculate R-squared
r_squared = correlation ** 2

print("\nSTATISTICAL RESULTS")
print("-" * 35)

print(f"Correlation: {correlation:.3f}")
print(f"R-squared: {r_squared:.3f}")
print(f"Slope: {slope:.3f}")
print(f"Intercept: {intercept:.3f}")

# Create scatterplot
plt.figure(figsize=(8, 5))

plt.scatter(resting_hr, recovery, label="Athletes")

# Create regression line
predicted = slope * resting_hr + intercept

plt.plot(
    resting_hr,
    predicted,
    label="Regression Line"
)

plt.title("Resting HR vs 1-Minute Recovery")
plt.xlabel("Resting Heart Rate (BPM)")
plt.ylabel("1-Minute Recovery (BPM)")

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("correlation_analysis.png")
plt.show()

print("\nStatistical analysis complete!")