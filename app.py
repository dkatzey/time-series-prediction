from flask import Flask, request, render_template
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse input data
        if request.is_json:  # Check if the request is JSON
            data = request.get_json()
            values = data.get("values")  # Extract "values" from JSON
            steps = data.get("steps", 5)  # Default to 5 steps
        else:
            # Handle form data (optional fallback)
            values = request.form.get("values")
            if values:
                values = [float(x) for x in values.split(",")]
            steps = int(request.form.get("steps", 5))

        # Validate input
        if not values:
            return render_template("error.html", error_message="Input values are required.")

        # Ensure "values" is a list of numbers
        if not isinstance(values, list) or not all(isinstance(x, (int, float)) for x in values):
            return render_template("error.html", error_message="Invalid input format for 'values'.")

        # Time series prediction
        time_series = pd.Series(values)
        model = ARIMA(time_series, order=(1, 1, 1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=steps)

        # Plot results
        plt.figure(figsize=(10, 6))
        plt.plot(time_series, label="Observed", marker='o')
        plt.plot(range(len(time_series), len(time_series) + steps), forecast, label="Forecast", marker='o')
        plt.title("Time Series Forecast")
        plt.xlabel("Time")
        plt.ylabel("Value")
        plt.legend()

        # Save plot as a base64 string
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        # Render the HTML page with results
        return render_template("results.html", plot_url=plot_url, forecast=forecast.tolist())
    except Exception as e:
        return render_template("error.html", error_message=str(e))

@app.route('/health', methods=['GET'])
def health_check():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

