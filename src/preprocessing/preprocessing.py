import pandas as pd
from sklearn.preprocessing import StandardScaler


FINAL_FEATURES = [
    "Have_IP",
    "Have_At",
    "URL_Length",
    "URL_Depth",
    "Redirection",
    "https_Domain",
    "TinyURL",
    "Prefix/Suffix",
    "DNS_Record",
    "Web_Traffic",
    "Domain_Age",
    "Domain_End",
    "iFrame",
    "Mouse_Over",
    "Web_Forwards",
]


def prepare_features(df):
    """
    Select the final model features from the dataset.
    """
    return df[FINAL_FEATURES].copy()


def create_scaler():
    """
    Create a StandardScaler for scale-sensitive models.
    """
    return StandardScaler()


def scale_features(X_train, X_test):
    """
    Fit StandardScaler on training data and transform
    both training and test data without data leakage.
    """
    scaler = create_scaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, scaler