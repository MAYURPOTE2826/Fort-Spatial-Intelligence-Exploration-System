import React from 'react';
import { Trail } from '../types/fortDetails';
import { Map, Footprints, Route, Timer, TrendingUp } from 'lucide-react';

interface Props {
  trails: Trail[];
}

export const TrailsList: React.FC<Props> = ({ trails }) => {
  if (!trails || trails.length === 0) {
    return <div className="text-slate-400 p-4 text-sm text-center">No trails documented yet.</div>;
  }

  return (
    <div className="space-y-6 p-4">
      {trails.map(trail => (
        <div key={trail.id} className="bg-terrain-800 border border-terrain-700 rounded-xl overflow-hidden shadow-lg relative">
          {/* Difficulty Ribbon */}
          <div className={`absolute top-0 right-0 px-3 py-1 text-xs font-bold uppercase rounded-bl-lg
            ${trail.difficulty === 'Easy' ? 'bg-emerald-500/20 text-emerald-400' : 
              trail.difficulty === 'Moderate' ? 'bg-amber-500/20 text-amber-400' : 
              'bg-rose-500/20 text-rose-400'}
          `}>
            {trail.difficulty}
          </div>

          <div className="p-5">
            <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2 mb-4">
              <Footprints className="w-5 h-5 text-emerald-500" />
              {trail.name}
            </h3>

            {/* Route visual */}
            <div className="flex items-center gap-3 mb-6 bg-terrain-900 p-3 rounded-lg border border-terrain-700/50">
              <div className="text-sm font-medium text-slate-300">{trail.start_point}</div>
              <div className="flex-1 border-t-2 border-dashed border-emerald-500/30 relative">
                <Route className="absolute -top-3 left-1/2 -translate-x-1/2 w-5 h-5 text-emerald-500/50" />
              </div>
              <div className="text-sm font-medium text-emerald-400">{trail.end_point}</div>
            </div>

            {/* Stats grid */}
            <div className="grid grid-cols-3 gap-4">
              <div className="text-center p-3 bg-terrain-900/50 rounded-lg">
                <Map className="w-4 h-4 text-slate-400 mx-auto mb-1" />
                <div className="text-lg font-bold text-slate-200">{trail.distance_km}<span className="text-xs text-slate-500 font-normal"> km</span></div>
                <div className="text-[10px] uppercase tracking-wider text-slate-500">Distance</div>
              </div>
              <div className="text-center p-3 bg-terrain-900/50 rounded-lg">
                <Timer className="w-4 h-4 text-slate-400 mx-auto mb-1" />
                <div className="text-lg font-bold text-slate-200">{trail.estimated_time_hours}<span className="text-xs text-slate-500 font-normal"> hrs</span></div>
                <div className="text-[10px] uppercase tracking-wider text-slate-500">Est. Time</div>
              </div>
              <div className="text-center p-3 bg-terrain-900/50 rounded-lg">
                <TrendingUp className="w-4 h-4 text-slate-400 mx-auto mb-1" />
                <div className="text-lg font-bold text-slate-200">{trail.elevation_gain}<span className="text-xs text-slate-500 font-normal"> m</span></div>
                <div className="text-[10px] uppercase tracking-wider text-slate-500">Elevation</div>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};
