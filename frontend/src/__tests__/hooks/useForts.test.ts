import { describe, it, expect, vi } from 'vitest';
import { renderHook } from '@testing-library/react';
import { useForts } from '../../hooks/useForts';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import React from 'react';

// Setup React Query provider for testing
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

describe('useForts', () => {
  it('returns loading state initially', () => {
    const { result } = renderHook(() => useForts(), { wrapper });
    
    // React Query might immediately be in pending state
    expect(result.current.isPending || result.current.isLoading).toBe(true);
  });
});
