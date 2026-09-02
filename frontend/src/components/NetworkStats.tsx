import React from 'react';
import { Activity, Map, Link as LinkIcon, AlertCircle } from 'lucide-react';
import { GraphNode, GraphEdge } from './VisibilityGraph';

interface Props {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export const NetworkStats: React.FC<Props> = ({ nodes, edges }) => {
  const visibleEdges = edges.filter(e => e.is_visible);
  
  // Calculate average visibility
  const totalScore = visibleEdges.reduce((acc, e) => acc + e.visibility_score, 0);
  const avgScore = visibleEdges.length > 0 ? (totalScore / visibleEdges.length).toFixed(2) : '0.00';
  
  // Calculate density
  const possibleEdges = nodes.length > 1 ? (nodes.length * (nodes.length - 1)) / 2 : 1; // Assuming undirected for density
  // Edges count / possible edges (simplified since we might have bidirectional edges in data)
  const undirectedEdgesCount = edges.length / 2; // Assuming symmetric data
  const density = nodes.length > 1 ? ((undirectedEdgesCount / possibleEdges) * 100).toFixed(1) : '0.0';

  // Find most connected fort
  const connectionCounts: Record<string, number> = {};
  visibleEdges.forEach(e => {
    connectionCounts[e.source] = (connectionCounts[e.source] || 0) + 1;
    connectionCounts[e.target] = (connectionCounts[e.target] || 0) + 1;
  });

  let maxConnections = 0;
  let mostConnectedFortId = '';
  Object.entries(connectionCounts).forEach(([id, count]) => {
    if (count > maxConnections) {
      maxConnections = count;
      mostConnectedFortId = id;
    }
  });

  const mostConnectedNode = nodes.find(n => String(n.id) === String(mostConnectedFortId));

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <div className="bg-terrain-800 border border-terrain-700 p-4 rounded-xl">
        <div className="flex items-center gap-2 text-slate-400 text-xs uppercase font-bold tracking-wider mb-2">
          <Map className="w-4 h-4 text-emerald-500" /> Total Forts
        </div>
        <div className="text-2xl font-mono text-slate-100">{nodes.length}</div>
      </div>
      
      <div className="bg-terrain-800 border border-terrain-700 p-4 rounded-xl">
        <div className="flex items-center gap-2 text-slate-400 text-xs uppercase font-bold tracking-wider mb-2">
          <LinkIcon className="w-4 h-4 text-amber-500" /> Visible Links
        </div>
        <div className="text-2xl font-mono text-slate-100">{visibleEdges.length}</div>
      </div>
      
      <div className="bg-terrain-800 border border-terrain-700 p-4 rounded-xl">
        <div className="flex items-center gap-2 text-slate-400 text-xs uppercase font-bold tracking-wider mb-2">
          <Activity className="w-4 h-4 text-blue-500" /> Avg Score
        </div>
        <div className="text-2xl font-mono text-slate-100">{avgScore}</div>
      </div>
      
      <div className="bg-terrain-800 border border-terrain-700 p-4 rounded-xl">
        <div className="flex items-center gap-2 text-slate-400 text-xs uppercase font-bold tracking-wider mb-2">
          <AlertCircle className="w-4 h-4 text-rose-500" /> Hub Node
        </div>
        <div className="text-lg font-bold text-slate-100 truncate">
          {mostConnectedNode ? mostConnectedNode.name : 'N/A'}
        </div>
      </div>
    </div>
  );
};
