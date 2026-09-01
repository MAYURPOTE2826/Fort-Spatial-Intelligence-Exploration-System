import React from 'react';
import { Location } from '../types/location';
import { Compass, Navigation } from 'lucide-react';

interface LocationPanelProps {
  location: Location | null;
  error: string | null;
}

export const LocationPanel: React.FC<LocationPanelProps> = ({ location, error }) => {
  if (error) {
    return (
      <div className="bg-terrain-800 p-4 rounded-lg border border-amber-500/50 shadow-lg text-sm">
        <h2 className="text-lg font-semibold text-slate-100 mb-2 flex items-center gap-2">
          <Navigation className="w-5 h-5 text-amber-500" />
          Default Location (Pune)
        </h2>
        <p className="text-amber-200/80 text-xs mb-3">
          {error}. Using default view.
        </p>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <span className="text-slate-400 block text-xs uppercase tracking-wider">Latitude</span>
            <span className="text-slate-200 font-mono">18.520400°</span>
          </div>
          <div>
            <span className="text-slate-400 block text-xs uppercase tracking-wider">Longitude</span>
            <span className="text-slate-200 font-mono">73.856700°</span>
          </div>
        </div>
      </div>
    );
  }

  if (!location) {
    return (
      <div className="bg-terrain-800 p-4 rounded-lg border border-terrain-700 animate-pulse">
        Waiting for location...
      </div>
    );
  }

  return (
    <div className="bg-terrain-800 p-4 rounded-lg border border-terrain-700 shadow-lg text-sm">
      <h2 className="text-lg font-semibold text-slate-100 mb-3 flex items-center gap-2">
        <Navigation className="w-5 h-5 text-emerald-500" />
        Current Location
      </h2>
      
      <div className="grid grid-cols-2 gap-4">
        <div>
          <span className="text-slate-400 block text-xs uppercase tracking-wider">Latitude</span>
          <span className="text-slate-200 font-mono">{location.latitude.toFixed(6)}°</span>
        </div>
        <div>
          <span className="text-slate-400 block text-xs uppercase tracking-wider">Longitude</span>
          <span className="text-slate-200 font-mono">{location.longitude.toFixed(6)}°</span>
        </div>
        
        {location.elevation !== undefined && (
          <div>
            <span className="text-slate-400 block text-xs uppercase tracking-wider">Elevation</span>
            <span className="text-slate-200 font-mono">{Math.round(location.elevation)}m</span>
          </div>
        )}
        
        {location.heading !== undefined && (
          <div>
            <span className="text-slate-400 block text-xs uppercase tracking-wider">Heading</span>
            <span className="text-slate-200 font-mono flex items-center gap-1">
              <Compass className="w-3 h-3" style={{ transform: `rotate(${location.heading}deg)` }} />
              {Math.round(location.heading)}°
            </span>
          </div>
        )}
      </div>
      
      {location.accuracy !== undefined && (
        <div className="mt-3 pt-3 border-t border-terrain-700">
          <span className="text-slate-400 text-xs">
            Accuracy: <span className="text-emerald-400 font-mono">±{Math.round(location.accuracy)}m</span>
          </span>
        </div>
      )}
    </div>
  );
};
