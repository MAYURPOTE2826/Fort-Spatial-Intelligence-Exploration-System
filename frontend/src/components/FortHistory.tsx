import React from 'react';
import { FortDetail } from '../types/fortDetails';
import { ScrollText, Pickaxe, BookOpen, Lightbulb } from 'lucide-react';

interface Props {
  fort: FortDetail;
}

export const FortHistory: React.FC<Props> = ({ fort }) => {
  return (
    <div className="space-y-6 p-4">
      {/* Main History */}
      <div className="bg-terrain-800 border border-terrain-700 rounded-xl p-5 shadow-lg">
        <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2 mb-4 border-b border-terrain-700 pb-2">
          <ScrollText className="w-5 h-5 text-amber-500" />
          Historical Overview
        </h3>
        <p className="text-slate-300 text-sm leading-relaxed mb-4">{fort.description}</p>
        <p className="text-slate-300 text-sm leading-relaxed">{fort.history}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Built By */}
        {fort.built_by && (
          <div className="bg-terrain-800 border border-terrain-700 rounded-xl p-4 flex gap-3">
            <Pickaxe className="w-5 h-5 text-slate-400 shrink-0" />
            <div>
              <span className="text-[10px] uppercase tracking-wider text-slate-500 font-bold block mb-1">Built By / Origin</span>
              <p className="text-slate-200 text-sm">{fort.built_by}</p>
            </div>
          </div>
        )}

        {/* Architecture */}
        {fort.architectural_style && (
          <div className="bg-terrain-800 border border-terrain-700 rounded-xl p-4 flex gap-3">
            <BookOpen className="w-5 h-5 text-slate-400 shrink-0" />
            <div>
              <span className="text-[10px] uppercase tracking-wider text-slate-500 font-bold block mb-1">Architectural Style</span>
              <p className="text-slate-200 text-sm">{fort.architectural_style}</p>
            </div>
          </div>
        )}
      </div>

      {/* Interesting Facts */}
      {fort.interesting_facts && fort.interesting_facts.length > 0 && (
        <div className="bg-terrain-800 border border-terrain-700 rounded-xl p-5 shadow-lg">
          <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2 mb-4 border-b border-terrain-700 pb-2">
            <Lightbulb className="w-5 h-5 text-emerald-500" />
            Interesting Facts
          </h3>
          <ul className="space-y-3">
            {fort.interesting_facts.map((fact, idx) => (
              <li key={idx} className="flex gap-3 text-sm text-slate-300">
                <span className="text-emerald-500 font-bold">•</span>
                <span className="leading-relaxed">{fact}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
