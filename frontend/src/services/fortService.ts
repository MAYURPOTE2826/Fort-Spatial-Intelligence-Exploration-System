import { FortDetail, Structure, Viewpoint, Trail, Connection } from '../types/fortDetails';

const API_BASE_URL = 'http://localhost:8000/api/v1/forts';

export const fortService = {
  getFortDetails: async (id: number): Promise<FortDetail> => {
    const res = await fetch(`${API_BASE_URL}/${id}`);
    if (!res.ok) throw new Error('Failed to fetch fort details');
    return res.json();
  },

  getStructures: async (id: number): Promise<Structure[]> => {
    const res = await fetch(`${API_BASE_URL}/${id}/structures`);
    if (!res.ok) throw new Error('Failed to fetch structures');
    const data = await res.json();
    return data.items;
  },

  getViewpoints: async (id: number): Promise<Viewpoint[]> => {
    const res = await fetch(`${API_BASE_URL}/${id}/viewpoints`);
    if (!res.ok) throw new Error('Failed to fetch viewpoints');
    const data = await res.json();
    return data.items;
  },

  getTrails: async (id: number): Promise<Trail[]> => {
    const res = await fetch(`${API_BASE_URL}/${id}/trails`);
    if (!res.ok) throw new Error('Failed to fetch trails');
    const data = await res.json();
    return data.items;
  },

  getConnections: async (id: number): Promise<Connection[]> => {
    const res = await fetch(`${API_BASE_URL}/${id}/connections`);
    if (!res.ok) throw new Error('Failed to fetch connections');
    const data = await res.json();
    return data.items;
  }
};
