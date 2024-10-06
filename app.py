from flask import Flask, request, jsonify
import joblib
import pandas as pd

# Load the trained model
model = joblib.load('sales_prediction_model.joblib')

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict_sales():
    """
    Input JSON format:
    {
        "shop_id": 25,
        "item_id": 2552,
        "item_price": 1000,
        "item_category_id": 20,
        "item_cnt_month_lag_1": 2,
        "item_cnt_month_lag_2": 1,
        "item_cnt_month_lag_3": 0
    }
    """

    input_data = request.json
    
    # Convert input JSON to a pandas DataFrame
    input_df = pd.DataFrame([input_data])

    # Ensure all required columns are present
    required_columns = ['shop_id', 'item_id', 'item_price', 'item_category_id',
                        'item_cnt_month_lag_1', 'item_cnt_month_lag_2', 'item_cnt_month_lag_3']
    
    # Check for missing columns
    for col in required_columns:
        if col not in input_df.columns:
            return jsonify({"error": f"Missing column: {col}"}), 400

    # Make prediction
    prediction = model.predict(input_df)
    
    # Return the predicted sales as JSON response
    return jsonify({'predicted_sales': float(prediction[0])})

if __name__ == '__main__':
    app.run(debug=True)
