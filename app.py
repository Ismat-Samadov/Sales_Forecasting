from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

# Load the trained model
model = joblib.load('sales_prediction_model.joblib')

app = Flask(__name__)

# Enable CORS for the app
CORS(app)

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

    # Filter the relevant rows for the specified month and year
    # You might need to convert the month and year to the `date_block_num`
    date_block_num = (year - 2013) * 12 + (month - 1)  # Assuming your data starts in 2013

    # Create a dataset for predictions using shop_id and date_block_num
    items = pd.read_csv('data/items.csv')  # Load item details
    predict_data = pd.DataFrame({
        'shop_id': shop_id,
        'item_id': items['item_id'],
        'item_price': 1000,  # Placeholder value, adjust as needed
        'item_category_id': items['item_category_id'],
        'item_cnt_month_lag_1': 0,  # Placeholder value for lag features
        'item_cnt_month_lag_2': 0,
        'item_cnt_month_lag_3': 0
    })

    # Predict sales for each item
    predictions = model.predict(predict_data)
    predict_data['predicted_sales'] = predictions

    # Sort predictions in descending order
    sorted_predictions = predict_data.sort_values(by='predicted_sales', ascending=False)

    # Create a horizontal bar chart
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

    # Return the bar chart image as a base64 string
    return jsonify({'chart': plot_url})

if __name__ == '__main__':
    app.run(debug=True)
