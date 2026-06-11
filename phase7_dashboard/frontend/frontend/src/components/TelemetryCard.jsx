export default function TelemetryCard({ telemetry }) {
  return (
    <div>
      <h3>Telemetry</h3>
      <pre>{JSON.stringify(telemetry, null, 2)}</pre>
    </div>
  )
}