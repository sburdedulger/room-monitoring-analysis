import serial
import csv
from datetime import datetime

PORT = 'COM8'
BAUD = 9600
CSV_FILE = 'sensor_log.csv'

ser = serial.Serial(PORT, BAUD, timeout=1)

with open(CSV_FILE, mode='a', newline='') as f:
    writer = csv.writer(f)
    if f.tell() == 0:
        writer.writerow(['timestamp', 'temp', 'humidity', 'gas_raw', 'gas_baseline', 'gas_diff', 'rain'])

    print("Logging started... (Ctrl+C to stop)")
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if not line.startswith("Temp:"):
                continue

            # Example line: "Temp: 29.30 Humidity: 44.00 Gas(raw): 594 Baseline: 594.00 Gas(diff): 0 Rain: 24"
            parts = line.replace(":", "").split()
            temp = parts[1]
            humidity = parts[3]
            gas_raw = parts[5]
            baseline = parts[7]
            gas_diff = parts[9]
            rain = parts[11]

            timestamp = datetime.now().isoformat()
            writer.writerow([timestamp, temp, humidity, gas_raw, baseline, gas_diff, rain])
            f.flush()
            print(f"{timestamp} | T:{temp} H:{humidity} Gas:{gas_raw} Rain:{rain}")

        except KeyboardInterrupt:
            print("Stopped.")
            break
        except Exception as e:
            print(f"Error: {e}")