from flask import Flask, render_template, request
from weather_api import get_weather, get_historical_weather
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend suitable for scripts
import matplotlib.pyplot as plt
import pandas as pd
import os

static_dir = os.path.join(os.path.dirname(__file__), 'static')
os.makedirs(static_dir, exist_ok=True)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    table = None
    city = ""
    
    if request.method == "POST":
        city = request.form["city"]

        # 1. Get real-time weather
        weather = get_weather(city)

        # 2. Get 10 days of historical weather
        df = get_historical_weather(city, "2024-06-01", "2024-06-10")

        if isinstance(df, pd.DataFrame):
            # 3. Generate line chart
            plt.figure(figsize=(10, 4))
            plt.plot(df["date"], df["temperature_2m_max"], label="Max Temp", color="red", marker="o")
            plt.plot(df["date"], df["temperature_2m_min"], label="Min Temp", color="blue", marker="o")
            plt.title(f"Temperature in {city}")
            plt.xlabel("Date")
            plt.ylabel("°C")
            plt.legend()
            plt.tight_layout()

            # Ensure static folder exists
            os.makedirs(os.path.join(app.root_path, "static"), exist_ok=True)

            # Save plot to static/
            plot_path = os.path.join(static_dir, 'plot.png')
            plt.savefig(plot_path)
            plt.close()

            # 4. Build table with summary
            avg_max = df["temperature_2m_max"].mean()
            std_max = df["temperature_2m_max"].std()
            avg_min = df["temperature_2m_min"].mean()
            std_min = df["temperature_2m_min"].std()

            summary_row = {
                "date": "Avg ± Std",
                "temperature_2m_max": f"{avg_max:.2f} ± {std_max:.2f}",
                "temperature_2m_min": f"{avg_min:.2f} ± {std_min:.2f}",
                "city": df["city"][0]
            }

            table_df = df[["date", "temperature_2m_max", "temperature_2m_min", "city"]].copy()
            summary_df = pd.DataFrame([summary_row])
            table = pd.concat([table_df, summary_df], ignore_index=True).to_dict(orient="records")

    return render_template("index.html", weather=weather, table=table, city=city)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=10000)