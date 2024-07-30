import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import lightgbm as lgb
from sklearn.preprocessing import LabelEncoder

# Define paths
train_path = 'data/train.csv'
test_path = 'data/test.csv'
stores_path = 'data/stores.csv'
holidays_path = 'data/holidays_events.csv'
oil_path = 'data/oil.csv'
transactions_path = 'data/transactions.csv'

# Load data
train = pd.read_csv(train_path)
test = pd.read_csv(test_path)
stores = pd.read_csv(stores_path)
holidays = pd.read_csv(holidays_path)
oil = pd.read_csv(oil_path)
transactions = pd.read_csv(transactions_path)

# Merge data
train = train.merge(stores, on='store_nbr', how='left')
train = train.merge(holidays, on='date', how='left')
train = train.merge(oil, on='date', how='left')
train = train.merge(transactions, on=['date', 'store_nbr'], how='left')

# Feature engineering
train['date'] = pd.to_datetime(train['date'])
train['year'] = train['date'].dt.year
train['month'] = train['date'].dt.month
train['day'] = train['date'].dt.day
train['dayofweek'] = train['date'].dt.dayofweek

# Encode categorical variables
label_encoder = LabelEncoder()
train['family'] = label_encoder.fit_transform(train['family'])

# Fill missing values
train.fillna(0, inplace=True)

# Define features and target
features = ['store_nbr', 'family', 'onpromotion', 'year', 'month', 'day', 'dayofweek']
X = train[features]
y = train['sales']

# Split data
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = lgb.LGBMRegressor()
model.fit(X_train, y_train)

# Validate model
y_pred = model.predict(X_val)
print('RMSE:', np.sqrt(mean_squared_error(y_val, y_pred)))

# Predict on test data
test['date'] = pd.to_datetime(test['date'])
test['year'] = test['date'].dt.year
test['month'] = test['date'].dt.month
test['day'] = test['date'].dt.day
test['dayofweek'] = test['date'].dt.dayofweek

# Encode categorical variables in test data
test['family'] = label_encoder.transform(test['family'])

test.fillna(0, inplace=True)

X_test = test[features]
test['sales'] = model.predict(X_test)

# Save submission
submission = test[['id', 'sales']]
submission.to_csv('submission.csv', index=False)
