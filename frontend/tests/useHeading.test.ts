import { renderHook, act } from '@testing-library/react-hooks';
import { useHeading } from '../src/hooks/useHeading';

describe('useHeading', () => {
  beforeEach(() => {
    // Mock window object events if necessary
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it('should initialize with default states', () => {
    const { result } = renderHook(() => useHeading());

    expect(result.current.headingData).toBeNull();
    expect(result.current.error).toBeNull();
    expect(result.current.loading).toBe(false);
    expect(result.current.permissionStatus).toBe('prompt');
  });

  it('should allow setting manual heading', () => {
    const { result } = renderHook(() => useHeading());

    act(() => {
      result.current.setManualHeading(180);
    });

    expect(result.current.headingData).toMatchObject({
      heading: 180,
      accuracy: 0,
    });
    expect(result.current.error).toBeNull();
  });
});
