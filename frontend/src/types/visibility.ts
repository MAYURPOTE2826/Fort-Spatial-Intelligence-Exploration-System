import { Fort } from './fort';

export type VisibilityStatus = 'visible' | 'uncertain' | 'blocked';

export interface VisibilityResult {
  fort_id: number;
  fort?: Fort;
  status: VisibilityStatus;
  distance_m: number;
  bearing: number;
  visibility_score?: number;
}
