import React, { useState, useEffect } from 'react';
import { Location, HeadingData } from '../types/location';
import { Compass, MapPin } from 'lucide-react';

interface DevLocationPanelProps {
  location: Location | null;
  headingData: HeadingData | null;
  setManualLocation: (lat: number, lng: number) => void;
  setManualHeading: (heading: number) => void;
}

export const DevLocationPanel: React.FC<DevLocationPanelProps> = ({
  location,
  headingData,
  setManualLocation,
  setManualHeading,
}) => {
  const [lat, setLat] = useState<string>('18.5204');
  const [lng, setLng] = useState<string>('73.8567');
  const [heading, setHeading] = useState<number>(0);

  // Sync inputs with current props when they change externally (e.g. initial load)
  useEffect(() => {
    if (location) {
      setLat(location.latitude.toString());
      setLng(location.longitude.toString());
    }
    if (headingData) {
      setHeading(Math.round(headingData.heading));
    }
  }, [location, headingData]);

  const handleUpdateLocation = () => {
    const parsedLat = parseFloat(lat);
    const parsedLng = parseFloat(lng);
    if (!isNaN(parsedLat) && !isNaN(parsedLng)) {
      setManualLocation(parsedLat, parsedLng);
    }
  };

  const handleHeadingChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = parseInt(e.target.value, 10);
    setHeading(val);
    setManualHeading(val);
  };

  return (
    <div className="bg-slate-900/90 backdrop-blur-md p-4 rounded-lg border border-purple-500/50 shadow-xl text-sm text-slate-200 pointer-events-auto">
      <div className="flex items-center gap-2 mb-4 border-b border-purple-500/30 pb-2">
        <MapPin className="w-4 h-4 text-purple-400" />
        <h3 className="font-bold text-purple-400 uppercase tracking-wider text-xs">Dev Tools</h3>
      </div>
      
      <div className="space-y-4">
        <div>
          <label className="block text-xs text-slate-400 mb-1">Latitude</label>
          <input
            type="number"
            step="0.0001"
            value={lat}
            onChange={(e) => setLat(e.target.value)}
            className="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-sm focus:border-purple-500 focus:outline-none"
          />
        </div>
        
        <div>
          <label className="block text-xs text-slate-400 mb-1">Longitude</label>
          <input
            type="number"
            step="0.0001"
            value={lng}
            onChange={(e) => setLng(e.target.value)}
            className="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-sm focus:border-purple-500 focus:outline-none"
          />
        </div>
        
        <button
          onClick={handleUpdateLocation}
          className="w-full bg-purple-600 hover:bg-purple-700 text-white text-xs font-semibold py-1.5 rounded transition-colors"
        >
          Update Location
        </button>

        <div className="pt-2 border-t border-slate-800">
          <label className="flex justify-between text-xs text-slate-400 mb-2">
            <span>Heading</span>
            <span className="font-mono text-purple-300">{heading}°</span>
          </label>
          <div className="flex items-center gap-2">
            <Compass className="w-4 h-4 text-slate-500" />
            <input
              type="range"
              min="0"
              max="360"
              value={heading}
              onChange={handleHeadingChange}
              className="flex-1 accent-purple-500"
            />
          </div>
        </div>
      </div>
    </div>
  );
};
