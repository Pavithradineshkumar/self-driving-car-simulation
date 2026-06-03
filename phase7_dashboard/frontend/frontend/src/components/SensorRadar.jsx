// src/components/SensorRadar.jsx
// Renders 7 sensor rays as a fan diagram using SVG

export default function SensorRadar({ readings = Array(7).fill(1) }) {
  const cx = 120, cy = 130, maxR = 110
  const spread = 180
  const step   = spread / (readings.length - 1)

  const rays = readings.map((val, i) => {
    const angleDeg = -90 - spread / 2 + i * step
    const angleRad = (angleDeg * Math.PI) / 180
    const r   = val * maxR
    const x   = cx + Math.cos(angleRad) * r
    const y   = cy + Math.sin(angleRad) * r
    // Color: green when clear, red when close
    const hue = Math.round(val * 120)   // 0=red, 120=green
    return { x, y, val, color: `hsl(${hue},90%,55%)` }
  })

  return (
    <div className="bg-dash-card border border-dash-border
                    rounded-lg p-3 flex flex-col items-center">
      <p className="text-xs text-gray-400 font-mono mb-2 self-start">
        SENSORS
      </p>
      <svg width="240" height="140" viewBox="0 0 240 140">
        {/* Arc background */}
        <path
          d={`M ${cx - maxR} ${cy} A ${maxR} ${maxR} 0 0 1 ${cx + maxR} ${cy}`}
          fill="none" stroke="#1e2330" strokeWidth="1"
        />
        {/* Grid arcs at 33%, 66%, 100% */}
        {[0.33, 0.66, 1.0].map((f, i) => (
          <path key={i}
            d={`M ${cx - f*maxR} ${cy}
                A ${f*maxR} ${f*maxR} 0 0 1 ${cx + f*maxR} ${cy}`}
            fill="none" stroke="#1e2330" strokeWidth="0.5"
          />
        ))}
        {/* Rays */}
        {rays.map((r, i) => (
          <g key={i}>
            <line
              x1={cx} y1={cy} x2={r.x} y2={r.y}
              stroke={r.color} strokeWidth="2"
              strokeLinecap="round"
            />
            <circle cx={r.x} cy={r.y} r="3" fill={r.color} />
          </g>
        ))}
        {/* Car dot */}
        <circle cx={cx} cy={cy} r="5" fill="#00e5a0" />
      </svg>
    </div>
  )
}