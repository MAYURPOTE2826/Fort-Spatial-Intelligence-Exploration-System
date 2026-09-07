import { describe, it, expect } from 'vitest';
import { formatDistance } from '../../utils/geo';

describe('formatDistance', () => {
  it('formats distances under 1000m correctly', () => {
    expect(formatDistance(500)).toBe('500 m');
    expect(formatDistance(999)).toBe('999 m');
  });

  it('formats distances over 1000m correctly', () => {
    expect(formatDistance(1000)).toBe('1.0 km');
    expect(formatDistance(1500)).toBe('1.5 km');
    expect(formatDistance(12345)).toBe('12.3 km');
  });

  it('handles 0 correctly', () => {
    expect(formatDistance(0)).toBe('0 m');
  });
});
