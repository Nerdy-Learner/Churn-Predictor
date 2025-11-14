# import pandas as pd
# import xgboost as xgb
# from sklearn.preprocessing import LabelEncoder
# from tkinter import Tk, ttk, Scrollbar, RIGHT, Y, X, BOTTOM

# # 1️⃣ Load new data
# new_df = pd.read_csv("End\\text_input.csv")

# # 2️⃣ Handle missing values
# for col in new_df.columns:
#     if new_df[col].isnull().any():
#         if new_df[col].dtype == 'object':
#             new_df[col] = new_df[col].fillna(new_df[col].mode()[0])
#         else:
#             new_df[col] = new_df[col].fillna(new_df[col].median())

# # 3️⃣ Encode categorical columns
# label_cols = ['subscription_type', 'favorite_genre', 'payment_method']
# for col in label_cols:
#     new_df[col + '_encoded'] = LabelEncoder().fit_transform(new_df[col])

# # 4️⃣ Select features
# X_new = new_df[['subscription_type_encoded', 'watch_hours', 'last_login_days',
#                 'monthly_fee', 'payment_method_encoded', 'number_of_profiles',
#                 'avg_watch_time_per_day', 'favorite_genre_encoded']]

# # 5️⃣ Load trained XGBoost model
# loaded_model = xgb.Booster()
# loaded_model.load_model("End\\xgboost_churn_model.json")

# # 6️⃣ Predict churn probabilities
# dnew = xgb.DMatrix(X_new)
# preds = loaded_model.predict(dnew)

# new_df["Probability_Churn"] = preds
# new_df["Predicted_Churn"] = (preds > 0.10).astype(int)

# # 7️⃣ Display selected columns
# columns_to_show = [
#     'subscription_type', 'watch_hours', 'last_login_days', 'monthly_fee',
#     'payment_method', 'number_of_profiles', 'avg_watch_time_per_day',
#     'favorite_genre', 'Predicted_Churn', 'Probability_Churn'
# ]

# display_df = new_df[columns_to_show]

# # 8️⃣ Create GUI window
# root = Tk()
# root.title("Churn Prediction Results")
# root.geometry("1100x400")

# # 9️⃣ Create Treeview widget
# tree = ttk.Treeview(root, columns=columns_to_show, show='headings')

# # Add column headings
# for col in columns_to_show:
#     tree.heading(col, text=col)
#     tree.column(col, width=120, anchor='center')

# # Add rows
# for _, row in display_df.iterrows():
#     tree.insert('', 'end', values=list(row))

# # Add scrollbars
# scroll_y = Scrollbar(root, orient='vertical', command=tree.yview)
# scroll_x = Scrollbar(root, orient='horizontal', command=tree.xview)
# tree.configure(yscroll=scroll_y.set, xscroll=scroll_x.set)

# scroll_y.pack(side=RIGHT, fill=Y)
# scroll_x.pack(side=BOTTOM, fill=X)
# tree.pack(expand=True, fill='both')

# # Run GUI
# root.mainloop()








# import pandas as pd
# import xgboost as xgb
# from sklearn.preprocessing import LabelEncoder
# from tkinter import *
# from tkinter import ttk, filedialog, messagebox

# # ========== Common Setup ==========

# # LabelEncoder helpers for consistent encoding
# def encode_column(col, data):
#     le = LabelEncoder()
#     return le.fit_transform(data[col])

# # Load model once
# loaded_model = xgb.Booster()
# loaded_model.load_model("End\\xgboost_churn_model.json")

# # Features for model
# feature_cols = [
#     'subscription_type_encoded', 'watch_hours', 'last_login_days',
#     'monthly_fee', 'payment_method_encoded', 'number_of_profiles',
#     'avg_watch_time_per_day', 'favorite_genre_encoded'
# ]

# categorical_cols = ['subscription_type', 'favorite_genre', 'payment_method']


# # ========== Prediction Logic ==========

