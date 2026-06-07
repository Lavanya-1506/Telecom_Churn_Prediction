import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                           f1_score, roc_auc_score, confusion_matrix,
                           classification_report)
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

class ModelTrainer:
    def __init__(self):
        self.models = {
            'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
            'Decision Tree': DecisionTreeClassifier(random_state=42, max_depth=10),
            'Random Forest': RandomForestClassifier(random_state=42, n_estimators=100),
            'XGBoost': XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss')
        }
        self.trained_models = {}
        self.results = {}
        self.best_model = None
        self.best_model_name = None
        self.feature_importance = {}
        
    def train_models(self, X_train, y_train):
        """Train all models"""
        print("="*50)
        print("Training Models")
        print("="*50)
        
        for name, model in self.models.items():
            print(f"\nTraining {name}...")
            model.fit(X_train, y_train)
            self.trained_models[name] = model
            print(f"{name} training completed!")
        
        return self.trained_models
    
    def evaluate_models(self, X_test, y_test):
        """Evaluate all trained models"""
        print("\n" + "="*50)
        print("Evaluating Models")
        print("="*50)
        
        results_list = []
        
        for name, model in self.trained_models.items():
            print(f"\nEvaluating {name}...")
            
            # Predictions
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)[:, 1]
            
            # Calculate metrics
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            roc_auc = roc_auc_score(y_test, y_pred_proba)
            
            # Store results
            self.results[name] = {
                'model': model,
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'roc_auc': roc_auc,
                'confusion_matrix': confusion_matrix(y_test, y_pred),
                'predictions': y_pred,
                'probabilities': y_pred_proba
            }
            
            results_list.append({
                'Model': name,
                'Accuracy': f"{accuracy:.4f}",
                'Precision': f"{precision:.4f}",
                'Recall': f"{recall:.4f}",
                'F1-Score': f"{f1:.4f}",
                'ROC-AUC': f"{roc_auc:.4f}"
            })
            
            print(f"Accuracy: {accuracy:.4f}")
            print(f"Precision: {precision:.4f}")
            print(f"Recall: {recall:.4f}")
            print(f"F1-Score: {f1:.4f}")
            print(f"ROC-AUC: {roc_auc:.4f}")
        
        # Create comparison dataframe
        comparison_df = pd.DataFrame(results_list)
        print("\n" + "="*50)
        print("Model Comparison Summary")
        print("="*50)
        print(comparison_df.to_string(index=False))
        
        # Select best model based on F1-Score
        self.best_model_name = max(self.results.keys(), 
                                   key=lambda x: self.results[x]['f1_score'])
        self.best_model = self.results[self.best_model_name]['model']
        
        print(f"\n🏆 Best Model: {self.best_model_name}")
        print(f"F1-Score: {self.results[self.best_model_name]['f1_score']:.4f}")
        
        return comparison_df
    
    def plot_confusion_matrices(self):
        """Plot confusion matrices for all models"""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        axes = axes.ravel()
        
        for idx, (name, result) in enumerate(self.results.items()):
            cm = result['confusion_matrix']
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx],
                       xticklabels=['Not Churn', 'Churn'],
                       yticklabels=['Not Churn', 'Churn'])
            axes[idx].set_title(f'{name}\nConfusion Matrix')
            axes[idx].set_xlabel('Predicted')
            axes[idx].set_ylabel('Actual')
        
        plt.tight_layout()
        plt.savefig('../frontend/public/confusion_matrices.png')
        plt.show()
    
    def calculate_feature_importance(self, X_train):
        """Calculate feature importance for tree-based models"""
        feature_names = X_train.columns
        
        # Get feature importance from Random Forest
        rf_model = self.trained_models['Random Forest']
        rf_importance = pd.DataFrame({
            'feature': feature_names,
            'importance': rf_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        # Get feature importance from XGBoost
        xgb_model = self.trained_models['XGBoost']
        xgb_importance = pd.DataFrame({
            'feature': feature_names,
            'importance': xgb_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        self.feature_importance = {
            'Random Forest': rf_importance,
            'XGBoost': xgb_importance
        }
        
        return rf_importance, xgb_importance
    
    def plot_feature_importance(self, top_n=10):
        """Plot top N feature importance"""
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Random Forest
        rf_importance = self.feature_importance['Random Forest'].head(top_n)
        axes[0].barh(rf_importance['feature'], rf_importance['importance'])
        axes[0].set_xlabel('Importance')
        axes[0].set_title('Random Forest - Top 10 Feature Importance')
        axes[0].invert_yaxis()
        
        # XGBoost
        xgb_importance = self.feature_importance['XGBoost'].head(top_n)
        axes[1].barh(xgb_importance['feature'], xgb_importance['importance'])
        axes[1].set_xlabel('Importance')
        axes[1].set_title('XGBoost - Top 10 Feature Importance')
        axes[1].invert_yaxis()
        
        plt.tight_layout()
        plt.savefig('../frontend/public/feature_importance.png')
        plt.show()
        
        # Print top features
        print("\n" + "="*50)
        print("Top 10 Most Important Features for Churn Prediction")
        print("="*50)
        for idx, row in rf_importance.head(10).iterrows():
            print(f"{idx+1}. {row['feature']}: {row['importance']:.4f}")
    
    def save_best_model(self, filepath='models/best_model.pkl'):
        """Save the best model"""
        import os
        os.makedirs('models', exist_ok=True)
        joblib.dump(self.best_model, filepath)
        print(f"\n✅ Best model saved to {filepath}")
        
        # Also save the preprocessor
        joblib.dump(self, 'models/model_trainer.pkl')
        
        return filepath