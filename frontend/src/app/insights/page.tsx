'use client';
import { useState, useEffect } from 'react';
import axios from 'axios';

export default function InsightsPage() {
  const [insights, setInsights] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchInsights() {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
        const res = await axios.get(`${apiUrl}/api/tests/insights`);
        setInsights(res.data);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    fetchInsights();
  }, []);

  return (
    <div className="max-w-5xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold text-white tracking-tight">AI Anomaly Insights</h1>
        <div className="bg-indigo-50 text-indigo-700 px-4 py-1.5 rounded-full text-sm font-bold flex items-center gap-2 border border-indigo-100 shadow-sm">
          <span className="w-2.5 h-2.5 rounded-full bg-indigo-500 animate-pulse"></span>
          Engine Active
        </div>
      </div>
      
      {loading ? (
        <div className="animate-pulse flex flex-col gap-4">
          {[1,2,3].map(i => <div key={i} className="h-24 bg-white/60 border border-gray-100 rounded-2xl w-full"></div>)}
        </div>
      ) : insights.length === 0 ? (
        <div className="bg-white p-12 rounded-3xl shadow-sm border border-gray-100 text-center flex flex-col items-center">
          <div className="w-16 h-16 bg-gray-50 rounded-2xl flex items-center justify-center text-3xl mb-4 border border-gray-100">✨</div>
          <h3 className="text-xl font-bold text-gray-800 mb-2">No Anomalies Detected</h3>
          <p className="text-gray-500 max-w-sm">The automation engine hasn't found any flaky tests, structural failures, or latency spikes in recent runs.</p>
        </div>
      ) : (
        <div className="grid gap-4">
          {insights.map((insight, i) => (
            <div key={i} className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex items-start gap-5 hover:shadow-md transition-shadow">
              <div className={`p-4 rounded-xl flex items-center justify-center text-xl font-bold ${
                insight.severity === 'critical' ? 'bg-red-50 text-red-600 border border-red-100' :
                insight.severity === 'high' ? 'bg-orange-50 text-orange-600 border border-orange-100' :
                'bg-yellow-50 text-yellow-600 border border-yellow-100'
              }`}>
                {insight.severity === 'critical' ? '🚨' : insight.severity === 'high' ? '⚠️' : '🔔'}
              </div>
              <div className="flex-1 mt-1">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-lg font-bold text-gray-900 capitalize tracking-tight">
                    {insight.type.replace('_', ' ').toLowerCase()}
                  </h3>
                  <span className="text-xs font-bold text-gray-600 bg-gray-100 px-2.5 py-1 rounded-md border border-gray-200">
                    Case #{insight.test_case_id}
                  </span>
                </div>
                <p className="text-gray-600 text-sm">{insight.description}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
