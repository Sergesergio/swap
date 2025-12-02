import { create } from "zustand";

export interface Listing {
  id: string;
  title: string;
  description: string;
  category: string;
  condition: string;
  price?: number;
  images: string[];
  owner_id: string;
  created_at: string;
}

export interface ListingState {
  listings: Listing[];
  currentListing: Listing | null;
  isLoading: boolean;
  error: string | null;
  setListings: (listings: Listing[]) => void;
  setCurrentListing: (listing: Listing | null) => void;
  addListing: (listing: Listing) => void;
  updateListing: (listing: Listing) => void;
  removeListing: (id: string) => void;
  setError: (error: string | null) => void;
  setLoading: (loading: boolean) => void;
}

export const useListingStore = create<ListingState>((set) => ({
  listings: [],
  currentListing: null,
  isLoading: false,
  error: null,
  setListings: (listings) => set({ listings }),
  setCurrentListing: (currentListing) => set({ currentListing }),
  addListing: (listing) =>
    set((state) => ({ listings: [...state.listings, listing] })),
  updateListing: (listing) =>
    set((state) => ({
      listings: state.listings.map((l) => (l.id === listing.id ? listing : l)),
    })),
  removeListing: (id) =>
    set((state) => ({
      listings: state.listings.filter((l) => l.id !== id),
    })),
  setError: (error) => set({ error }),
  setLoading: (loading) => set({ isLoading: loading }),
}));
