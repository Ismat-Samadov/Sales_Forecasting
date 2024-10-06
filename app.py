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
model = joblib.load('sales_prediction_model.joblib')

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='.')
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_sales():
    """
    Input JSON format:
    {
        "month": 6,
        "year": 2023,
        "shop_id": 25
    }
    """
    input_data = request.json
    month = input_data['month']
    year = input_data['year']
    shop_id = input_data['shop_id']

    # Convert month and year to date_block_num if needed
    date_block_num = (year - 2013) * 12 + (month - 1)

    # Create a dataset for predictions using shop_id and date_block_num
    items = pd.read_csv('data/items.csv')
    predict_data = pd.DataFrame({
        'shop_id': shop_id,
        'item_id': items['item_id'],
        'item_price': 1000,  # Placeholder value
        'item_category_id': items['item_category_id'],
        'item_cnt_month_lag_1': 0,  # Placeholder for lags
        'item_cnt_month_lag_2': 0,
        'item_cnt_month_lag_3': 0
    })

    # Predict sales
    predictions = model.predict(predict_data)
    predict_data['predicted_sales'] = predictions

    # Sort predictions
    sorted_predictions = predict_data.sort_values(by='predicted_sales', ascending=False)

    # Plot horizontal bar chart
    plt.barh(sorted_predictions['item_id'], sorted_predictions['predicted_sales'], color='skyblue')
    plt.xlabel('Predicted Sales')
    plt.ylabel('Item ID')
    plt.title(f'Sales Prediction for Shop {shop_id} in {month}/{year}')
    plt.gca().invert_yaxis()

    # Convert plot to image
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    # Return the base64 encoded image
    return jsonify({'chart': plot_url})

if __name__ == '__main__':
    app.run(debug=True)
