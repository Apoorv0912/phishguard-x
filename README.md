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
- PostgreSQL-ready workflow
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

📊 Dataset
PHISHGUARD-X uses multiple raw data sources for building the phishing URL detection dataset and supporting domain-intelligence features.

Raw Data Sources
The original raw files are stored under:
data/raw/


File                                  Purpose
1.Benign_list_big_final.csv  Source of legitimate/benign URLs
2.online-valid.csv            Source of phishing URLs
tranco_GQJ9K.csv              Tranco domain ranking used for web-traffic/domain popularity feature extraction     
These raw datasets are processed through the project's feature-extraction pipeline before being used for EDA, feature engineering, and machine-learning experiments.


🧬 Feature Extraction
Feature extraction is implemented in:
src/features/url_features.py
The feature-extraction pipeline analyzes URL structure, domain information, DNS/WHOIS information, web traffic ranking, and webpage behavior.
The extraction pipeline initially generates the following fields:
Domain
Have_IP
Have_At
URL_Length
URL_Depth
Redirection
https_Domain
TinyURL
Prefix/Suffix
DNS_Record
Web_Traffic
Domain_Age
Domain_End
iFrame
Mouse_Over
Right_Click
Web_Forwards
Label

Feature Categories

URL Structure

Have_IP
Have_At
URL_Length
URL_Depth
Redirection
https_Domain
TinyURL
Prefix/Suffix

Domain Intelligence

DNS_Record
Web_Traffic
Domain_Age
Domain_End

Web Behavior

iFrame
Mouse_Over
Right_Click
Web_Forwards

Domain is retained for domain-level analysis and grouping.
Label is the target variable.

🧹 Data Processing
After feature extraction, the generated datasets are processed through the project's EDA and feature-engineering workflow.

The final machine-learning feature set contains 15 features.

Right_Click is excluded from the final model because it was found to be constant and therefore provided no useful variation for classification.

The final model features are:
Have_IP
Have_At
URL_Length
URL_Depth
Redirection
https_Domain
TinyURL
Prefix/Suffix
DNS_Record
Web_Traffic
Domain_Age
Domain_End
iFrame
Mouse_Over
Web_Forwards

📁 Processed Dataset
The final processed dataset is stored at:
data/processed/phishguard_features_final_11500.csv

Dataset summary:

Property                    Value

Total URLs                   11,500
Legitimate URLs              6,500
Phishing URLs                5,000 
ML Features                  15
Target                       Label
Train/Test Domain Overlap    0

🔬 Domain-Aware Evaluation

A domain-aware train/test split is used to reduce domain leakage.

Domain is used as the grouping variable with GroupShuffleSplit.

Training rows: 9,111
Testing rows: 2,389

Training domains: 3,953
Testing domains: 989

Domain overlap: 0

This prevents the same domain from appearing in both training and testing groups.

🤖 Baseline Models
The following baseline models were evaluated:





Model             Accuracy Precision Recall  F1  ROC-AUC       
Decision Tree       0.9008  0,8921  0.8680  0.8799  0.9586
Random Forest       0.8853  0.8616  0.8650  0.8633  0.9568
Logistic Regression 0.8757  0.8240  0.8940  0.8576  0.9105
KNN                 0.8397  0.7454  0.9370  0.8303  0.8795
XGBoost             0.8472  0.7900  0.8650  0.8258  0.9560
SVM RBF             0.8062  0.8604  0.6410  0.7347  0.9220


⚙️ XGBoost Hyperparameter Tuning

XGBoost was optimized using RandomizedSearchCV with GroupKFold.

Best Parameters

n_estimators = 200
max_depth = 5
learning_rate = 0.02
subsample = 0.8
colsample_bytree = 0.9

The best group cross-validation F1 score was:
0.8402

🏆 Final Tuned XGBoost Model
The final tuned XGBoost model achieved the following performance on the domain-aware held-out test set:

Metric         Score

Accuracy       0.9108
Precision      0.9263
Recall         0.8550
F1 Score       0.8892
ROC-AUC        0.9634

Confusion Matrix
                 Predicted
                 Legit  Phishing

Actual Legit      1321      68
Actual Phishing   145      855

🎚️ Classification Threshold
The classification threshold was evaluated using cross-validated training probabilities.

The selected threshold is:
0.48

The final decision rule is:
Phishing probability >= 0.48
        → PHISHING

Phishing probability < 0.48
        → LEGITIMATE

The threshold is saved as:
models/classification_threshold.joblib

🧠 Explainable AI with SHAP
PHISHGUARD-X uses SHAP (SHapley Additive exPlanations) to explain model predictions.

SHAP is used for:

1.Global feature importance
2.Individual URL explanations
3.False-positive analysis
4.Understanding the direction and magnitude of feature contributions

The global mean absolute SHAP analysis identified the following among the most influential features:

URL_Length
Prefix/Suffix
URL_Depth
Web_Traffic
iFrame
Web_Forwards
Domain_End
Domain_Age

The trained SHAP explainer is stored at:

models/shap_explainer.joblib

🧪 Unseen Validation
An additional unseen validation dataset containing 100 legitimate URLs was used as a sanity check.

Results:
Total validation URLs : 100
Legitimate detected   : 97
False positives       : 3
False positive rate   : 3%

The identified false positives were:

cloud.microsoft
workers.dev
cloudflare-dns.com

SHAP analysis was performed on these cases to investigate why the model assigned elevated phishing probabilities.

This validation set is an additional sanity check and should not be interpreted as a general estimate of production-world performance.

🌐 Real-World Sanity Checks
The model was additionally tested on manually selected well-known legitimate and suspicious-looking URLs.

Examples of legitimate domains correctly classified during sanity testing included:

