import React, { useRef, useEffect, useState } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import { useNavigate } from 'react-router-dom';

export interface GraphNode {
  id: string;
  name: string;
  val: number; // size
  color?: string;
}

export interface GraphEdge {
  source: string;
  target: string;
  is_visible: boolean;
  distance_km: number;
  visibility_score: number;
}

interface Props {
  nodes: GraphNode[];
  edges: GraphEdge[];
  width?: number;
  height?: number;
}

export const VisibilityGraph: React.FC<Props> = ({ nodes, edges, width = 800, height = 600 }) => {
  const fgRef = useRef<any>();
  const navigate = useNavigate();
  const [containerSize, setContainerSize] = useState({ width, height });
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleResize = () => {
      if (containerRef.current) {
        setContainerSize({
          width: containerRef.current.clientWidth,
          height: containerRef.current.clientHeight
        });
      }
    };
    
    window.addEventListener('resize', handleResize);
    handleResize(); // Initial size
    
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  useEffect(() => {
    // Apply layout forces
    if (fgRef.current) {
      fgRef.current.d3Force('charge').strength(-200);
      fgRef.current.d3Force('link').distance((link: any) => link.distance_km * 5); // Approximate visual distance
    }
  }, [nodes, edges]);

  return (
    <div ref={containerRef} className="w-full h-full bg-terrain-900 rounded-xl overflow-hidden border border-terrain-700 shadow-2xl relative">
      <ForceGraph2D
        ref={fgRef}
        width={containerSize.width}
        height={containerSize.height}
        graphData={{ nodes, links: edges }}
        nodeLabel="name"
        nodeColor={(node: any) => node.color || '#10b981'} // Emerald default
        nodeRelSize={6}
        linkDirectionalParticles={(link: any) => (link.is_visible ? 2 : 0)}
        linkDirectionalParticleSpeed={(link: any) => link.visibility_score * 0.01}
        linkColor={(link: any) => (link.is_visible ? 'rgba(16, 185, 129, 0.6)' : 'rgba(239, 68, 68, 0.2)')}
        linkWidth={(link: any) => (link.is_visible ? link.visibility_score * 3 : 1)}
        onNodeClick={(node: any) => navigate(`/fort/${node.id}`)}
        cooldownTicks={100}
      />
      <div className="absolute bottom-4 left-4 bg-terrain-800/80 backdrop-blur px-3 py-2 rounded text-xs text-slate-300 pointer-events-none border border-terrain-700">
        <div className="flex items-center gap-2 mb-1">
          <div className="w-3 h-3 rounded-full bg-emerald-500"></div> Visible (LOS)
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-rose-500/50"></div> Blocked (No LOS)
        </div>
      </div>
    </div>
  );
};
