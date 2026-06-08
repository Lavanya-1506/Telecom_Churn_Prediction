import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar
} from 'recharts';
import { Brain, Target, TrendingUp, Award } from 'lucide-react';

const API_URL = '/api';

function ModelInfo() {
  const [modelInfo, setModelInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchModelInfo();
  }, []);

  const fetchModelInfo = async () => {
    try {
      const response = await axios.get(`${API_URL}/model-info`);
      setModelInfo(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to load model information');
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (error || !modelInfo) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        {error || 'No model information available'}
      </div>
    );
  }

  const performance = modelInfo.performance || {};
  const featureImportance = modelInfo.feature_importance || [];

  const radarData = [
    { metric: 'Accuracy', value: parseFloat(performance.accuracy) * 100 },
    { metric: 'Precision', value: parseFloat(performance.precision) * 100 },
    { metric: 'Recall', value: parseFloat(performance.recall) * 100 },
    { metric: 'F1-Score', value: parseFloat(performance.f1_score) * 100 },
    { metric: 'ROC-AUC', value: parseFloat(performance.roc_auc) * 100 }
  ];

  const MetricCard = ({ title, value, icon: Icon, color }) => (
    <div className="bg-white rounded-lg shadow p-4">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-500 text-sm">{title}</p>
          <p className="text-2xl font-bold text-gray-800">{value}</p>
        </div>
        <div className={`p-2 rounded-full ${color}`}>
          <Icon className="h-5 w-5 text-white" />
        </div>
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-800">Model Performance & Insights</h1>
      
      {/* Best Model Info */}
      <div className="bg-linear-to-r from-indigo-500 to-purple-600 rounded-lg shadow p-6 text-white">
        <div className="flex items-center space-x-3 mb-2">
          <Award className="h-8 w-8" />
          <h2 className="text-2xl font-bold">Best Performing Model</h2>
        </div>
        <p className="text-3xl font-bold mt-2">{modelInfo.best_model}</p>
        <p className="text-indigo-100 mt-1">Selected based on F1-Score performance</p>
      </div>

      {/* Performance Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <MetricCard
          title="Accuracy"
          value={`${(parseFloat(performance.accuracy) * 100).toFixed(2)}%`}
          icon={Target}
          color="bg-blue-500"
        />
        <MetricCard
          title="Precision"
          value={`${(parseFloat(performance.precision) * 100).toFixed(2)}%`}
          icon={Target}
          color="bg-green-500"
        />
        <MetricCard
          title="Recall"
          value={`${(parseFloat(performance.recall) * 100).toFixed(2)}%`}
          icon={Target}
          color="bg-yellow-500"
        />
        <MetricCard
          title="F1-Score"
          value={`${(parseFloat(performance.f1_score) * 100).toFixed(2)}%`}
          icon={Brain}
          color="bg-purple-500"
        />
        <MetricCard
          title="ROC-AUC"
          value={`${(parseFloat(performance.roc_auc) * 100).toFixed(2)}%`}
          icon={TrendingUp}
          color="bg-red-500"
        />
      </div>

      {/* Performance Radar Chart */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Model Performance Metrics</h2>
        <ResponsiveContainer width="100%" height={400}>
          <RadarChart data={radarData}>
            <PolarGrid />
            <PolarAngleAxis dataKey="metric" />
            <PolarRadiusAxis domain={[0, 100]} />
            <Radar
              name="Performance"
              dataKey="value"
              stroke="#8884d8"
              fill="#8884d8"
              fillOpacity={0.6}
            />
            <Tooltip />
            <Legend />
          </RadarChart>
        </ResponsiveContainer>
      </div>

      {/* Feature Importance */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Top 10 Features Influencing Churn</h2>
        <ResponsiveContainer width="100%" height={500}>
          <BarChart
            data={featureImportance}
            layout="vertical"
            margin={{ top: 5, right: 30, left: 100, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" />
            <YAxis type="category" dataKey="feature" width={100} />
            <Tooltip formatter={(value) => (value * 100).toFixed(2) + '%'} />
            <Legend />
            <Bar dataKey="importance" fill="#8884d8" name="Importance Score" />
          </BarChart>
        </ResponsiveContainer>
        
        <div className="mt-6 p-4 bg-blue-50 rounded-lg">
          <h3 className="font-semibold text-blue-800 mb-2">Business Insights:</h3>
          <ul className="list-disc list-inside space-y-1 text-sm text-blue-700">
            <li><strong>Contract Type</strong> is the strongest predictor - month-to-month contracts have highest churn</li>
            <li><strong>Tenure</strong> shows that newer customers are more likely to churn</li>
            <li><strong>Monthly Charges</strong> - customers with higher monthly charges are more likely to churn</li>
            <li><strong>Tech Support</strong> - lack of tech support increases churn risk</li>
            <li><strong>Payment Method</strong> - electronic check users show higher churn rates</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default ModelInfo;