from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load the trained sales prediction model
model = joblib.load('sales_prediction_model.joblib')

# Load historical sales data (from CSV or database)
historical_sales = pd.read_csv('data/sales_train.csv')
shops = pd.read_csv('data/shops.csv')

# Generate lag features for model input
def create_lag_features(data, lags=3):
    for lag in range(1, lags + 1):
        data[f'item_cnt_month_lag_{lag}'] = data['item_cnt_month'].shift(lag)
    return data.dropna()

# Prediction for a selected shop over a time window
def predict_sales_for_time_window(shop_id, months_to_predict):
    # Filter sales for the selected shop
    shop_data = historical_sales[historical_sales['shop_id'] == shop_id]

    # Create lag features based on past data
    shop_data_with_lags = create_lag_features(shop_data)

    predictions = []
    for month in range(1, months_to_predict + 1):
        # Predict sales using the trained model
        predicted_sales = model.predict(shop_data_with_lags.drop(columns=['item_cnt_month']))
        predictions.append({
            'month': month,
            'predicted_sales': predicted_sales.sum()  # Sum sales predictions across all items for that shop
        })

    return predictions

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_sales():
    try:
        input_data = request.json
        shop_id = int(input_data['shop_id'])
        months_to_predict = int(input_data['months_to_predict'])

        # Call prediction function
        predictions = predict_sales_for_time_window(shop_id, months_to_predict)

        # Prepare bar chart
        df_predictions = pd.DataFrame(predictions)
        plt.figure(figsize=(8, 6))
        plt.bar(df_predictions['month'], df_predictions['predicted_sales'])
        plt.xlabel('Month')
        plt.ylabel('Predicted Sales')
        plt.title(f'Shop {shop_id} - Sales Prediction')

        # Convert chart to image
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        chart_url = base64.b64encode(img.getvalue()).decode()

        return jsonify({'chart': chart_url, 'predictions': predictions})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
