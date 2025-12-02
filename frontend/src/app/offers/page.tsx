"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { offerApi } from "@/lib/api-client";
import { useOfferStore } from "@/stores/offer.store";
import { LoadingSpinner, EmptyState } from "@/components/LoadingStates";
import type { Offer } from "@/types";

export default function OffersPage() {
  const offers = useOfferStore((state) => state.offers);
  const setOffers = useOfferStore((state) => state.setOffers);
  const [isLoading, setIsLoading] = useState(true);
  const [tab, setTab] = useState<"received" | "sent">("received");
  const [filteredOffers, setFilteredOffers] = useState<Offer[]>([]);

  useEffect(() => {
    const fetchOffers = async () => {
      try {
        const response = await offerApi.getOffers();
        const data = response.data.data || response.data;
        setOffers(Array.isArray(data) ? data : []);
      } catch (error) {
        console.error("Failed to fetch offers:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchOffers();
  }, [setOffers]);

  useEffect(() => {
    // In a real app, you'd have a way to distinguish sent vs received
    // For now, we'll show all offers in the received tab
    setFilteredOffers(offers);
  }, [offers, tab]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case "accepted":
        return "bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300";
      case "rejected":
        return "bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300";
      case "pending":
        return "bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300";
      default:
        return "bg-gray-100 dark:bg-dark-700 text-gray-700 dark:text-gray-300";
    }
  };

  return (
    <main className="min-h-screen bg-white dark:bg-dark-900">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary-600 to-blue-600 text-white py-8">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl font-bold mb-2">My Offers</h1>
          <p className="text-blue-100">Manage your swap negotiations</p>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        {/* Tabs */}
        <div className="flex gap-4 mb-8 border-b border-gray-200 dark:border-dark-700">
          <button
            onClick={() => setTab("received")}
            className={`px-6 py-3 font-semibold border-b-2 transition-colors ${
              tab === "received"
                ? "border-primary-600 text-primary-600"
                : "border-transparent text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-300"
            }`}
          >
            Received Offers ({filteredOffers.length})
          </button>
          <button
            onClick={() => setTab("sent")}
            className={`px-6 py-3 font-semibold border-b-2 transition-colors ${
              tab === "sent"
                ? "border-primary-600 text-primary-600"
                : "border-transparent text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-300"
            }`}
          >
            Sent Offers (0)
          </button>
        </div>

        {/* Content */}
        {isLoading ? (
          <LoadingSpinner />
        ) : filteredOffers.length > 0 ? (
          <div className="space-y-4">
            {filteredOffers.map((offer) => (
              <Link key={offer.id} href={`/offers/${offer.id}`}>
                <div className="bg-white dark:bg-dark-800 rounded-2xl p-6 hover:shadow-lg transition-shadow cursor-pointer border border-gray-200 dark:border-dark-700">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-1">
                        Swap Offer #{offer.id.slice(0, 8)}
                      </h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {new Date(offer.created_at).toLocaleDateString()}
                      </p>
                    </div>
                    <span
                      className={`px-3 py-1 rounded-full text-sm font-semibold capitalize ${getStatusColor(
                        offer.status
                      )}`}
                    >
                      {offer.status}
                    </span>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                    <div>
                      <p className="text-xs text-gray-600 dark:text-gray-400 uppercase tracking-wide mb-2">
                        Listing
                      </p>
                      <p className="font-semibold text-gray-900 dark:text-white">
                        {offer.listing?.title || "Item"}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-600 dark:text-gray-400 uppercase tracking-wide mb-2">
                        Items Offered
                      </p>
                      <p className="font-semibold text-gray-900 dark:text-white">
                        {offer.items_offered.length} item
                        {offer.items_offered.length !== 1 ? "s" : ""}
                      </p>
                    </div>
                    {offer.money_add_on && (
                      <div>
                        <p className="text-xs text-gray-600 dark:text-gray-400 uppercase tracking-wide mb-2">
                          Cash Offer
                        </p>
                        <p className="font-semibold text-green-600">
                          ${offer.money_add_on}
                        </p>
                      </div>
                    )}
                  </div>

                  <div className="flex justify-between items-center pt-4 border-t border-gray-200 dark:border-dark-700">
                    {offer.message && (
                      <p className="text-sm text-gray-600 dark:text-gray-400 italic">
                        "{offer.message}"
                      </p>
                    )}
                    <span className="text-primary-600 font-semibold text-sm hover:text-primary-700">
                      View Details →
                    </span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        ) : (
          <EmptyState
            title="No offers yet"
            description="Start browsing listings and making offers to begin trading!"
            action={
              <Link
                href="/listings"
                className="px-6 py-2 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700"
              >
                Browse Listings
              </Link>
            }
          />
        )}
      </div>
    </main>
  );
}
