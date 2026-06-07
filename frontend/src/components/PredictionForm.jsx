import React, { useState } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';
import { TrendingUp, AlertTriangle, CheckCircle, Activity } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || '/api';

function PredictionForm() {
  const [formData, setFormData] = useState({
    gender: 'Male',
    SeniorCitizen: 'No',
    Partner: 'No',
    Dependents: 'No',
    tenure: 12,
    PhoneService: 'Yes',
    MultipleLines: 'No',
    InternetService: 'Fiber optic',
    OnlineSecurity: 'No',
    OnlineBackup: 'No',
    DeviceProtection: 'No',
    TechSupport: 'No',
    StreamingTV: 'No',
    StreamingMovies: 'No',
    Contract: 'Month-to-month',
    PaperlessBilling: 'Yes',
    PaymentMethod: 'Electronic check',
    MonthlyCharges: 70,
    TotalCharges: 500
  });

  const [predictionResult, setPredictionResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await axios.post(`${API_URL}/predict`, formData);
      setPredictionResult(response.data);
      toast.success('Prediction completed!');
    } catch (error) {
      toast.error('Failed to get prediction');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (riskLevel) => {
    switch(riskLevel) {
      case 'Low': return 'text-green-600 bg-green-100';
      case 'Medium': return 'text-yellow-600 bg-yellow-100';
      case 'High': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getRiskIcon = (riskLevel) => {
    switch(riskLevel) {
      case 'Low': return <CheckCircle className="h-8 w-8 text-green-600" />;
      case 'Medium': return <AlertTriangle className="h-8 w-8 text-yellow-600" />;
      case 'High': return <TrendingUp className="h-8 w-8 text-red-600" />;
      default: return <Activity className="h-8 w-8 text-gray-600" />;
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-800">Customer Churn Prediction</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Prediction Form */}
        <div className="bg-white rounded-lg shadow p-6">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Gender</label>
                <select
                  name="gender"
                  value={formData.gender}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <option>Male</option>
                  <option>Female</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Senior Citizen</label>
                <select
                  name="SeniorCitizen"
                  value={formData.SeniorCitizen}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <option>No</option>
                  <option>Yes</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Partner</label>
                <select
                  name="Partner"
                  value={formData.Partner}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <option>No</option>
                  <option>Yes</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Dependents</label>
                <select
                  name="Dependents"
                  value={formData.Dependents}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <option>No</option>
                  <option>Yes</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Tenure (months)</label>
              <input
                type="number"
                name="tenure"
                value={formData.tenure}
                onChange={handleChange}
                min="0"
                max="72"
                className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Contract Type</label>
              <select
                name="Contract"
                value={formData.Contract}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option>Month-to-month</option>
                <option>One year</option>
                <option>Two year</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Internet Service</label>
              <select
                name="InternetService"
                value={formData.InternetService}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option>DSL</option>
                <option>Fiber optic</option>
                <option>No</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Tech Support</label>
              <select
                name="TechSupport"
                value={formData.TechSupport}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option>No</option>
                <option>Yes</option>
                <option>No internet service</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Payment Method</label>
              <select
                name="PaymentMethod"
                value={formData.PaymentMethod}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option>Electronic check</option>
                <option>Mailed check</option>
                <option>Bank transfer (automatic)</option>
                <option>Credit card (automatic)</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Monthly Charges ($)</label>
              <input
                type="number"
                name="MonthlyCharges"
                value={formData.MonthlyCharges}
                onChange={handleChange}
                step="0.01"
                min="0"
                max="200"
                className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Predicting...' : 'Predict Churn Risk'}
            </button>
          </form>
        </div>

        {/* Prediction Results */}
        {predictionResult && (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Prediction Result</h2>
            
            <div className={`rounded-lg p-6 ${getRiskColor(predictionResult.risk_level)}`}>
              <div className="flex items-center justify-between mb-4">
                <div>
                  <p className="text-sm font-medium opacity-75">Churn Prediction</p>
                  <p className="text-2xl font-bold">{predictionResult.churn_status}</p>
                </div>
                {getRiskIcon(predictionResult.risk_level)}
              </div>
              
              <div className="mt-4">
                <p className="text-sm font-medium opacity-75">Churn Probability</p>
                <p className="text-3xl font-bold">{(predictionResult.probability * 100).toFixed(1)}%</p>
              </div>
              
              <div className="mt-4">
                <p className="text-sm font-medium opacity-75">Risk Level</p>
                <p className="text-xl font-semibold">{predictionResult.risk_level}</p>
              </div>
              
              <div className="mt-6 pt-4 border-t border-current border-opacity-20">
                <p className="text-sm">{predictionResult.message}</p>
              </div>
            </div>

            {/* Recommendations based on risk level */}
            <div className="mt-6">
              <h3 className="font-semibold text-gray-800 mb-2">Recommendations:</h3>
              {predictionResult.risk_level === 'High' && (
                <ul className="list-disc list-inside space-y-1 text-sm text-gray-600">
                  <li>Offer loyalty discounts or promotions</li>
                  <li>Provide proactive customer support</li>
                  <li>Suggest upgrading to long-term contract</li>
                  <li>Review service quality and address issues</li>
                </ul>
              )}
              {predictionResult.risk_level === 'Medium' && (
                <ul className="list-disc list-inside space-y-1 text-sm text-gray-600">
                  <li>Send engagement emails with offers</li>
                  <li>Check service satisfaction regularly</li>
                  <li>Offer small incentives for loyalty</li>
                </ul>
              )}
              {predictionResult.risk_level === 'Low' && (
                <ul className="list-disc list-inside space-y-1 text-sm text-gray-600">
                  <li>Maintain current service quality</li>
                  <li>Send occasional appreciation offers</li>
                  <li>Encourage referrals</li>
                </ul>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default PredictionForm;