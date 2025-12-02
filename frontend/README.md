# Swap Frontend

Modern Next.js 14 frontend for the Swap platform with TypeScript, Tailwind CSS, and real-time features.

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: TailwindCSS + Lucide Icons
- **State**: Zustand
- **API**: Axios + WebSocket
- **Forms**: React Hook Form + Zod
- **Auth**: JWT with HttpOnly Cookies

## Project Structure

```
frontend/
├── public/              # Static assets
├── src/
│   ├── app/            # Next.js 14 app router
│   ├── components/     # Reusable React components
│   ├── lib/            # Utilities, helpers, constants
│   ├── services/       # API client services
│   ├── stores/         # Zustand state management
│   ├── types/          # TypeScript type definitions
│   └── hooks/          # Custom React hooks
├── .env.example        # Environment variables template
├── .env.local          # Local environment (not committed)
├── tailwind.config.ts  # Tailwind configuration
├── tsconfig.json       # TypeScript configuration
└── next.config.js      # Next.js configuration
```

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Environment Configuration

Copy `.env.example` to `.env.local` and update values:

```bash
cp .env.example .env.local
```

**`.env.local`:**

```
NEXT_PUBLIC_API_URL=http://localhost:8080
NEXT_PUBLIC_SOCKET_URL=ws://localhost:8080
```

### 3. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view.

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - Check TypeScript types

## Features

### Authentication

- User registration and login
- JWT stored in HttpOnly cookies
- Email verification
- Profile management
- KYC verification with file uploads

### Listings

- Browse all listings with filters
- Create new listings
- Upload images (via MinIO signed URLs)
- View listing details
- Swap or Buy options

### Offers & Negotiation

- Send and receive swap offers
- Offer details with negotiation chat
- Accept/Reject offers
- Real-time chat per offer

### Payments & Wallet

- Wallet balance display
- Payment history
- Escrow management
- Top-up and withdraw options
- Dispute handling

### Real-time Chat

- WebSocket-based messaging
- Typing indicators
- Online status
- Message notifications

### Notifications

- Bell icon with dropdown
- Real-time WebSocket updates
- Direct links to actions
- Mark as read functionality

### Disputes & Admin

- Create disputes for transactions
- Dispute history and tracking
- Admin dashboard (for admins)
- User and dispute management

## API Integration

All API calls go through the Nginx gateway at `http://localhost:8080`:

```
GET  /api/auth/health
POST /api/auth/register
POST /api/auth/login
GET  /api/users/{id}
GET  /api/listings
POST /api/listings
GET  /api/offers
POST /api/offers
POST /api/payments/charge
WS   /ws/chat/{offer_id}
GET  /api/notifications
```

## Component Library

UI components are built with:

- TailwindCSS for styling
- Lucide React for icons
- Framer Motion for animations
- Custom components in `src/components/`

## State Management

Zustand stores in `src/stores/`:

- `authStore` - Authentication state
- `listingStore` - Listings data
- `offerStore` - Offers and negotiations
- `chatStore` - Chat messages
- `notificationStore` - Notifications
- `walletStore` - Wallet information

## Docker

Build and run with Docker:

```bash
docker build -t swap-frontend:latest .
docker run -p 3000:3000 swap-frontend:latest
```

## Deployment

### Production Build

```bash
npm run build
npm start
```

### With Docker Compose

```bash
docker-compose up frontend
```

Frontend will be available at `http://localhost:3000` or through Nginx at `http://localhost:8080/`

## Troubleshooting

### CORS Issues

All requests go through Nginx gateway (`http://localhost:8080`), which handles CORS.

### WebSocket Connection Failed

Ensure Nginx is running and WebSocket support is enabled for `/ws/` paths.

### Environment Variables Not Loading

Ensure `.env.local` is in the root `frontend/` directory. Restart dev server after changes.

## Code Standards

- Use TypeScript strict mode
- Component folder structure: component.tsx + component.module.css (if needed)
- Use React Hooks (no class components)
- Custom hooks in `/hooks` directory
- API calls only through service layer in `/services`
- Zustand stores for global state
- React Hook Form for forms

## Security

- JWT tokens in HttpOnly cookies (set by backend)
- CSRF tokens in meta tags (from backend)
- All API calls through Nginx proxy
- Environment variables never exposed to client (except NEXT*PUBLIC*\*)
- Input validation with Zod
- XSS prevention with React sanitization

## Performance

- Image optimization with Next.js Image component
- Code splitting by route
- API caching with Axios interceptors
- Lazy loading for components
- WebSocket connection pooling

## Support

For issues or questions, refer to:

- [Next.js Documentation](https://nextjs.org/docs)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)
- [Zustand Documentation](https://github.com/pmndrs/zustand)
