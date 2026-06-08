from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "best_model.pkl"
SCALER_PATH = BASE_DIR / "models" / "scaler.pkl"
RAW_DATA_PATH = BASE_DIR.parent / "data" / "raw" / "teleco_churn.csv"
FRONTEND_DIST = BASE_DIR.parent / "frontend" / "dist"

MODEL = None
SCALER = None
MODEL_FEATURES = None
REFERENCE_DF = None
RAW_DATA_DF = None

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


def load_model_assets():
    global MODEL, SCALER, MODEL_FEATURES, REFERENCE_DF, RAW_DATA_DF

    if MODEL is not None and SCALER is not None and MODEL_FEATURES is not None and RAW_DATA_DF is not None:
        return

    MODEL = joblib.load(MODEL_PATH)
    SCALER = joblib.load(SCALER_PATH)

    raw_df = pd.read_csv(RAW_DATA_PATH)
    RAW_DATA_DF = raw_df.copy()
    reference_df = raw_df.drop(columns=["Churn"]).copy() if "Churn" in raw_df.columns else raw_df.copy()

    # Keep the raw TotalCharges values as strings to match the training pipeline,
    # which encoded TotalCharges as categorical dummies.
    reference_df["TotalCharges"] = reference_df["TotalCharges"].astype(str).fillna(" ")
    reference_df["tenure"] = pd.to_numeric(reference_df["tenure"], errors="coerce").fillna(0).astype(int)
    reference_df["MonthlyCharges"] = pd.to_numeric(reference_df["MonthlyCharges"], errors="coerce").fillna(0.0)

    REFERENCE_DF = reference_df
    MODEL_FEATURES = pd.get_dummies(REFERENCE_DF, drop_first=True).columns.tolist()


def build_input_vector(payload: dict) -> pd.DataFrame:
    load_model_assets()

    input_df = pd.DataFrame([payload])

    # Helper to robustly parse SeniorCitizen values coming from the frontend
    def _parse_senior(val):
        if pd.isna(val):
            return 0
        if isinstance(val, str):
            v = val.strip().lower()
            if v in ("yes", "y", "1", "true", "t"):
                return 1
            if v in ("no", "n", "0", "false", "f"):
                return 0
            # Some UIs send 'No' / 'Yes' or numeric strings like '0'/'1'
            try:
                return int(float(v))
            except Exception:
                return 0
        try:
            return int(val)
        except Exception:
            return 0

    # Ensure expected columns are present and properly typed
    expected_columns = [
        "gender",
        "SeniorCitizen",
        "Partner",
        "Dependents",
        "tenure",
        "PhoneService",
        "MultipleLines",
        "InternetService",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies",
        "Contract",
        "PaperlessBilling",
        "PaymentMethod",
        "MonthlyCharges",
        "TotalCharges",
    ]

    missing_columns = [col for col in expected_columns if col not in input_df.columns]
    if missing_columns:
        raise ValueError(f"Missing required fields: {', '.join(missing_columns)}")

    # Coerce SeniorCitizen into 0/1 regardless of how the frontend sends it
    input_df["SeniorCitizen"] = input_df["SeniorCitizen"].apply(_parse_senior)
    input_df["tenure"] = pd.to_numeric(input_df["tenure"], errors="coerce").fillna(0).astype(int)
    input_df["MonthlyCharges"] = pd.to_numeric(input_df["MonthlyCharges"], errors="coerce").fillna(0.0)
    input_df["TotalCharges"] = pd.to_numeric(input_df["TotalCharges"], errors="coerce").fillna(0.0)

    combined = pd.concat([REFERENCE_DF.iloc[:0], input_df], ignore_index=True, sort=False)
    encoded = pd.get_dummies(combined, drop_first=True)
    encoded = encoded.reindex(columns=MODEL_FEATURES, fill_value=0)

    return encoded.iloc[[-1]]


@app.route("/", methods=["GET"])
def root():
    if FRONTEND_DIST.exists():
        return send_from_directory(str(FRONTEND_DIST), "index.html")
    return jsonify({"message": "Telco Churn Prediction API is running", "status": "ok", "routes": ["/api/health", "/api/predict"]})


