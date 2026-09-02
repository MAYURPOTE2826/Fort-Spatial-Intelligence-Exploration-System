import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap, ZoomControl, Circle } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { Fort } from '../types/fort';
import { Location, HeadingData } from '../types/location';
import { VisibilityResult } from '../types/visibility';
import { getStatusColor } from '../utils/colorScheme';

// Fix Leaflet's default icon path issues
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';
let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

interface MapProps {
  location: Location | null;
  headingData: HeadingData | null;
  forts: Fort[] | undefined;
  visibilityData: VisibilityResult[] | undefined;
  onFortClick: (fort: Fort) => void;
}

const MapUpdater: React.FC<{ center: [number, number] }> = ({ center }) => {
  const map = useMap();
  useEffect(() => {
    map.setView(center, map.getZoom(), { animate: true });
  }, [center, map]);
  return null;
};

export const Map: React.FC<MapProps> = ({ location, headingData, forts, visibilityData, onFortClick }) => {
  const defaultCenter: [number, number] = [18.5204, 73.8567]; // Pune center
  const center: [number, number] = location ? [location.latitude, location.longitude] : defaultCenter;

  const currentHeading = headingData?.heading ?? location?.heading ?? 0;
  
  // Custom marker for user that rotates based on heading
  const userIcon = L.divIcon({
    className: 'custom-user-marker',
    html: `
      <div style="
        width: 24px; 
        height: 24px; 
        background-color: #3b82f6; 
        border-radius: 50%; 
        border: 3px solid white; 
        box-shadow: 0 0 10px rgba(0,0,0,0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
      ">
        <div style="
          position: absolute;
          top: -8px;
          width: 0;
          height: 0;
          border-left: 6px solid transparent;
          border-right: 6px solid transparent;
          border-bottom: 10px solid #3b82f6;
          transform: rotate(${currentHeading}deg);
          transform-origin: 50% 20px;
        "></div>
      </div>
    `,
    iconSize: [24, 24],
    iconAnchor: [12, 12],
  });

  return (
    <div className="w-full h-full relative z-0">
      <MapContainer center={center} zoom={10} className="w-full h-full" zoomControl={false}>
        <ZoomControl position="bottomright" />
        {/* Dark theme tiles (using CSS filter on standard OSM) */}
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          className="map-tiles"
        />
        
        {location && <MapUpdater center={center} />}

        {/* User Location Accuracy Circle */}
        {location && location.accuracy && location.accuracy > 0 && (
          <Circle
            center={[location.latitude, location.longitude]}
            radius={location.accuracy}
            pathOptions={{ color: '#3b82f6', fillColor: '#3b82f6', fillOpacity: 0.15, weight: 1 }}
          />
        )}

        {/* User Location Marker */}
        {location && (
          <Marker position={[location.latitude, location.longitude]} icon={userIcon}>
            <Popup>You are here</Popup>
          </Marker>
        )}

        {/* Fort Markers */}
        {forts?.map((fort) => {
          const visibility = visibilityData?.find((v) => v.fort_id === fort.id);
          const statusColor = getStatusColor(visibility?.status);
          
          const customIcon = L.divIcon({
            className: 'custom-fort-marker',
            html: `<div style="background-color: ${statusColor}; width: 16px; height: 16px; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 5px rgba(0,0,0,0.5);"></div>`,
            iconSize: [16, 16],
            iconAnchor: [8, 8],
          });

          return (
            <Marker 
              key={fort.id} 
              position={[fort.latitude, fort.longitude]}
              icon={customIcon}
              eventHandlers={{
                click: () => onFortClick(fort),
              }}
            >
              <Popup>
                <div className="text-gray-900">
                  <h3 className="font-bold text-lg">{fort.name}</h3>
                  <p className="text-sm">Status: <strong className="capitalize">{visibility?.status || 'Unknown'}</strong></p>
                </div>
              </Popup>
            </Marker>
          );
        })}
      </MapContainer>
    </div>
  );
};
