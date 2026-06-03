export default function VideoFeed() {
  return (
    <div>
      <h2>Live Camera Feed</h2>

      <img
        src="http://127.0.0.1:8000/video"
        alt="camera"
        style={{
          width: "600px",
          border: "2px solid black"
        }}
      />
    </div>
  )
}