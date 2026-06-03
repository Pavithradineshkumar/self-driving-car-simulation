// src/components/BehaviorState.jsx
const STATE_CONFIG = {
  CRUISE:             { color: '#00e5a0', label: 'CRUISE',       icon: '▶' },
  CAUTION:            { color: '#3b9eff', label: 'CAUTION',      icon: '◈' },
  SLOW:               { color: '#ffcc00', label: 'SLOW',         icon: '⬇' },
  STOP:               { color: '#ff6b35', label: 'FULL STOP',    icon: '⬛' },
  AVOID:              { color: '#c084fc', label: 'AVOIDING',     icon: '↩' },
  TRAFFIC_LIGHT_STOP: { color: '#ff6b35', label: 'RED LIGHT',   icon: '🛑' },
  IDLE:               { color: '#6b7280', label: 'IDLE',         icon: '○' },
}

export default function BehaviorState({ state = 'IDLE', epsilon = 1,
                                        episode = 0, qValues = [] }) {
  const cfg = STATE_CONFIG[state] || STATE_CONFIG.IDLE

  return (
    <div className="bg-dash-card border border-dash-border rounded-lg p-4">
      <p className="text-xs text-gray-400 font-mono mb-3">BEHAVIOR / RL</p>

      {/* State badge */}
      <div className="flex items-center gap-3 mb-4">
        <div className="w-3 h-3 rounded-full animate-pulse"
             style={{ backgroundColor: cfg.color }} />
        <span className="text-xl font-mono font-bold"
              style={{ color: cfg.color }}>
          {cfg.icon} {cfg.label}
        </span>
      </div>

      {/* RL stats */}
      <div className="grid grid-cols-2 gap-2 mb-4">
        {[
          { label: 'EPISODE',  value: episode },
          { label: 'EPSILON',  value: `${(epsilon * 100).toFixed(1)}%` },
        ].map(({ label, value }) => (
          <div key={label}
               className="bg-dash-bg rounded p-2 text-center">
            <p className="text-xs text-gray-500 font-mono">{label}</p>
            <p className="text-sm font-mono font-bold text-white">{value}</p>
          </div>
        ))}
      </div>

      {/* Q-values bar chart */}
      {qValues.length > 0 && (
        <div>
          <p className="text-xs text-gray-500 font-mono mb-2">Q-VALUES</p>
          <div className="space-y-1">
            {['STRAIGHT', 'LEFT', 'RIGHT', 'BRAKE'].map((label, i) => {
              const v    = qValues[i] ?? 0
              const vmin = Math.min(...qValues)
              const vmax = Math.max(...qValues)
              const pct  = vmax === vmin ? 50
                         : ((v - vmin) / (vmax - vmin)) * 100
              const best = v === Math.max(...qValues)
              return (
                <div key={label} className="flex items-center gap-2">
                  <span className="text-xs font-mono text-gray-500 w-16">
                    {label}
                  </span>
                  <div className="flex-1 h-1.5 bg-dash-border rounded-full">
                    <div className="h-full rounded-full transition-all"
                         style={{
                           width:      `${pct}%`,
                           backgroundColor: best ? '#00e5a0' : '#3b9eff'
                         }} />
                  </div>
                  <span className="text-xs font-mono text-gray-400 w-10
                                   text-right">
                    {v.toFixed(2)}
                  </span>
                </div>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}