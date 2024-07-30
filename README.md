# Store Sales - Time Series Forecasting

This repository contains the code for the Kaggle competition "Store Sales - Time Series Forecasting." The objective is to predict store sales using historical data, including store information, sales, holidays, oil prices, and transactions.

## Project Structure

- `train.csv`: Training dataset.
- `test.csv`: Test dataset.
- `stores.csv`: Store information.
- `holidays_events.csv`: Holiday events data.
- `oil.csv`: Oil prices data.
- `transactions.csv`: Store transactions data.
- `store_sales_forecasting.ipynb`: Jupyter Notebook with data preprocessing, feature engineering, model training, and prediction.

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/Ismat-Samadov/Store-Sales---Time-Series-Forecasting.git
   cd Store-Sales---Time-Series-Forecasting
   ```

2. Install the required libraries:
   ```bash
   pip install numpy pandas matplotlib seaborn scikit-learn lightgbm
   ```

3. Open and run the Jupyter Notebook:
   ```bash
   jupyter notebook store_sales_forecasting.ipynb
   ```

## Model and Features

- **Model**: LightGBM Regressor
- **Features**: Store number, family, promotions, date components (year, month, day, day of the week), lag features, rolling means.

## Results

- Model evaluation using RMSE (Root Mean Squared Error).

## Contribution

Feel free to contribute by opening issues or submitting pull requests.