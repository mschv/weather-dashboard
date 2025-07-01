import pandas as pd
import matplotlib.pyplot as plt
from weather_api import get_historical_weather

df = get_historical_weather("Ithaca", "2024-06-01", "2024-06-10")

plt.figure(figsize=(10,5))
plt.plot(df["date"],df["temperature_2m_max"],label="Max Temp (°C)", color="tomato",marker="o")
plt.plot(df["date"], df["temperature_2m_min"], label="Min Temp (°C)", color="royalblue", marker="o")

# Labels and title
plt.title(f"Daily Temperatures in {df['city'][0]}")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

# Show the plot
plt.show()

# Summary stats
avg_max = df["temperature_2m_max"].mean()
std_max = df["temperature_2m_max"].std()
avg_min = df["temperature_2m_min"].mean()
std_min = df["temperature_2m_min"].std()

summary_row = {
    "date": "Average / Std",
    "temperature_2m_max": f"{avg_max:.2f} ± {std_max:.2f}",
    "temperature_2m_min": f"{avg_min:.2f} ± {std_min:.2f}",
    "city": df['city'][0]
}

# Create printable DataFrame
table_df = df[["date", "temperature_2m_max", "temperature_2m_min", "city"]].copy()
summary_df = pd.DataFrame([summary_row])
table_df = pd.concat([table_df, summary_df], ignore_index=True)

# Print as table
print("\n🌡️ Daily Temperature Table:\n")
print(table_df.to_string(index=False))


