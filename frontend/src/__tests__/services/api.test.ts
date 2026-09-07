import { describe, it, expect, vi } from 'vitest';
import { apiClient } from '../../services/api';

vi.mock('axios', () => {
  return {
    default: {
      create: vi.fn(() => ({
        interceptors: {
          request: { use: vi.fn(), eject: vi.fn() },
          response: { use: vi.fn(), eject: vi.fn() }
        },
        get: vi.fn(),
        post: vi.fn()
      }))
    }
  };
});

describe('API Client', () => {
  it('is created successfully', () => {
    expect(apiClient).toBeDefined();
  });
});
