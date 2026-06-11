import VideoFeed from "./components/VideoFeed"
import SensorRadar from "./components/SensorRadar"
import SpeedGauge from "./components/SpeedGauge"
import BehaviorState from "./components/BehaviorState"
import AnalyticsChart from "./components/AnalyticsChart"
import ThreeSimulation from "./components/ThreeSimulation"
import WarningPanel from "./components/WarningPanel"
import { useWebSocket } from "./hooks/useWebSocket"

export default function App() {
  const { data, status } = useWebSocket("ws://localhost:8000/ws")
  console.log(data)

  return (
    <div style={{ padding: "20px" }}>
      <h1>Self Driving Dashboard</h1>

      <p>
        WebSocket Status: {status}
      </p>

      <h2 style={{ color: "red" }}>
        SPEED = {data?.speed}
      </h2>

      <h2 style={{ color: "blue" }}>
        STATE = {data?.behavior_state}
      </h2>

      <VideoFeed />

      <hr />

      <SensorRadar
        readings={data?.sensor_readings || [1,1,1,1,1,1,1]}
      />

      <hr />

      <SpeedGauge
        speed={data?.speed || 0}
        throttle={data?.throttle || 0}
        steer={data?.steer || 0}
      />

      <hr />

      <BehaviorState
        state={data?.behavior_state || "IDLE"}
        epsilon={data?.epsilon || 0}
        episode={data?.episode || 0}
        qValues={data?.q_values || [0,0,0,0]}
      />

      <hr />

      <AnalyticsChart
        speedHistory={data?.speed_history || []}
        rewardHistory={data?.reward_history || []}
      />

      <hr />

      <ThreeSimulation />

      <hr />

      <WarningPanel
        warnings={data?.warnings || []}
      />

      <hr />
    </div>
  )
}