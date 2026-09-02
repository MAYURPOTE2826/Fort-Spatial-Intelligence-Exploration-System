import React from 'react';
import { Connection } from '../types/fortDetails';
import { Link } from 'react-router-dom';
import { Link as LinkIcon, Navigation } from 'lucide-react';

interface Props {
  connections: Connection[];
}

export const RelatedForts: React.FC<Props> = ({ connections }) => {
  if (!connections || connections.length === 0) {
    return <div className="text-slate-400 p-4 text-sm text-center">No connected forts documented.</div>;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4">
      {connections.map(conn => (
        <Link 
          to={`/fort/${conn.target_fort_id}`} 
          key={conn.target_fort_id}
          className="block bg-terrain-800 border border-terrain-700 rounded-xl p-4 hover:border-emerald-500/50 hover:bg-terrain-800/80 transition-all group"
        >
          <div className="flex justify-between items-start mb-3">
            <h3 className="text-lg font-bold text-slate-200 group-hover:text-emerald-400 transition-colors flex items-center gap-2">
              <LinkIcon className="w-4 h-4 text-slate-500 group-hover:text-emerald-500" />
              {conn.target_fort_name}
            </h3>
          </div>
          
          <div className="flex items-center gap-4 text-sm text-slate-400 mb-3 bg-terrain-900/50 p-2 rounded">
            <div className="flex items-center gap-1">
              <Navigation className="w-3 h-3" />
              <span className="font-mono">{conn.distance_km} km</span>
            </div>
            <div className="flex items-center gap-1">
              <span className="text-[10px] uppercase tracking-wider">Bearing:</span>
              <span className="font-mono">{conn.bearing_deg}°</span>
            </div>
          </div>
          
          {conn.historical_connection && (
            <p className="text-xs text-slate-400 leading-relaxed italic border-l-2 border-terrain-600 pl-2">
              {conn.historical_connection}
            </p>
          )}
        </Link>
      ))}
    </div>
  );
};
