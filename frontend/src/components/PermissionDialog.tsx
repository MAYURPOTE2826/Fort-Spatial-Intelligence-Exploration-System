import React, { useState } from 'react';
import { PermissionStatus } from '../types/location';
import { MapPin, Compass, ShieldAlert } from 'lucide-react';

interface PermissionDialogProps {
  locationStatus: PermissionStatus;
  headingStatus: PermissionStatus;
  onRequestLocation: () => void;
  onRequestHeading: () => void;
  onDismiss: () => void;
}

export const PermissionDialog: React.FC<PermissionDialogProps> = ({
  locationStatus,
  headingStatus,
  onRequestLocation,
  onRequestHeading,
  onDismiss,
}) => {
  const [showPrivacy, setShowPrivacy] = useState(false);

  // Only show if at least one needs prompting or is denied (and we want to show a message)
  // But typically we only show the dialog if we want to prompt.
  if (locationStatus === 'granted' && headingStatus === 'granted') {
    return null;
  }
  
  if (locationStatus === 'unsupported' && headingStatus === 'unsupported') {
    return null;
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
      <div className="bg-terrain-800 border border-terrain-700 rounded-xl shadow-2xl w-full max-w-md overflow-hidden flex flex-col">
        <div className="p-6">
          <h2 className="text-xl font-bold text-slate-100 mb-2 flex items-center gap-2">
            <ShieldAlert className="text-emerald-500 w-6 h-6" />
            Sensor Permissions
          </h2>
          <p className="text-slate-300 text-sm mb-6">
            FortSight AI uses your device's sensors to provide a tactical view of nearby historical forts. Data is processed locally.
          </p>

          <div className="space-y-4">
            {/* Location Permission */}
            <div className="bg-terrain-900 p-4 rounded-lg border border-terrain-700 flex items-center justify-between">
              <div className="flex items-start gap-3">
                <MapPin className={`w-5 h-5 mt-0.5 ${locationStatus === 'granted' ? 'text-emerald-500' : 'text-slate-400'}`} />
                <div>
                  <h3 className="font-semibold text-slate-200 text-sm">GPS Location</h3>
                  <p className="text-xs text-slate-400 mt-1">Needed to find nearby forts.</p>
                </div>
              </div>
              <div>
                {locationStatus === 'prompt' && (
                  <button 
                    onClick={onRequestLocation}
                    className="bg-emerald-600 hover:bg-emerald-500 text-white text-xs px-3 py-1.5 rounded transition-colors"
                  >
                    Allow
                  </button>
                )}
                {locationStatus === 'granted' && <span className="text-emerald-500 text-xs font-bold">Granted</span>}
                {locationStatus === 'denied' && <span className="text-rose-500 text-xs font-bold">Denied</span>}
              </div>
            </div>

            {/* Compass Permission */}
            <div className="bg-terrain-900 p-4 rounded-lg border border-terrain-700 flex items-center justify-between">
              <div className="flex items-start gap-3">
                <Compass className={`w-5 h-5 mt-0.5 ${headingStatus === 'granted' ? 'text-emerald-500' : 'text-slate-400'}`} />
                <div>
                  <h3 className="font-semibold text-slate-200 text-sm">Compass Heading</h3>
                  <p className="text-xs text-slate-400 mt-1">Needed to orient the map.</p>
                </div>
              </div>
              <div>
                {headingStatus === 'prompt' && (
                  <button 
                    onClick={onRequestHeading}
                    className="bg-emerald-600 hover:bg-emerald-500 text-white text-xs px-3 py-1.5 rounded transition-colors"
                  >
                    Allow
                  </button>
                )}
                {headingStatus === 'granted' && <span className="text-emerald-500 text-xs font-bold">Granted</span>}
                {headingStatus === 'denied' && <span className="text-rose-500 text-xs font-bold">Denied</span>}
                {headingStatus === 'unsupported' && <span className="text-slate-500 text-xs font-bold">N/A</span>}
              </div>
            </div>
          </div>

          {showPrivacy ? (
            <div className="mt-4 p-3 bg-terrain-900 rounded text-xs text-slate-400 h-32 overflow-y-auto">
              <p className="mb-2"><strong>Data Usage:</strong> GPS and compass data are used exclusively on your device to calculate distance and bearing. They are never sent to our servers.</p>
              <p>You can revoke these permissions at any time through your browser settings. If denied, you can use the Dev Panel to manually input coordinates.</p>
            </div>
          ) : (
            <button 
              onClick={() => setShowPrivacy(true)}
              className="mt-4 text-xs text-emerald-500 hover:text-emerald-400 underline"
            >
              Read Privacy Statement
            </button>
          )}

        </div>
        <div className="bg-terrain-900 p-4 border-t border-terrain-700 flex justify-end">
          <button 
            onClick={onDismiss}
            className="text-slate-300 hover:text-white text-sm font-medium px-4 py-2"
          >
            Continue with current settings
          </button>
        </div>
      </div>
    </div>
  );
};
