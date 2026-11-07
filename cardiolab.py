import pandas as pd
import matplotlib.pyplot as plt

print("=" * 40)
print("     CARDIOLAB")
print(" CARDIOVASCULAR ANALYSIS")
print("=" * 40)

# Example heart rate measurements
heart_rate_data = {
    "Time": ["Exercise End", "1 Minute", "2 Minutes", "3 Minutes"],
    "Heart_Rate": [170, 145, 130, 120]
}

# Create a data table
df = pd.DataFrame(heart_rate_data)

print("\nHEART RATE DATA")
print(df.to_string(index=False))

# Calculate recovery
starting_hr = df.loc[0, "Heart_Rate"]
one_minute_hr = df.loc[1, "Heart_Rate"]
two_minute_hr = df.loc[2, "Heart_Rate"]

recovery_1 = starting_hr - one_minute_hr
recovery_2 = starting_hr - two_minute_hr

three_minute_hr = df.loc[3, "Heart_Rate"]

recovery_3 = starting_hr - three_minute_hr

average_hr = df["Heart_Rate"].mean()
maximum_hr = df["Heart_Rate"].max()
minimum_hr = df["Heart_Rate"].min()

recovery_percentage = (recovery_1 / starting_hr) * 100

print("\nRECOVERY RESULTS")
print(f"1-minute recovery: {recovery_1} bpm")
print(f"2-minute recovery: {recovery_2} bpm")
print(f"3-minute recovery: {recovery_3} bpm")
print(f"Average heart rate: {average_hr:.1f} bpm")
print(f"Maximum heart rate: {maximum_hr} bpm")
print(f"Minimum heart rate: {minimum_hr} bpm")

print(f"1-minute recovery percentage: {recovery_percentage:.1f}%")

# Create a graph
plt.plot(df["Time"], df["Heart_Rate"], marker='o')

plt.title("Heart Rate Recovery")
plt.xlabel("Time")
plt.ylabel("Heart Rate (BPM)")

plt.grid(True)
plt.tight_layout()

plt.savefig("heart_rate_recovery.png")
plt.show()

# Calculate recovery percentages
recovery_percentages = (
    (starting_hr - df["Heart_Rate"]) / starting_hr 
) * 100

# Create a second graph

plt.figure(figsize=(8, 5))

plt.plot(
    df["Time"],
    recovery_percentages,
    marker='o',
)

plt.title("Heart Rate Recovery Percentage")
plt.xlabel("Time")
plt.ylabel("Recovery (%)")

plt.grid(True)
plt.tight_layout()

plt.savefig("recovery_percentage.png")
plt.show()
# COMBINED CARDIOLAB DASHBOARD

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# First graph: Heart rate
axes[0].plot(
    df["Time"],
    df["Heart_Rate"],
    marker="o"
)

axes[0].set_title("Heart Rate Over Time")
axes[0].set_xlabel("Time")
axes[0].set_ylabel("Heart Rate (BPM)")
axes[0].grid(True)

# Second graph: Recovery percentage
axes[1].plot(
    df["Time"],
    recovery_percentages,
    marker="o"
)

axes[1].set_title("Heart Rate Recovery")
axes[1].set_xlabel("Time")
axes[1].set_ylabel("Recovery (%)")
axes[1].grid(True)

# Add dashboard title
fig.suptitle("CARDIOLAB | Cardiovascular Analysis", fontsize=16)

plt.tight_layout()

plt.savefig("cardiolab_dashboard.png")
plt.show()

print("\nAnalysis complete!")