@app.route("/<path:path>", methods=["GET"])
def serve_frontend(path):
    if FRONTEND_DIST.exists():
        target = FRONTEND_DIST / path
        if target.exists():
            return send_from_directory(str(FRONTEND_DIST), path)
        return send_from_directory(str(FRONTEND_DIST), "index.html")
    return jsonify({"error": "Not found"}), 404
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/model-info", methods=["GET"])
def model_info():
    load_model_assets()

    raw = RAW_DATA_DF.copy()
    if "Churn" not in raw.columns:
        return jsonify({"error": "Raw data does not contain Churn column"}), 400

    df = raw.copy()
    y = df["Churn"].map({"No": 0, "Yes": 1}).astype(int)
    # replace churn column with numeric values (same as training notebook) so
    # get_dummies won't create extra churn_* columns
    df["Churn"] = y

    # One-hot encode full dataframe same as training
    df_encoded = pd.get_dummies(df, drop_first=True)
    X = df_encoded.drop(columns=["Churn"]) if "Churn" in df_encoded.columns else df_encoded.copy()

    # Split using same parameters as in training notebook
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Align test columns with model features, fill missing columns with 0
    model_features = getattr(MODEL, "feature_names_in_", None)
    if model_features is not None:
        X_test_aligned = X_test.reindex(columns=model_features, fill_value=0)
    else:
        X_test_aligned = X_test

    # Scale and predict
    X_test_scaled = SCALER.transform(X_test_aligned)
    preds = MODEL.predict(X_test_scaled)
    probs = MODEL.predict_proba(X_test_scaled)[:, 1]

    perf = {
        "accuracy": float(accuracy_score(y_test, preds)),
        "precision": float(precision_score(y_test, preds, zero_division=0)),
        "recall": float(recall_score(y_test, preds, zero_division=0)),
        "f1_score": float(f1_score(y_test, preds, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, probs)),
    }

    # Feature importance from model coefficients (top 10)
    feature_importance = []
    coefs = getattr(MODEL, "coef_", None)
    mf = MODEL_FEATURES if MODEL_FEATURES is not None else getattr(MODEL, "feature_names_in_", None)
    if coefs is not None:
        coef = coefs[0]
        if mf is not None and len(coef) == len(mf):
            index = list(mf)
        else:
            # Fallback to generic feature names when the model coefficient length doesn't match expected features
            index = [f"feature_{i}" for i in range(len(coef))]

        abscoef = pd.Series(coef, index=index).abs()
        top = abscoef.sort_values(ascending=False).head(10)
        feature_importance = [{"feature": f, "importance": float(abscoef.loc[f])} for f in top.index]

    return jsonify({
        "best_model": type(MODEL).__name__,
        "performance": perf,
        "feature_importance": feature_importance,
    })


@app.route("/api/dashboard-stats", methods=["GET"])
def dashboard_stats():
    load_model_assets()

    raw = RAW_DATA_DF.copy()
    # Basic validation
    if raw is None or raw.empty:
        return jsonify({"error": "No data available"}), 400

    # Ensure types
    raw["MonthlyCharges"] = pd.to_numeric(raw.get("MonthlyCharges", 0), errors="coerce").fillna(0.0)
    if "tenure" in raw.columns:
        raw["tenure"] = pd.to_numeric(raw["tenure"], errors="coerce").fillna(0).astype(int)

    # Map churn to numeric 0/1 for aggregation
    if "Churn" in raw.columns:
        raw["_churn_num"] = raw["Churn"].map({"No": 0, "Yes": 1}).fillna(0).astype(int)
    else:
        raw["_churn_num"] = 0

    total_customers = int(len(raw))
    churned_customers = int(raw["_churn_num"].sum())
    churn_rate = (churned_customers / total_customers * 100) if total_customers > 0 else 0.0

    monthly_stats = {
        "mean": float(raw["MonthlyCharges"].mean()),
        "median": float(raw["MonthlyCharges"].median()),
        "min": float(raw["MonthlyCharges"].min()),
        "max": float(raw["MonthlyCharges"].max()),
    }

    tenure_stats = None
    if "tenure" in raw.columns:
        tenure_stats = {
            "mean": float(raw["tenure"].mean()),
            "median": int(raw["tenure"].median()),
            "min": int(raw["tenure"].min()),
            "max": int(raw["tenure"].max()),
        }

    contract_distribution = raw["Contract"].value_counts(dropna=True).to_dict() if "Contract" in raw.columns else {}
    payment_distribution = raw["PaymentMethod"].value_counts(dropna=True).to_dict() if "PaymentMethod" in raw.columns else {}

    churn_by_contract = {}
    if "Contract" in raw.columns:
        grp = raw.groupby("Contract")["_churn_num"].mean() * 100
        churn_by_contract = {k: float(v) for k, v in grp.to_dict().items()}

    return jsonify({
        "total_customers": total_customers,
        "churned_customers": churned_customers,
        "churn_rate": float(churn_rate),
        "monthly_charges_stats": monthly_stats,
        "tenure_stats": tenure_stats,
        "contract_distribution": contract_distribution,
        "payment_distribution": payment_distribution,
        "churn_by_contract": churn_by_contract,
    })


@app.route("/api/predict", methods=["POST"])
def predict():
    request_data = request.get_json(silent=True)
    if not request_data:
        return jsonify({"error": "Invalid JSON payload"}), 400

    try:
        input_vector = build_input_vector(request_data)
        scaled_vector = SCALER.transform(input_vector)
        probability = float(MODEL.predict_proba(scaled_vector)[:, 1][0])
        prediction = int(MODEL.predict(scaled_vector)[0])

        churn_status = "Yes" if prediction == 1 else "No"
        if probability >= 0.7:
            risk_level = "High"
        elif probability >= 0.3:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        message = (
            "This customer has a high risk of churn." if risk_level == "High"
            else "This customer has a moderate risk of churn." if risk_level == "Medium"
            else "This customer has a low risk of churn."
        )

        return jsonify({
            "churn_status": churn_status,
            "probability": probability,
            "risk_level": risk_level,
            "message": message,
        })

    except Exception as exc:
        app.logger.exception("Prediction error")
        return jsonify({"error": "Prediction failed", "details": str(exc)}), 400


if __name__ == "__main__":
    load_model_assets()
    app.run(host="0.0.0.0", port=5000, debug=True)
