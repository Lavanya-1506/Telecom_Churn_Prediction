# 🎓 AI Student Performance Tracker

## 📌 Internship Details

| Field            | Details                        |
| ---------------- | ------------------------------ |
| **Intern ID**    | CITS2184                       |
| **Intern Name**  | Lavanya Vaidya                 |
| **Duration**     | 4 Weeks                        |
| **Project Name** | Telecom Churn Prediction       |
| **Domain**       | Machine Learning               |

---

# 📖 Project Overview
# Telecom Customer Churn Prediction System

The Telecom Customer Churn Prediction System is a Machine Learning-based web application designed to identify customers who are likely to discontinue telecom services. Customer churn is one of the most significant challenges faced by telecom companies, as acquiring new customers is often more expensive than retaining existing ones.

This project leverages historical customer data, including demographic information, service subscriptions, contract details, and billing information, to predict the likelihood of customer churn. By analyzing customer behavior patterns, the system helps telecom providers proactively identify at-risk customers and implement retention strategies.

The application provides data-driven insights through interactive visualizations, churn prediction models, feature importance analysis, and business recommendations, enabling organizations to improve customer retention and reduce revenue loss.

---

# 🎯 Project Scope

* Customer churn prediction using Machine Learning algorithms.

* Data cleaning and preprocessing.

* Exploratory Data Analysis (EDA).

* Feature engineering and transformation.

* Training and comparison of multiple classification models.

* Model evaluation using standard performance metrics.

* Feature importance analysis.

* Interactive dashboard for business insights.

* Customer churn prediction interface.

* Flask REST API integration.

* React-based frontend application.

---

# ✨ Key Features

* Customer Churn Prediction using Machine Learning
* Exploratory Data Analysis (EDA) with Visualizations
* Feature Engineering for Improved Model Performance
* Multiple Model Training and Comparison
* Model Evaluation using Accuracy, Precision, Recall, F1-Score, and ROC-AUC
* Feature Importance Analysis to Identify Churn Factors
* Interactive Dashboard for Business Insights
* Real-Time Churn Prediction Interface
* Flask REST API Integration
* React-Based User Interface
* Customer Risk Level Classification (Low, Medium, High)

---

# 🔄 Project Workflow

```text
Telecom Customer Churn Dataset
                │
                ▼
      Data Understanding
                │
                ▼
        Data Cleaning
 (Missing Values, Duplicates,
 Data Type Conversion)
                │
                ▼
  Exploratory Data Analysis
     (EDA & Visualizations)
                │
                ▼
      Feature Engineering
 (Service Count, Loyalty Score,
 Average Spending, etc.)
                │
                ▼
        Data Encoding &
         Feature Scaling
                │
                ▼
      Train-Test Splitting
                │
                ▼
        Model Training
(Logistic Regression, Decision Tree,
 Random Forest, XGBoost)
                │
                ▼
       Model Evaluation
(Accuracy, Precision, Recall,
 F1-Score, ROC-AUC)
                │
                ▼
    Feature Importance Analysis
                │
                ▼
      SHAP Explainability
                │
                ▼
        Best Model Selection
                │
                ▼
          Model Saving
                │
                ▼
          Flask API
                │
                ▼
         React Frontend
                │
                ▼
     Customer Churn Prediction
                │
                ▼
      Dashboard & Insights
```

---

# 🏗️ System Architecture

```text
+--------------------+
|   Telecom Dataset  |
+--------------------+
           |
           v
+--------------------+
| Data Preprocessing |
+--------------------+
           |
           v
+--------------------+
|        EDA         |
+--------------------+
           |
           v
+--------------------+
| Feature Engineering|
+--------------------+
           |
           v
+--------------------+
| Model Training     |
| LR, DT, RF, XGB    |
+--------------------+
           |
           v
+--------------------+
| Model Evaluation   |
+--------------------+
           |
           v
+--------------------+
| Best Model Saving  |
+--------------------+
           |
           v
+--------------------+
| Flask REST API     |
+--------------------+
           |
           v
+--------------------+
| React Frontend     |
+--------------------+
           |
           v
+--------------------+
| Prediction Results |
+--------------------+
```

---

# 🤖 Machine Learning Models Used

The following algorithms were implemented and evaluated:

* Logistic Regression
* Decision Tree Regression
* Random Forest Regression
* XGBoost Regressor

The best-performing model was selected based on evaluation metrics.

---

# 🛠️ Technology Stack

* Frontend      : React.js, Vite, Axios
* Backend       : Flask, Flask-CORS
* Machine Learning : Scikit-Learn, XGBoost, Imbalanced-Learn
* Data Analysis : Pandas, NumPy
* Visualization : Matplotlib, Seaborn, Plotly, Missingno
* Model Storage : Joblib
* Development   : Jupyter Notebook, VS Code
* Version Control : Git, GitHub
* Dataset       : IBM Telco Customer Churn Dataset

---

# 📁 Project Structure

```text
TELECOM_CHURN_PREDICTION/
│
├── backend/
│   │
│   ├── __pycache__/
│   │
│   ├── models/
│   │   ├── best_model.pkl
│   │   ├── best_model.pkl.bak
│   │   ├── scaler.pkl
│   │   └── scaler.pkl.bak
│   │
│   ├── notebooks/
│   │   ├── business_insights.ipynb
│   │   ├── data_cleaning.ipynb
│   │   ├── data_understanding.ipynb
│   │   ├── eda.ipynb
│   │   ├── feature_engineering.ipynb
│   │   ├── feature_importance.ipynb
│   │   ├── model_training.ipynb
│   │   └── shap_analysis.ipynb
│   │
│   ├── reports/
│   │   └── business_summary.csv
│   │
│   ├── app.py
│   └── requirements.txt
│
├── data/
│   │
│   ├── processed/
│   │   ├── cleaned_telco.csv
│   │   └── engineered_telco.csv
│   │
│   └── raw/
│       └── telco_churn.csv
│
├── frontend/
│   │
│   ├── node_modules/
│   │
│   ├── public/
│   │
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── .gitignore
│   ├── eslint.config.js
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── README.md
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

---

⚙️ Installation & Setup

🚀 How to Run the Project

* Clone Repository
  
https://github.com/Lavanya-1506/Telecom_Churn_Prediction.git
* Install Dependencies
  
pip install -r requirements.txt
* Run Frontend
  
npm run dev
* Run Application
  
python app.py

---

# 🎯 Project Outcomes

* Developed an end-to-end Machine Learning system for predicting telecom customer churn.
* Performed comprehensive data cleaning, preprocessing, and feature engineering on telecom customer data.
* Conducted Exploratory Data Analysis (EDA) to identify customer behavior patterns and churn trends.
* Trained and compared multiple Machine Learning models, including Logistic Regression, Decision Tree, Random Forest, and XGBoost.
* Evaluated model performance using Accuracy, Precision, Recall, F1-Score, ROC-AUC Score, and Confusion Matrix.
* Identified key factors influencing customer churn through feature importance analysis.
* Built a predictive model capable of classifying customers as likely to churn or remain with the company.
* Developed a Flask-based REST API for model integration and prediction services.
* Created an interactive React dashboard for visualizing churn insights and prediction results.

---

# 👨‍💻 Developed By

**Lavanya Vaidya**

**Machine Learning Intern** 

---



