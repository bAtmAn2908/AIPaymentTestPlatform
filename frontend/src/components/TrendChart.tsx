'use client';

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export function TrendChart({ data }: { data: any[] }) {
  if (!data || data.length === 0) {
    return (
      <div className="h-72 w-full bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex items-center justify-center">
        <p className="text-gray-400 text-sm">No latency data available</p>
      </div>
    );
  }

  return (
    <div className="h-80 w-full bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
      <h3 className="text-base font-semibold mb-6 text-gray-800 flex items-center gap-2">
        <span className="w-2 h-2 rounded-full bg-blue-500"></span>
        Global Latency Trends (ms)
      </h3>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
          <XAxis 
            dataKey="timestamp" 
            stroke="#94a3b8" 
            fontSize={11} 
            tickLine={false} 
            axisLine={false} 
            dy={10}
            tickFormatter={(val) => new Date(val).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          />
          <YAxis 
            stroke="#94a3b8" 
            fontSize={11} 
            tickLine={false} 
            axisLine={false} 
            dx={-10}
          />
          <Tooltip 
            contentStyle={{ 
              borderRadius: '12px', 
              border: '1px solid #e2e8f0', 
              boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)',
              fontSize: '12px'
            }}
          />
          <Line 
            type="monotone" 
            dataKey="latency_ms" 
            name="Latency"
            stroke="#3b82f6" 
            strokeWidth={3}
            dot={false}
            activeDot={{ r: 6, fill: '#3b82f6', stroke: '#fff', strokeWidth: 2 }}
            animationDuration={1500}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
