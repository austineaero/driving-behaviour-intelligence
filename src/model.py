"""
Train LightGBM risk classifier with hyperparameter tuning.
"""
import os
import joblib
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report

FEATURES = [
    "speed_kph",
    "acc_mag",
    "acc_north",
    "acc_east",
    "yaw_rate"
]

def train_model(df, model_dir="output"):
    """
    Train LightGBM classifier with parameter tuning; print classification report.

    Returns
    -------
    LGBMClassifier
    """
    os.makedirs(model_dir, exist_ok=True)
    X = df[FEATURES]
    y = df["risky"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    param_grid = {
        'learning_rate': [0.01, 0.05, 0.1],
        'num_leaves': [7, 15, 31],
        'n_estimators': [80, 150, 250],
        'max_depth': [4, 6, 8]
    }
    lgbm = LGBMClassifier(class_weight='balanced', random_state=42)
    clf = GridSearchCV(
        lgbm,
        param_grid,
        cv=3,
        n_jobs=-1,
        scoring="f1",
        verbose=1
    )
    clf.fit(X_train, y_train)
    print("Best params:", clf.best_params_)
    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred))
    joblib.dump(clf.best_estimator_, os.path.join(model_dir, "risk_model_lgbm.pkl"))

    return clf.best_estimator_