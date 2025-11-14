# ==================================================== IMPORTS ===================================================================
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns


from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import accuracy_score, mean_squared_error






# ================================================ DATA READ =================================================================
df=pd.read_csv('D:\\College\\Churn-Prediction\\End\\netflix_customer_churn.csv')
numeric_columns_data=df.select_dtypes( include= ['number'])



# ==================================================== DATA CLEANING ====================================================

# print("Missing values before handling:\n", df.isnull().sum())

if df.isnull().sum().any():
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].fillna(df[col].mode()[0]) 
        else:
            df[col] = df[col].fillna(df[col].median())  

# print("\nMissing values after handling:\n", df.isnull().sum())




# ================================================= PREPROCESSING ===============================================================
data= df.copy()
df['subscription_type_encoded'] = LabelEncoder().fit_transform(df['subscription_type'])
df['favorite_genre_encoded'] = LabelEncoder().fit_transform(df['favorite_genre'])
df['payment_method_encoded'] = LabelEncoder().fit_transform(df['payment_method'])




# ================================================ FEATURES SELECTION ============================================================
y = df['churned']
X = df[['subscription_type_encoded', 'watch_hours', 'last_login_days', 'monthly_fee', 'payment_method_encoded', 'number_of_profiles', 'avg_watch_time_per_day', 'favorite_genre_encoded']]




# =================================================== DATA SPLITTING =============================================================

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)




# ====================================================== MODEL TRAINING ==========================================================

dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

params = {
    'objective': 'binary:logistic',  # 'reg:squarederror' for regression
    'eval_metric': 'logloss',        # 'rmse' for regression
    'max_depth': 5,
    'eta': 0.1,                      # Learning rate
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'seed': 42
}

# Train the model
num_round = 100  # Number of boosting rounds
bst = xgb.train(params, dtrain, num_round)




bst.save_model("xgboost_churn_model.json")
print("✅ Model saved successfully.")