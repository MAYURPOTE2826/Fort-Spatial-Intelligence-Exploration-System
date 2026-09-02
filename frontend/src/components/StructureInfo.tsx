import React from 'react';
import { Structure } from '../types/fortDetails';
import { Landmark, DoorOpen, Droplets, Shield, LucideIcon } from 'lucide-react';

interface Props {
  structures: Structure[];
}

const getIconForType = (type: string): LucideIcon => {
  switch (type.toLowerCase()) {
    case 'gate': return DoorOpen;
    case 'water tank': return Droplets;
    case 'memorial': return Landmark;
    case 'bastion': return Shield;
    default: return Landmark;
  }
};

export const StructureInfo: React.FC<Props> = ({ structures }) => {
  if (!structures || structures.length === 0) {
    return <div className="text-slate-400 p-4 text-sm text-center">No structural data available for this fort.</div>;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4">
      {structures.map(structure => {
        const Icon = getIconForType(structure.type);
        return (
          <div key={structure.id} className="bg-terrain-800 border border-terrain-700 rounded-lg p-4 shadow-sm hover:border-emerald-500/50 transition-colors">
            <div className="flex items-start gap-3">
              <div className="p-2 bg-terrain-900 rounded-lg text-emerald-500 shrink-0">
                <Icon className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-slate-200 font-bold flex items-center gap-2">
                  {structure.name}
                  <span className="text-[10px] uppercase tracking-wider bg-terrain-900 px-2 py-0.5 rounded text-slate-400 border border-terrain-700">{structure.type}</span>
                </h3>
                <p className="text-slate-400 text-sm mt-2 leading-relaxed">{structure.description}</p>
                {structure.historical_significance && (
                  <div className="mt-3 bg-terrain-900/50 p-3 rounded border-l-2 border-amber-500">
                    <span className="text-xs text-amber-500 font-semibold block mb-1 uppercase tracking-wider">Historical Significance</span>
                    <p className="text-slate-300 text-xs italic">"{structure.historical_significance}"</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};
