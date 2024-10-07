from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import io
import base64

# Use the 'Agg' backend for Matplotlib to avoid GUI issues
matplotlib.use('Agg')

# Load the trained model
try:
    model = joblib.load('sales_prediction_model.joblib')
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='.')
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

# Load actual shops and items dataset from your provided CSVs
shops = pd.read_csv('data/shops.csv')  # Replace with actual path to shops.csv
items = pd.read_csv('data/items.csv')  # Replace with actual path to items.csv

def predict_sales_for_year(shop_id, year):
    """Predict sales for each month of the selected year for the selected shop."""
    monthly_sales = []
    
    for month in range(1, 13):
        # Convert month and year to date_block_num
        date_block_num = (year - 2013) * 12 + (month - 1)
        print(f"Predicting sales for shop {shop_id} in {year}, month {month}")

        # Create the prediction dataset for the shop and month
        shop_items = pd.DataFrame({
            'shop_id': [shop_id] * len(items),
            'item_id': items['item_id'],
            'item_price': 1000,  # Placeholder value
            'item_category_id': items['item_category_id'],
            'item_cnt_month_lag_1': 0,  # Placeholder lag values
            'item_cnt_month_lag_2': 0,  # Placeholder lag values
            'item_cnt_month_lag_3': 0   # Placeholder lag values
        })

        # Predict sales using the model
        predicted_sales_batch = model.predict(shop_items)
        total_shop_sales = predicted_sales_batch.sum()

        # Append the result for the month
        monthly_sales.append({
            'month': month,
            'predicted_sales': total_shop_sales
        })

    return pd.DataFrame(monthly_sales)

@app.route('/predict', methods=['POST'])
def predict_sales():
    try:
        # Log the received data
        input_data = request.json
        print(f"Received input data: {input_data}")

        year = input_data['year']
        shop_id = input_data['shop_id']

        # Predict sales for each month of the selected year
        monthly_sales_df = predict_sales_for_year(shop_id, year)

        # Sort and prepare the table data
        table_data = monthly_sales_df.to_dict(orient='records')

        # Plot a bar chart for the monthly sales
        plt.figure(figsize=(8, 6))
        plt.bar(monthly_sales_df['month'], monthly_sales_df['predicted_sales'])
        plt.xlabel('Month')
        plt.ylabel('Predicted Sales')
        plt.title(f'Shop {shop_id} - Predicted Sales for {year}')
        
        # Convert the bar chart to a base64 image
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        print("Prediction complete, returning response...")
        return jsonify({'chart': plot_url, 'table': table_data})

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({"error": "Something went wrong on the server."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