google.com
microsoft.com
apple.com
github.com
youtube.com

Suspicious-looking test domains were also classified as phishing during the sanity checks.

These manually selected examples are intended for demonstration and sanity checking rather than statistical estimation of real-world performance.

🖥️ Streamlit Application
PHISHGUARD-X includes an interactive Streamlit security dashboard.

Application Sections
Command Center
URL Scanner
CSV Scanner
AI Explanation
URL Fingerprint
Model Lab
Validation Lab
Scan History
About

🔎 URL Scanner
The URL Scanner allows users to analyze an individual URL.

The scanner provides:

1.Phishing probability
2.Legitimate probability
3.Risk level
4.Final security verdict
5.SHAP explanation
6.Security signal analysis

The application automatically extracts the required features and passes them to the trained XGBoost model.

📂 CSV Scanner
The CSV Scanner enables batch phishing detection.

Supported functionality includes:

CSV upload
Automatic URL-column detection
Batch URL feature extraction
Batch XGBoost prediction
Phishing/legitimate counts
Threat-level classification
Result filtering
Downloadable scan results

Expected CSV structure:
url
https://example.com
https://example.org
https://example.net

The scanner can also detect common URL-column names such as:
url
URL
link
website
domain

🔐 URL Fingerprint
The URL Fingerprint section provides a visual summary of the URL's security signals.

The analysis is grouped into:
URL Structure
Domain Intelligence
Web Behavior

It also displays:

1.Phishing probability
2.Classification threshold
3.Security signal distribution

📈 Model Lab
The Model Lab presents the baseline model comparison and final tuned XGBoost performance.

It allows users to inspect:

1.Accuracy
2.Precision
3.Recall
4.F1 score
5.ROC-AUC
6.Confusion matrices
7.ROC curves
8.Precision-Recall curves
9.Tuned vs baseline performance

🧪 Validation Lab
The Validation Lab provides the results of the unseen validation experiment.

It displays:

1.Total validation URLs
2.Legitimate detections
3.False positives
4.False-positive rate
5.False-positive URLs

🗂️ Scan History

The application maintains a session-level history of recently scanned URLs.

The history includes:

1.URL
2.Phishing probability
3.Verdict
4.Risk level

📁 Project Structure
phishguard-x/
│
├── data/
│   ├── raw/
│   │   ├── 1.Benign_list_big_final.csv
│   │   ├── 2.online-valid.csv
│   │   └── tranco_GQJ9K.csv
│   │
│   ├── processed/
│   │   ├── legitimate_features.csv
│   │   ├── phishing_features.csv
│   │   ├── phishguard_features.csv
│   │   ├── improved_legitimate_raw.csv
│   │   ├── augmented_legitimate_features.csv
│   │   └── phishguard_features_final_11500.csv
│   │
│   └── validation/
│       ├── unseen_validation.csv
│       ├── false_positive_shap_summary.csv
│       └── checkpoints/
│
├── models/
│   ├── tuned_xgboost_final.joblib
│   ├── final_features.joblib
│   ├── classification_threshold.joblib
│   └── shap_explainer.joblib
│
├── notebooks/
│   ├── 01_feature_extraction.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_baseline_model.ipynb
│   ├── 05_shap_explainability.ipynb
│   └── 06_google_false_positive_debugging.ipynb
│
├── src/
│   ├── features/
│   │   └── url_features.py
│   ├── eda/
│   ├── preprocessing/
│   └── explainability/
│
├── app.py
├── README.md
└── requirements.txt

🛠️ Technologies Used

Python
Pandas
NumPy
Scikit-learn
XGBoost
SHAP
Matplotlib
SciPy
Requests
Python-WHOIS
Streamlit
Joblib

⚙️ Installation
Clone the repository:

git clone <YOUR_GITHUB_REPOSITORY_URL>
cd phishguard-x

Create a virtual environment:

python -m venv .venv

Activate the environment on Windows:

.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

▶️ Run the Application

Start the Streamlit application:

python -m streamlit run app.py
The application will then open in the browser.

💾 Model Artifacts
The trained model and supporting artifacts are stored in:
models/
Important artifacts:
tuned_xgboost_final.joblib
final_features.joblib
classification_threshold.joblib
shap_explainer.joblib
These artifacts allow the Streamlit application to perform inference and explanations without retraining the model during application startup.

📊 Generated Analysis
The project also generates analytical visualizations for:

Baseline model comparison
Confusion matrices
ROC curves
Precision-Recall curves
Tuned vs baseline XGBoost
Threshold analysis
SHAP feature importance
SHAP beeswarm analysis
SHAP dependence analysis
Individual prediction explanations
False-positive investigation

⚠️ Limitations
PHISHGUARD-X is a research, educational, and portfolio project.

Potential limitations include:

WHOIS information may be unavailable for some domains.
Network requests can fail or timeout.
Domain popularity information can change over time.
Domain age and expiration information depend on available WHOIS data.
Web-page behavior features may depend on whether a page is reachable.
Model predictions depend on the quality and distribution of the training data.
Manual real-world examples are not representative of all internet traffic.
The unseen validation set is limited in size and should not be treated as a production benchmark.
A machine-learning prediction should not be treated as a definitive security guarantee.

🔮 Future Improvements
Potential future improvements include:

Larger and more diverse phishing datasets
Temporal validation
Better handling of WHOIS failures
Probability calibration
Continuous model monitoring
Automated model retraining
Additional domain reputation signals
Adversarial phishing URL testing
API-based inference
Production deployment
Monitoring and logging

👨‍💻 Author
Apoorv Kumar
B.Tech Computer Science & Engineering

📄 License
This project is intended for educational, research, and portfolio purposes.