import pandas as pd
from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load the historical sales data and the trained model
data = pd.read_csv('data/Adidas_US_Sales_Cleaned.csv')

# Convert the Invoice Date column to datetime format
data['Invoice Date'] = pd.to_datetime(data['Invoice Date'], format='%Y-%m-%d')

# Print the available date range in the dataset
print(f"Available date range: {data['Invoice Date'].min()} to {data['Invoice Date'].max()}")

# Load the saved model
model = joblib.load('data/linear_regression_model.pkl')

# Function to filter data by year and month
def get_data_by_date(year, month):
    print(f"Filtering data for year: {year}, month: {month}")
    filtered_data = data[(data['Invoice Date'].dt.year == int(year)) & (data['Invoice Date'].dt.month == int(month))]
    print(f"Filtered Data for {year}-{month}:")
    print(filtered_data)
    return filtered_data

# Function to predict sales for each product in the given month
def predict_sales_for_month(filtered_data):
    results = []
    for index, row in filtered_data.iterrows():
        # Prepare the input features (Price per Unit, Units Sold, Operating Profit)
        features = np.array([[row['Price per Unit'], row['Units Sold'], row['Operating Profit']]])
        
        # Print input features for debugging
        print(f"Input features for row {index}: {features}")
        
        # Make the prediction
        predicted_sales = model.predict(features)[0]
        
        # Ensure the prediction is non-negative
        predicted_sales = max(0, predicted_sales)
        
        # Append the results for this row
        results.append({
            'Retailer': row['Retailer'],
            'Product': row['Product'],
            'Predicted Sales': predicted_sales
        })
    
    return results



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_sales():
    data = request.json
    year = data['year']
    month = data['month']
    
    # Get the data for the selected month and year
    filtered_data = get_data_by_date(year, month)
    
    # If no data is found for the selected date, return a message
    if filtered_data.empty:
        return jsonify({'message': 'No data found for the selected month and year'})
    
    # Predict sales for the month
    predictions = predict_sales_for_month(filtered_data)
    
    return jsonify({'predictions': predictions})

if __name__ == '__main__':
    app.run(debug=True)
