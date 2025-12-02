"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useAuthStore } from "@/stores/auth.store";
import { useListingStore } from "@/stores/listing.store";
import { listingApi } from "@/lib/api-client";
import {
  LoadingSpinner,
  EmptyState,
  CardSkeleton,
} from "@/components/LoadingStates";

export default function DashboardPage() {
  const user = useAuthStore((state) => state.user);
  const listings = useListingStore((state) => state.listings);
  const setListings = useListingStore((state) => state.setListings);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchListings = async () => {
      try {
        const response = await listingApi.getListings({ limit: 6 });
        setListings(response.data.data || response.data);
      } catch (error) {
        console.error("Failed to fetch listings:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchListings();
  }, [setListings]);

  if (isLoading) {
    return <LoadingSpinner />;
  }

  return (
    <main className="min-h-screen bg-white dark:bg-dark-900">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary-600 to-blue-600 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-4xl font-bold mb-2">
                Welcome back, {user?.username}! 👋
              </h1>
              <p className="text-blue-100">
                Here's what's happening on your account
              </p>
            </div>
            <Link
              href="/listings/create"
              className="px-6 py-2 bg-white text-primary-600 rounded-lg font-semibold hover:bg-blue-50 transition-colors"
            >
              + Create Listing
            </Link>
          </div>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          <div className="bg-white dark:bg-dark-800 p-6 rounded-2xl shadow-sm hover:shadow-md transition-shadow">
            <div className="text-3xl mb-2">📊</div>
            <p className="text-gray-600 dark:text-gray-400 text-sm">
              Active Listings
            </p>
            <p className="text-3xl font-bold text-gray-900 dark:text-white">
              8
            </p>
          </div>

          <div className="bg-white dark:bg-dark-800 p-6 rounded-2xl shadow-sm hover:shadow-md transition-shadow">
            <div className="text-3xl mb-2">💰</div>
            <p className="text-gray-600 dark:text-gray-400 text-sm">
              Wallet Balance
            </p>
            <p className="text-3xl font-bold text-gray-900 dark:text-white">
              $500.00
            </p>
          </div>

          <div className="bg-white dark:bg-dark-800 p-6 rounded-2xl shadow-sm hover:shadow-md transition-shadow">
            <div className="text-3xl mb-2">📨</div>
            <p className="text-gray-600 dark:text-gray-400 text-sm">
              Pending Offers
            </p>
            <p className="text-3xl font-bold text-gray-900 dark:text-white">
              3
            </p>
          </div>

          <div className="bg-white dark:bg-dark-800 p-6 rounded-2xl shadow-sm hover:shadow-md transition-shadow">
            <div className="text-3xl mb-2">⭐</div>
            <p className="text-gray-600 dark:text-gray-400 text-sm">
              Your Rating
            </p>
            <p className="text-3xl font-bold text-gray-900 dark:text-white">
              4.8
            </p>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Recent Listings */}
          <div className="lg:col-span-2">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                Recent Listings
              </h2>
              <Link
                href="/listings"
                className="text-primary-600 hover:text-primary-700 font-semibold text-sm"
              >
                View all →
              </Link>
            </div>

            {listings.length > 0 ? (
              <div className="space-y-4">
                {listings.slice(0, 4).map((listing) => (
                  <div
                    key={listing.id}
                    className="bg-white dark:bg-dark-800 p-4 rounded-xl hover:shadow-md transition-shadow border border-gray-200 dark:border-dark-700"
                  >
                    <div className="flex gap-4">
                      {listing.images[0] && (
                        <img
                          src={listing.images[0]}
                          alt={listing.title}
                          className="w-20 h-20 rounded-lg object-cover"
                        />
                      )}
                      <div className="flex-1">
                        <div className="flex justify-between items-start">
                          <div>
                            <h3 className="font-semibold text-gray-900 dark:text-white">
                              {listing.title}
                            </h3>
                            <p className="text-sm text-gray-600 dark:text-gray-400">
                              {listing.category}
                            </p>
                          </div>
                          {listing.price && (
                            <p className="font-bold text-primary-600">
                              ${listing.price}
                            </p>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <EmptyState
                title="No listings yet"
                description="Create your first listing to start trading!"
                action={
                  <Link
                    href="/listings/create"
                    className="px-6 py-2 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700"
                  >
                    Create Listing
                  </Link>
                }
              />
            )}
          </div>

          {/* Quick Links */}
          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
              Quick Actions
            </h2>
            <div className="space-y-3">
              <Link
                href="/listings"
                className="flex items-center gap-3 p-4 bg-white dark:bg-dark-800 rounded-xl hover:shadow-md transition-shadow border border-gray-200 dark:border-dark-700"
              >
                <div className="text-2xl">🔍</div>
                <div>
                  <p className="font-semibold text-gray-900 dark:text-white">
                    Browse Items
                  </p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Find what to swap
                  </p>
                </div>
              </Link>

              <Link
                href="/offers"
                className="flex items-center gap-3 p-4 bg-white dark:bg-dark-800 rounded-xl hover:shadow-md transition-shadow border border-gray-200 dark:border-dark-700"
              >
                <div className="text-2xl">💬</div>
                <div>
                  <p className="font-semibold text-gray-900 dark:text-white">
                    My Offers
                  </p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    View negotiations
                  </p>
                </div>
              </Link>

              <Link
                href="/chat"
                className="flex items-center gap-3 p-4 bg-white dark:bg-dark-800 rounded-xl hover:shadow-md transition-shadow border border-gray-200 dark:border-dark-700"
              >
                <div className="text-2xl">💭</div>
                <div>
                  <p className="font-semibold text-gray-900 dark:text-white">
                    Messages
                  </p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Check conversations
                  </p>
                </div>
              </Link>

              <Link
                href="/wallet"
                className="flex items-center gap-3 p-4 bg-white dark:bg-dark-800 rounded-xl hover:shadow-md transition-shadow border border-gray-200 dark:border-dark-700"
              >
                <div className="text-2xl">💳</div>
                <div>
                  <p className="font-semibold text-gray-900 dark:text-white">
                    Wallet
                  </p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Manage funds
                  </p>
                </div>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
