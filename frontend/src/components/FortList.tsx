import React from 'react';
import { Fort } from '../types/fort';
import { VisibilityResult } from '../types/visibility';
import { Eye, EyeOff, HelpCircle } from 'lucide-react';
import { getStatusColor } from '../utils/colorScheme';

interface FortListProps {
  forts: Fort[] | undefined;
  visibilityData: VisibilityResult[] | undefined;
  onFortClick: (fort: Fort) => void;
  isLoading: boolean;
}

export const FortList: React.FC<FortListProps> = ({ forts, visibilityData, onFortClick, isLoading }) => {
  if (isLoading) {
    return (
      <div className="bg-terrain-800 p-4 rounded-lg animate-pulse">
        Loading forts...
      </div>
    );
  }

  if (!forts?.length) {
    return (
      <div className="bg-terrain-800 p-4 rounded-lg text-slate-400">
        No forts found in this area.
      </div>
    );
  }

  return (
    <div className="bg-terrain-800 p-4 rounded-lg shadow-lg max-h-[400px] overflow-y-auto">
      <h2 className="text-lg font-semibold text-slate-100 mb-4 sticky top-0 bg-terrain-800 py-2">
        Nearby Forts
      </h2>
      <div className="space-y-3">
        {forts.map(fort => {
          const visibility = visibilityData?.find(v => v.fort_id === fort.id);
          const status = visibility?.status || 'uncertain';
          
          return (
            <button
              key={fort.id}
              onClick={() => onFortClick(fort)}
              className="w-full text-left p-3 rounded bg-terrain-900/50 hover:bg-terrain-700 transition-colors border border-terrain-700/50 flex items-center justify-between group"
            >
              <div>
                <h3 className="font-medium text-slate-200 group-hover:text-white">{fort.name}</h3>
                {visibility && (
                  <p className="text-xs text-slate-400 mt-1">
                    {Math.round(visibility.distance_m / 1000)} km away
                  </p>
                )}
              </div>
              <div 
                className="flex items-center justify-center w-8 h-8 rounded-full bg-terrain-800"
                style={{ color: getStatusColor(status) }}
                title={`Status: ${status}`}
              >
                {status === 'visible' && <Eye className="w-4 h-4" />}
                {status === 'blocked' && <EyeOff className="w-4 h-4" />}
                {status === 'uncertain' && <HelpCircle className="w-4 h-4" />}
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
};
