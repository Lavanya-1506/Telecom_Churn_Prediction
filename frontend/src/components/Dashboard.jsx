import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell
} from 'recharts';
import { Users, TrendingUp, DollarSign, Calendar, Activity } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || '/api';

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardStats();
  }, []);

  const fetchDashboardStats = async () => {
    try {
      const response = await axios.get(`${API_URL}/dashboard-stats`);
      setStats(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to load dashboard statistics');
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

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        {error}
      </div>
    );
  }

  // Prepare data for charts
  const contractData = stats?.contract_distribution ? Object.entries(stats.contract_distribution).map(([name, value]) => ({
    name,
    value
  })) : [];

  const paymentData = stats?.payment_distribution ? Object.entries(stats.payment_distribution).map(([name, value]) => ({
    name,
    value
  })) : [];

  const churnByContractData = stats?.churn_by_contract ? Object.entries(stats.churn_by_contract).map(([name, value]) => ({
    name,
    churnRate: value
  })) : [];

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

  const StatCard = ({ title, value, icon: Icon, color }) => (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-500 text-sm font-medium">{title}</p>
          <p className="text-2xl font-bold text-gray-800">{value}</p>
        </div>
        <div className={`p-3 rounded-full ${color}`}>
          <Icon className="h-6 w-6 text-white" />
        </div>
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-800">Customer Analytics Dashboard</h1>
      
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Customers"
          value={stats?.total_customers?.toLocaleString()}
          icon={Users}
          color="bg-blue-500"
        />
        <StatCard
          title="Churned Customers"
          value={stats?.churned_customers?.toLocaleString()}
          icon={TrendingUp}
          color="bg-red-500"
        />
        <StatCard
          title="Churn Rate"
          value={`${stats?.churn_rate?.toFixed(1)}%`}
          icon={Activity}
          color="bg-yellow-500"
        />
        <StatCard
          title="Avg Monthly Charges"
          value={`$${stats?.monthly_charges_stats?.mean?.toFixed(2)}`}
          icon={DollarSign}
          color="bg-green-500"
        />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Contract Distribution */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Contract Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={contractData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {contractData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Churn Rate by Contract */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Churn Rate by Contract Type</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={churnByContractData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis unit="%" />
              <Tooltip />
              <Legend />
              <Bar dataKey="churnRate" fill="#FF8042" name="Churn Rate (%)" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Payment Method Distribution */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Payment Methods</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={paymentData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name.substring(0, 15)} (${(percent * 100).toFixed(0)}%)`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {paymentData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Additional Stats */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Customer Tenure Statistics</h2>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Average Tenure:</span>
              <span className="text-2xl font-bold text-indigo-600">
                {stats?.tenure_stats?.mean?.toFixed(1)} months
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Median Tenure:</span>
              <span className="text-2xl font-bold text-green-600">
                {stats?.tenure_stats?.median} months
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Tenure Range:</span>
              <span className="text-lg text-gray-800">
                {stats?.tenure_stats?.min} - {stats?.tenure_stats?.max} months
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;