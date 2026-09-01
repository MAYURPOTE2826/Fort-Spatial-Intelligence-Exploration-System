import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../services/api';
import { Fort } from '../types/fort';

export const useForts = () => {
  return useQuery({
    queryKey: ['forts'],
    queryFn: async (): Promise<Fort[]> => {
      const response = await apiClient.get('/api/v1/forts');
      return response.data.items || response.data;
    },
  });
};

export const useFort = (id: number) => {
  return useQuery({
    queryKey: ['forts', id],
    queryFn: async (): Promise<Fort> => {
      const response = await apiClient.get(`/api/v1/forts/${id}`);
      return response.data;
    },
    enabled: !!id,
  });
};
