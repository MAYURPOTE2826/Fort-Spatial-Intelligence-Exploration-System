import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap, ZoomControl, Polygon, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { FortDetail, Structure, Viewpoint, Trail } from '../types/fortDetails';
import { Layers } from 'lucide-react';

interface Props {
  fort: FortDetail;
  structures: Structure[];
  viewpoints: Viewpoint[];
  trails: Trail[];
}

const MapUpdater: React.FC<{ center: [number, number], zoom: number }> = ({ center, zoom }) => {
  const map = useMap();
  useEffect(() => {
    map.setView(center, zoom, { animate: true });
  }, [center, zoom, map]);
  return null;
};

// Create custom icons mapping based on type
const getIconHtml = (type: string, color: string) => {
  return `<div style="
    background-color: ${color}; 
    width: 20px; 
    height: 20px; 
    border-radius: 50%; 
    border: 2px solid white; 
    box-shadow: 0 0 5px rgba(0,0,0,0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 10px;
    font-weight: bold;
  ">${type[0].toUpperCase()}</div>`;
};

export const FortMap: React.FC<Props> = ({ fort, structures, viewpoints, trails }) => {
  const center: [number, number] = [fort.latitude, fort.longitude];
  const [activeLayer, setActiveLayer] = useState<'all' | 'structures' | 'viewpoints' | 'trails'>('all');

  return (
    <div className="w-full h-full relative z-0 min-h-[400px] rounded-xl overflow-hidden border border-terrain-700">
      
      {/* Layer Controls overlay */}
      <div className="absolute top-4 right-4 z-[400] bg-terrain-800/90 backdrop-blur-md p-2 rounded-lg border border-terrain-700 shadow-xl">
        <div className="flex items-center gap-2 mb-2 px-2 border-b border-terrain-700 pb-2">
          <Layers className="w-4 h-4 text-emerald-500" />
          <span className="text-xs font-bold text-slate-200 uppercase tracking-wider">Layers</span>
        </div>
        <div className="flex flex-col gap-1">
          {(['all', 'structures', 'viewpoints', 'trails'] as const).map(layer => (
            <button
              key={layer}
              onClick={() => setActiveLayer(layer)}
              className={`text-left text-xs px-3 py-1.5 rounded transition-colors capitalize ${activeLayer === layer ? 'bg-emerald-600/30 text-emerald-400 font-bold' : 'text-slate-400 hover:bg-terrain-700 hover:text-slate-200'}`}
            >
              {layer}
            </button>
          ))}
        </div>
      </div>

      <MapContainer center={center} zoom={16} className="w-full h-full bg-terrain-900" zoomControl={false}>
        <ZoomControl position="bottomright" />
        
        {/* Satellite/Terrain Base layer (simulated with standard for now, but configured for styling) */}
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          className="map-tiles grayscale contrast-125 brightness-75"
        />
        
        <MapUpdater center={center} zoom={16} />

        {/* Fort Center Marker (Main) */}
        <Marker 
          position={center} 
          icon={L.divIcon({
            className: 'fort-center-marker',
            html: `<div style="background-color: transparent; border: 2px dashed #10b981; width: 40px; height: 40px; border-radius: 50%; transform: translate(-10px, -10px);"></div>`,
            iconSize: [20, 20],
          })}
        >
          <Popup>Center of {fort.name}</Popup>
        </Marker>

        {/* Structures Layer */}
        {(activeLayer === 'all' || activeLayer === 'structures') && structures.map(struct => (
          <Marker 
            key={`struct-${struct.id}`}
            position={[struct.latitude, struct.longitude]}
            icon={L.divIcon({
              className: 'custom-struct-icon',
              html: getIconHtml(struct.type, '#f59e0b'), // Amber for structures
              iconSize: [20, 20],
              iconAnchor: [10, 10]
            })}
          >
            <Popup>
              <div className="text-gray-900">
                <h4 className="font-bold">{struct.name}</h4>
                <span className="text-xs uppercase bg-gray-200 px-1 rounded">{struct.type}</span>
                <p className="text-xs mt-1">{struct.description}</p>
              </div>
            </Popup>
          </Marker>
        ))}

        {/* Viewpoints Layer */}
        {(activeLayer === 'all' || activeLayer === 'viewpoints') && viewpoints.map(vp => (
          <Marker 
            key={`vp-${vp.id}`}
            position={[vp.latitude, vp.longitude]}
            icon={L.divIcon({
              className: 'custom-vp-icon',
              html: getIconHtml('V', '#3b82f6'), // Blue for viewpoints
              iconSize: [20, 20],
              iconAnchor: [10, 10]
            })}
          >
            <Popup>
              <div className="text-gray-900">
                <h4 className="font-bold">{vp.name}</h4>
                <p className="text-xs font-semibold text-blue-600">Facing: {vp.direction}</p>
                <div className="text-xs mt-1">
                  <strong>Visible:</strong>
                  <ul className="list-disc pl-3 m-0">
                    {vp.visible_features.map((f, i) => <li key={i}>{f}</li>)}
                  </ul>
                </div>
              </div>
            </Popup>
          </Marker>
        ))}

        {/* Trails Layer */}
        {(activeLayer === 'all' || activeLayer === 'trails') && trails.map(trail => {
          if (!trail.waypoints || trail.waypoints.length === 0) return null;
          return (
            <React.Fragment key={`trail-${trail.id}`}>
              <Polyline 
                positions={trail.waypoints} 
                pathOptions={{ 
                  color: trail.difficulty === 'Easy' ? '#10b981' : trail.difficulty === 'Moderate' ? '#f59e0b' : '#ef4444', 
                  weight: 3,
                  dashArray: '5, 5'
                }} 
              />
              {/* Start marker */}
              <Marker position={trail.waypoints[0]} icon={L.divIcon({
                  className: 'trail-start',
                  html: `<div style="width:10px;height:10px;background:white;border-radius:50%;border:2px solid #10b981;"></div>`,
                  iconSize: [10, 10], iconAnchor: [5, 5]
              })}>
                 <Popup><div className="text-gray-900 font-bold">{trail.start_point} (Start)</div></Popup>
              </Marker>
            </React.Fragment>
          );
        })}
      </MapContainer>
    </div>
  );
};
