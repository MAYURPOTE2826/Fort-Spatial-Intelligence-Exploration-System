import React, { useState } from 'react';
import { Map } from '../components/Map';
import { LocationPanel } from '../components/LocationPanel';
import { FortList } from '../components/FortList';
import { DevLocationPanel } from '../components/DevLocationPanel';
import { PermissionDialog } from '../components/PermissionDialog';
import { useLocation } from '../hooks/useLocation';
import { useHeading } from '../hooks/useHeading';
import { useForts } from '../hooks/useForts';
import { useVisibility } from '../hooks/useVisibility';
import { Fort } from '../types/fort';
import { useNavigate } from 'react-router-dom';

export const MapPage: React.FC = () => {
  const { 
    location, 
    error: locationError, 
    permissionStatus: locationPermission,
    requestPermission: requestLocationPermission,
    setManualLocation 
  } = useLocation();

  const {
    headingData,
    permissionStatus: headingPermission,
    requestPermission: requestHeadingPermission,
    setManualHeading
  } = useHeading();

  const { data: forts, isLoading: isLoadingForts } = useForts();
  
  // Use combined location and heading for visibility if needed later
  const { data: visibilityData } = useVisibility(location);

  const [selectedFort, setSelectedFort] = useState<Fort | null>(null);
  const [showDevPanel, setShowDevPanel] = useState(import.meta.env.DEV || false);
  const [dismissPermissions, setDismissPermissions] = useState(false);
  const navigate = useNavigate();

  const handleFortClick = (fort: Fort) => {
    navigate(`/fort/${fort.id}`);
  };

  return (
    <div className="flex flex-col h-screen w-full bg-terrain-900 text-slate-100 overflow-hidden relative">
      
      {!dismissPermissions && (
        <PermissionDialog
          locationStatus={locationPermission}
          headingStatus={headingPermission}
          onRequestLocation={requestLocationPermission}
          onRequestHeading={requestHeadingPermission}
          onDismiss={() => setDismissPermissions(true)}
        />
      )}

      {/* Map takes full background */}
      <div className="absolute inset-0 z-0">
        <Map 
          location={location} 
          headingData={headingData}
          forts={forts} 
          visibilityData={visibilityData} 
          onFortClick={handleFortClick} 
        />
      </div>

      {/* Floating UI Elements */}
      <div className="relative z-10 p-2 sm:p-4 pointer-events-none h-full flex flex-col justify-between">
        
        {/* Top layer (Location etc) */}
        <div className="flex justify-between items-start pointer-events-auto w-full">
          <div className="w-full sm:w-80 max-w-[65vw] sm:max-w-none">
            <LocationPanel location={location} headingData={headingData} error={locationError} />
          </div>
          
          <div className="flex flex-col gap-2 items-end">
            <div className="bg-terrain-800 p-2 sm:p-3 rounded-lg shadow-lg border border-terrain-700 ml-2 shrink-0 text-right sm:text-left cursor-pointer pointer-events-auto" onClick={() => setShowDevPanel(!showDevPanel)}>
              <h1 className="text-base sm:text-xl font-bold text-emerald-500">FortSight</h1>
              <p className="text-[9px] sm:text-xs text-slate-400">Tactical Map View</p>
            </div>
            
            {showDevPanel && (
              <div className="w-64 max-w-full">
                <DevLocationPanel 
                  location={location}
                  headingData={headingData}
                  setManualLocation={setManualLocation}
                  setManualHeading={setManualHeading}
                />
              </div>
            )}
          </div>
        </div>

        {/* Bottom layer (Fort list) */}
        <div className="w-full sm:w-80 pointer-events-auto pb-2 sm:pb-4 max-h-[40vh] sm:max-h-none overflow-y-auto">
          <FortList 
            forts={forts} 
            visibilityData={visibilityData} 
            onFortClick={handleFortClick} 
            isLoading={isLoadingForts}
          />
        </div>
        
      </div>

      {/* Slide-over removed, we now navigate to FortDetailsPage */}
    </div>
  );
};
