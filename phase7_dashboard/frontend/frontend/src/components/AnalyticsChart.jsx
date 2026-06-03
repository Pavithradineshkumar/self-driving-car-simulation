// src/components/AnalyticsChart.jsx
import {
  LineChart, Line, XAxis, YAxis,
  Tooltip, ResponsiveContainer, Legend
} from 'recharts'

export default function AnalyticsChart({ speedHistory = [],
                                         rewardHistory = [] }) {
  // Build combined dataset for recharts
  const data = speedHistory.map((s, i) => ({
    t:      i,
    speed:  parseFloat(s.toFixed(2)),
    reward: parseFloat((rewardHistory[i] ?? 0).toFixed(2)),
  }))

  const tooltipStyle = {
    backgroundColor: '#141720',
    border: '1px solid #1e2330',
    borderRadius: 6,
    fontSize: 11,
    fontFamily: 'monospace',
  }

  return (
    <div className="bg-dash-card border border-dash-border rounded-lg p-4">
      <p className="text-xs text-gray-400 font-mono mb-3">ANALYTICS</p>
      <ResponsiveContainer width="100%" height={160}>
        <LineChart data={data}
                   margin={{ top: 4, right: 8, bottom: 0, left: -20 }}>
          <XAxis dataKey="t" hide />
          <YAxis tick={{ fontSize: 10, fill: '#6b7280' }} />
          <Tooltip contentStyle={tooltipStyle} />
          <Legend wrapperStyle={{ fontSize: 11, fontFamily: 'monospace' }} />
          <Line type="monotone" dataKey="speed"
                stroke="#00e5a0" dot={false}
                strokeWidth={1.5} isAnimationActive={false} />
          <Line type="monotone" dataKey="reward"
                stroke="#3b9eff" dot={false}
                strokeWidth={1.5} isAnimationActive={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}