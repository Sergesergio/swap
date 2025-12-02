import { create } from "zustand";

export interface ChatMessage {
  id: string;
  sender_id: string;
  content: string;
  timestamp: string;
  read: boolean;
}

export interface ChatState {
  messages: ChatMessage[];
  currentConversation: string | null;
  isConnected: boolean;
  isLoading: boolean;
  error: string | null;
  addMessage: (message: ChatMessage) => void;
  setMessages: (messages: ChatMessage[]) => void;
  setCurrentConversation: (conversationId: string | null) => void;
  setConnected: (connected: boolean) => void;
  setError: (error: string | null) => void;
  setLoading: (loading: boolean) => void;
  clearMessages: () => void;
}

export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  currentConversation: null,
  isConnected: false,
  isLoading: false,
  error: null,
  addMessage: (message) =>
    set((state) => ({ messages: [...state.messages, message] })),
  setMessages: (messages) => set({ messages }),
  setCurrentConversation: (currentConversation) => set({ currentConversation }),
  setConnected: (isConnected) => set({ isConnected }),
  setError: (error) => set({ error }),
  setLoading: (isLoading) => set({ isLoading }),
  clearMessages: () => set({ messages: [] }),
}));
