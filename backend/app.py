from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
from preprocess import DataPreprocessor
from model_training import ModelTrainer
import json

app = Flask(__name__)
CORS(app)

# Global variables for models and preprocessor
model_trainer = None
preprocessor = None
best_model = None

def initialize_system():
    """Initialize the system by training models or loading saved ones"""
    global model_trainer, preprocessor, best_model
    
    try:
        # Try to load saved model
        best_model = joblib.load('models/best_model.pkl')
        model_trainer = joblib.load('models/model_trainer.pkl')
        print("✅ Loaded saved model successfully!")
    except:
        print("🔄 Training new models...")
        # Initialize preprocessor
        preprocessor = DataPreprocessor()
        
        # Prepare data
        X_train, X_test, y_train, y_test, df = preprocessor.prepare_data('../data/WA_Fn-UseC_-Telco-Customer-Churn.csv')
        
        # Train models
        model_trainer = ModelTrainer()
        model_trainer.train_models(X_train, y_train)
        
        # Evaluate models
        comparison_df = model_trainer.evaluate_models(X_test, y_test)
        
        # Calculate feature importance
        model_trainer.calculate_feature_importance(X_train)
        
        # Save best model
        best_model = model_trainer.best_model
        model_trainer.save_best_model()
        
        # Save feature names for prediction
        feature_names = X_train.columns.tolist()
        joblib.dump(feature_names, 'models/feature_names.pkl')
        joblib.dump(preprocessor.scaler, 'models/scaler.pkl')
        joblib.dump(preprocessor.label_encoders, 'models/label_encoders.pkl')
        
        print("✅ Model training completed!")

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Telecom Churn Prediction API is running'})

@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict churn for a single customer"""
    try:
        data = request.json
        
        # Create DataFrame from input
        input_data = pd.DataFrame([data])
        
        # Preprocess input
        processed_input = preprocess_input(input_data)
        
        # Make prediction
        prediction = best_model.predict(processed_input)[0]
        probability = best_model.predict_proba(processed_input)[0][1]
        
        # Determine risk level
        if probability < 0.3:
            risk_level = "Low"
        elif probability < 0.7:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        response = {
            'prediction': int(prediction),
            'churn_status': 'Likely to Churn' if prediction == 1 else 'Not Likely to Churn',
            'probability': float(probability),
            'risk_level': risk_level,
            'message': f"Customer is {risk_level} risk of churning with {probability:.1%} probability"
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/batch-predict', methods=['POST'])
def batch_predict():
    """Predict churn for multiple customers"""
    try:
        data = request.json
        customers = data.get('customers', [])
        
        results = []
        for customer in customers:
            input_data = pd.DataFrame([customer])
            processed_input = preprocess_input(input_data)
            prediction = best_model.predict(processed_input)[0]
            probability = best_model.predict_proba(processed_input)[0][1]
            
            results.append({
                'customer_id': customer.get('customerID', 'Unknown'),
                'churn_prediction': int(prediction),
                'churn_probability': float(probability)
            })
        
        return jsonify({'results': results})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Get information about the trained model"""
    if model_trainer and model_trainer.best_model_name:
        return jsonify({
            'best_model': model_trainer.best_model_name,
            'performance': model_trainer.results[model_trainer.best_model_name],
            'feature_importance': model_trainer.feature_importance['Random Forest'].head(10).to_dict('records')
        })
    else:
        return jsonify({'error': 'Model not trained yet'}), 404

@app.route('/api/dashboard-stats', methods=['GET'])
def dashboard_stats():
    """Get statistics for dashboard"""
    try:
        # Load original data for statistics
        df = pd.read_csv('../data/WA_Fn-UseC_-Telco-Customer-Churn.csv')
        
        # Calculate statistics
        total_customers = len(df)
        churned_customers = df[df['Churn'] == 'Yes'].shape[0]
        churn_rate = (churned_customers / total_customers) * 100
        
        # Contract distribution
        contract_dist = df['Contract'].value_counts().to_dict()
        
        # Payment method distribution
        payment_dist = df['PaymentMethod'].value_counts().to_dict()
        
        # Internet service distribution
        internet_dist = df['InternetService'].value_counts().to_dict()
        
        # Monthly charges statistics
        monthly_charges_stats = {
            'mean': float(df['MonthlyCharges'].mean()),
            'median': float(df['MonthlyCharges'].median()),
            'min': float(df['MonthlyCharges'].min()),
            'max': float(df['MonthlyCharges'].max())
        }
        
        # Tenure statistics
        tenure_stats = {
            'mean': float(df['tenure'].mean()),
            'median': float(df['tenure'].median()),
            'min': float(df['tenure'].min()),
            'max': float(df['tenure'].max())
        }
        
        # Churn by contract type
        churn_by_contract = df.groupby('Contract')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100).to_dict()
        
        # Churn by payment method
        churn_by_payment = df.groupby('PaymentMethod')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100).to_dict()
        
        return jsonify({
            'total_customers': total_customers,
            'churned_customers': churned_customers,
            'churn_rate': churn_rate,
            'contract_distribution': contract_dist,
            'payment_distribution': payment_dist,
            'internet_distribution': internet_dist,
            'monthly_charges_stats': monthly_charges_stats,
            'tenure_stats': tenure_stats,
            'churn_by_contract': churn_by_contract,
            'churn_by_payment': churn_by_payment
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def preprocess_input(df):
    """Preprocess single customer input for prediction"""
    # This function should mirror the preprocessing done during training
    # For now, we'll use the preprocessor from training
    global preprocessor
    
    if preprocessor is None:
        preprocessor = DataPreprocessor()
    
    # Create features
    df = preprocessor.create_features(df)
    
    # Encode categorical features
    df_encoded = preprocessor.encode_categorical_features(df)
    
    # Load feature names from training
    feature_names = joblib.load('models/feature_names.pkl')
    
    # Ensure all features are present
    for feature in feature_names:
        if feature not in df_encoded.columns:
            df_encoded[feature] = 0
    
    # Select only features used in training
    df_encoded = df_encoded[feature_names]
    
    # Scale features
    scaler = joblib.load('models/scaler.pkl')
    numerical_features = ['tenure', 'MonthlyCharges', 'TotalCharges']
    numerical_present = [f for f in numerical_features if f in df_encoded.columns]
    df_encoded[numerical_present] = scaler.transform(df_encoded[numerical_present])
    
    return df_encoded

if __name__ == '__main__':
    initialize_system()
    app.run(debug=True, port=5000)