import { create } from "zustand";

export interface Offer {
  id: string;
  listing_id: string;
  proposer_id: string;
  items_offered: string[];
  money_add_on?: number;
  status: "pending" | "accepted" | "rejected" | "completed";
  created_at: string;
}

export interface OfferState {
  offers: Offer[];
  currentOffer: Offer | null;
  isLoading: boolean;
  error: string | null;
  setOffers: (offers: Offer[]) => void;
  setCurrentOffer: (offer: Offer | null) => void;
  addOffer: (offer: Offer) => void;
  updateOffer: (offer: Offer) => void;
  removeOffer: (id: string) => void;
  setError: (error: string | null) => void;
  setLoading: (loading: boolean) => void;
}

export const useOfferStore = create<OfferState>((set) => ({
  offers: [],
  currentOffer: null,
  isLoading: false,
  error: null,
  setOffers: (offers) => set({ offers }),
  setCurrentOffer: (currentOffer) => set({ currentOffer }),
  addOffer: (offer) => set((state) => ({ offers: [...state.offers, offer] })),
  updateOffer: (offer) =>
    set((state) => ({
      offers: state.offers.map((o) => (o.id === offer.id ? offer : o)),
    })),
  removeOffer: (id) =>
    set((state) => ({
      offers: state.offers.filter((o) => o.id !== id),
    })),
  setError: (error) => set({ error }),
  setLoading: (loading) => set({ isLoading: loading }),
}));
