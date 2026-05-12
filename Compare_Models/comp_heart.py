import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, recall_score


path = os.path.join(os.path.dirname(__file__), "..", "dataset", "heart.csv")
data = pd.read_csv(path)

X = data.drop(columns='target', axis=1)
y = data['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=2)

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "SVM": SVC(kernel='linear'),
    "Decision Tree": DecisionTreeClassifier(),
    "Random Forest": RandomForestClassifier()
}

print(f"\n{'BỆNH TIM':<25} | {'Accuracy':<10} | {'Recall':<10}")
print("-" * 50)
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"{name:<25} | {accuracy_score(y_test, y_pred):<10.2f} | {recall_score(y_test, y_pred):<10.2f}")