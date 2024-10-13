# Sales Forecasting with Linear Regression

This project demonstrates a simple sales forecasting model using Linear Regression. It predicts total sales based on factors like price per unit, units sold, and operating profit.

## Project Structure

```
.
├── README.md
├── app.py
├── data
│   ├── Adidas_US_Sales_Cleaned.csv
│   └── linear_regression_model.pkl
├── model.ipynb
├── requirements.txt
├── static
│   ├── app.js
│   └── style.css
└── templates
    └── index.html
```

### Dataset

The dataset used in this project is `Adidas_US_Sales_Cleaned.csv`, which contains the following key columns:

- **Price per Unit**: Price of a single unit of a product.
- **Units Sold**: Number of units sold.
- **Operating Profit**: Profit generated from operations.
- **Total Sales**: The target variable for prediction, representing the total sales amount.

### Model

The model used is a **Linear Regression** model, which aims to predict `Total Sales` based on the features `Price per Unit`, `Units Sold`, and `Operating Profit`.

### Model Training and Testing

The data is split into training and testing sets using an 80-20 split. After training, predictions are made on the test set, and the performance is evaluated using **Mean Squared Error (MSE)**.

### Key Steps

1. **Load the Dataset**: The dataset is read from a CSV file located in the `data` folder.
   
   ```python
   data = pd.read_csv('data/Adidas_US_Sales_Cleaned.csv')
   ```

2. **Feature Selection**: The relevant features for the model are selected:
   
   ```python
   X = data[['Price per Unit', 'Units Sold', 'Operating Profit']]
   y = data['Total Sales']
   ```

3. **Train-Test Split**: The data is split into training and testing sets:
   
   ```python
   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
   ```

4. **Model Training**: The linear regression model is trained on the training data:
   
   ```python
   model = LinearRegression()
   model.fit(X_train, y_train)
   ```

5. **Model Prediction**: Predictions are made on the test data:
   
   ```python
   y_pred = model.predict(X_test)
   ```

6. **Model Evaluation**: The model's performance is evaluated using Mean Squared Error:
   
   ```python
   mse = mean_squared_error(y_test, y_pred)
   ```

7. **Model Saving**: The trained model is saved as a `.pkl` file using `joblib`:
   
   ```python
   joblib.dump(model, 'data/linear_regression_model.pkl')
   ```

### Results

- **Mean Squared Error (MSE)**: The MSE value represents the model's prediction error. The lower the MSE, the better the model's predictions.
- **Model Coefficients**: The coefficients of the linear regression model show the relationship between the features and the target variable.

### Dependencies

Install the required Python packages using the following command:

```bash
pip install -r requirements.txt
```

### How to Run the Code

1. Clone the repository:
   ```bash
   git clone https://github.com/Ismat-Samadov/Sales_Forecasting.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Sales_Forecasting
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask app:
   ```bash
   python app.py
   ```

5. Open a browser and go to `http://localhost:5000` to use the web interface for sales prediction.