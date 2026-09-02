import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, Network, Download, Play, RefreshCw, AlertTriangle } from 'lucide-react';
import { VisibilityGraph, GraphNode, GraphEdge } from '../components/VisibilityGraph';
import { NetworkStats } from '../components/NetworkStats';
import { NetworkFilters } from '../components/NetworkFilters';
import { useForts } from '../hooks/useForts';

const API_BASE_URL = 'http://localhost:8000/api/v1/visibility';

export const NetworkPage: React.FC = () => {
  const { forts, isLoading: fortsLoading } = useForts();
  
  const [nodes, setNodes] = useState<GraphNode[]>([]);
  const [edges, setEdges] = useState<GraphEdge[]>([]);
  
  const [filterStatus, setFilterStatus] = useState<'all' | 'visible' | 'blocked'>('all');
  const [minScore, setMinScore] = useState<number>(0);
  
  const [jobId, setJobId] = useState<string | null>(null);
  const [jobStatus, setJobStatus] = useState<'IDLE' | 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED'>('IDLE');
  const [progress, setProgress] = useState<number>(0);
  const [error, setError] = useState<string | null>(null);
  const [calculationTime, setCalculationTime] = useState<number | null>(null);

  const pollInterval = useRef<number | null>(null);

  // Poll for job status
  useEffect(() => {
    if (jobId && (jobStatus === 'PENDING' || jobStatus === 'PROCESSING')) {
      pollInterval.current = window.setInterval(async () => {
        try {
          const res = await fetch(`${API_BASE_URL}/job/${jobId}`);
          if (res.ok) {
            const data = await res.json();
            setJobStatus(data.status);
            if (data.progress !== undefined) setProgress(data.progress);
            
            if (data.status === 'COMPLETED' && data.result) {
              processNetworkData(data.result);
              if (pollInterval.current) clearInterval(pollInterval.current);
            } else if (data.status === 'FAILED') {
              setError(data.error || 'Job failed');
              if (pollInterval.current) clearInterval(pollInterval.current);
            }
          }
        } catch (err) {
          console.error("Failed to poll job status", err);
        }
      }, 2000);
    }
    
    return () => {
      if (pollInterval.current) clearInterval(pollInterval.current);
    };
  }, [jobId, jobStatus]);

  const processNetworkData = (data: any) => {
    if (!forts) return;
    
    // Create nodes
    const newNodes = data.nodes.map((nodeId: string) => {
      const fort = forts.find(f => String(f.id) === String(nodeId));
      return {
        id: nodeId,
        name: fort?.name || `Fort ${nodeId}`,
        val: 10, // Default size
      };
    });
    
    setNodes(newNodes);
    setEdges(data.edges);
    setCalculationTime(data.calculation_time_ms);
  };

  const handleBuildNetwork = async () => {
    if (!forts || forts.length === 0) return;
    
    setJobStatus('PENDING');
    setProgress(0);
    setError(null);
    setCalculationTime(null);
    
    try {
      const fortIds = forts.map(f => String(f.id));
      const res = await fetch(`${API_BASE_URL}/build-network`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fort_ids: fortIds, async: true })
      });
      
      if (!res.ok) throw new Error('Failed to start network build');
      
      const data = await res.json();
      if (data.job_id) {
        setJobId(data.job_id);
      } else if (data.edges) {
        // Returned synchronously (e.g. from cache)
        setJobStatus('COMPLETED');
        processNetworkData(data);
      }
    } catch (err: any) {
      setJobStatus('FAILED');
      setError(err.message);
    }
  };

  const exportNetwork = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify({ nodes, edges }));
    const downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute("href", dataStr);
    downloadAnchorNode.setAttribute("download", "visibility_network.json");
    document.body.appendChild(downloadAnchorNode); // required for firefox
    downloadAnchorNode.click();
    downloadAnchorNode.remove();
  };

  // Filter edges for display
  const displayEdges = edges.filter(e => {
    if (filterStatus === 'visible' && !e.is_visible) return false;
    if (filterStatus === 'blocked' && e.is_visible) return false;
    if (e.visibility_score < minScore) return false;
    return true;
  });

  return (
    <div className="min-h-screen bg-terrain-900 text-slate-100 flex flex-col">
      <header className="bg-terrain-800 border-b border-terrain-700 p-4 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link to="/" className="p-2 bg-terrain-900 rounded-lg hover:bg-terrain-700 text-slate-400 hover:text-white transition-colors">
              <ArrowLeft className="w-5 h-5" />
            </Link>
            <div>
              <h1 className="text-2xl font-bold text-emerald-400 flex items-center gap-3">
                <Network className="w-6 h-6" />
                Fort Visibility Network
              </h1>
              <p className="text-sm text-slate-400 mt-1">Force-directed line-of-sight graph</p>
            </div>
          </div>
          
          <div className="flex gap-3">
            {nodes.length > 0 && (
              <button 
                onClick={exportNetwork}
                className="flex items-center gap-2 px-4 py-2 bg-terrain-700 hover:bg-terrain-600 rounded-lg font-medium transition-colors border border-terrain-600"
              >
                <Download className="w-4 h-4" /> Export JSON
              </button>
            )}
            
            <button 
              onClick={handleBuildNetwork}
              disabled={jobStatus === 'PENDING' || jobStatus === 'PROCESSING' || fortsLoading}
              className={`flex items-center gap-2 px-6 py-2 rounded-lg font-bold transition-colors ${
                jobStatus === 'PENDING' || jobStatus === 'PROCESSING' || fortsLoading
                  ? 'bg-emerald-600/50 text-emerald-200 cursor-not-allowed' 
                  : 'bg-emerald-600 hover:bg-emerald-500 text-white shadow-lg shadow-emerald-900/50'
              }`}
            >
              {jobStatus === 'PENDING' || jobStatus === 'PROCESSING' ? (
                <><RefreshCw className="w-4 h-4 animate-spin" /> Processing...</>
              ) : (
                <><Play className="w-4 h-4" /> {nodes.length > 0 ? 'Rebuild Network' : 'Build Network'}</>
              )}
            </button>
          </div>
        </div>
      </header>

      <main className="flex-1 max-w-7xl mx-auto w-full p-4 flex flex-col">
        {error && (
          <div className="mb-6 p-4 bg-rose-900/30 border border-rose-500/50 rounded-xl flex items-center gap-3 text-rose-400">
            <AlertTriangle className="w-5 h-5 flex-shrink-0" />
            <p>{error}</p>
          </div>
        )}
        
        {(jobStatus === 'PENDING' || jobStatus === 'PROCESSING') && (
          <div className="mb-6 p-6 bg-terrain-800 border border-terrain-700 rounded-xl text-center">
            <RefreshCw className="w-8 h-8 text-emerald-500 animate-spin mx-auto mb-4" />
            <h3 className="text-lg font-bold text-slate-200 mb-2">Analyzing Line of Sight Matrix</h3>
            <p className="text-slate-400 text-sm mb-4">Calculating permutations for {forts?.length || 0} forts using terrain elevation data...</p>
            
            <div className="w-full max-w-md mx-auto bg-terrain-900 rounded-full h-3 border border-terrain-700 overflow-hidden">
              <div 
                className="bg-emerald-500 h-full rounded-full transition-all duration-300"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
            <div className="mt-2 text-xs font-mono text-emerald-400">{progress}% Complete</div>
          </div>
        )}

        {nodes.length > 0 ? (
          <>
            <NetworkStats nodes={nodes} edges={edges} />
            <NetworkFilters 
              filterStatus={filterStatus} setFilterStatus={setFilterStatus}
              minScore={minScore} setMinScore={setMinScore}
            />
            
            <div className="flex-1 min-h-[600px] mb-4">
              <VisibilityGraph nodes={nodes} edges={displayEdges} />
            </div>
            
            {calculationTime && (
              <div className="text-xs text-slate-500 text-center font-mono">
                Network built in {(calculationTime / 1000).toFixed(2)}s
              </div>
            )}
          </>
        ) : (
          jobStatus === 'IDLE' && (
            <div className="flex-1 flex flex-col items-center justify-center text-center p-8 bg-terrain-800/50 rounded-xl border border-dashed border-terrain-700">
              <Network className="w-16 h-16 text-terrain-600 mb-4" />
              <h2 className="text-2xl font-bold text-slate-300 mb-2">No Network Generated</h2>
              <p className="text-slate-400 max-w-md">
                Click "Build Network" to calculate the line-of-sight visibility matrix between all known forts in the area. 
                This uses highly accurate DEM topographical data to determine which forts can see each other.
              </p>
            </div>
          )
        )}
      </main>
    </div>
  );
};
