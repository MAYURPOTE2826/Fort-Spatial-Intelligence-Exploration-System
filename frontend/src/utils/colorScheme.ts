import { VisibilityStatus } from '../types/visibility';

export const getStatusColor = (status: VisibilityStatus | undefined): string => {
  switch (status) {
    case 'visible':
      return '#10b981'; // emerald-500
    case 'uncertain':
      return '#f59e0b'; // amber-500
    case 'blocked':
      return '#ef4444'; // red-500
    default:
      return '#6b7280'; // gray-500
  }
};
