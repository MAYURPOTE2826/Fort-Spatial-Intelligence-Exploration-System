import { useState, useEffect } from 'react'
import Map, { NavigationControl } from 'react-map-gl'
import maplibregl from 'maplibre-gl'

function App() {
  const [health, setHealth] = useState<string>('Checking backend...')

  useEffect(() => {
    // Check backend health
    fetch(import.meta.env.VITE_API_URL + '/health')
      .then(res => res.json())
      .then(data => setHealth(data.message))
      .catch(err => setHealth('Backend offline: ' + err.message))
  }, [])

  return (
    <div className="w-full h-screen relative font-sans">
      <Map
        mapLib={maplibregl}
        initialViewState={{
          longitude: 73.8567, // Pune longitude
          latitude: 18.5204,  // Pune latitude
          zoom: 8
        }}
        style={{ width: '100%', height: '100%' }}
        mapStyle="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"
      >
        <NavigationControl position="top-left" />
      </Map>

      <div className="absolute top-4 right-4 bg-white/90 backdrop-blur p-4 rounded-xl shadow-lg border border-slate-200">
        <h1 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
          FortSight AI
        </h1>
        <p className="text-sm text-slate-600 mt-1">
          Terrain-aware line-of-sight analysis.
        </p>
        <div className="mt-3 text-xs px-2 py-1 bg-slate-100 rounded-md text-slate-700">
          Status: <span className="font-semibold text-emerald-600">{health}</span>
        </div>
      </div>
    </div>
  )
}

export default App
