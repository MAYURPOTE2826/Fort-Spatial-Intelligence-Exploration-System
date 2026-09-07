import { describe, it, expect } from 'vitest';
import { bearingToDirection } from '../../utils/geo';

describe('bearingToDirection', () => {
  it('returns N for 0 degrees', () => {
    expect(bearingToDirection(0)).toBe('N');
  });

  it('returns E for 90 degrees', () => {
    expect(bearingToDirection(90)).toBe('E');
  });

  it('returns S for 180 degrees', () => {
    expect(bearingToDirection(180)).toBe('S');
  });

  it('returns W for 270 degrees', () => {
    expect(bearingToDirection(270)).toBe('W');
  });

  it('handles negative bearings correctly', () => {
    expect(bearingToDirection(-90)).toBe('W');
  });

  it('handles > 360 bearings correctly', () => {
    expect(bearingToDirection(370)).toBe('N');
    expect(bearingToDirection(450)).toBe('E');
  });
});
