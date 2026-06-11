export default function AlertsPanel({ alerts }) {
  return (
    <div>
      <h3>Alerts</h3>
      {alerts.map((a, i) => (
        <p key={i}>{a}</p>
      ))}
    </div>
  )
}