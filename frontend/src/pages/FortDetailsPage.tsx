import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Map as MapIcon, Image as ImageIcon, BookOpen, Navigation, Footprints, Eye, MapPin } from 'lucide-react';
import { fortService } from '../services/fortService';
import { FortDetail, Structure, Viewpoint, Trail, Connection } from '../types/fortDetails';
import { FortMap } from '../components/FortMap';
import { StructureInfo } from '../components/StructureInfo';
import { ViewpointsList } from '../components/ViewpointsList';
import { TrailsList } from '../components/TrailsList';
import { FortHistory } from '../components/FortHistory';
import { FortGallery } from '../components/FortGallery';
import { RelatedForts } from '../components/RelatedForts';

export const FortDetailsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const fortId = parseInt(id || '1', 10);

  const [fort, setFort] = useState<FortDetail | null>(null);
  const [structures, setStructures] = useState<Structure[]>([]);
  const [viewpoints, setViewpoints] = useState<Viewpoint[]>([]);
  const [trails, setTrails] = useState<Trail[]>([]);
  const [connections, setConnections] = useState<Connection[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'overview' | 'map' | 'viewpoints' | 'trails' | 'gallery' | 'related'>('overview');

  useEffect(() => {
    const fetchAllData = async () => {
      setLoading(true);
      try {
        const [f, s, v, t, c] = await Promise.all([
          fortService.getFortDetails(fortId),
          fortService.getStructures(fortId),
          fortService.getViewpoints(fortId),
          fortService.getTrails(fortId),
          fortService.getConnections(fortId)
        ]);
        setFort(f);
        setStructures(s);
        setViewpoints(v);
        setTrails(t);
        setConnections(c);
      } catch (err) {
        console.error("Failed to load fort details", err);
      } finally {
        setLoading(false);
      }
    };
    fetchAllData();
  }, [fortId]);

  if (loading) {
    return <div className="min-h-screen bg-terrain-900 text-emerald-500 flex items-center justify-center font-mono">Loading Tactical Data...</div>;
  }

  if (!fort) {
    return <div className="min-h-screen bg-terrain-900 text-rose-500 flex items-center justify-center font-mono">Fort not found.</div>;
  }

  const tabs = [
    { id: 'overview', label: 'Overview', icon: BookOpen },
    { id: 'map', label: 'Internal Map', icon: MapIcon },
    { id: 'viewpoints', label: 'Viewpoints', icon: Eye },
    { id: 'trails', label: 'Trails', icon: Footprints },
    { id: 'gallery', label: 'Gallery', icon: ImageIcon },
    { id: 'related', label: 'Related', icon: Navigation },
  ] as const;

  return (
    <div className="min-h-screen bg-terrain-900 text-slate-100 flex flex-col">
      {/* Header */}
      <header className="bg-terrain-800 border-b border-terrain-700 sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <div className="flex items-center gap-4 mb-2">
            <Link to="/" className="p-2 bg-terrain-900 rounded-lg hover:bg-terrain-700 text-slate-400 hover:text-white transition-colors">
              <ArrowLeft className="w-5 h-5" />
            </Link>
            <div>
              <h1 className="text-2xl font-bold text-emerald-400 flex items-center gap-3">
                {fort.name}
                {fort.marathi_name && (
                  <span className="text-sm font-normal text-amber-500 bg-terrain-900 px-2 py-1 rounded border border-terrain-700">
                    {fort.marathi_name}
                  </span>
                )}
              </h1>
              <div className="flex items-center gap-4 text-xs text-slate-400 mt-1">
                <span className="flex items-center gap-1"><MapPin className="w-3 h-3"/> {fort.district || 'Unknown District'}</span>
                {fort.elevation && <span className="flex items-center gap-1"><Mountain className="w-3 h-3"/> {fort.elevation}m Elev</span>}
              </div>
            </div>
          </div>
          
          {/* Tabs Navigation */}
          <div className="flex overflow-x-auto hide-scrollbar gap-2 mt-4">
            {tabs.map(tab => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-4 py-2 rounded-t-lg font-medium text-sm transition-colors whitespace-nowrap border-b-2
                    ${activeTab === tab.id 
                      ? 'bg-terrain-900 text-emerald-400 border-emerald-500' 
                      : 'text-slate-400 hover:text-slate-200 hover:bg-terrain-800 border-transparent'
                    }`}
                >
                  <Icon className="w-4 h-4" />
                  {tab.label}
                </button>
              );
            })}
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 max-w-6xl mx-auto w-full p-4 overflow-y-auto">
        <div className="bg-terrain-900 rounded-xl">
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2">
                <FortHistory fort={fort} />
              </div>
              <div className="space-y-6 pt-4 lg:pt-0">
                <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2 px-4">
                  <MapPin className="w-5 h-5 text-emerald-500" />
                  Structures Highlights
                </h3>
                <StructureInfo structures={structures.slice(0, 4)} />
              </div>
            </div>
          )}
          
          {activeTab === 'map' && (
             <div className="h-[600px] w-full bg-terrain-800 rounded-xl overflow-hidden shadow-2xl p-2 border border-terrain-700">
               <FortMap fort={fort} structures={structures} viewpoints={viewpoints} trails={trails} />
             </div>
          )}

          {activeTab === 'viewpoints' && <ViewpointsList viewpoints={viewpoints} />}
          {activeTab === 'trails' && <TrailsList trails={trails} />}
          {activeTab === 'gallery' && <FortGallery fort={fort} />}
          {activeTab === 'related' && <RelatedForts connections={connections} />}
        </div>
      </main>
    </div>
  );
};

// Simple mountain icon component for header since it's not imported at top
const Mountain = ({ className }: { className?: string }) => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
    <path d="m8 3 4 8 5-5 5 15H2L8 3z"/>
  </svg>
);
