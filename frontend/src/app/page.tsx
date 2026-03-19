'use client';
import { useEffect, useState } from 'react';
import axios from 'axios';
import { TrendChart } from '@/components/TrendChart';

export default function Dashboard() {
  const [runs, setRuns] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
        const res = await axios.get(`${apiUrl}/api/tests/runs`);
        setRuns(res.data);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  const trendData = runs.map(r => ({
    timestamp: r.created_at,
    latency_ms: r.total_latency_ms || 0
  })).reverse();

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex items-center justify-between xl:mb-10 mb-8">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight mb-2">Platform Overview</h1>
          <p className="text-gray-500 text-sm">Monitor simulated payment execution metrics and automated suite latency.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex flex-col justify-center">
          <p className="text-gray-500 font-medium text-sm mb-1 uppercase tracking-wider">Total Suite Runs</p>
          <div className="text-4xl font-black text-gray-800 tracking-tighter">{runs.length}</div>
        </div>
        <div className="bg-blue-600 p-6 rounded-2xl shadow-md border border-blue-500 flex flex-col justify-center text-white relative overflow-hidden">
          <div className="absolute -right-6 -top-6 w-24 h-24 bg-white opacity-10 rounded-full blur-2xl"></div>
          <p className="text-blue-100 font-medium text-sm mb-1 uppercase tracking-wider text-opacity-80">Avg Suite Latency</p>
          <div className="text-4xl font-black tracking-tighter relative z-10">
            {runs.length ? (runs.reduce((a, b) => a + (b.total_latency_ms || 0), 0) / runs.length).toFixed(0) : 0}ms
          </div>
        </div>
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex flex-col justify-center">
          <p className="text-gray-500 font-medium text-sm mb-1 uppercase tracking-wider">Queue Status</p>
          <div className="flex items-center gap-3 mt-1">
            <span className="w-3 h-3 rounded-full bg-green-500 animate-[ping_2s_ease-in-out_infinite] absolute mix-blend-multiply opacity-75"></span>
            <span className="w-3 h-3 rounded-full bg-green-500 relative inline-flex"></span>
            <span className="text-xl font-bold text-gray-800 tracking-tight">Operational</span>
          </div>
        </div>
      </div>

      <div className="mb-10">
        <TrendChart data={trendData} />
      </div>

      <div>
        <h3 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
          <span className="w-2.5 h-2.5 rounded-full bg-slate-300"></span>
          Recent Executions
        </h3>
        
        {loading ? (
          <div className="animate-pulse flex flex-col gap-4">
            {[1,2].map(i => <div key={i} className="h-20 bg-white/60 border border-gray-100 rounded-2xl w-full"></div>)}
          </div>
        ) : runs.length === 0 ? (
          <div className="bg-gray-50 text-sm font-medium p-10 flex items-center justify-center text-gray-500 rounded-2xl border border-dashed border-gray-200 shadow-inner">
            No executions recorded. Switch to the Execute tab to trigger a suite.
          </div>
        ) : (
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-gray-50/80 border-b border-gray-100 text-xs uppercase tracking-wider text-gray-500 font-bold">
                  <th className="py-4 px-6 w-24">ID</th>
                  <th className="py-4 px-6">Status</th>
                  <th className="py-4 px-6">Created At</th>
                  <th className="py-4 px-6 text-right">Latency (ms)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {runs.slice(0, 10).map((r) => (
                  <tr key={r.id} className="hover:bg-gray-50/50 transition-colors group">
                    <td className="py-4 px-6 font-mono text-sm text-gray-500 font-semibold group-hover:text-blue-600 transition-colors">#{r.id}</td>
                    <td className="py-4 px-6">
                      <span className={`px-2.5 py-1 text-xs font-bold rounded-md uppercase tracking-wider ${
                        r.status === 'completed' ? 'bg-green-50 text-green-700 border border-green-100 shadow-sm' :
                        r.status === 'running' ? 'bg-blue-50 text-blue-700 border border-blue-100 shadow-sm animate-pulse' :
                        'bg-gray-50 text-gray-600 border border-gray-200'
                      }`}>
                        {r.status}
                      </span>
                    </td>
                    <td className="py-4 px-6 text-sm font-medium text-gray-600">
                      {new Date(r.created_at).toLocaleString()}
                    </td>
                    <td className="py-4 px-6 font-mono text-sm text-gray-700 font-bold text-right">
                      {r.total_latency_ms ? r.total_latency_ms.toFixed(1) : '-'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
