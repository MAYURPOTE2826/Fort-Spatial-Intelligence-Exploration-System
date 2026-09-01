import React, { useState } from 'react';
import { Map } from '../components/Map';
import { LocationPanel } from '../components/LocationPanel';
import { FortList } from '../components/FortList';
import { useLocation } from '../hooks/useLocation';
import { useForts } from '../hooks/useForts';
import { useVisibility } from '../hooks/useVisibility';
import { Fort } from '../types/fort';

export const MapPage: React.FC = () => {
  const { location, error: locationError } = useLocation();
  const { data: forts, isLoading: isLoadingForts } = useForts();
  const { data: visibilityData } = useVisibility(location);

  const [selectedFort, setSelectedFort] = useState<Fort | null>(null);

  const handleFortClick = (fort: Fort) => {
    setSelectedFort(fort);
    // Could route to details page or show slide-over
    console.log('Selected fort:', fort.name);
  };

  return (
    <div className="flex flex-col h-screen w-full bg-terrain-900 text-slate-100 overflow-hidden relative">
      {/* Map takes full background */}
      <div className="absolute inset-0 z-0">
        <Map 
          location={location} 
          forts={forts} 
          visibilityData={visibilityData} 
          onFortClick={handleFortClick} 
        />
      </div>

      {/* Floating UI Elements */}
      <div className="relative z-10 p-2 sm:p-4 pointer-events-none h-full flex flex-col justify-between">
        
        {/* Top layer (Location etc) */}
        <div className="flex justify-between items-start pointer-events-auto w-full">
          <div className="w-full sm:w-80 max-w-[65vw] sm:max-w-none">
            <LocationPanel location={location} error={locationError} />
          </div>
          
          <div className="bg-terrain-800 p-2 sm:p-3 rounded-lg shadow-lg border border-terrain-700 ml-2 shrink-0 text-right sm:text-left">
            <h1 className="text-base sm:text-xl font-bold text-emerald-500">FortSight</h1>
            <p className="text-[9px] sm:text-xs text-slate-400">Tactical Map View</p>
          </div>
        </div>

        {/* Bottom layer (Fort list) */}
        <div className="w-full sm:w-80 pointer-events-auto pb-2 sm:pb-4 max-h-[40vh] sm:max-h-none overflow-y-auto">
          <FortList 
            forts={forts} 
            visibilityData={visibilityData} 
            onFortClick={handleFortClick} 
            isLoading={isLoadingForts}
          />
        </div>
        
      </div>

      {/* Slide-over for Fort Details */}
      {selectedFort && (
        <div className="absolute inset-0 z-50 flex pointer-events-auto">
          {/* Backdrop */}
          <div 
            className="absolute inset-0 bg-black/60 backdrop-blur-sm transition-opacity" 
            onClick={() => setSelectedFort(null)} 
          />
          
          {/* Panel */}
          <div className="absolute inset-y-0 right-0 w-full sm:w-96 bg-terrain-800 border-l border-terrain-700 shadow-2xl p-6 overflow-y-auto transform transition-transform duration-300">
            <button 
              onClick={() => setSelectedFort(null)}
              className="absolute top-4 right-4 p-2 text-slate-400 hover:text-white rounded-full hover:bg-terrain-700 transition-colors"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
            <h2 className="text-2xl font-bold text-emerald-400 mb-2 mt-2">{selectedFort.name}</h2>
            <p className="text-slate-300 mb-6 text-sm leading-relaxed">{selectedFort.description || "No description available."}</p>
            
            <div className="space-y-4">
              <div className="bg-terrain-900 p-4 rounded-lg border border-terrain-700">
                <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">Location Data</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <span className="text-slate-400 block text-xs uppercase">Latitude</span>
                    <span className="text-slate-200 font-mono text-sm">{selectedFort.latitude.toFixed(6)}°</span>
                  </div>
                  <div>
                    <span className="text-slate-400 block text-xs uppercase">Longitude</span>
                    <span className="text-slate-200 font-mono text-sm">{selectedFort.longitude.toFixed(6)}°</span>
                  </div>
                  {selectedFort.elevation !== undefined && (
                    <div className="col-span-2">
                      <span className="text-slate-400 block text-xs uppercase">Elevation</span>
                      <span className="text-slate-200 font-mono text-sm">{selectedFort.elevation}m</span>
                    </div>
                  )}
                </div>
              </div>
              
              {(() => {
                const vis = visibilityData?.find((v) => v.fort_id === selectedFort.id);
                if (!vis) return null;
                return (
                  <div className="bg-terrain-900 p-4 rounded-lg border border-terrain-700">
                    <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">Tactical Visibility</h3>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="col-span-2">
                        <span className="text-slate-400 block text-xs uppercase">Status</span>
                        <span className="text-amber-400 font-semibold text-sm capitalize">{vis.status}</span>
                      </div>
                      <div>
                        <span className="text-slate-400 block text-xs uppercase">Distance</span>
                        <span className="text-slate-200 font-mono text-sm">{Math.round(vis.distance_m)}m</span>
                      </div>
                      <div>
                        <span className="text-slate-400 block text-xs uppercase">Bearing</span>
                        <span className="text-slate-200 font-mono text-sm">{Math.round(vis.bearing)}°</span>
                      </div>
                    </div>
                  </div>
                );
              })()}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
