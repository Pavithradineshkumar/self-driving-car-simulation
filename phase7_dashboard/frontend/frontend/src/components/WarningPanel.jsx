// src/components/WarningPanel.jsx
export default function WarningPanel({ warnings = [] }) {
  return (
    <div className="bg-dash-card border border-dash-border rounded-lg p-4">
      <p className="text-xs text-gray-400 font-mono mb-3">
        WARNINGS ({warnings.length})
      </p>
      <div className="space-y-1.5 max-h-32 overflow-y-auto">
        {warnings.length === 0 ? (
          <p className="text-xs text-dash-accent font-mono">
            ✓ All clear
          </p>
        ) : (
          warnings.map((w, i) => (
            <div key={i}
                 className="flex items-start gap-2 text-xs font-mono
                            text-dash-warning animate-pulse">
              <span>!</span>
              <span>{w}</span>
            </div>
          ))
        )}
      </div>
    </div>
  )
}