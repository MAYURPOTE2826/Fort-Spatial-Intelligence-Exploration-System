export type PermissionStatus = 'prompt' | 'granted' | 'denied' | 'unsupported';

export interface Location {
  latitude: number;
  longitude: number;
  elevation?: number;
  accuracy?: number; // GPS accuracy in meters
  heading?: number;
  timestamp?: number;
}

export interface HeadingData {
  heading: number; // 0-360 degrees
  accuracy?: number; // degrees
  timestamp?: number;
}
