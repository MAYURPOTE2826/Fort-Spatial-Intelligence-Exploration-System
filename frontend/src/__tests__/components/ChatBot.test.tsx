import { describe, it, expect, vi } from 'vitest';
import { render, fireEvent } from '@testing-library/react';
import { ChatBot } from '../../components/ChatBot';
import React from 'react';

// Mocking the query mutation to prevent real API calls
vi.mock('../../hooks/useChat', () => ({
  useChat: () => ({
    sendMessage: vi.fn(),
    messages: [],
    isLoading: false
  })
}));

describe('ChatBot Component', () => {
  it('renders input field and send button', () => {
    const { getByPlaceholderText, getByRole } = render(<ChatBot />);
    
    expect(getByPlaceholderText(/Ask/i)).toBeDefined();
    expect(getByRole('button')).toBeDefined();
  });
});
