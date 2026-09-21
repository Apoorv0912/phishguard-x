import pandas as pd


def load_dataset(file_path):
    """Load the processed PhishGuard dataset."""
    return pd.read_csv(file_path)


def dataset_summary(df):
    """Return basic dataset information."""
    summary = {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
    }

    return summary


def label_distribution(df):
    """Return label counts and percentages."""
    counts = df["Label"].value_counts().sort_index()
    percentages = (
        df["Label"]
        .value_counts(normalize=True)
        .sort_index()
        .mul(100)
        .round(2)
    )

    return counts, percentages