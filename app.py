import pandas as pd
from flask import Flask, request, jsonify, render_template
import joblib
import matplotlib.pyplot as plt
import io
import base64

# Initialize Flask app
app = Flask(__name__)

# Load the trained model and the original columns
model = joblib.load('xgb_coffee_sales_model.joblib')
original_columns = joblib.load('columns.pkl')  # Load the columns used during training

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    input_data = request.json
    year = int(input_data['year'])
    month = int(input_data['month'])
    store_location = input_data['store_location']

    # Map store location to dummy variables
    store_dummy = [0, 0]  # Hell's Kitchen, Lower Manhattan
    if store_location == "Hell's Kitchen":
        store_dummy[0] = 1
    elif store_location == 'Lower Manhattan':
        store_dummy[1] = 1

    # Create input features
    input_features = {
        'year': [year],
        'month': [month],
        "store_location_Hell's Kitchen": [store_dummy[0]],
        'store_location_Lower Manhattan': [store_dummy[1]]
    }

    input_df = pd.DataFrame(input_features)

    # Add missing columns and set them to 0
    for col in original_columns:
        if col not in input_df.columns:
            input_df[col] = 0

    # Ensure correct column order
    input_df = input_df[original_columns]

    # Remove 'Total Sales' from the input dataframe if it exists
    if 'Total Sales' in input_df.columns:
        input_df = input_df.drop('Total Sales', axis=1)

    # Make prediction
    predicted_sales = model.predict(input_df)

    # Prepare the output (sample for predefined categories)
    categories = ['Coffee', 'Tea', 'Drinking Chocolate', 'Bakery', 'Flavours', 'Loose Tea', 'Coffee beans', 'Packaged Chocolate', 'Branded']
    sales_predictions = {category: predicted_sales[0] for category in categories}

    # Plot a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(sales_predictions.keys(), sales_predictions.values())
    plt.xlabel('Product Category')
    plt.ylabel('Predicted Sales')
    plt.title(f'Predicted Sales for {store_location} in {year}-{month}')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode()

    return jsonify({'chart': chart_url, 'sales': sales_predictions})

if __name__ == '__main__':
    app.run(debug=True)
