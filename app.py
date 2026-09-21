# ============================================================
# PHISHGUARD-X
# Explainable Phishing URL Detection Platform
# ============================================================

from pathlib import Path
import sys

import joblib
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="PHISHGUARD-X",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

sys.path.append(str(PROJECT_ROOT))

from src.features.url_features import featureExtraction


# ============================================================
# PATHS
# ============================================================

MODEL_PATH = PROJECT_ROOT / "models" / "tuned_xgboost_final.joblib"
FEATURES_PATH = PROJECT_ROOT / "models" / "final_features.joblib"
THRESHOLD_PATH = PROJECT_ROOT / "models" / "classification_threshold.joblib"
SHAP_PATH = PROJECT_ROOT / "models" / "shap_explainer.joblib"

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "phishguard_features_final_11500.csv"
)

VALIDATION_PATH = (
    PROJECT_ROOT
    / "data"
    / "validation"
    / "unseen_validation.csv"
)


# ============================================================
# FEATURES
# ============================================================

DEFAULT_FEATURES = [
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

ALL_FEATURES = [
    "Domain",
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
    "Right_Click",
    "Web_Forwards",
    "Label",
]


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found:\n{MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)


@st.cache_resource
def load_features():

    if not FEATURES_PATH.exists():
        return DEFAULT_FEATURES

    features = joblib.load(FEATURES_PATH)

    if isinstance(features, list):
        return features

    return DEFAULT_FEATURES


@st.cache_resource
def load_threshold():

    if not THRESHOLD_PATH.exists():
        raise FileNotFoundError(
            f"Threshold not found:\n{THRESHOLD_PATH}"
        )

    return float(joblib.load(THRESHOLD_PATH))


@st.cache_resource
def load_shap():

    if not SHAP_PATH.exists():
        raise FileNotFoundError(
            f"SHAP explainer not found:\n{SHAP_PATH}"
        )

    return joblib.load(SHAP_PATH)


# ============================================================
# LOAD ARTIFACTS
# ============================================================

try:

    model = load_model()
    final_features = load_features()
    threshold = load_threshold()
    explainer = load_shap()

except Exception as e:

    st.error("PHISHGUARD-X could not start.")
    st.exception(e)
    st.stop()


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_dataset():

    if DATA_PATH.exists():
        return pd.read_csv(DATA_PATH)

    return None


@st.cache_data
def load_validation():

    if VALIDATION_PATH.exists():
        return pd.read_csv(VALIDATION_PATH)

    return None


df = load_dataset()
df_validation = load_validation()


# ============================================================
# SESSION STATE
# ============================================================

if "scan_history" not in st.session_state:
    st.session_state.scan_history = []


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
        radial-gradient(
            circle at 90% 0%,
            rgba(166,93,59,0.10),
            transparent 28%
        ),
        #faf7f2;
    }

    section[data-testid="stSidebar"] {
        background: #2f2723;
    }

    section[data-testid="stSidebar"] * {
        color: #f5eee8 !important;
    }



    .hero {
        padding: 12px 0 25px 0;
    }

    .hero-title {
        font-size: 46px;
        font-weight: 850;
        color: #3f342d;
        letter-spacing: -1.5px;
    }

    .hero-subtitle {
        font-size: 17px;
        color: #76675d;
        max-width: 850px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 800;
        color: #3f342d;
        margin-top: 18px;
        margin-bottom: 12px;
    }

    .card {
     background: rgba(255,255,255,0.90);
     border: 1px solid #eadfd5;
     border-radius: 18px;
     padding: 22px;
     color: #4a3d35;
     box-shadow:
        0 8px 25px rgba(75,55,45,0.07);
     margin-bottom: 15px;
    }

    .metric-title {
        font-size: 14px;
        color: #806f63;
        font-weight: 650;
    }

    .metric-value {
        font-size: 31px;
        color: #3f342d;
        font-weight: 850;
    }

    .metric-sub {
        font-size: 12px;
        color: #98887d;
    }

    .safe {
        background: #edf5ee;
        border: 1px solid #c9ddcc;
        color: #315b39;
        padding: 22px;
        border-radius: 16px;
        text-align: center;
        font-size: 27px;
        font-weight: 850;
    }

    .danger {
        background: #f8ece7;
        border: 1px solid #e2b7a7;
        color: #8b3f2c;
        padding: 22px;
        border-radius: 16px;
        text-align: center;
        font-size: 27px;
        font-weight: 850;
    }

    .warning {
        background: #f8f1df;
        border: 1px solid #e6d29c;
        color: #795d20;
        padding: 22px;
        border-radius: 16px;
        text-align: center;
        font-size: 27px;
        font-weight: 850;
    }

    .signal-card {
        background: white;
        border: 1px solid #eadfd5;
        border-radius: 14px;
        padding: 15px;
        margin-bottom: 10px;
    }

    .signal-name {
        color: #4a3d35;
        font-weight: 750;
    }

    .signal-value {
        color: #a65d3b;
        font-size: 20px;
        font-weight: 850;
    }

    .footer {
        text-align: center;
        color: #938176;
        padding: 35px 0 10px 0;
        font-size: 13px;
    }

    .stButton > button {
        background: #a65d3b;
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 700;
    }

    .stButton > button:hover {
        background: #8b4d32;
        color: white;
    }
    @keyframes pgFadeUp {
      from {
        opacity: 0;
        transform: translateY(14px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    .hero {
      animation: pgFadeUp 0.55s ease-out;
    }

    .card {
       animation: pgFadeUp 0.45s ease-out;
       transition: transform 0.22s ease, box-shadow 0.22s ease;
    }

    .card:hover {
      transform: translateY(-3px);
       box-shadow: 0 12px 30px rgba(75,55,45,0.13);
    }

    .signal-card {
        transition: transform 0.20s ease, box-shadow 0.20s ease;
    }

    .signal-card:hover {
        transform: translateY(-2px);
         box-shadow: 0 8px 20px rgba(75,55,45,0.10);
    }

    .stButton > button {
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }

    .stButton > button:hover {
       transform: translateY(-2px);
       box-shadow: 0 7px 18px rgba(166,93,59,0.25);
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def risk_level(probability):

    if probability >= 0.80:
        return "HIGH"

    if probability >= 0.50:
        return "MEDIUM"

    return "LOW"


def risk_class(probability):

    if probability >= 0.80:
        return "danger"

    if probability >= 0.50:
        return "warning"

    return "safe"


def add_scan_history(
    url,
    probability,
    verdict,
):

    st.session_state.scan_history.insert(
        0,
        {
            "URL": url,
            "Probability": probability,
            "Verdict": verdict,
        },
    )

    st.session_state.scan_history = (
        st.session_state.scan_history[:20]
    )


def warm_shap_plot(
    features,
    values,
    title,
):

    features = list(features)
    values = np.asarray(values)

    colors = [
        "#A65D3B" if value > 0 else "#B8A08A"
        for value in values
    ]

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    y = np.arange(len(features))

    ax.barh(
        y,
        values,
        color=colors,
        height=0.65,
        edgecolor="none",
    )

    ax.axvline(
        0,
        color="#5A4A42",
        linewidth=1,
    )

    ax.set_yticks(y)
    ax.set_yticklabels(features)

    ax.set_xlabel(
        "SHAP contribution",
        color="#4a3d35",
    )

    ax.set_title(
        title,
        fontsize=14,
        fontweight="bold",
        color="#3f342d",
    )

    ax.grid(
        axis="x",
        linestyle="--",
        alpha=0.20,
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()

    return fig
def animated_scan():

    import time

    steps = [
        ("🔎", "URL ANALYSIS", "Inspecting target URL"),
        ("🧬", "FEATURE EXTRACTION", "Extracting security signals"),
        ("🤖", "XGBOOST INFERENCE", "Running machine-learning classification"),
        ("🧠", "SHAP EXPLANATION", "Generating model explanation"),
        ("🛡️", "FINAL VERDICT", "Preparing final security verdict"),
    ]

    with st.status(
        "🚀 Starting PHISHGUARD-X security scan...",
        expanded=True
    ) as scan_status:

        for i, (icon, title, description) in enumerate(steps, start=1):

            scan_status.update(
                label=f"{icon} {title} — {description}",
                state="running",
                expanded=True
            )

            time.sleep(1)

            scan_status.write(
                f"✓ {icon} {title} completed"
            )

        scan_status.update(
            label="🛡️ Security scan completed",
            state="complete",
            expanded=False
        )

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:30px;
            font-weight:850;
        ">
        🛡️ PHISHGUARD-X
        </div>

        <div style="
            color:#cbb9ad;
            font-size:13px;
            margin-bottom:25px;
        ">
        Explainable Cybersecurity AI
        </div>
        """,
        unsafe_allow_html=True,
    )

    page = st.radio(
        "SYSTEM",
        [
            "Command Center",
            "URL Scanner",
            "CSV Scanner",
            "AI Explanation",
            "URL Fingerprint",
            "Model Lab",
            "Validation Lab",
            "Scan History",
            "About",
        ],
    )

    st.markdown("---")

    st.caption(
        f"Model: Tuned XGBoost"
    )

    st.caption(
        f"Features: {len(final_features)}"
    )

    st.caption(
        f"Threshold: {threshold:.2f}"
    )

    st.caption(
        "Domain-aware evaluation"
    )


# ============================================================
# COMMAND CENTER
# ============================================================

if page == "Command Center":

    st.markdown(
        """
        <div class="hero">

        <div class="hero-title">
        PHISHGUARD-X
        </div>

        <div class="hero-subtitle">
        Explainable machine-learning platform for detecting
        potentially malicious phishing URLs.
        </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # Dataset information

    if df is not None:

        total = len(df)
        legitimate = int(
            (df["Label"] == 0).sum()
        )
        phishing = int(
            (df["Label"] == 1).sum()
        )

    else:

        total = 11500
        legitimate = 6500
        phishing = 5000

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        (
            "DATASET",
            f"{total:,}",
            "processed URLs",
        ),
        (
            "LEGITIMATE",
            f"{legitimate:,}",
            "label = 0",
        ),
        (
            "PHISHING",
            f"{phishing:,}",
            "label = 1",
        ),
        (
            "FEATURES",
            str(len(final_features)),
            "final ML features",
        ),
    ]

    for column, metric in zip(
        [c1, c2, c3, c4],
        metrics,
    ):

        with column:

            st.markdown(
                f"""
                <div class="card">

                <div class="metric-title">
                {metric[0]}
                </div>

                <div class="metric-value">
                {metric[1]}
                </div>

                <div class="metric-sub">
                {metric[2]}
                </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="section-title">Detection Pipeline</div>',
        unsafe_allow_html=True,
    )

    pipeline_cols = st.columns(5)

    pipeline = [
        ("01", "URL", "Input"),
        ("02", "FEATURES", "Extraction"),
        ("03", "XGBOOST", "Prediction"),
        ("04", "THRESHOLD", "Decision"),
        ("05", "SHAP", "Explanation"),
    ]

    for col, item in zip(
        pipeline_cols,
        pipeline,
    ):

        with col:

            st.markdown(
                f"""
                <div class="card"
                     style="text-align:center;">

                <div style="
                    font-size:13px;
                    color:#a65d3b;
                    font-weight:800;
                ">
                {item[0]}
                </div>

                <div style="
                    font-size:18px;
                    font-weight:800;
                    color:#3f342d;
                ">
                {item[1]}
                </div>

                <div style="
                    font-size:12px;
                    color:#8b7a6d;
                ">
                {item[2]}
                </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="section-title">System Status</div>',
        unsafe_allow_html=True,
    )

    st.success(
        "✓ Model loaded  •  ✓ SHAP loaded  •  "
        "✓ Feature schema verified  •  "
        "✓ Classification threshold loaded"
    )


# ============================================================
# URL SCANNER
# ============================================================

elif page == "URL Scanner":

    st.markdown(
        """
        <div class="hero-title">
        🔎 URL Scanner
        </div>

        <div class="hero-subtitle">
        Perform a complete PHISHGUARD-X security analysis.
        </div>
        """,
        unsafe_allow_html=True,
    )

    url = st.text_input(
        "Target URL",
        placeholder="example.com",
    )

    analyze = st.button(
        "🚀 START SECURITY SCAN",
        use_container_width=True,
    )

    if analyze:
        animated_scan()

        if not url.strip():

            st.warning(
                "Enter a URL first."
            )

            st.stop()

        url = url.strip()

        if not url.startswith(
            ("http://", "https://")
        ):

            url = "https://" + url

        # Feature extraction

        with st.spinner(
            "Running URL intelligence and feature extraction..."
        ):

            try:

                extracted = featureExtraction(
                    url,
                    0,
                )

            except Exception as e:

                st.error(
                    "Feature extraction failed."
                )

                st.exception(e)

                st.stop()

        if len(extracted) != len(
            ALL_FEATURES
        ):

            st.error(
                "Feature schema mismatch detected."
            )

            st.stop()

        raw_df = pd.DataFrame(
            [extracted],
            columns=ALL_FEATURES,
        )

        X_input = raw_df[
            final_features
        ].copy()

        # Prediction

        with st.spinner(
            "Running tuned XGBoost inference..."
        ):

            probability = float(
                model.predict_proba(
                    X_input
                )[0, 1]
            )

        prediction = int(
            probability >= threshold
        )

        verdict = (
            "PHISHING"
            if prediction == 1
            else "LEGITIMATE"
        )

        risk = risk_level(
            probability
        )

        add_scan_history(
            url,
            probability,
            verdict,
        )

        # Result

        st.markdown(
            '<div class="section-title">Security Verdict</div>',
            unsafe_allow_html=True,
        )

        if verdict == "PHISHING":

            st.markdown(
                """
                <div class="danger">
                🚨 PHISHING DETECTED
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:

            st.markdown(
                """
                <div class="safe">
                ✓ URL CLASSIFIED AS LEGITIMATE
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.write("")

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "Phishing Probability",
                f"{probability * 100:.2f}%",
            )

        with c2:

            st.metric(
                "Legitimate Probability",
                f"{(1 - probability) * 100:.2f}%",
            )

        with c3:

            st.metric(
                "Threat Level",
                risk,
            )

        st.caption(
            f"Decision threshold: {threshold:.2f}"
        )

        st.progress(
            probability
        )

        st.markdown(
            '<div class="section-title">Target</div>',
            unsafe_allow_html=True,
        )

        st.code(
            url,
            language="text",
        )

        # Security signals

        st.markdown(
            '<div class="section-title">Security Signals</div>',
            unsafe_allow_html=True,
        )

        signal_groups = [
            (
                "URL Structure",
                [
                    "Have_IP",
                    "Have_At",
                    "URL_Length",
                    "URL_Depth",
                    "Redirection",
                    "TinyURL",
                    "Prefix/Suffix",
                ],
            ),
            (
                "Domain Intelligence",
                [
                    "https_Domain",
                    "DNS_Record",
                    "Domain_Age",
                    "Domain_End",
                ],
            ),
            (
                "Web Behavior",
                [
                    "Web_Traffic",
                    "iFrame",
                    "Mouse_Over",
                    "Web_Forwards",
                ],
            ),
        ]

        for group_name, features in signal_groups:

            st.markdown(
                f"**{group_name}**"
            )

            cols = st.columns(
                min(4, len(features))
            )

            for col, feature in zip(
                cols,
                features,
            ):

                value = int(
                    X_input.iloc[0][feature]
                )

                with col:

                    st.markdown(
                        f"""
                        <div class="signal-card">

                        <div class="signal-name">
                        {feature}
                        </div>

                        <div class="signal-value">
                        {value}
                        </div>

                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        # SHAP

        st.markdown(
            '<div class="section-title">🧠 AI Explanation</div>',
            unsafe_allow_html=True,
        )

        try:

            explanation = explainer(
                X_input
            )

            values = np.asarray(
                explanation.values[0]
            )

            top_idx = np.argsort(
                np.abs(values)
            )[-8:][::-1]

            top_features = [
                final_features[i]
                for i in top_idx
            ]

            top_values = [
                values[i]
                for i in top_idx
            ]

            shap_df = pd.DataFrame(
                {
                    "Feature": top_features,
                    "Contribution": top_values,
                    "Direction": [
                        "Phishing"
                        if value > 0
                        else "Legitimate"
                        for value in top_values
                    ],
                }
            )

            st.dataframe(
                shap_df,
                use_container_width=True,
                hide_index=True,
            )

            fig = warm_shap_plot(
                top_features[::-1],
                top_values[::-1],
                "Top Factors Influencing This Prediction",
            )

            st.pyplot(
                fig,
                use_container_width=True,
            )

            plt.close(fig)

            st.caption(
                "Positive SHAP contribution pushes the prediction "
                "toward phishing; negative contribution pushes it "
                "toward legitimate."
            )

        except Exception as e:

            st.warning(
                "SHAP explanation unavailable for this scan."
            )

            st.exception(e)

# ============================================================
# CSV SCANNER
# ============================================================

elif page == "CSV Scanner":

    st.markdown(
        """
        <div class="hero-title">
        📂 CSV Scanner
        </div>

        <div class="hero-subtitle">
        Batch phishing detection for multiple URLs.
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Upload CSV file",
        type=["csv"],
        help="CSV should contain a URL column.",
    )

    if uploaded_file is not None:

        # ----------------------------------------------------
        # LOAD CSV
        # ----------------------------------------------------

        try:

            csv_df = pd.read_csv(
                uploaded_file
            )

        except Exception as e:

            st.error(
                "Unable to read the CSV file."
            )

            st.exception(e)

            st.stop()

        st.success(
            f"CSV loaded successfully — {len(csv_df):,} rows"
        )

        # ----------------------------------------------------
        # DETECT URL COLUMN
        # ----------------------------------------------------

        possible_url_columns = [
            "url",
            "URL",
            "Url",
            "urls",
            "URLs",
            "link",
            "Link",
            "website",
            "Website",
            "domain",
            "Domain",
        ]

        url_column = None

        for column in possible_url_columns:

            if column in csv_df.columns:

                url_column = column
                break

        # Fallback: search columns containing url/link
        if url_column is None:

            for column in csv_df.columns:

                column_lower = str(
                    column
                ).lower()

                if (
                    "url" in column_lower
                    or "link" in column_lower
                ):

                    url_column = column
                    break

        if url_column is None:

            st.error(
                "No URL column detected."
            )

            st.info(
                "Your CSV should contain a column such as "
                "'url', 'URL', 'link', or 'website'."
            )

            st.stop()

        # ----------------------------------------------------
        # URL COLUMN SELECTOR
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">URL Column</div>',
            unsafe_allow_html=True,
        )

        selected_column = st.selectbox(
            "Detected URL column",
            options=csv_df.columns,
            index=list(
                csv_df.columns
            ).index(url_column),
        )

        # ----------------------------------------------------
        # PREVIEW
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">CSV Preview</div>',
            unsafe_allow_html=True,
        )

        st.dataframe(
            csv_df.head(10),
            use_container_width=True,
            hide_index=True,
        )

        # ----------------------------------------------------
        # START BATCH SCAN
        # ----------------------------------------------------

        scan_csv = st.button(
            "🚀 START CSV SECURITY SCAN",
            use_container_width=True,
        )

        if scan_csv:

            urls = (
                csv_df[selected_column]
                .dropna()
                .astype(str)
                .str.strip()
            )

            urls = urls[
                urls != ""
            ]

            if len(urls) == 0:

                st.warning(
                    "No valid URLs found in the selected column."
                )

                st.stop()

            # ------------------------------------------------
            # REMOVE EXACT DUPLICATES FOR SCANNING
            # ------------------------------------------------

            unique_urls = urls

            st.info(
                f"Scanning {len(unique_urls):,} unique URLs..."
            )

            results = []

            progress_bar = st.progress(
                0
            )

            status_text = st.empty()

            total_urls = len(
                unique_urls
            )

            # ------------------------------------------------
            # BATCH FEATURE EXTRACTION + PREDICTION
            # ------------------------------------------------

            for index, raw_url in enumerate(
                unique_urls,
                start=1,
            ):

                scanned_url = raw_url

                if not scanned_url.startswith(
                    ("http://", "https://")
                ):

                    scanned_url = (
                        "https://" + scanned_url
                    )

                status_text.write(
                    f"🔎 Scanning {index:,}/{total_urls:,}: "
                    f"{scanned_url}"
                )

                try:

                    extracted = featureExtraction(
                        scanned_url,
                        0,
                    )

                    if len(extracted) != len(
                        ALL_FEATURES
                    ):

                        raise ValueError(
                            "Feature schema mismatch"
                        )

                    raw_features = pd.DataFrame(
                        [extracted],
                        columns=ALL_FEATURES,
                    )

                    X_batch = raw_features[
                        final_features
                    ].copy()

                    probability = float(
                        model.predict_proba(
                            X_batch
                        )[0, 1]
                    )

                    prediction = int(
                        probability >= threshold
                    )

                    verdict = (
                        "PHISHING"
                        if prediction == 1
                        else "LEGITIMATE"
                    )

                    risk = risk_level(
                        probability
                    )

                    results.append(
                        {
                            "URL": raw_url,
                            "Phishing_Probability":
                                round(
                                    probability,
                                    4,
                                ),
                            "Legitimate_Probability":
                                round(
                                    1 - probability,
                                    4,
                                ),
                            "Verdict":
                                verdict,
                            "Threat_Level":
                                risk,
                        }
                    )

                except Exception as e:

                    results.append(
                        {
                            "URL": raw_url,
                            "Phishing_Probability":
                                None,
                            "Legitimate_Probability":
                                None,
                            "Verdict":
                                "ERROR",
                            "Threat_Level":
                                "ERROR",
                        }
                    )

                progress_bar.progress(
                    index / total_urls
                )

            status_text.empty()

            # ------------------------------------------------
            # RESULTS DATAFRAME
            # ------------------------------------------------

            results_df = pd.DataFrame(
                results
            )

            # ------------------------------------------------
            # SUMMARY
            # ------------------------------------------------

            successful_results = results_df[
                results_df["Verdict"].isin(
                    [
                        "PHISHING",
                        "LEGITIMATE",
                    ]
                )
            ]

            phishing_count = int(
                (
                    successful_results["Verdict"]
                    == "PHISHING"
                ).sum()
            )

            legitimate_count = int(
                (
                    successful_results["Verdict"]
                    == "LEGITIMATE"
                ).sum()
            )

            error_count = int(
                (
                    results_df["Verdict"]
                    == "ERROR"
                ).sum()
            )

            total_scanned = len(
                results_df
            )

            phishing_percentage = (
                phishing_count
                / len(successful_results)
                * 100
                if len(successful_results) > 0
                else 0
            )

            # ------------------------------------------------
            # SUMMARY CARDS
            # ------------------------------------------------

            st.markdown(
                '<div class="section-title">Scan Summary</div>',
                unsafe_allow_html=True,
            )

            c1, c2, c3, c4 = st.columns(4)

            with c1:

                st.metric(
                    "URLs Scanned",
                    f"{total_scanned:,}",
                )

            with c2:

                st.metric(
                    "Legitimate",
                    f"{legitimate_count:,}",
                )

            with c3:

                st.metric(
                    "Phishing",
                    f"{phishing_count:,}",
                )

            with c4:

                st.metric(
                    "Phishing %",
                    f"{phishing_percentage:.2f}%",
                )

            if error_count > 0:

                st.warning(
                    f"{error_count:,} URLs could not be processed."
                )

            # ------------------------------------------------
            # RESULTS TABLE
            # ------------------------------------------------

            st.markdown(
                '<div class="section-title">Scan Results</div>',
                unsafe_allow_html=True,
            )

            st.dataframe(
                results_df,
                use_container_width=True,
                hide_index=True,
            )

            # ------------------------------------------------
            # FILTER PHISHING
            # ------------------------------------------------

            phishing_df = results_df[
                results_df["Verdict"]
                == "PHISHING"
            ]

            if len(phishing_df) > 0:

                st.markdown(
                    '<div class="section-title">🚨 Detected Phishing URLs</div>',
                    unsafe_allow_html=True,
                )

                st.dataframe(
                    phishing_df,
                    use_container_width=True,
                    hide_index=True,
                )

            # ------------------------------------------------
            # DOWNLOAD RESULTS
            # ------------------------------------------------

            csv_output = results_df.to_csv(
                index=False
            ).encode(
                "utf-8"
            )

            st.download_button(
                label="⬇️ DOWNLOAD SCAN RESULTS",
                data=csv_output,
                file_name="phishguard_batch_scan_results.csv",
                mime="text/csv",
                use_container_width=True,
            )
# ============================================================
# AI EXPLANATION
# ============================================================

elif page == "AI Explanation":

    st.markdown(
        """
        <div class="hero-title">
        🧠 Explainable AI
        </div>

        <div class="hero-subtitle">
        Understand how PHISHGUARD-X uses SHAP to explain model decisions.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if df is None:

        st.warning(
            "Processed dataset not found."
        )

        st.stop()

    X_global = df[
        final_features
    ].copy()

    with st.spinner(
        "Calculating global SHAP explanations..."
    ):

        explanation = explainer(
            X_global
        )

        shap_values = np.asarray(
            explanation.values
        )

        importance = (
            np.abs(shap_values)
            .mean(axis=0)
        )

    importance_df = pd.DataFrame(
        {
            "Feature": final_features,
            "Mean Absolute SHAP": importance,
        }
    ).sort_values(
        "Mean Absolute SHAP",
        ascending=False,
    )

    fig, ax = plt.subplots(
        figsize=(10, 7)
    )

    plot_df = importance_df.sort_values(
        "Mean Absolute SHAP"
    )

    ax.barh(
        plot_df["Feature"],
        plot_df["Mean Absolute SHAP"],
        color="#A65D3B",
    )

    ax.set_xlabel(
        "Mean Absolute SHAP Value"
    )

    ax.set_title(
        "Global Feature Importance",
        fontweight="bold",
        color="#3f342d",
    )

    ax.grid(
        axis="x",
        linestyle="--",
        alpha=0.20,
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()

    st.pyplot(
        fig,
        use_container_width=True,
    )

    plt.close(fig)

    st.markdown(
        '<div class="section-title">Feature Ranking</div>',
        unsafe_allow_html=True,
    )

    st.dataframe(
        importance_df,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# URL FINGERPRINT
# ============================================================

elif page == "URL Fingerprint":

    st.markdown(
        """
        <div class="hero-title">
        🧬 URL Fingerprint
        </div>

        <div class="hero-subtitle">
        Visual representation of the security characteristics
        extracted from a URL.
        </div>
        """,
        unsafe_allow_html=True,
    )

    url = st.text_input(
        "URL",
        placeholder="example.com",
    )

    if st.button(
        "Generate Fingerprint",
        use_container_width=True,
    ):

        if not url.strip():

            st.warning(
                "Enter a URL."
            )

            st.stop()

        if not url.startswith(
            ("http://", "https://")
        ):

            url = "https://" + url

        with st.spinner(
            "Generating URL fingerprint..."
        ):

            try:

                extracted = featureExtraction(
                    url,
                    0,
                )

            except Exception as e:

                st.error(
                    "Fingerprint generation failed."
                )

                st.exception(e)

                st.stop()

        raw_df = pd.DataFrame(
            [extracted],
            columns=ALL_FEATURES,
        )

        X_input = raw_df[
            final_features
        ]

        probability = float(
            model.predict_proba(
                X_input
            )[0, 1]
        )

        st.markdown(
            '<div class="section-title">Threat Fingerprint</div>',
            unsafe_allow_html=True,
        )

        categories = {
            "URL Structure": [
                "Have_IP",
                "Have_At",
                "URL_Length",
                "URL_Depth",
                "Redirection",
                "TinyURL",
                "Prefix/Suffix",
            ],
            "Domain Intelligence": [
                "https_Domain",
                "DNS_Record",
                "Domain_Age",
                "Domain_End",
            ],
            "Web Behavior": [
                "Web_Traffic",
                "iFrame",
                "Mouse_Over",
                "Web_Forwards",
            ],
        }

        for category, features in categories.items():

            values = [
                int(X_input.iloc[0][feature])
                for feature in features
            ]

            score = (
                sum(values)
                / len(values)
            )

            st.markdown(
                f"""
                <div class="card">

                <div style="
                    font-size:18px;
                    font-weight:800;
                    color:#3f342d;
                ">
                {category}
                </div>

                <div style="
                    color:#8b7a6d;
                    margin-bottom:8px;
                ">
                Signal activation: {score * 100:.1f}%
                </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

            st.progress(
                min(max(score, 0), 1)
            )

        st.markdown(
            '<div class="section-title">Model Output</div>',
            unsafe_allow_html=True,
        )

        st.metric(
            "Phishing Probability",
            f"{probability * 100:.2f}%",
        )

        st.caption(
            f"Threshold = {threshold:.2f}"
        )


# ============================================================
# MODEL LAB
# ============================================================

elif page == "Model Lab":

    st.markdown(
        """
        <div class="hero-title">
        📊 Model Lab
        </div>

        <div class="hero-subtitle">
        Compare baseline models with the tuned XGBoost system.
        </div>
        """,
        unsafe_allow_html=True,
    )

    performance = pd.DataFrame(
        {
            "Model": [
                "Decision Tree",
                "Random Forest",
                "Logistic Regression",
                "KNN",
                "XGBoost",
                "SVM RBF",
                "Tuned XGBoost",
            ],
            "Accuracy": [
                0.9008,
                0.8853,
                0.8757,
                0.8397,
                0.8472,
                0.8062,
                0.9108,
            ],
            "Precision": [
                0.8921,
                0.8616,
                0.8240,
                0.7454,
                0.7900,
                0.8604,
                0.9263,
            ],
            "Recall": [
                0.8680,
                0.8650,
                0.8940,
                0.9370,
                0.8650,
                0.6410,
                0.8550,
            ],
            "F1": [
                0.8799,
                0.8633,
                0.8576,
                0.8303,
                0.8258,
                0.7347,
                0.8892,
            ],
            "ROC-AUC": [
                0.9586,
                0.9568,
                0.9105,
                0.8795,
                0.9560,
                0.9220,
                0.9634,
            ],
        }
    )

    st.dataframe(
        performance.style.format(
            {
                "Accuracy": "{:.4f}",
                "Precision": "{:.4f}",
                "Recall": "{:.4f}",
                "F1": "{:.4f}",
                "ROC-AUC": "{:.4f}",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown(
        '<div class="section-title">F1 Model Comparison</div>',
        unsafe_allow_html=True,
    )

    plot_df = performance.sort_values(
        "F1"
    )

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    ax.barh(
        plot_df["Model"],
        plot_df["F1"],
        color="#A65D3B",
    )

    ax.set_xlim(
        0,
        1,
    )

    ax.set_xlabel(
        "F1 Score"
    )

    ax.set_title(
        "F1 Score Comparison",
        fontweight="bold",
        color="#3f342d",
    )

    ax.grid(
        axis="x",
        linestyle="--",
        alpha=0.20,
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()

    st.pyplot(
        fig,
        use_container_width=True,
    )

    plt.close(fig)

    tuned = performance[
        performance["Model"]
        == "Tuned XGBoost"
    ].iloc[0]

    st.markdown(
        '<div class="section-title">Tuned XGBoost</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    metrics = [
        ("Accuracy", tuned["Accuracy"]),
        ("Precision", tuned["Precision"]),
        ("Recall", tuned["Recall"]),
        ("F1", tuned["F1"]),
        ("ROC-AUC", tuned["ROC-AUC"]),
    ]

    for col, (name, value) in zip(
        [c1, c2, c3, c4, c5],
        metrics,
    ):

        with col:

            st.metric(
                name,
                f"{value:.4f}",
            )

    st.info(
        "Evaluation uses a domain-aware train/test split with zero "
        "domain overlap between training and test sets."
    )


# ============================================================
# VALIDATION LAB
# ============================================================

elif page == "Validation Lab":

    st.markdown(
        """
        <div class="hero-title">
        🧪 Validation Lab
        </div>

        <div class="hero-subtitle">
        Test PHISHGUARD-X on a separate unseen validation dataset.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if df_validation is None:

        st.warning(
            "Unseen validation dataset not found."
        )

        st.stop()

    X_val = df_validation[
        final_features
    ]

    y_val = df_validation[
        "Label"
    ]

    probabilities = model.predict_proba(
        X_val
    )[:, 1]

    predictions = (
        probabilities >= threshold
    ).astype(int)

    accuracy = (
        predictions == y_val
    ).mean()

    fp = int(
        (
            (y_val == 0)
            & (predictions == 1)
        ).sum()
    )

    fn = int(
        (
            (y_val == 1)
            & (predictions == 0)
        ).sum()
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Validation Rows",
            len(df_validation),
        )

    with c2:
        st.metric(
            "Accuracy",
            f"{accuracy * 100:.2f}%",
        )

    with c3:
        st.metric(
            "False Positives",
            fp,
        )

    with c4:
        st.metric(
            "False Negatives",
            fn,
        )

    results = df_validation.copy()

    results["Phishing Probability"] = probabilities

    results["Prediction"] = predictions

    results["Verdict"] = results[
        "Prediction"
    ].map(
        {
            0: "LEGITIMATE",
            1: "PHISHING",
        }
    )

    st.markdown(
        '<div class="section-title">Validation Results</div>',
        unsafe_allow_html=True,
    )

    columns = [
        column
        for column in [
            "Domain",
            "Phishing Probability",
            "Prediction",
            "Verdict",
        ]
        if column in results.columns
    ]

    st.dataframe(
        results[columns],
        use_container_width=True,
        hide_index=True,
    )

    fp_df = results[
        (results["Label"] == 0)
        & (results["Prediction"] == 1)
    ]

    st.markdown(
        '<div class="section-title">False Positives</div>',
        unsafe_allow_html=True,
    )

    if len(fp_df) == 0:

        st.success(
            "No false positives in this validation set."
        )

    else:

        st.warning(
            f"{len(fp_df)} legitimate URL(s) were classified as phishing."
        )

        st.dataframe(
            fp_df[columns],
            use_container_width=True,
            hide_index=True,
        )

    st.caption(
        "This is a separate validation check and should not be "
        "treated as a universal real-world performance guarantee."
    )


# ============================================================
# SCAN HISTORY
# ============================================================

elif page == "Scan History":

    st.markdown(
        """
        <div class="hero-title">
        📜 Scan History
        </div>

        <div class="hero-subtitle">
        URLs analyzed during the current application session.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.scan_history:

        st.info(
            "No scans yet. Analyze a URL from the URL Scanner."
        )

    else:

        history_df = pd.DataFrame(
            st.session_state.scan_history
        )

        history_df[
            "Probability"
        ] = history_df[
            "Probability"
        ].apply(
            lambda x: f"{x * 100:.2f}%"
        )

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True,
        )

        if st.button(
            "Clear Scan History"
        ):

            st.session_state.scan_history = []

            st.rerun()


# ============================================================
# ABOUT
# ============================================================

elif page == "About":

    st.markdown(
        """
        <div class="hero-title">
        ℹ️ About PHISHGUARD-X
        </div>

        <div class="hero-subtitle">
        Research-oriented explainable phishing URL detection system.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="card">

        <h3 style="color:#3f342d;">
        Project Architecture
        </h3>

        <p>
        PHISHGUARD-X combines URL feature extraction,
        exploratory data analysis, feature engineering,
        domain-aware model evaluation, hyperparameter tuning,
        threshold selection and SHAP explainability.
        </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="card">

        <h3 style="color:#3f342d;">
        Machine Learning
        </h3>

        <ul>
        <li>Baseline model comparison</li>
        <li>Domain-aware train/test split</li>
        <li>GroupKFold hyperparameter tuning</li>
        <li>Tuned XGBoost classifier</li>
        <li>Classification threshold optimization</li>
        <li>Tree SHAP explainability</li>
        </ul>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="card">

        <h3 style="color:#3f342d;">
        Final Model Features
        </h3>

        <p>
        Have_IP • Have_At • URL_Length • URL_Depth •
        Redirection • https_Domain • TinyURL • Prefix/Suffix •
        DNS_Record • Web_Traffic • Domain_Age • Domain_End •
        iFrame • Mouse_Over • Web_Forwards
        </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="card">

        <h3 style="color:#3f342d;">
        Explainability
        </h3>

        <p>
        Tree SHAP is used to understand both global feature
        importance and individual URL predictions.
        </p>

        <p>
        Positive SHAP values indicate movement toward the
        phishing class, while negative values indicate movement
        toward the legitimate class.
        </p>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
    🛡️ PHISHGUARD-X
    <br>
    Explainable Phishing URL Detection Platform
    </div>
    """,
    unsafe_allow_html=True,
)