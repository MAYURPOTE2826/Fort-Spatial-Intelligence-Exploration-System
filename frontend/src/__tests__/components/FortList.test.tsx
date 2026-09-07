import { describe, it, expect, vi } from 'vitest';
import { render, fireEvent } from '@testing-library/react';
import { FortList } from '../../components/FortList';
import React from 'react';

const mockForts = [
  { id: 1, name: 'Rajgad', marathi_name: 'राजगड', latitude: 18.0, longitude: 73.0 },
  { id: 2, name: 'Torna', marathi_name: 'तोरणा', latitude: 18.1, longitude: 73.1 }
];

describe('FortList Component', () => {
  it('renders a list of forts', () => {
    const { getByText } = render(<FortList forts={mockForts} onFortSelect={vi.fn()} />);
    
    expect(getByText('Rajgad')).toBeDefined();
    expect(getByText('Torna')).toBeDefined();
  });

  it('calls onFortSelect when a fort is clicked', () => {
    const handleSelect = vi.fn();
    const { getByText } = render(<FortList forts={mockForts} onFortSelect={handleSelect} />);
    
    fireEvent.click(getByText('Rajgad'));
    expect(handleSelect).toHaveBeenCalledWith(mockForts[0]);
  });
});
