// src/components/SpeedGauge.jsx
export default function SpeedGauge({ speed = 0, maxSpeed = 8,
                                     steer = 0, throttle = 0,
                                     brake = false }) {
  const pct    = Math.min(speed / maxSpeed, 1)
  const radius = 54
  const circ   = 2 * Math.PI * radius
  const dash   = pct * circ * 0.75   // 270° arc
  const offset = circ * 0.125        // Start at bottom-left

  const color  = brake ? '#ff6b35'
               : speed > maxSpeed * 0.8 ? '#ff6b35'
               : speed > maxSpeed * 0.5 ? '#ffcc00'
               : '#00e5a0'

  return (
    <div className="bg-dash-card border border-dash-border
                    rounded-lg p-4 flex flex-col items-center gap-3">
      <p className="text-xs text-gray-400 font-mono self-start">SPEED</p>

      {/* Arc gauge */}
      <div className="relative" style={{ width: 128, height: 128 }}>
        <svg width="128" height="128" viewBox="0 0 128 128"
             style={{ transform: 'rotate(135deg)' }}>
          {/* Track */}
          <circle cx="64" cy="64" r={radius}
            fill="none" stroke="#1e2330" strokeWidth="10"
            strokeDasharray={`${circ * 0.75} ${circ}`}
            strokeDashoffset={-offset}
            strokeLinecap="round"
          />
          {/* Value arc */}
          <circle cx="64" cy="64" r={radius}
            fill="none" stroke={color} strokeWidth="10"
            strokeDasharray={`${dash} ${circ}`}
            strokeDashoffset={-offset}
            strokeLinecap="round"
            style={{ transition: 'stroke-dasharray 0.1s' }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col
                        items-center justify-center">
          <span className="text-2xl font-mono font-bold"
                style={{ color }}>
            {speed.toFixed(1)}
          </span>
          <span className="text-xs text-gray-500">px/f</span>
        </div>
      </div>

      {/* Throttle / brake bar */}
      <div className="w-full space-y-1">
        <div className="flex justify-between text-xs text-gray-500 font-mono">
          <span>THROTTLE</span><span>{(throttle*100).toFixed(0)}%</span>
        </div>
        <div className="w-full h-2 bg-dash-border rounded-full overflow-hidden">
          <div className="h-full bg-dash-accent rounded-full transition-all"
               style={{ width: `${throttle * 100}%` }} />
        </div>
        {brake && (
          <p className="text-xs text-dash-warning font-mono text-center
                        animate-pulse mt-1">
            ⬛ BRAKING
          </p>
        )}
      </div>

      {/* Steering indicator */}
      <div className="w-full">
        <p className="text-xs text-gray-500 font-mono mb-1">STEER</p>
        <div className="relative h-2 bg-dash-border rounded-full">
          <div className="absolute top-1/2 left-1/2 w-0.5 h-3
                          bg-gray-600 -translate-x-1/2 -translate-y-1/2" />
          <div className="absolute top-1/2 w-3 h-3 rounded-full bg-dash-info
                          -translate-y-1/2 transition-all"
               style={{
                 left: `calc(50% + ${steer * 18}px - 6px)`
               }} />
        </div>
        <div className="flex justify-between text-xs text-gray-600 mt-1">
          <span>L</span><span>{steer.toFixed(2)}</span><span>R</span>
        </div>
      </div>
    </div>
  )
}