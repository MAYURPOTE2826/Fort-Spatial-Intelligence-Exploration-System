import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../services/api';
import { Location } from '../types/location';
import { VisibilityResult } from '../types/visibility';

export const useVisibility = (location: Location | null, radiusKm: number = 50) => {
  return useQuery({
    queryKey: ['visibility', location?.latitude, location?.longitude, radiusKm],
    queryFn: async (): Promise<VisibilityResult[]> => {
      if (!location) return [];
      const response = await apiClient.get('/api/v1/visibility/from-location', {
        params: {
          observer_lat: location.latitude,
          observer_lon: location.longitude,
          observer_elevation: location.elevation || 2.0, // Default 2m observer height
          radius_km: radiusKm,
        },
      });
      return response.data;
    },
    enabled: !!location,
  });
};
