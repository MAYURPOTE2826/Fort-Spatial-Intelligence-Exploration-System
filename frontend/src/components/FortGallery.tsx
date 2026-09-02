import React, { useState } from 'react';
import { FortDetail } from '../types/fortDetails';
import { Maximize2, X } from 'lucide-react';

interface Props {
  fort: FortDetail;
}

export const FortGallery: React.FC<Props> = ({ fort }) => {
  const [fullscreenImage, setFullscreenImage] = useState<string | null>(null);

  // In a real app, fort.images would be an array. Using main image as a placeholder gallery.
  const images = fort.image_url ? [fort.image_url] : [];

  if (images.length === 0) {
    return <div className="text-slate-400 p-4 text-sm text-center">No images available for this fort.</div>;
  }

  return (
    <div className="p-4">
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        {images.map((img, idx) => (
          <div 
            key={idx} 
            className="group relative aspect-video bg-terrain-900 rounded-lg overflow-hidden border border-terrain-700 cursor-pointer"
            onClick={() => setFullscreenImage(img)}
          >
            <img 
              src={img} 
              alt={`${fort.name} - View ${idx + 1}`} 
              loading="lazy"
              className="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-opacity duration-300"
            />
            <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors flex items-center justify-center">
              <Maximize2 className="w-6 h-6 text-white opacity-0 group-hover:opacity-100 transition-opacity" />
            </div>
          </div>
        ))}
      </div>

      {/* Fullscreen Modal */}
      {fullscreenImage && (
        <div className="fixed inset-0 z-[100] bg-black/95 flex items-center justify-center p-4 backdrop-blur-md">
          <button 
            onClick={() => setFullscreenImage(null)}
            className="absolute top-6 right-6 p-2 bg-terrain-800/50 hover:bg-terrain-700 text-white rounded-full transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
          <img 
            src={fullscreenImage} 
            alt="Fullscreen view" 
            className="max-w-full max-h-[90vh] object-contain rounded shadow-2xl border border-terrain-700/50"
          />
          {fort.source && (
            <div className="absolute bottom-6 text-xs text-slate-400 bg-terrain-900/50 px-3 py-1 rounded">
              Source: {fort.source}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
