import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# Load the transaction data
# Assuming the data is in a CSV file named 'transaction_data.csv'
def load_and_preprocess_data(file_path):
    # Load the data
    data = pd.read_csv(file_path)

    # Convert Time_step to datetime and extract features
    data["Time_step"] = pd.to_datetime(data["Time_step"])
    data["Hour"] = data["Time_step"].dt.hour
    data["Day"] = data["Time_step"].dt.day
    data["Month"] = data["Time_step"].dt.month
    data["Year"] = data["Time_step"].dt.year
    data["Weekday"] = data["Time_step"].dt.weekday

    # Handle missing values in numeric columns
    num_cols = ["USD_amount"]
    data[num_cols] = data[num_cols].fillna(0)

    # Handle missing values in categorical columns
    cat_cols = [
        "Sender_Country",
        "Sender_Sector",
        "Sender_lob",
        "Bene_Country",
        "Transaction_Type",
    ]
    for col in cat_cols:
        if col in data.columns:
            data[col] = data[col].fillna("Unknown")

    return data


def prepare_features_target(data):
    # Define features to use
    numerical_features = ["USD_amount", "Hour", "Day", "Month", "Year", "Weekday"]
    categorical_features = [
        "Sender_Country",
        "Sender_Sector",
        "Sender_lob",
        "Bene_Country",
        "Transaction_Type",
    ]

    # Drop features that shouldn't be used for prediction
    features_to_drop = [
        "Time_step",
        "Transaction_Id",
        "Sender_Id",
        "Sender_Account",
        "Bene_Id",
        "Bene_Account",
        "Label",
    ]

    # Prepare feature matrix X and target vector y
    X = data.drop(features_to_drop, axis=1, errors="ignore")
    y = data["Label"]

    # Keep track of all feature names for later analysis
    all_features = []
    for col in numerical_features:
        if col in X.columns:
            all_features.append(col)

    # Filter categorical features to only include those present in the data
    categorical_features = [col for col in categorical_features if col in X.columns]

    return X, y, numerical_features, categorical_features, all_features


def build_logistic_regression_pipeline(numerical_features, categorical_features):
    # Preprocessing for numerical features
    numerical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    # Preprocessing for categorical features
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value="Unknown")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    # Create the preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numerical_transformer, numerical_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    # Create the full pipeline
    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
        ]
    )

    return pipeline


def analyze_feature_importance(
    pipeline, X, numerical_features, categorical_features, all_features
):
    # Get the trained logistic regression model
    model = pipeline.named_steps["classifier"]

    # Get the column transformer
    preprocessor = pipeline.named_steps["preprocessor"]

    # Get feature names after one-hot encoding
    ohe = preprocessor.named_transformers_["cat"].named_steps["onehot"]
    cat_feature_names = []
    if hasattr(ohe, "get_feature_names_out"):
        cat_feature_names = list(ohe.get_feature_names_out(categorical_features))
    else:
        cat_feature_names = list(ohe.get_feature_names(categorical_features))
    feature_names = numerical_features + cat_feature_names

    # Get feature coefficients
    coefficients = model.coef_[0]

    # Create a DataFrame of feature names and their coefficients
    feature_importance = pd.DataFrame(
        {
            "Feature": feature_names,
            "Coefficient": coefficients,
            "Abs_Coefficient": np.abs(coefficients),
        }
    )

    # Sort by absolute coefficient value
    feature_importance = feature_importance.sort_values(
        "Abs_Coefficient", ascending=False
    )

    return feature_importance


def main(file_path):
    # Load and preprocess the data
    data = load_and_preprocess_data(file_path)

    # Prepare features and target
    X, y, numerical_features, categorical_features, all_features = (
        prepare_features_target(data)
    )

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Build and train the pipeline
    pipeline = build_logistic_regression_pipeline(
        numerical_features, categorical_features
    )
    pipeline.fit(X_train, y_train)

    # Evaluate the model
    train_score = pipeline.score(X_train, y_train)
    test_score = pipeline.score(X_test, y_test)
    print(f"Training accuracy: {train_score:.4f}")
    print(f"Test accuracy: {test_score:.4f}")

    # Analyze feature importance
    feature_importance = analyze_feature_importance(
        pipeline, X, numerical_features, categorical_features, all_features
    )

    # Display top 20 features
    print("\nTop 20 most important features:")
    print(feature_importance.head(20))

    # Plot feature importance
    plt.figure(figsize=(12, 8))
    top_features = feature_importance.head(15)
    plt.barh(top_features["Feature"], top_features["Coefficient"])
    plt.xlabel("Coefficient")
    plt.ylabel("Feature")
    plt.title("Top 15 Feature Importance in Logistic Regression")
    plt.tight_layout()
    plt.savefig("feature_importance.png")
    plt.show()

    return feature_importance


if __name__ == "__main__":
    file_path = "test_data/fraud_payment_data/fraud_payment_data"  # Replace with your actual file path
    feature_importance = main(file_path)
