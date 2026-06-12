export default function AlertsPanel({
  warnings = [],
  emergency = false
}) {
  return (
    <div>
      <h3>Alerts</h3>

      {emergency && (
        <p style={{ color: "red" }}>
          EMERGENCY ACTIVE
        </p>
      )}

      {warnings.length === 0 ? (
        <p>No warnings</p>
      ) : (
        warnings.map((a, i) => (
          <p key={i}>{a}</p>
        ))
      )}
    </div>
  )
}