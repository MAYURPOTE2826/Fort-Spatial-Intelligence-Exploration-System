import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useLocation } from '../../hooks/useLocation';

describe('useLocation', () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  it('initializes with default state', () => {
    const { result } = renderHook(() => useLocation());
    
    expect(result.current.location).toBeNull();
    expect(result.current.error).toBeNull();
  });

  it('handles geolocation not supported', () => {
    // Mock navigator.geolocation as undefined
    Object.defineProperty(global.navigator, 'geolocation', {
      value: undefined,
      configurable: true
    });

    const { result } = renderHook(() => useLocation());
    
    expect(result.current.error).toBeTruthy();
  });
});
