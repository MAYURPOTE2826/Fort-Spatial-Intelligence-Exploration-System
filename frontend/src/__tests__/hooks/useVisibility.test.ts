import { describe, it, expect } from 'vitest';
import { renderHook } from '@testing-library/react';
import { useVisibility } from '../../hooks/useVisibility';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import React from 'react';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

const wrapper = ({ children }: { children: React.ReactNode }) => (
  React.createElement(QueryClientProvider, { client: queryClient }, children)
);

describe('useVisibility', () => {
  it('handles mutation state correctly', () => {
    const { result } = renderHook(() => useVisibility(), { wrapper });
    
    expect(result.current.calculateVisibility).toBeDefined();
    expect(result.current.isCalculating).toBe(false);
  });
});
