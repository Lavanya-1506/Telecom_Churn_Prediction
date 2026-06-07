import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

class DataPreprocessor:
    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.numerical_features = ['tenure', 'MonthlyCharges', 'TotalCharges']
        self.categorical_features = ['gender', 'Partner', 'Dependents', 'PhoneService',
                                      'MultipleLines', 'InternetService', 'OnlineSecurity',
                                      'OnlineBackup', 'DeviceProtection', 'TechSupport',
                                      'StreamingTV', 'StreamingMovies', 'Contract',
                                      'PaperlessBilling', 'PaymentMethod']
        
    def load_data(self, filepath):
        """Load and initial inspect dataset"""
        df = pd.read_csv(filepath)
        print(f"Dataset shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        return df
    
    def handle_missing_values(self, df):
        """Handle missing values"""
        # Replace empty strings with NaN
        df = df.replace(' ', np.nan)
        
        # Check missing values
        print("\nMissing values before handling:")
        print(df.isnull().sum())
        
        # For TotalCharges, convert to numeric and fill with median
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
        df['TotalCharges'].fillna(df['TotalCharges'].median(), inplace=True)
        
        # Drop any remaining rows with missing values
        df.dropna(inplace=True)
        
        print("\nMissing values after handling:")
        print(df.isnull().sum())
        
        return df
    
    def remove_duplicates(self, df):
        """Remove duplicate rows"""
        initial_shape = df.shape
        df = df.drop_duplicates()
        print(f"\nRemoved {initial_shape[0] - df.shape[0]} duplicate rows")
        return df
    
    def convert_data_types(self, df):
        """Convert data types appropriately"""
        # Convert SeniorCitizen to categorical
        df['SeniorCitizen'] = df['SeniorCitizen'].astype('object')
        
        # Ensure TotalCharges is float
        df['TotalCharges'] = df['TotalCharges'].astype(float)
        
        return df
    
    def encode_categorical_features(self, df):
        """Encode categorical features"""
        df_encoded = df.copy()
        
        # Binary encoding for binary categorical features
        binary_features = ['gender', 'Partner', 'Dependents', 'PhoneService',
                          'PaperlessBilling', 'Churn']
        
        for feature in binary_features:
            if feature in df_encoded.columns:
                le = LabelEncoder()
                df_encoded[feature] = le.fit_transform(df_encoded[feature])
                self.label_encoders[feature] = le
        
        # One-hot encoding for multi-category features
        multi_category_features = ['MultipleLines', 'InternetService', 'OnlineSecurity',
                                   'OnlineBackup', 'DeviceProtection', 'TechSupport',
                                   'StreamingTV', 'StreamingMovies', 'Contract',
                                   'PaymentMethod']
        
        df_encoded = pd.get_dummies(df_encoded, columns=multi_category_features, drop_first=True)
        
        return df_encoded
    
    def detect_outliers(self, df):
        """Detect and handle outliers using IQR method"""
        outlier_summary = {}
        
        for feature in self.numerical_features:
            if feature in df.columns:
                Q1 = df[feature].quantile(0.25)
                Q3 = df[feature].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = df[(df[feature] < lower_bound) | (df[feature] > upper_bound)]
                outlier_summary[feature] = len(outliers)
                
                # Cap outliers instead of removing
                df[feature] = df[feature].clip(lower_bound, upper_bound)
        
        print("\nOutliers detected and capped:")
        for feature, count in outlier_summary.items():
            print(f"{feature}: {count} outliers")
        
        return df
    
    def scale_features(self, X_train, X_test):
        """Scale numerical features"""
        # Ensure numerical features exist in the data
        numerical_present = [f for f in self.numerical_features if f in X_train.columns]
        
        X_train_scaled = X_train.copy()
        X_test_scaled = X_test.copy()
        
        X_train_scaled[numerical_present] = self.scaler.fit_transform(X_train[numerical_present])
        X_test_scaled[numerical_present] = self.scaler.transform(X_test[numerical_present])
        
        return X_train_scaled, X_test_scaled
    
    def create_features(self, df):
        """Feature Engineering - Create new features"""
        df_fe = df.copy()
        
        # Service Count - Count of services subscribed
        service_columns = ['PhoneService', 'MultipleLines', 'InternetService', 
                          'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                          'TechSupport', 'StreamingTV', 'StreamingMovies']
        
        # Convert Yes/No to binary for counting
        for col in service_columns:
            if col in df_fe.columns:
                df_fe[f'{col}_binary'] = df_fe[col].apply(lambda x: 1 if x == 'Yes' else 0)
        
        service_binary_cols = [col for col in df_fe.columns if col.endswith('_binary')]
        if service_binary_cols:
            df_fe['ServiceCount'] = df_fe[service_binary_cols].sum(axis=1)
        
        # Customer Loyalty Score
        max_tenure = df_fe['tenure'].max()
        df_fe['LoyaltyScore'] = df_fe['tenure'] / max_tenure
        
        # Average Monthly Spending
        df_fe['AvgMonthlySpending'] = df_fe['TotalCharges'] / (df_fe['tenure'] + 1)  # +1 to avoid division by zero
        
        # Revenue Category
        df_fe['RevenueCategory'] = pd.qcut(df_fe['MonthlyCharges'], 
                                           q=3, 
                                           labels=['Low', 'Medium', 'High'])
        
        # Tenure Group
        df_fe['TenureGroup'] = pd.cut(df_fe['tenure'], 
                                      bins=[0, 12, 24, 48, 72], 
                                      labels=['0-1 Year', '1-2 Years', '2-4 Years', '4-6 Years'])
        
        return df_fe
    
    def prepare_data(self, filepath):
        """Complete data preprocessing pipeline"""
        print("="*50)
        print("Starting Data Preprocessing Pipeline")
        print("="*50)
        
        # Load data
        df = self.load_data(filepath)
        
        # Remove customerID as it's not useful for prediction
        if 'customerID' in df.columns:
            df = df.drop('customerID', axis=1)
        
        # Handle missing values
        df = self.handle_missing_values(df)
        
        # Remove duplicates
        df = self.remove_duplicates(df)
        
        # Convert data types
        df = self.convert_data_types(df)
        
        # Create new features
        df = self.create_features(df)
        
        # Encode categorical features
        df_encoded = self.encode_categorical_features(df)
        
        # Separate features and target
        X = df_encoded.drop('Churn', axis=1)
        y = df_encoded['Churn']
        
        # Handle outliers
        X = self.detect_outliers(X)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                            random_state=42, stratify=y)
        
        # Scale features
        X_train_scaled, X_test_scaled = self.scale_features(X_train, X_test)
        
        print(f"\nFinal training set shape: {X_train_scaled.shape}")
        print(f"Final test set shape: {X_test_scaled.shape}")
        print(f"Churn rate in training: {y_train.mean():.2%}")
        print(f"Churn rate in test: {y_test.mean():.2%}")
        
        return X_train_scaled, X_test_scaled, y_train, y_test, df