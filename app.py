import pandas as pd
from flask import Flask, request, jsonify, render_template
import joblib
import matplotlib.pyplot as plt
import io
import base64
import matplotlib

# Use the 'Agg' backend to prevent GUI-related issues with Matplotlib
matplotlib.use('Agg')

# Initialize Flask app
app = Flask(__name__)

# Load the trained model and columns
model = joblib.load('xgb_coffee_sales_model.joblib')
original_columns = joblib.load('columns.pkl')

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

    # Define product categories
    categories = ['Coffee', 'Tea', 'Drinking Chocolate', 'Bakery', 'Flavours', 'Loose Tea', 'Coffee beans', 'Packaged Chocolate', 'Branded']

    sales_predictions = {}

    # Predict sales for each product category
    for category in categories:
        # Create input features for each category
        input_features = {
            'year': [year],
            'month': [month],
            "store_location_Hell's Kitchen": [store_dummy[0]],
            'store_location_Lower Manhattan': [store_dummy[1]],
            f'product_category_{category}': [1]  # Set the current category to 1
        }

        input_df = pd.DataFrame(input_features)

        # Add missing columns and set them to 0
        for col in original_columns:
            if col not in input_df.columns:
                input_df[col] = 0

        # Ensure correct column order
        input_df = input_df[original_columns]

        # Remove 'Total Sales' if it exists
        if 'Total Sales' in input_df.columns:
            input_df = input_df.drop('Total Sales', axis=1)

        # Make prediction for the current category
        predicted_sales = model.predict(input_df)
        sales_predictions[category] = float(predicted_sales[0])  # Convert to Python float for JSON serialization

    # Sort sales_predictions by value (predicted sales)
    sorted_sales_predictions = dict(sorted(sales_predictions.items(), key=lambda item: item[1], reverse=True))

    # Plot a line chart (sorted by predicted sales)
    plt.figure(figsize=(10, 6))
    plt.plot(list(sorted_sales_predictions.keys()), list(sorted_sales_predictions.values()), marker='o')
    plt.xlabel('Product Category')
    plt.ylabel('Predicted Sales')
    plt.title(f'Predicted Sales for {store_location} in {year}-{month}')
    plt.xticks(rotation=45)  # Rotate category names for better readability

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode()

    # Return JSON response
    return jsonify({'chart': chart_url, 'sales': sorted_sales_predictions})

if __name__ == '__main__':
    app.run(debug=True)
