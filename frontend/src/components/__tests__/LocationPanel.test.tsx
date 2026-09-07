import { render, screen } from '@testing-library/react';
import { LocationPanel } from '../LocationPanel';
import { describe, it, expect } from 'vitest';

describe('LocationPanel', () => {
  it('displays loading state when location is null', () => {
    render(<LocationPanel location={null} headingData={null} error={null} />);
    expect(screen.getByText('Locating...')).toBeInTheDocument();
  });

  it('displays error message when error is provided', () => {
    render(<LocationPanel location={null} headingData={null} error="Permission denied" />);
    expect(screen.getByText('Permission denied')).toBeInTheDocument();
  });

  it('displays coordinates when location is provided', () => {
    render(<LocationPanel location={{ lat: 18.5, lng: 73.5, alt: null, acc: 5 }} headingData={null} error={null} />);
    expect(screen.getByText(/18.500000/)).toBeInTheDocument();
    expect(screen.getByText(/73.500000/)).toBeInTheDocument();
  });
});
