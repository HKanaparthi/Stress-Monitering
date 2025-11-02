import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import os

def load_and_preprocess_data():
    """Load and preprocess the stress dataset"""
    df = pd.read_csv('../data/StressLevelDataset.csv')

    # Features (all columns except stress_level)
    feature_columns = [col for col in df.columns if col != 'stress_level']
    X = df[feature_columns]
    y = df['stress_level']

    print(f"Dataset shape: {df.shape}")
    print(f"Features: {len(feature_columns)}")
    print(f"Stress level distribution:\n{y.value_counts().sort_index()}")

    return X, y, feature_columns

def train_model():
    """Train Random Forest model for stress prediction"""
    # Load data
    X, y, feature_columns = load_and_preprocess_data()

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train Random Forest model
    rf_model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2
    )

    rf_model.fit(X_train_scaled, y_train)

    # Make predictions
    y_pred = rf_model.predict(X_test_scaled)
    y_pred_proba = rf_model.predict_proba(X_test_scaled)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)

    # Print evaluation metrics
    print(f"\nModel Performance:")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred,
                              target_names=['Low Stress', 'Medium Stress', 'High Stress']))

    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)

    print(f"\nTop 10 Most Important Features:")
    print(feature_importance.head(10))

    # Save model, scaler, and feature names
    os.makedirs('models', exist_ok=True)
    joblib.dump(rf_model, 'models/stress_model.pkl')
    joblib.dump(scaler, 'models/scaler.pkl')
    joblib.dump(feature_columns, 'models/feature_columns.pkl')
    joblib.dump(feature_importance, 'models/feature_importance.pkl')

    print(f"\nModel saved successfully!")
    print(f"Files saved:")
    print(f"- models/stress_model.pkl")
    print(f"- models/scaler.pkl")
    print(f"- models/feature_columns.pkl")
    print(f"- models/feature_importance.pkl")

    return rf_model, scaler, feature_columns, feature_importance

if __name__ == "__main__":
    model, scaler, features, importance = train_model()