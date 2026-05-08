
import pandas as pd
import os
import pickle
import warnings
warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# =========================
# Load dataset
# =========================
DATA_PATH = "dataset/kidney_disease.csv"
df = pd.read_csv(DATA_PATH)

# Drop ID
df.drop("id", axis=1, inplace=True)

# Rename columns
df.columns = [
    'age', 'bp', 'sg', 'al', 'su',
    'rbc', 'pc', 'pcc', 'ba',
    'bgr', 'bu', 'sc', 'sod',
    'pot', 'hemo', 'pcv',
    'wc', 'rc', 'htn',
    'dm', 'cad', 'appet',
    'pe', 'ane', 'class'
]

# =========================
# Fix numeric columns stored as text
# =========================
num_fix_cols = ['pcv', 'wc', 'rc']
for col in num_fix_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# =========================
# Clean inconsistent text values
# =========================
df.replace({
    '\tno': 'no',
    '\tyes': 'yes',
    ' yes': 'yes',
    'ckd\t': 'ckd',
    'notckd': 'notckd'
}, inplace=True)

# =========================
# Encode categorical manually
# =========================
binary_map = {
    'yes': 1, 'no': 0,
    'present': 1, 'notpresent': 0,
    'normal': 1, 'abnormal': 0,
    'good': 1, 'poor': 0
}

binary_cols = [
    'rbc', 'pc', 'pcc', 'ba',
    'htn', 'dm', 'cad',
    'appet', 'pe', 'ane'
]

for col in binary_cols:
    df[col] = df[col].map(binary_map)

# Encode target
df['class'] = df['class'].map({'ckd': 1, 'notckd': 0})

# =========================
# Handle missing values (STORE MEDIAN & MODE)
# =========================
num_fill_values = {}
cat_fill_values = {}

for col in df.columns:
    if col == 'class':
        continue

    if df[col].dtype in ['int64', 'float64']:
        median_value = df[col].median()
        num_fill_values[col] = median_value
        df[col].fillna(median_value, inplace=True)
    else:
        mode_value = df[col].mode()[0]
        cat_fill_values[col] = mode_value
        df[col].fillna(mode_value, inplace=True)

# =========================
# Save cleaned dataset
# =========================
os.makedirs("cleaned_data", exist_ok=True)
df.to_csv("cleaned_data/kidney_cleaned.csv", index=False)

# =========================
# Train model
# =========================
X = df.drop("class", axis=1)
y = df["class"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

train_acc = accuracy_score(y_train, model.predict(X_train))
print("Kidney model training accuracy:", train_acc)

acc = accuracy_score(y_test, model.predict(X_test))
print("Kidney model test accuracy:", acc)

# =========================
# Save model & fill values
# =========================
os.makedirs("saved_models", exist_ok=True)

model_path = "saved_models/kidney_model.sav"
fill_values_path = "saved_models/kidney_fill_values.pkl"

with open(model_path, "wb") as f:
    pickle.dump(model, f)

with open(fill_values_path, "wb") as f:
    pickle.dump({
        "numeric": num_fill_values,
        "categorical": cat_fill_values
    }, f)

print("Model saved at:", model_path)
print("Fill values saved at:", fill_values_path)
print("Total features:", X.shape[1])

