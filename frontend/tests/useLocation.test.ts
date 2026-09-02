import { renderHook, act } from '@testing-library/react-hooks';
import { useLocation } from '../src/hooks/useLocation';

describe('useLocation', () => {
  let mockGeolocation: any;

  beforeEach(() => {
    mockGeolocation = {
      watchPosition: vi.fn(),
      clearWatch: vi.fn(),
    };
    Object.defineProperty(global.navigator, 'geolocation', {
      value: mockGeolocation,
      configurable: true,
    });
    Object.defineProperty(global.navigator, 'permissions', {
      value: {
        query: vi.fn().mockResolvedValue({ state: 'prompt', addEventListener: vi.fn() }),
      },
      configurable: true,
    });
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it('should initialize with default states', async () => {
    const { result, waitForNextUpdate } = renderHook(() => useLocation());
    
    // allow useEffects to run
    await act(async () => {
      await new Promise((resolve) => setTimeout(resolve, 0));
    });

    expect(result.current.location).toBeNull();
    expect(result.current.error).toBeNull();
    expect(result.current.loading).toBe(false); // Finished loading because we're at prompt
    expect(result.current.permissionStatus).toBe('prompt');
  });

  it('should allow setting manual location', () => {
    const { result } = renderHook(() => useLocation());

    act(() => {
      result.current.setManualLocation(18.5204, 73.8567, 90);
    });

    expect(result.current.location).toMatchObject({
      latitude: 18.5204,
      longitude: 73.8567,
      heading: 90,
      accuracy: 0,
    });
    expect(result.current.error).toBeNull();
    expect(result.current.loading).toBe(false);
  });
});
