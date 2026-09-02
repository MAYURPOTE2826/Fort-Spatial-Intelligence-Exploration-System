import React from 'react';
import { Viewpoint } from '../types/fortDetails';
import { Mountain, Compass, Eye, Clock } from 'lucide-react';

interface Props {
  viewpoints: Viewpoint[];
}

export const ViewpointsList: React.FC<Props> = ({ viewpoints }) => {
  if (!viewpoints || viewpoints.length === 0) {
    return <div className="text-slate-400 p-4 text-sm text-center">No viewpoints documented yet.</div>;
  }

  return (
    <div className="space-y-4 p-4">
      {viewpoints.map(vp => (
        <div key={vp.id} className="bg-terrain-800 border border-terrain-700 rounded-lg overflow-hidden">
          <div className="bg-terrain-900 px-4 py-3 border-b border-terrain-700 flex justify-between items-center">
            <h3 className="text-emerald-400 font-bold flex items-center gap-2">
              <Mountain className="w-4 h-4" />
              {vp.name}
            </h3>
            <span className="text-xs bg-terrain-800 px-2 py-1 rounded text-slate-300 border border-terrain-600 flex items-center gap-1">
              <Compass className="w-3 h-3 text-amber-500" />
              {vp.direction} Facing
            </span>
          </div>
          <div className="p-4 grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <span className="text-xs text-slate-500 uppercase font-semibold flex items-center gap-1 mb-2">
                <Eye className="w-3 h-3" /> Visible Features
              </span>
              <ul className="list-disc pl-4 text-sm text-slate-300 space-y-1">
                {vp.visible_features.map((feature, idx) => (
                  <li key={idx}>{feature}</li>
                ))}
              </ul>
            </div>
            <div className="space-y-3">
              <div className="flex justify-between items-center bg-terrain-900/50 p-2 rounded text-sm">
                <span className="text-slate-400">Difficulty</span>
                <span className={`font-medium ${vp.difficulty === 'Easy' ? 'text-emerald-400' : 'text-amber-400'}`}>{vp.difficulty}</span>
              </div>
              <div className="flex justify-between items-center bg-terrain-900/50 p-2 rounded text-sm">
                <span className="text-slate-400 flex items-center gap-1"><Clock className="w-3 h-3"/> Reach in</span>
                <span className="text-slate-200">{vp.time_to_visit}</span>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};
