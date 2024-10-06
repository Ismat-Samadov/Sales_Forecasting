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

# Load necessary datasets
items = pd.read_csv('data/items.csv')  # Load items data
shops = pd.read_csv('data/shops.csv')  # Load shops data

# Load the preprocessed sales data
try:
    monthly_sales = joblib.load('data/processed_sales.pkl')
    print("Preprocessed data loaded successfully.")
except Exception as e:
    print(f"Error loading preprocessed data: {e}")

def predict_in_batches(predict_data, model, batch_size=100):
    """Predict sales in smaller batches to avoid memory overload."""
    total_sales = []
    
    for i in range(0, len(predict_data), batch_size):
        batch = predict_data.iloc[i:i + batch_size].copy()  # Make an explicit copy of the batch to avoid the SettingWithCopyWarning
        predictions = model.predict(batch)
        batch.loc[:, 'predicted_sales'] = predictions  # Use .loc to avoid SettingWithCopyWarning
        total_sales.append(batch)
        
    total_sales_df = pd.concat(total_sales, ignore_index=True)
    return total_sales_df

@app.route('/predict', methods=['POST'])
def predict_sales():
    try:
        # Log the received data
        input_data = request.json
        print(f"Received input data: {input_data}")

        month = input_data['month']
        year = input_data['year']

        # Convert month and year to date_block_num
        date_block_num = (year - 2013) * 12 + (month - 1)
        print(f"Using date_block_num: {date_block_num}")

        # Filter the sales data for the specific date_block_num
        sales_data_for_date = monthly_sales[monthly_sales['date_block_num'] == date_block_num]
        print("Filtered data for the date.")

        # Generate prediction dataset
        predict_data = pd.DataFrame({
            'shop_id': shops['shop_id'].reset_index(drop=True),
            'item_price': 1000,  # Placeholder value
        })

        # Predict sales for each shop in batches to prevent memory overload
        total_sales = []
        for shop_id in shops['shop_id']:
            print(f"Predicting for shop {shop_id}")
            shop_items = pd.DataFrame({
                'shop_id': [shop_id] * len(items),
                'item_id': items['item_id'],
                'item_price': 1000,  # Placeholder value
                'item_category_id': items['item_category_id'],
                'item_cnt_month_lag_1': 0,  # Placeholder lag values
                'item_cnt_month_lag_2': 0,  # Placeholder lag values
                'item_cnt_month_lag_3': 0   # Placeholder lag values
            })

            # Use batched predictions to avoid memory issues
            predicted_sales_batch = predict_in_batches(shop_items, model)
            total_shop_sales = predicted_sales_batch['predicted_sales'].sum()
            total_sales.append({
                'shop_id': shop_id,
                'predicted_sales': total_shop_sales
            })

        # Sort the results and create the chart
        print("Sorting and generating chart...")
        total_sales_df = pd.DataFrame(total_sales)
        sorted_sales = total_sales_df.sort_values(by='predicted_sales', ascending=False).head(5)

        table_data = sorted_sales.to_dict(orient='records')

        # Plot a pie chart for the top 5 shops
        plt.figure(figsize=(8, 8))
        plt.pie(sorted_sales['predicted_sales'], labels=sorted_sales['shop_id'], autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
        plt.title(f'Top 5 Shops by Predicted Sales for {month}/{year}')
        plt.axis('equal')

        # Convert the pie chart to a base64 image
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