# def predict_from_dataframe(df):
#     # Handle missing values safely
#     for col in df.columns:
#         if df[col].isnull().any():
#             if df[col].dtype == 'object':
#                 df[col] = df[col].fillna(df[col].mode()[0])
#             else:
#                 df[col] = df[col].fillna(df[col].median())

#     # Encode categorical columns
#     for col in categorical_cols:
#         df[col + '_encoded'] = encode_column(col, df)

#     # Select features
#     X_new = df[feature_cols]

#     # Predict
#     dnew = xgb.DMatrix(X_new)
#     preds = loaded_model.predict(dnew)

#     # Add prediction columns
#     df["Probability_Churn"] = preds
#     df["Predicted_Churn"] = (preds > 0.10).astype(int)

#     return df


# # ========== GUI Display ==========

# def show_table(df):
#     # Create new window for displaying table
#     result_window = Toplevel(root)
#     result_window.title("Churn Prediction Results")
#     result_window.geometry("1100x400")

#     columns_to_show = [
#         'subscription_type', 'watch_hours', 'last_login_days', 'monthly_fee',
#         'payment_method', 'number_of_profiles', 'avg_watch_time_per_day',
#         'favorite_genre', 'Predicted_Churn', 'Probability_Churn'
#     ]

#     tree = ttk.Treeview(result_window, columns=columns_to_show, show='headings')
#     for col in columns_to_show:
#         tree.heading(col, text=col)
#         tree.column(col, width=120, anchor='center')

#     for _, row in df[columns_to_show].iterrows():
#         tree.insert('', 'end', values=list(row))

#     scroll_y = Scrollbar(result_window, orient='vertical', command=tree.yview)
#     scroll_x = Scrollbar(result_window, orient='horizontal', command=tree.xview)
#     tree.configure(yscroll=scroll_y.set, xscroll=scroll_x.set)

#     scroll_y.pack(side=RIGHT, fill=Y)
#     scroll_x.pack(side=BOTTOM, fill=X)
#     tree.pack(expand=True, fill='both')


# # ========== Mode 1: CSV File Mode ==========

# def csv_mode():
#     filepath = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV files", "*.csv")])
#     if not filepath:
#         return
#     try:
#         df = pd.read_csv(filepath)
#         df = predict_from_dataframe(df)
#         show_table(df)
#     except Exception as e:
#         messagebox.showerror("Error", f"Failed to process file:\n{e}")


# # ========== Mode 2: Single Entry Mode ==========

# def single_entry_mode():
#     entry_window = Toplevel(root)
#     entry_window.title("Single Entry Prediction")
#     entry_window.geometry("500x600")

#     fields = {
#         "subscription_type": ["Basic", "Standard", "Premium"],
#         "watch_hours": None,
#         "last_login_days": None,
#         "monthly_fee": None,
#         "payment_method": ["Credit Card", "Debit Card", "PayPal", "Gift Card"],
#         "number_of_profiles": None,
#         "avg_watch_time_per_day": None,
#         "favorite_genre": ["Action", "Comedy", "Drama", "Romance", "Horror"]
#     }

#     entries = {}

#     row = 0
#     for field, options in fields.items():
#         Label(entry_window, text=field, font=("Arial", 10, "bold")).grid(row=row, column=0, pady=5, padx=10, sticky='w')
#         if options:
#             var = StringVar()
#             combo = ttk.Combobox(entry_window, textvariable=var, values=options, state="readonly")
#             combo.grid(row=row, column=1, pady=5, padx=10)
#             entries[field] = var
#         else:
#             var = StringVar()
#             entry = Entry(entry_window, textvariable=var)
#             entry.grid(row=row, column=1, pady=5, padx=10)
#             entries[field] = var
#         row += 1

#     def predict_single():
#         try:
#             data = {k: [v.get()] for k, v in entries.items()}
#             df = pd.DataFrame(data)

#             # Convert numerics
#             numeric_cols = ['watch_hours', 'last_login_days', 'monthly_fee', 'number_of_profiles', 'avg_watch_time_per_day']
#             for col in numeric_cols:
#                 df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

