import { create } from "zustand";

export interface User {
  id: string;
  email: string;
  username: string;
  avatar?: string;
  is_verified: boolean;
  role: "user" | "verified_seller" | "admin";
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  token: string | null;
  setUser: (user: User) => void;
  setToken: (token: string) => void;
  clearAuth: () => void;
  setError: (error: string | null) => void;
  setLoading: (loading: boolean) => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,
  token: null,
  setUser: (user) => set({ user, isAuthenticated: true }),
  setToken: (token) => set({ token }),
  clearAuth: () => set({ user: null, isAuthenticated: false, token: null }),
  setError: (error) => set({ error }),
  setLoading: (loading) => set({ isLoading: loading }),
}));
