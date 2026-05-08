import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, recall_score

# Đường dẫn đến file ĐÃ LÀM SẠCH
path = os.path.join(os.path.dirname(__file__), "..", "cleaned_data", "kidney_cleaned.csv")

if not os.path.exists(path):
    print("Lỗi: Không tìm thấy file cleaned_data/kidney_cleaned.csv.")
    print("Vui lòng chạy file 'Multiple disease prediction system - kidney.py' trước để tạo file sạch.")
else:
    data = pd.read_csv(path)

    # Trong file cleaned, cột kết quả tên là 'class'
    X = data.drop(columns='class', axis=1)
    y = data['class']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "SVM": SVC(kernel='linear'),
        "Decision Tree": DecisionTreeClassifier(),
        "Random Forest": RandomForestClassifier()
    }

    print(f"\n{'BỆNH THẬN (DỮ LIỆU SẠCH)':<25} | {'Accuracy':<10} | {'Recall':<10}")
    print("-" * 55)
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        print(f"{name:<25} | {accuracy_score(y_test, y_pred):<10.2f} | {recall_score(y_test, y_pred):<10.2f}")