// src/components/ThreeSimulation.jsx
import { useEffect, useRef } from 'react'
import * as THREE from 'three'

export default function ThreeSimulation({ speed = 0, steer = 0,
                                          sensorReadings = [] }) {
  const mountRef = useRef(null)
  const stateRef = useRef({ speed, steer, sensorReadings })

  // Keep latest props accessible inside animation loop
  useEffect(() => {
    stateRef.current = { speed, steer, sensorReadings }
  }, [speed, steer, sensorReadings])

  useEffect(() => {
    const el     = mountRef.current
    const W      = el.clientWidth
    const H      = 220

    // ── Scene setup ────────────────────────────────────────────
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })
    renderer.setSize(W, H)
    renderer.setPixelRatio(window.devicePixelRatio)
    el.appendChild(renderer.domElement)

    const scene  = new THREE.Scene()
    const camera = new THREE.PerspectiveCamera(55, W / H, 0.1, 100)
    camera.position.set(0, 4, 8)
    camera.lookAt(0, 0, 0)

    // ── Lighting ───────────────────────────────────────────────
    scene.add(new THREE.AmbientLight(0xffffff, 0.6))
    const dir = new THREE.DirectionalLight(0xffffff, 0.8)
    dir.position.set(5, 10, 5)
    scene.add(dir)

    // ── Road plane ─────────────────────────────────────────────
    const roadGeo  = new THREE.PlaneGeometry(6, 40)
    const roadMat  = new THREE.MeshStandardMaterial({ color: 0x333344 })
    const road     = new THREE.Mesh(roadGeo, roadMat)
    road.rotation.x = -Math.PI / 2
    scene.add(road)

    // Lane markings (dashes)
    for (let z = -18; z < 20; z += 3) {
      const dashGeo = new THREE.PlaneGeometry(0.08, 1.2)
      const dashMat = new THREE.MeshStandardMaterial({ color: 0xffdd44 })
      const dash    = new THREE.Mesh(dashGeo, dashMat)
      dash.rotation.x = -Math.PI / 2
      dash.position.set(-2, 0.01, z)
      scene.add(dash.clone())
      dash.position.set(2, 0.01, z)
      scene.add(dash)
    }

    // ── Car body ───────────────────────────────────────────────
    const carGroup = new THREE.Group()

    const bodyGeo = new THREE.BoxGeometry(1.4, 0.55, 2.6)
    const bodyMat = new THREE.MeshStandardMaterial({ color: 0xcc3333 })
    const body    = new THREE.Mesh(bodyGeo, bodyMat)
    body.position.y = 0.4
    carGroup.add(body)

    const roofGeo = new THREE.BoxGeometry(1.0, 0.4, 1.4)
    const roofMat = new THREE.MeshStandardMaterial({ color: 0xaa2222 })
    const roof    = new THREE.Mesh(roofGeo, roofMat)
    roof.position.set(0, 0.85, -0.2)
    carGroup.add(roof)

    // Wheels
    const wheelGeo = new THREE.CylinderGeometry(0.28, 0.28, 0.22, 16)
    const wheelMat = new THREE.MeshStandardMaterial({ color: 0x111111 })
    const wPositions = [
      [-0.75, 0.28,  0.9],
      [ 0.75, 0.28,  0.9],
      [-0.75, 0.28, -0.9],
      [ 0.75, 0.28, -0.9],
    ]
    wPositions.forEach(([x, y, z]) => {
      const w = new THREE.Mesh(wheelGeo, wheelMat)
      w.rotation.z = Math.PI / 2
      w.position.set(x, y, z)
      carGroup.add(w)
    })

    carGroup.position.set(0, 0, 1)
    scene.add(carGroup)

    // ── Sensor ray lines ───────────────────────────────────────
    const rayLines = []
    const numRays  = 7
    const spread   = Math.PI

    for (let i = 0; i < numRays; i++) {
      const geo = new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(0, 0.6, 0),
        new THREE.Vector3(0, 0.6, -4),
      ])
      const mat  = new THREE.LineBasicMaterial({ color: 0x00ff88 })
      const line = new THREE.Line(geo, mat)
      carGroup.add(line)
      rayLines.push(line)
    }

    // ── Road scroll offset ─────────────────────────────────────
    let roadOffset = 0

    // ── Animation loop ─────────────────────────────────────────
    let animId
    const animate = () => {
      animId = requestAnimationFrame(animate)

      const { speed: spd, steer: str, sensorReadings: rays }
        = stateRef.current

      // Scroll road texture by offsetting position (loop)
      roadOffset = (roadOffset + spd * 0.04) % 3
      road.position.z = roadOffset

      // Steer car
      carGroup.rotation.y = -str * 0.3

      // Update sensor rays
      rayLines.forEach((line, i) => {
        const angle    = -spread / 2 + (i / (numRays - 1)) * spread
        const reading  = rays[i] ?? 1
        const len      = reading * 4
        const hue      = reading   // 1=green, 0=red
        line.material.color.setHSL(hue * 0.33, 0.9, 0.55)

        const pts = [
          new THREE.Vector3(0, 0.6, 0),
          new THREE.Vector3(
            Math.sin(angle) * len,
            0.6,
            -Math.cos(angle) * len
          ),
        ]
        line.geometry.setFromPoints(pts)
      })

      renderer.render(scene, camera)
    }
    animate()

    // ── Cleanup ────────────────────────────────────────────────
    return () => {
      cancelAnimationFrame(animId)
      renderer.dispose()
      el.removeChild(renderer.domElement)
    }
  }, [])   // Run once — state updates via stateRef

  return (
    <div className="bg-dash-card border border-dash-border rounded-lg p-3">
      <p className="text-xs text-gray-400 font-mono mb-2">3D VIEW</p>
      <div ref={mountRef} className="w-full rounded overflow-hidden" />
    </div>
  )
}