#             df = predict_from_dataframe(df)

#             prob = df["Probability_Churn"].iloc[0]
#             pred = "Churn" if df["Predicted_Churn"].iloc[0] == 1 else "No Churn"

#             messagebox.showinfo("Prediction Result", f"Predicted: {pred}\nProbability of Churn: {prob:.2f}")
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to predict:\n{e}")

#     Button(entry_window, text="Predict", command=predict_single, bg="#0078D7", fg="white", width=20).grid(row=row, column=0, columnspan=2, pady=20)


# # ========== Main Window ==========

# root = Tk()
# root.title("Churn Prediction System")
# root.geometry("400x250")

# Label(root, text="Select Mode", font=("Arial", 14, "bold")).pack(pady=20)

# Button(root, text="📂 CSV File Mode", command=csv_mode, bg="#4CAF50", fg="white", width=25, height=2).pack(pady=10)
# Button(root, text="🧍 Single Entry Mode", command=single_entry_mode, bg="#2196F3", fg="white", width=25, height=2).pack(pady=10)

# root.mainloop()






import pandas as pd
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
from tkinter import *
from tkinter import ttk, filedialog, messagebox

# ========== Common Setup ==========

def encode_column(col, data):
    le = LabelEncoder()
    return le.fit_transform(data[col])

# Load model once
loaded_model = xgb.Booster()
loaded_model.load_model("End\\xgboost_churn_model.json")

feature_cols = [
    'subscription_type_encoded', 'watch_hours', 'last_login_days',
    'monthly_fee', 'payment_method_encoded', 'number_of_profiles',
    'avg_watch_time_per_day', 'favorite_genre_encoded'
]

categorical_cols = ['subscription_type', 'favorite_genre', 'payment_method']


# ========== Recommendation Generator ==========

def generate_recommendations(row):
    recs = []

    if row["Predicted_Churn"] == 1:  # High churn risk
        if row["watch_hours"] < 10:
            recs.append("Offer a free premium trial to boost engagement.")
        if row["last_login_days"] > 20:
            recs.append("Send a reactivation email with trending shows.")
        if row["subscription_type"] == "Basic":
            recs.append("Recommend upgrade to Standard or Premium plan.")
        if row["avg_watch_time_per_day"] < 1:
            recs.append("Recommend personalized shows based on interests.")
        if not recs:
            recs.append("Offer loyalty rewards to retain customer.")
    else:  # Low churn risk
        recs.append("Send appreciation email for loyalty.")
        recs.append("Provide early access to new releases.")
        recs.append("Encourage participation in referral program.")

    while len(recs) < 3:
        recs.append("Keep customer engaged through personalized offers.")
    return recs[:3]


# ========== Prediction Logic ==========

def predict_from_dataframe(df):
    # Handle missing values safely
    for col in df.columns:
        if df[col].isnull().any():
            if df[col].dtype == 'object':
                df[col] = df[col].fillna(df[col].mode()[0])
            else:
                df[col] = df[col].fillna(df[col].median())

    # Encode categorical columns
    for col in categorical_cols:
        df[col + '_encoded'] = encode_column(col, df)

    # Select features
    X_new = df[feature_cols]
    dnew = xgb.DMatrix(X_new)
    preds = loaded_model.predict(dnew)

    df["Probability_Churn"] = preds
    df["Predicted_Churn"] = (preds > 0.10).astype(int)

    # Add recommendations
    recs = df.apply(generate_recommendations, axis=1)
    df["recommendation_1"] = recs.apply(lambda x: x[0])
    df["recommendation_2"] = recs.apply(lambda x: x[1])
    df["recommendation_3"] = recs.apply(lambda x: x[2])

    return df


# ========== GUI Display ==========

