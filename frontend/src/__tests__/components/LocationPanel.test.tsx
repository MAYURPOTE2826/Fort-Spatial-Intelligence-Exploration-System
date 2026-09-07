import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import { LocationPanel } from '../../components/LocationPanel';
import React from 'react';

describe('LocationPanel Component', () => {
  it('renders location information', () => {
    const location = { lat: 18.5204, lng: 73.8567, accuracy: 10 };
    const { getByText } = render(
      <LocationPanel location={location} heading={null} error={null} />
    );
    
    // Check if parts of the coordinates are rendered
    expect(getByText(/18.520/)).toBeDefined();
    expect(getByText(/73.856/)).toBeDefined();
  });

  it('renders error message if provided', () => {
    const { getByText } = render(
      <LocationPanel location={null} heading={null} error="Permission denied" />
    );
    expect(getByText(/Permission denied/)).toBeDefined();
  });
});
