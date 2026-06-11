export default function MonitoringCard({ cpu, ram, backend }) {
  return (
    <div>
      <h3>Monitoring</h3>
      <p>CPU: {cpu}%</p>
      <p>RAM: {ram}%</p>
      <p>Backend: {backend}</p>
    </div>
  )
}