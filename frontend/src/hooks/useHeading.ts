import { useState, useEffect, useCallback } from 'react';
import { HeadingData, PermissionStatus } from '../types/location';

interface UseHeadingResult {
  headingData: HeadingData | null;
  error: string | null;
  loading: boolean;
  permissionStatus: PermissionStatus;
  requestPermission: () => Promise<void>;
  setManualHeading: (heading: number) => void;
}

export const useHeading = (): UseHeadingResult => {
  const [headingData, setHeadingData] = useState<HeadingData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [permissionStatus, setPermissionStatus] = useState<PermissionStatus>('prompt');
  const [isWatching, setIsWatching] = useState<boolean>(false);

  const handleOrientation = useCallback((event: DeviceOrientationEvent) => {
    let heading: number | null = null;
    let accuracy = 15; // default accuracy guess

    // iOS devices
    if ('webkitCompassHeading' in event) {
      heading = (event as any).webkitCompassHeading;
      accuracy = (event as any).webkitCompassAccuracy || 15;
    } 
    // Android / Standard (absolute true)
    else if (event.absolute && event.alpha !== null) {
      // For absolute orientation, alpha is rotation around z-axis.
      // Compass heading is 360 - alpha.
      heading = 360 - event.alpha;
    }

    if (heading !== null) {
      setHeadingData({
        heading,
        accuracy,
        timestamp: Date.now(),
      });
      setError(null);
    }
  }, []);

  const stopWatching = useCallback(() => {
    if (typeof window !== 'undefined') {
      window.removeEventListener('deviceorientationabsolute', handleOrientation as EventListener);
      window.removeEventListener('deviceorientation', handleOrientation);
      setIsWatching(false);
    }
  }, [handleOrientation]);

  const startWatching = useCallback(() => {
    if (typeof window !== 'undefined') {
      if ('ondeviceorientationabsolute' in window) {
        window.addEventListener('deviceorientationabsolute', handleOrientation as EventListener, true);
      } else if ('ondeviceorientation' in window) {
        window.addEventListener('deviceorientation', handleOrientation, true);
      } else {
        setError('Device orientation not supported');
        setPermissionStatus('unsupported');
        return;
      }
      setIsWatching(true);
      setPermissionStatus('granted');
    }
  }, [handleOrientation]);

  const requestPermission = async () => {
    setLoading(true);
    setError(null);

    try {
      // Check for iOS 13+ permission request
      if (typeof (DeviceOrientationEvent as any).requestPermission === 'function') {
        const permissionState = await (DeviceOrientationEvent as any).requestPermission();
        if (permissionState === 'granted') {
          startWatching();
        } else {
          setPermissionStatus('denied');
          setError('Compass permission denied.');
        }
      } else {
        // Non-iOS 13+ devices, directly start
        startWatching();
      }
    } catch (err: any) {
      setError(err.message || 'Failed to request compass permission');
      setPermissionStatus('unsupported');
    } finally {
      setLoading(false);
    }
  };

  const setManualHeading = useCallback((heading: number) => {
    stopWatching();
    setHeadingData({
      heading,
      accuracy: 0,
      timestamp: Date.now(),
    });
    setError(null);
  }, [stopWatching]);

  useEffect(() => {
    return () => {
      stopWatching();
    };
  }, [stopWatching]);

  return {
    headingData,
    error,
    loading,
    permissionStatus,
    requestPermission,
    setManualHeading,
  };
};
