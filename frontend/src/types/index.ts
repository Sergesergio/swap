// User types
export interface User {
  id: string;
  email: string;
  username: string;
  avatar?: string;
  bio?: string;
  is_verified: boolean;
  role: "user" | "verified_seller" | "admin";
  created_at: string;
}

// Listing types
export interface Listing {
  id: string;
  title: string;
  description: string;
  category: string;
  condition: "new" | "like_new" | "good" | "fair" | "poor";
  item_type: "digital" | "tangible";
  price?: number;
  swap_value?: number;
  images: string[];
  owner_id: string;
  owner?: User;
  is_available: boolean;
  created_at: string;
  updated_at: string;
}

// Offer types
export interface Offer {
  id: string;
  listing_id: string;
  listing?: Listing;
  proposer_id: string;
  proposer?: User;
  items_offered: string[];
  money_add_on?: number;
  status: "pending" | "accepted" | "rejected" | "completed" | "cancelled";
  message?: string;
  created_at: string;
  updated_at: string;
}

// Payment types
export interface Payment {
  id: string;
  offer_id: string;
  buyer_id: string;
  seller_id: string;
  amount: number;
  currency: string;
  status:
    | "pending"
    | "processing"
    | "held"
    | "released"
    | "failed"
    | "refunded";
  payment_method: string;
  escrow_held_at?: string;
  released_at?: string;
  created_at: string;
}

// Chat types
export interface ChatMessage {
  id: string;
  conversation_id: string;
  sender_id: string;
  content: string;
  attachments?: string[];
  read: boolean;
  created_at: string;
}

export interface Conversation {
  id: string;
  participants: string[];
  last_message?: ChatMessage;
  unread_count: number;
  created_at: string;
}

// Notification types
export interface Notification {
  id: string;
  user_id: string;
  title: string;
  message: string;
  type: "offer" | "payment" | "dispute" | "message" | "system";
  related_id?: string;
  related_type?: string;
  read: boolean;
  created_at: string;
}

// Dispute types
export interface Dispute {
  id: string;
  offer_id: string;
  opened_by_id: string;
  reason: string;
  description: string;
  status: "open" | "in_review" | "resolved" | "closed";
  resolution?: string;
  created_at: string;
  updated_at: string;
}

// Wallet types
export interface Wallet {
  id: string;
  user_id: string;
  balance: number;
  locked_balance: number; // Escrow funds
  currency: string;
  created_at: string;
  updated_at: string;
}

export interface Transaction {
  id: string;
  wallet_id: string;
  type:
    | "deposit"
    | "withdrawal"
    | "payment"
    | "refund"
    | "escrow_hold"
    | "escrow_release";
  amount: number;
  description: string;
  status: "pending" | "completed" | "failed";
  created_at: string;
}

// KYC types
export interface KYCVerification {
  id: string;
  user_id: string;
  document_type: string;
  document_url: string;
  status: "pending" | "approved" | "rejected";
  verified_at?: string;
  rejection_reason?: string;
}

// API Response types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}
