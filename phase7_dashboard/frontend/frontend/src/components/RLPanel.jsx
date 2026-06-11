export default function RLPanel({ episode, epsilon, reward }) {
  return (
    <div>
      <h3>RL Panel</h3>
      <p>Episode: {episode}</p>
      <p>Epsilon: {epsilon}</p>
      <p>Reward: {reward}</p>
    </div>
  )
}