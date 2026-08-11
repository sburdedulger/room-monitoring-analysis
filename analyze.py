import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load the data
df = pd.read_csv('sensor_log.csv', parse_dates=['timestamp'])

# Convert numeric columns properly (in case of stray strings)
df['temp'] = pd.to_numeric(df['temp'], errors='coerce')
df['humidity'] = pd.to_numeric(df['humidity'], errors='coerce')
df['gas_diff'] = pd.to_numeric(df['gas_diff'], errors='coerce')
df['rain'] = pd.to_numeric(df['rain'], errors='coerce')

# Quick look
print(df.head())
print("\n--- General info ---")
print(df.info())

print("\n--- Summary statistics ---")
print(df.describe())

print(f"\nTotal records: {len(df)}")
print(f"Start: {df['timestamp'].min()}")
print(f"End: {df['timestamp'].max()}")

# --- Plotting ---
fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

axes[0].plot(df['timestamp'], df['temp'], color='tomato')
axes[0].set_ylabel('Temperature (°C)')
axes[0].grid(True, alpha=0.3)

axes[1].plot(df['timestamp'], df['humidity'], color='steelblue')
axes[1].set_ylabel('Humidity (%)')
axes[1].grid(True, alpha=0.3)

axes[2].plot(df['timestamp'], df['gas_diff'], color='seagreen')
axes[2].axhline(y=50, color='red', linestyle='--', alpha=0.5, label='Threshold')
axes[2].axhline(y=-50, color='red', linestyle='--', alpha=0.5)
axes[2].set_ylabel('Gas Diff')
axes[2].set_xlabel('Time')
axes[2].legend()
axes[2].grid(True, alpha=0.3)

for ax in axes:
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('sensor_analysis.png', dpi=150)
print("\nGraph saved as sensor_analysis.png")

plt.savefig('sensor_analysis.png', dpi=150)
print("\nGraph saved as sensor_analysis.png")

# --- Anomaly detection ---
THRESHOLD = 15
anomalies = df[df['gas_diff'].abs() > THRESHOLD].copy()
print(f"\n--- Gas anomaly events (threshold = {THRESHOLD}) ---")
print(f"Total anomalies detected: {len(anomalies)}")
if len(anomalies) > 0:
    anomalies['time_only'] = anomalies['timestamp'].dt.strftime('%H:%M')
    print(anomalies[['time_only', 'gas_raw', 'gas_diff']].to_string(index=False))


print(f"\n--- Rain sensor check ---")
print(f"Rain value range: {df['rain'].min()} - {df['rain'].max()}")
print(f"Rain value std (variation): {df['rain'].std():.2f}")
print(f"Unique rain values: {sorted(df['rain'].unique())}")


# --- Hourly summary ---
print(f"\n--- Hourly summary ---")
df['hour'] = df['timestamp'].dt.hour
hourly = df.groupby('hour').agg(
    avg_temp=('temp', 'mean'),
    avg_humidity=('humidity', 'mean'),
    max_gas_diff=('gas_diff', lambda x: x.abs().max()),
    readings=('temp', 'count')
).round(2)
print(hourly.to_string())

hottest_hour = hourly['avg_temp'].idxmax()
coldest_hour = hourly['avg_temp'].idxmin()
most_humid_hour = hourly['avg_humidity'].idxmax()

print(f"\nHottest hour: {hottest_hour}:00 ({hourly.loc[hottest_hour, 'avg_temp']}°C)")
print(f"Coldest hour: {coldest_hour}:00 ({hourly.loc[coldest_hour, 'avg_temp']}°C)")
print(f"Most humid hour: {most_humid_hour}:00 ({hourly.loc[most_humid_hour, 'avg_humidity']}%)")

hourly.to_csv('hourly_summary.csv')
print("\nHourly summary saved as hourly_summary.csv")

# En sonda goster
plt.show()

# --- Anomaly detection ---
THRESHOLD = 15
anomalies = df[df['gas_diff'].abs() > THRESHOLD].copy()

print(f"\n--- Gas anomaly events (threshold = {THRESHOLD}) ---")
print(f"Total anomalies detected: {len(anomalies)}")

if len(anomalies) > 0:
    anomalies['time_only'] = anomalies['timestamp'].dt.strftime('%H:%M')
    print(anomalies[['time_only', 'gas_raw', 'gas_diff']].to_string(index=False))
else:
    print("No anomalies detected.")

plt.show()

print(f"\n--- Rain sensor check ---")
print(f"Rain value range: {df['rain'].min()} - {df['rain'].max()}")
print(f"Rain value std (variation): {df['rain'].std():.2f}")
print(f"Unique rain values: {sorted(df['rain'].unique())}")


