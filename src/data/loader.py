"""
Data loading and sampling utilities for PhishGuard-X.

This module loads phishing and legitimate URLs and creates
balanced samples for downstream feature extraction and modeling.
"""

from pathlib import Path

import pandas as pd


# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

DEFAULT_SAMPLE_SIZE = 5_000
DEFAULT_RANDOM_STATE = 12


# -------------------------------------------------------------------
# Data Loading
# -------------------------------------------------------------------

def load_phishing_data(file_path):
    """
    Load phishing URLs from a PhishTank CSV file.

    Parameters
    ----------
    file_path : str or Path
        Path to the PhishTank CSV file.

    Returns
    -------
    pandas.DataFrame
        Phishing URL dataframe.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Phishing dataset not found: {file_path}"
        )

    return pd.read_csv(file_path)


def load_legitimate_data(file_path):
    """
    Load legitimate URLs from the benign URL dataset.

    Parameters
    ----------
    file_path : str or Path
        Path to the legitimate URL CSV file.

    Returns
    -------
    pandas.DataFrame
        Legitimate URL dataframe with column name 'URLs'.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Legitimate dataset not found: {file_path}"
        )

    data = pd.read_csv(file_path)

    # Match the reference dataset structure
    data.columns = ["URLs"]

    return data


# -------------------------------------------------------------------
# Sampling
# -------------------------------------------------------------------

def sample_phishing_urls(
    data,
    sample_size=DEFAULT_SAMPLE_SIZE,
    random_state=DEFAULT_RANDOM_STATE,
):
    """
    Randomly select phishing URLs.

    Parameters
    ----------
    data : pandas.DataFrame
        Phishing URL dataframe.
    sample_size : int, default=5000
        Number of phishing URLs to sample.
    random_state : int, default=12
        Random seed for reproducibility.

    Returns
    -------
    pandas.DataFrame
        Sampled phishing URLs with reset index.
    """
    if len(data) < sample_size:
        raise ValueError(
            f"Dataset contains only {len(data)} rows, "
            f"but {sample_size} samples were requested."
        )

    sampled_data = data.sample(
        n=sample_size,
        random_state=random_state,
    ).copy()

    sampled_data = sampled_data.reset_index(drop=True)

    return sampled_data


def sample_legitimate_urls(
    data,
    sample_size=DEFAULT_SAMPLE_SIZE,
    random_state=DEFAULT_RANDOM_STATE,
):
    """
    Randomly select legitimate URLs.

    Parameters
    ----------
    data : pandas.DataFrame
        Legitimate URL dataframe.
    sample_size : int, default=5000
        Number of legitimate URLs to sample.
    random_state : int, default=12
        Random seed for reproducibility.

    Returns
    -------
    pandas.DataFrame
        Sampled legitimate URLs with reset index.
    """
    if len(data) < sample_size:
        raise ValueError(
            f"Dataset contains only {len(data)} rows, "
            f"but {sample_size} samples were requested."
        )

    sampled_data = data.sample(
        n=sample_size,
        random_state=random_state,
    ).copy()

    sampled_data = sampled_data.reset_index(drop=True)

    return sampled_data
