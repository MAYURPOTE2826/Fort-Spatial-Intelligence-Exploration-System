import { describe, it, expect, vi } from 'vitest';
import { render } from '@testing-library/react';
import { Map } from '../../components/Map';
import React from 'react';

// Mock react-leaflet components
vi.mock('react-leaflet', () => ({
  MapContainer: ({ children }: any) => <div data-testid="map-container">{children}</div>,
  TileLayer: () => <div data-testid="tile-layer" />,
  Marker: ({ children }: any) => <div data-testid="marker">{children}</div>,
  Popup: ({ children }: any) => <div data-testid="popup">{children}</div>,
}));

describe('Map Component', () => {
  it('renders MapContainer', () => {
    const { getByTestId } = render(<Map forts={[]} userLocation={null} />);
    expect(getByTestId('map-container')).toBeDefined();
    expect(getByTestId('tile-layer')).toBeDefined();
  });
});
