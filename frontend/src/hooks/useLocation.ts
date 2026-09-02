import { useState, useEffect, useCallback } from 'react';
import { Location, PermissionStatus } from '../types/location';

interface UseLocationResult {
  location: Location | null;
  error: string | null;
  loading: boolean;
  permissionStatus: PermissionStatus;
  requestPermission: () => void;
  setManualLocation: (lat: number, lng: number, heading?: number) => void;
}

export const useLocation = (): UseLocationResult => {
  const [location, setLocation] = useState<Location | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [permissionStatus, setPermissionStatus] = useState<PermissionStatus>('prompt');
  
  // Track watch ID to allow cleanups
  const [watchId, setWatchId] = useState<number | null>(null);

  // Check initial permission status if Permissions API is available
  useEffect(() => {
    if (navigator.permissions && navigator.permissions.query) {
      navigator.permissions.query({ name: 'geolocation' }).then((result) => {
        setPermissionStatus(result.state as PermissionStatus);
        
        result.addEventListener('change', () => {
          setPermissionStatus(result.state as PermissionStatus);
        });
      }).catch(() => {
        // Fallback for browsers that don't support geolocation permission query well (Safari)
        setPermissionStatus('prompt');
      });
    } else {
      setPermissionStatus('prompt');
    }
  }, []);

  const startWatching = useCallback(() => {
    if (!navigator.geolocation) {
      setError('Geolocation is not supported by your browser');
      setPermissionStatus('unsupported');
      setLoading(false);
      return;
    }

    setLoading(true);
    const id = navigator.geolocation.watchPosition(
      (position) => {
        setLocation({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
          elevation: position.coords.altitude || undefined,
          accuracy: position.coords.accuracy,
          heading: position.coords.heading || undefined,
          timestamp: position.timestamp,
        });
        setError(null);
        setLoading(false);
        setPermissionStatus('granted');
      },
      (err) => {
        if (err.code === err.PERMISSION_DENIED) {
          setPermissionStatus('denied');
          setError('Location permission denied.');
        } else {
          setError(err.message);
        }
        setLoading(false);
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 0,
      }
    );
    setWatchId(id);
  }, []);

  const requestPermission = useCallback(() => {
    startWatching();
  }, [startWatching]);

  const setManualLocation = useCallback((lat: number, lng: number, heading?: number) => {
    if (watchId !== null) {
      navigator.geolocation.clearWatch(watchId);
      setWatchId(null);
    }
    setLocation((prev) => ({
      latitude: lat,
      longitude: lng,
      heading: heading !== undefined ? heading : prev?.heading,
      accuracy: 0, // 0 accuracy indicates manual
      timestamp: Date.now(),
    }));
    setError(null);
    setLoading(false);
  }, [watchId]);

  // Clean up on unmount
  useEffect(() => {
    return () => {
      if (watchId !== null) {
        navigator.geolocation.clearWatch(watchId);
      }
    };
  }, [watchId]);

  // Try to start immediately if already granted
  useEffect(() => {
    if (permissionStatus === 'granted' && watchId === null) {
      startWatching();
    } else if (permissionStatus === 'prompt' && watchId === null) {
      setLoading(false); // Waiting for user to click request
    }
  }, [permissionStatus, startWatching, watchId]);

  return { 
    location, 
    error, 
    loading, 
    permissionStatus, 
    requestPermission, 
    setManualLocation 
  };
};
