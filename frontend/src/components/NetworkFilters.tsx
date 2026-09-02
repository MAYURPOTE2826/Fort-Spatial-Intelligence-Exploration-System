import React from 'react';
import { Filter, Eye, EyeOff } from 'lucide-react';

interface Props {
  filterStatus: 'all' | 'visible' | 'blocked';
  setFilterStatus: (status: 'all' | 'visible' | 'blocked') => void;
  minScore: number;
  setMinScore: (score: number) => void;
}

export const NetworkFilters: React.FC<Props> = ({ filterStatus, setFilterStatus, minScore, setMinScore }) => {
  return (
    <div className="bg-terrain-800 border border-terrain-700 p-4 rounded-xl mb-6 flex flex-col sm:flex-row gap-6 items-center justify-between">
      <div className="flex items-center gap-3">
        <Filter className="w-5 h-5 text-emerald-500" />
        <h3 className="font-bold text-slate-200">Network Filters</h3>
      </div>
      
      <div className="flex items-center gap-4 flex-wrap">
        {/* Status Toggle */}
        <div className="flex bg-terrain-900 rounded-lg p-1 border border-terrain-700">
          <button 
            onClick={() => setFilterStatus('all')}
            className={`px-3 py-1.5 text-xs rounded transition-colors ${filterStatus === 'all' ? 'bg-terrain-700 text-white font-bold' : 'text-slate-400 hover:text-slate-200'}`}
          >
            All Connections
          </button>
          <button 
            onClick={() => setFilterStatus('visible')}
            className={`px-3 py-1.5 text-xs rounded transition-colors flex items-center gap-1 ${filterStatus === 'visible' ? 'bg-emerald-600/30 text-emerald-400 font-bold' : 'text-slate-400 hover:text-slate-200'}`}
          >
            <Eye className="w-3 h-3" /> Visible Only
          </button>
          <button 
            onClick={() => setFilterStatus('blocked')}
            className={`px-3 py-1.5 text-xs rounded transition-colors flex items-center gap-1 ${filterStatus === 'blocked' ? 'bg-rose-600/30 text-rose-400 font-bold' : 'text-slate-400 hover:text-slate-200'}`}
          >
            <EyeOff className="w-3 h-3" /> Blocked Only
          </button>
        </div>
        
        {/* Score Slider */}
        <div className="flex items-center gap-3 bg-terrain-900 px-4 py-2 rounded-lg border border-terrain-700">
          <span className="text-xs text-slate-400 font-medium">Min Score:</span>
          <input 
            type="range" 
            min="0" 
            max="1" 
            step="0.1" 
            value={minScore} 
            onChange={(e) => setMinScore(parseFloat(e.target.value))}
            className="w-24 accent-emerald-500"
          />
          <span className="text-xs font-mono text-emerald-400">{minScore.toFixed(1)}</span>
        </div>
      </div>
    </div>
  );
};
