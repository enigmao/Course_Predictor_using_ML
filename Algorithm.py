# suggestion_system_small_data.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score
import joblib

# --------------------
# 1. Load dataset
# --------------------
df = pd.read_csv("RemedyDataClean.csv")  # Make sure file has q1...q20 + Enrol

X = df.drop("Enrol", axis=1)
y = df["Enrol"]

# --------------------
# 2. Train/Test split (90/10 because dataset is small)
# --------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.1, random_state=42, stratify=y
)

# --------------------
# 3. Define models
# --------------------
models = {
    "Logistic Regression": LogisticRegression(max_iter=500),
    "Random Forest": RandomForestClassifier(n_estimators=150, max_depth=6, random_state=42),
    "LightGBM": LGBMClassifier(n_estimators=150, learning_rate=0.05, random_state=42)
}

# --------------------
# 4. Train & Evaluate
# --------------------
results = {}

for name, model in models.items():
    # Cross-validation on training data (5 folds)
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy")
    avg_cv = np.mean(cv_scores)
    
    # Train on training set
    model.fit(X_train, y_train)
    
    # Evaluate on test set
    y_pred = model.predict(X_test)
    test_acc = accuracy_score(y_test, y_pred)
    
    results[name] = {
        "CV Accuracy": avg_cv,
        "Test Accuracy": test_acc,
        "Model": model
    }
    print(f"{name} → CV: {avg_cv:.4f}, Test: {test_acc:.4f}")

# --------------------
# 5. Pick best model
# --------------------
best_model_name = max(results, key=lambda x: results[x]["Test Accuracy"])
best_model = results[best_model_name]["Model"]

print("\nBest Model:", best_model_name)
print("Test Accuracy:", results[best_model_name]["Test Accuracy"])

# --------------------
# 6. Save best model
# --------------------
joblib.dump(best_model, "RemedyModel.pkl")
print("RemedyModel.pkl")

