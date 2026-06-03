// src/hooks/useWebSocket.js
import { useState, useEffect, useRef } from 'react'

export function useWebSocket(url) {
  const [data,   setData]   = useState(null)
  const [status, setStatus] = useState('connecting')
  const wsRef = useRef(null)

  useEffect(() => {
    function connect() {
      const ws = new WebSocket(url)
      wsRef.current = ws

      ws.onopen    = () => setStatus('connected')
      ws.onclose   = () => {
        setStatus('reconnecting')
        // Auto-reconnect after 2 seconds
        setTimeout(connect, 2000)
      }
      ws.onerror   = () => setStatus('error')
      ws.onmessage = (e) => {
        try {
          setData(JSON.parse(e.data))
        } catch (_) {}
      }
    }
    connect()
    return () => wsRef.current?.close()
  }, [url])

  return { data, status }
}