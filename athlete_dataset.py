import pandas as pd
import numpy as np

print("=" * 45)
print("       CARDIOLAB")
print("  ATHLETE DATASET ANALYSIS")
print("=" * 45)

# Generate repeatable simulated data
rng = np.random.default_rng(42)

number_of_athletes = 100

# Generate resting heart rates
resting_hr = rng.normal(68, 8, number_of_athletes)
resting_hr = np.clip(resting_hr, 45, 95)

# Generate exercise-ending heart rates
exercise_hr = rng.normal(165, 12, number_of_athletes)
exercise_hr = np.clip(exercise_hr, 135, 195)

# Generate heart-rate recovery amounts
recovery_1 = rng.normal(25, 7, number_of_athletes)
recovery_1 = np.clip(recovery_1, 5, 45)

additional_recovery = rng.normal(15, 5, number_of_athletes)
additional_recovery = np.clip(additional_recovery, 2, 30)

third_recovery = rng.normal(10, 4, number_of_athletes)
third_recovery = np.clip(third_recovery, 1, 25)

# Calculate heart rate after exercise
hr_1min = exercise_hr - recovery_1

hr_2min = hr_1min - additional_recovery

hr_3min = hr_2min - third_recovery

# Create the dataset
data = {
    "Athlete_ID": range(1, number_of_athletes + 1),
    "Resting_HR": resting_hr,
    "Exercise_End_HR": exercise_hr,
    "HR_1_Min": hr_1min,
    "HR_2_Min": hr_2min,
    "HR_3_Min": hr_3min
}

df = pd.DataFrame(data)

# Round measurements
df = df.round(1)

# Calculate recovery
df["Recovery_1_Min"] = (
    df["Exercise_End_HR"] - df["HR_1_Min"]
)

df["Recovery_2_Min"] = (
    df["Exercise_End_HR"] - df["HR_2_Min"]
)

df["Recovery_3_Min"] = (
    df["Exercise_End_HR"] - df["HR_3_Min"]
)

# Display dataset
print("\nFIRST 10 ATHLETES")
print(df.head(10).to_string(index=False))

# Calculate overall statistics
print("\nDATASET STATISTICS")
print("-" * 35)

print(f"Number of athletes: {len(df)}")

print(
    f"Average resting HR: "
    f"{df['Resting_HR'].mean():.1f} bpm"
)

print(
    f"Average exercise-ending HR: "
    f"{df['Exercise_End_HR'].mean():.1f} bpm"
)

print(
    f"Average 1-minute recovery: "
    f"{df['Recovery_1_Min'].mean():.1f} bpm"
)

print(
    f"Average 2-minute recovery: "
    f"{df['Recovery_2_Min'].mean():.1f} bpm"
)

# Save dataset
df.to_csv("athlete_data.csv", index=False)

print("\nDataset saved as athlete_data.csv")
print("\nAnalysis complete!")