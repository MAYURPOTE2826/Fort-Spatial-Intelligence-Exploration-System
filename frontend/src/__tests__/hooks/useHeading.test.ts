import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useHeading } from '../../hooks/useHeading';

describe('useHeading', () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  it('initializes with default state', () => {
    const { result } = renderHook(() => useHeading());
    
    expect(result.current.heading).toBeNull();
    expect(result.current.accuracy).toBeNull();
  });
});
