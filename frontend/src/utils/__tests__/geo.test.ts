import { describe, it, expect } from 'vitest';
import { bearingToDirection } from '../geo';

describe('geo utils', () => {
  describe('bearingToDirection', () => {
    it('returns N for 0', () => {
      expect(bearingToDirection(0)).toBe('N');
    });

    it('returns E for 90', () => {
      expect(bearingToDirection(90)).toBe('E');
    });

    it('returns S for 180', () => {
      expect(bearingToDirection(180)).toBe('S');
    });

    it('returns W for 270', () => {
      expect(bearingToDirection(270)).toBe('W');
    });

    it('handles wrapping past 360', () => {
      expect(bearingToDirection(360)).toBe('N');
      expect(bearingToDirection(380)).toBe('NNE'); // roughly 20 deg
    });
  });
});
