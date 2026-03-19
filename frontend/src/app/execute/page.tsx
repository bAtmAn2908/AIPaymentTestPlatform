'use client';
import { useState } from 'react';
import axios from 'axios';

export default function ExecutePage() {
  const [status, setStatus] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);

  const triggerRun = async () => {
    try {
      setIsLoading(true);
      setStatus('Triggering automation engine...');
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const res = await axios.post(`${apiUrl}/api/tests/runs`);
      setStatus(`Successfully queued run! ID: ${res.data.test_run_id}`);
    } catch (e: any) {
      setStatus(`Error triggering run: ${e.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-white mb-8 tracking-tight">Execute Test Suites</h1>
      
      <div className="bg-white p-8 rounded-3xl shadow-sm border border-gray-100 mb-8 flex flex-col items-center justify-center min-h-[400px]">
        <div className="text-center max-w-md">
          <div className="w-20 h-20 bg-blue-50 text-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-6 text-3xl shadow-inner border border-blue-100">
            🚀
          </div>
          <h2 className="text-2xl font-bold mb-3 text-gray-800">Run Automation Suite</h2>
          <p className="text-gray-500 mb-10 leading-relaxed">
            Trigger a complete simulation of standard and edge-case payment scenarios including latency spikes, network drops, and invalid tokens.
          </p>
          
          <button 
            onClick={triggerRun}
            disabled={isLoading}
            className={`w-full text-white font-medium py-4 px-8 rounded-xl shadow-lg transition-all transform hover:scale-105 active:scale-95 ${
              isLoading ? 'bg-blue-400 cursor-not-allowed hidden shadow-none' : 'bg-blue-600 hover:bg-blue-700 shadow-blue-500/30'
            }`}
          >
            {isLoading ? 'Triggering...' : 'Execute All Tests'}
          </button>
          
          {status && (
            <div className={`mt-6 p-4 text-sm rounded-xl border font-medium ${
              status.includes('Error') ? 'bg-red-50 text-red-700 border-red-100' : 
              status.includes('queued') ? 'bg-green-50 text-green-700 border-green-100' :
              'bg-blue-50 text-blue-700 border-blue-100'
            }`}>
              {status}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
