# 🛡️ PHISHGUARD-X

### Explainable Phishing URL Detection Platform

An end-to-end machine learning system for detecting phishing URLs using **Tuned XGBoost**, domain-aware evaluation, and **SHAP explainability**.

## 🚀 Live Demo

🔗 [Launch PHISHGUARD-X](https://phishguard-x-myvar8ezigk4bydncy95w2.streamlit.app/)

## 📊 Key Results

| Metric | Result |
|---|---:|
| Dataset Size | 11,500 URLs |
| Legitimate URLs | 6,500 |
| Phishing URLs | 5,000 |
| ML Features | 15 |
| Model | Tuned XGBoost |
| F1 Score | 0.8892 |
| ROC-AUC | 0.9634 |
| Decision Threshold | 0.48 |

## 🧰 Tech Stack

### Machine Learning
- Python
- Scikit-learn
- XGBoost
- SHAP

### Data Processing & Analysis
- Pandas
- NumPy
- SciPy
- Matplotlib
- Seaborn

### Web Application
- Streamlit

### Data & Model Utilities
- Joblib
- Requests
- Python WHOIS

### Development & Deployment
- Git
- GitHub
- Streamlit Community Cloud
## 🚀 Key Features

- 🔎 Single URL phishing detection
- 📂 Batch CSV URL scanning
- 🤖 Tuned XGBoost classification
- 🧠 SHAP-based prediction explanation
- 🌐 Domain-aware train/test evaluation
- 📊 Baseline model comparison
- 🧪 Unseen real-world validation
- 🔐 URL security fingerprint
- 📈 Model and validation analytics
- 🗂️ Scan history
- ⚡ Interactive Streamlit interface

---

## 🔄 Project Workflow

```text
Raw URL Datasets
       ↓
Data Understanding & Cleaning
       ↓
Feature Extraction
       ↓
EDA & Feature Analysis
       ↓
Domain-Aware Train/Test Split
       ↓
Baseline Model Comparison
       ↓
XGBoost Hyperparameter Tuning
       ↓
Classification Threshold Optimization
       ↓
SHAP Explainability
       ↓
Unseen Validation
       ↓
Streamlit Web Application
       ↓
Live Deployment

```

## 📈 Model Performance

### Baseline Models

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Decision Tree | 0.9008 | 0.8921 | 0.8680 | 0.8799 | 0.9586 |
| Random Forest | 0.8853 | 0.8616 | 0.8650 | 0.8633 | 0.9568 |
| Logistic Regression | 0.8757 | 0.8240 | 0.8940 | 0.8576 | 0.9105 |
| KNN | 0.8397 | 0.7454 | 0.9370 | 0.8303 | 0.8795 |
| XGBoost | 0.8472 | 0.7900 | 0.8650 | 0.8258 | 0.9560 |
| SVM RBF | 0.8062 | 0.8604 | 0.6410 | 0.7347 | 0.9220 |

### Tuned XGBoost

| Metric | Score |
|---|---:|
| Accuracy | **0.9108** |
| Precision | **0.9263** |
| Recall | **0.8550** |
| F1 Score | **0.8892** |
| ROC-AUC | **0.9634** |

The final model uses **domain-aware evaluation**, ensuring that domains appearing in the training set do not appear in the test set.


## 🧠 Explainability with SHAP

PHISHGUARD-X uses **SHAP (SHapley Additive exPlanations)** to explain why the model assigns a phishing probability to a URL.

### Global Feature Importance

The most influential features include:

1. URL_Length
2. Prefix/Suffix
3. URL_Depth
4. Web_Traffic
5. iFrame
6. Web_Forwards
7. Domain_End
8. Domain_Age

SHAP explanations are available at both:
- **Global level** — overall feature importance
- **Individual URL level** — why a particular URL received its verdict

The Streamlit application displays the major positive and negative feature contributions for each scanned URL.

## 🧪 Validation

### Unseen Legitimate-Domain Validation

An additional validation set containing **100 previously unseen legitimate domains** was evaluated.

| Result | Count |
|---|---:|
| Correctly classified as legitimate | 97 |
| False positives | 3 |
| False Positive Rate | **3%** |

The false positives were further investigated using SHAP to understand which features contributed to the incorrect predictions.

> This validation set is used as an additional sanity check and should not be interpreted as a full estimate of real-world generalization performance.

## 🌐 Real-World Sanity Checks

The deployed application was manually tested on selected legitimate and suspicious-looking URLs.

The tests included examples from domains such as Google, Microsoft, Apple, GitHub and YouTube, along with deliberately suspicious-looking domains.

These checks are qualitative sanity checks and are **not** used as a replacement for the held-out domain-aware evaluation.


## 📁 Project Structure

```text
phishguard-x/
│
├── data/
│   ├── raw/                 # Original datasets
│   ├── processed/           # Processed features and Tranco Top-100K
│   └── validation/          # Unseen validation datasets
│
├── models/                 # Trained models and explainability artifacts
│
├── src/
│   ├── data/               # Data loading utilities
│   ├── features/           # URL feature extraction
│   ├── eda/                # Exploratory data analysis utilities
│   ├── preprocessing/      # Feature preparation and scaling
│   └── explainability/     # SHAP utilities
│
├── notebooks/              # Research and experimentation notebooks
│
├── reports/
│   └── figures/             # Generated analysis figures
│
├── app.py                  # Streamlit application
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── .gitignore
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Apoorv0912/phishguard-x.git
cd phishguard-x
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python -m streamlit run app.py
```

The application will open in your default browser.


## 💾 Model Artifacts

The trained model and supporting artifacts are stored in the `models/` directory.

| Artifact | Purpose |
|---|---|
| `tuned_xgboost_final.joblib` | Final tuned XGBoost model |
| `final_features.joblib` | Final 15-feature list |
| `classification_threshold.joblib` | Optimized classification threshold |
| `shap_explainer.joblib` | SHAP explainability artifact |

These artifacts allow the Streamlit application to perform inference and generate explanations without retraining the model during application startup.

## 📊 Generated Analysis

The project generates analytical visualizations for:

- Baseline model comparison
- Confusion matrices
- ROC curves
- Precision-Recall curves
- Tuned vs baseline XGBoost
- Classification threshold analysis
- SHAP feature importance
- SHAP beeswarm analysis
- SHAP dependence analysis
- Individual prediction explanations
- False-positive investigation


## ⚠️ Limitations

PHISHGUARD-X is a research, educational, and portfolio project.

Potential limitations include:

- WHOIS information may be unavailable for some domains.
- Network requests can fail or timeout.
- Domain popularity information can change over time.
- Domain age and expiration information depend on available WHOIS data.
- Web-page behavior features may depend on whether a page is reachable.
- Model predictions depend on the quality and distribution of the training data.
- Manual real-world examples are not representative of all internet traffic.
- The unseen validation set is limited in size and should not be treated as a production benchmark.
- A machine-learning prediction should not be treated as a definitive security guarantee.

## 🔮 Future Improvements

Potential future improvements include:

- Larger and more diverse phishing datasets
- Temporal validation
- Better handling of WHOIS failures
- Probability calibration
- Continuous model monitoring
- Automated model retraining
- Additional domain reputation signals
- Adversarial phishing URL testing
- API-based inference
- Production deployment
- Monitoring and logging

## 👨‍💻 Author

**Apoorv Kumar**

B.Tech Computer Science & Engineering

## 📄 License

This project is intended for educational, research, and portfolio purposes.