def show_table(df):
    result_window = Toplevel(root)
    result_window.title("Churn Prediction Results")
    result_window.geometry("1350x500")

    columns_to_show = [
        'subscription_type', 'watch_hours', 'last_login_days', 'monthly_fee',
        'payment_method', 'number_of_profiles', 'avg_watch_time_per_day',
        'favorite_genre', 'Predicted_Churn', 'Probability_Churn',
        'recommendation_1', 'recommendation_2', 'recommendation_3'
    ]

    tree = ttk.Treeview(result_window, columns=columns_to_show, show='headings')
    for col in columns_to_show:
        tree.heading(col, text=col)
        tree.column(col, width=180 if "recommendation" in col else 120, anchor='center')

    for _, row in df[columns_to_show].iterrows():
        tree.insert('', 'end', values=list(row))

    scroll_y = Scrollbar(result_window, orient='vertical', command=tree.yview)
    scroll_x = Scrollbar(result_window, orient='horizontal', command=tree.xview)
    tree.configure(yscroll=scroll_y.set, xscroll=scroll_x.set)

    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.pack(side=BOTTOM, fill=X)
    tree.pack(expand=True, fill='both')


# ========== Mode 1: CSV File Mode ==========

def csv_mode():
    filepath = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV files", "*.csv")])
    if not filepath:
        return
    try:
        df = pd.read_csv(filepath)
        df = predict_from_dataframe(df)
        show_table(df)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process file:\n{e}")


# ========== Mode 2: Single Entry Mode ==========

def single_entry_mode():
    entry_window = Toplevel(root)
    entry_window.title("Single Entry Prediction")
    entry_window.geometry("500x600")

    fields = {
        "subscription_type": ["Basic", "Standard", "Premium"],
        "watch_hours": None,
        "last_login_days": None,
        "monthly_fee": None,
        "payment_method": ["Credit Card", "Debit Card", "PayPal", "Gift Card"],
        "number_of_profiles": None,
        "avg_watch_time_per_day": None,
        "favorite_genre": ["Action", "Comedy", "Drama", "Romance", "Horror"]
    }

    entries = {}

    row = 0
    for field, options in fields.items():
        Label(entry_window, text=field, font=("Arial", 10, "bold")).grid(row=row, column=0, pady=5, padx=10, sticky='w')
        if options:
            var = StringVar()
            combo = ttk.Combobox(entry_window, textvariable=var, values=options, state="readonly")
            combo.grid(row=row, column=1, pady=5, padx=10)
            entries[field] = var
        else:
            var = StringVar()
            entry = Entry(entry_window, textvariable=var)
            entry.grid(row=row, column=1, pady=5, padx=10)
            entries[field] = var
        row += 1

    def predict_single():
        try:
            data = {k: [v.get()] for k, v in entries.items()}
            df = pd.DataFrame(data)

            # Convert numerics
            numeric_cols = ['watch_hours', 'last_login_days', 'monthly_fee', 'number_of_profiles', 'avg_watch_time_per_day']
            for col in numeric_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

            df = predict_from_dataframe(df)

            prob = df["Probability_Churn"].iloc[0]
            pred = "Churn" if df["Predicted_Churn"].iloc[0] == 1 else "No Churn"

            recs = [
                df["recommendation_1"].iloc[0],
                df["recommendation_2"].iloc[0],
                df["recommendation_3"].iloc[0],
            ]

            messagebox.showinfo(
                "Prediction Result",
                f"Predicted: {pred}\nProbability of Churn: {prob:.2f}\n\nRecommendations:\n1. {recs[0]}\n2. {recs[1]}\n3. {recs[2]}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to predict:\n{e}")

    Button(entry_window, text="Predict", command=predict_single, bg="#0078D7", fg="white", width=20).grid(row=row, column=0, columnspan=2, pady=20)


# ========== Main Window ==========

root = Tk()
root.title("Churn Prediction System")
root.geometry("400x250")

Label(root, text="Select Mode", font=("Arial", 14, "bold")).pack(pady=20)

Button(root, text="📂 CSV File Mode", command=csv_mode, bg="#4CAF50", fg="white", width=25, height=2).pack(pady=10)
Button(root, text="🧍 Single Entry Mode", command=single_entry_mode, bg="#2196F3", fg="white", width=25, height=2).pack(pady=10)

root.mainloop()
