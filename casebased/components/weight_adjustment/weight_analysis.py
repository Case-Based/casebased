import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, StandardScaler


class FraudWeightAnalyzer:
    def __init__(
        self, model_path="casebased/components/weight_adjustment/logistic_model.pkl"
    ):
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self.encoder = None
        self.feature_names = None

    def preprocess_data(self, df):
        # Define categorical and numerical features
        categorical_features = [
            "Sender_Country",
            "Sender_Sector",
            "Sender_lob",
            "Bene_Country",
            "Transaction_Type",
        ]
        numerical_features = ["USD_amount"]

        # Define transformers
        self.encoder = OneHotEncoder(handle_unknown="ignore")
        self.scaler = StandardScaler()

        # Create preprocessing pipeline
        preprocessor = ColumnTransformer(
            [
                ("num", self.scaler, numerical_features),
                ("cat", self.encoder, categorical_features),
            ]
        )

        X = df[categorical_features + numerical_features]
        y = df["Label"]

        return preprocessor, X, y

    def train_model(self, df):
        preprocessor, X, y = self.preprocess_data(df)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # Create a pipeline
        self.model = Pipeline(
            [
                ("preprocessor", preprocessor),
                (
                    "classifier",
                    LogisticRegression(class_weight="balanced", max_iter=500),
                ),
            ]
        )

        # Train the model
        self.model.fit(X_train, y_train)

        # Store feature names
        self.feature_names = preprocessor.get_feature_names_out()

        # Save the trained model
        joblib.dump(self.model, self.model_path)
        print("Model trained and saved successfully.")

    def get_feature_weights(self):
        if not self.model:
            self.model = joblib.load(self.model_path)

        # Extract weights
        weights = self.model.named_steps["classifier"].coef_[0]

        # Normalize weights between 0 and 1
        scaler = MinMaxScaler()
        weights = scaler.fit_transform(weights.reshape(-1, 1)).flatten()

        # Create a DataFrame with feature names and their weights
        weights_df = pd.DataFrame({"Feature": self.feature_names, "Weight": weights})
        weights_df = weights_df.sort_values(by="Weight", ascending=False)

        # Save weights
        weights_df.to_csv(
            "casebased/components/weight_adjustment/feature_weights.csv", index=False
        )
        print("Feature weights saved to feature_weights.csv")

        return weights_df


# Example Usage:
df = pd.read_csv("test_data/fraud_payment_data/fraud_payment_data")
analyzer = FraudWeightAnalyzer()
analyzer.train_model(df)
weights = analyzer.get_feature_weights()
# print(weights)
