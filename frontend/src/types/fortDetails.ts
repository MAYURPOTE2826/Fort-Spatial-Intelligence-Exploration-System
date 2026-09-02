export interface FortDetail {
  id: number;
  name: string;
  marathi_name?: string;
  latitude: number;
  longitude: number;
  elevation?: number;
  district?: string;
  difficulty?: string;
  best_season?: string;
  description?: string;
  history?: string;
  image_url?: string;
  source?: string;
  architectural_style?: string;
  built_by?: string;
  interesting_facts?: string[];
}

export interface Structure {
  id: number;
  name: string;
  type: string;
  description: string;
  historical_significance?: string;
  latitude: number;
  longitude: number;
}

export interface Viewpoint {
  id: number;
  name: string;
  direction: string;
  visible_features: string[];
  difficulty: string;
  time_to_visit: string;
  latitude: number;
  longitude: number;
}

export interface Trail {
  id: number;
  name: string;
  start_point: string;
  end_point: string;
  distance_km: number;
  estimated_time_hours: number;
  difficulty: string;
  elevation_gain: number;
  waypoints: [number, number][]; // [lat, lng] tuples
}

export interface Connection {
  target_fort_id: number;
  target_fort_name: string;
  distance_km: number;
  bearing_deg: number;
  historical_connection?: string;
}
