import React, { useEffect, useState } from 'react';
import { Location, HeadingData } from '../types/location';
import { Compass, Navigation, SignalHigh, SignalMedium, SignalLow, Clock } from 'lucide-react';

interface LocationPanelProps {
  location: Location | null;
  headingData: HeadingData | null;
  error: string | null;
}

const getAccuracyColor = (accuracy?: number) => {
  if (!accuracy) return 'text-slate-400';
  if (accuracy <= 10) return 'text-emerald-400';
  if (accuracy <= 30) return 'text-amber-400';
  return 'text-rose-400';
};

const getAccuracyIcon = (accuracy?: number) => {
  if (!accuracy) return <SignalLow className="w-3 h-3 text-slate-400" />;
  if (accuracy <= 10) return <SignalHigh className="w-3 h-3 text-emerald-400" />;
  if (accuracy <= 30) return <SignalMedium className="w-3 h-3 text-amber-400" />;
  return <SignalLow className="w-3 h-3 text-rose-400" />;
};

export const LocationPanel: React.FC<LocationPanelProps> = ({ location, headingData, error }) => {
  const [dataAge, setDataAge] = useState<number>(0);

  useEffect(() => {
    const interval = setInterval(() => {
      if (location?.timestamp) {
        setDataAge(Math.floor((Date.now() - location.timestamp) / 1000));
      }
    }, 1000);
    return () => clearInterval(interval);
  }, [location?.timestamp]);

  if (error) {
    return (
      <div className="bg-terrain-800 p-4 rounded-lg border border-amber-500/50 shadow-lg text-sm pointer-events-auto">
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
      <div className="bg-terrain-800 p-4 rounded-lg border border-terrain-700 animate-pulse pointer-events-auto">
        <span className="text-slate-400 text-sm">Acquiring location data...</span>
      </div>
    );
  }

  const accuracyColor = getAccuracyColor(location.accuracy);

  return (
    <div className="bg-terrain-800/90 backdrop-blur-md p-4 rounded-lg border border-terrain-700 shadow-lg text-sm pointer-events-auto">
      <div className="flex justify-between items-center mb-3">
        <h2 className="text-lg font-semibold text-slate-100 flex items-center gap-2">
          <Navigation className="w-5 h-5 text-emerald-500" />
          Sensor Data
        </h2>
        {location.timestamp && (
          <div className="flex items-center gap-1 text-xs text-slate-400">
            <Clock className="w-3 h-3" />
            {dataAge}s ago
          </div>
        )}
      </div>
      
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
        
        {(headingData || location.heading !== undefined) && (
          <div>
            <span className="text-slate-400 block text-xs uppercase tracking-wider">Heading</span>
            <span className="text-slate-200 font-mono flex items-center gap-1">
              <Compass 
                className="w-3 h-3 text-emerald-400" 
                style={{ transform: `rotate(${headingData ? headingData.heading : location.heading}deg)` }} 
              />
              {Math.round(headingData ? headingData.heading : (location.heading || 0))}°
            </span>
          </div>
        )}
      </div>
      
      <div className="mt-3 pt-3 border-t border-terrain-700 flex justify-between items-center">
        <div className="flex items-center gap-1.5">
          {getAccuracyIcon(location.accuracy)}
          <span className="text-slate-400 text-xs">
            GPS: <span className={`${accuracyColor} font-mono`}>{location.accuracy ? `±${Math.round(location.accuracy)}m` : 'Manual'}</span>
          </span>
        </div>
        {headingData?.accuracy !== undefined && headingData.accuracy > 0 && (
          <div className="text-slate-400 text-xs">
            Compass: <span className="text-emerald-400 font-mono">±{Math.round(headingData.accuracy)}°</span>
          </div>
        )}
      </div>
    </div>
  );
};
