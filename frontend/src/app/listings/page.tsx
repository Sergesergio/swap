"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { listingApi } from "@/lib/api-client";
import { useListingStore } from "@/stores/listing.store";
import {
  LoadingSpinner,
  CardSkeleton,
  EmptyState,
} from "@/components/LoadingStates";
import type { Listing } from "@/types";

const CATEGORIES = [
  "Electronics",
  "Books",
  "Clothing",
  "Furniture",
  "Sports",
  "Art",
  "Gaming",
  "Other",
];

const CONDITIONS = ["New", "Like New", "Good", "Fair", "Poor"];

export default function ListingsPage() {
  const listings = useListingStore((state) => state.listings);
  const setListings = useListingStore((state) => state.setListings);
  const [isLoading, setIsLoading] = useState(true);
  const [filters, setFilters] = useState({
    category: "",
    condition: "",
    itemType: "all",
    minPrice: "",
    maxPrice: "",
    search: "",
  });
  const [filteredListings, setFilteredListings] = useState<Listing[]>([]);

  useEffect(() => {
    const fetchListings = async () => {
      try {
        const response = await listingApi.getListings();
        const data = response.data.data || response.data;
        setListings(Array.isArray(data) ? data : []);
      } catch (error) {
        console.error("Failed to fetch listings:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchListings();
  }, [setListings]);

  useEffect(() => {
    let filtered = listings;

    if (filters.search) {
      filtered = filtered.filter(
        (l) =>
          l.title.toLowerCase().includes(filters.search.toLowerCase()) ||
          l.description.toLowerCase().includes(filters.search.toLowerCase())
      );
    }

    if (filters.category) {
      filtered = filtered.filter((l) => l.category === filters.category);
    }

    if (filters.condition) {
      filtered = filtered.filter(
        (l) => l.condition === filters.condition.toLowerCase()
      );
    }

    if (filters.itemType !== "all") {
      filtered = filtered.filter((l) => l.item_type === filters.itemType);
    }

    if (filters.minPrice) {
      filtered = filtered.filter(
        (l) => !l.price || l.price >= parseInt(filters.minPrice)
      );
    }

    if (filters.maxPrice) {
      filtered = filtered.filter(
        (l) => !l.price || l.price <= parseInt(filters.maxPrice)
      );
    }

    setFilteredListings(filtered);
  }, [listings, filters]);

  const handleFilterChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFilters((prev) => ({ ...prev, [name]: value }));
  };

  const handleReset = () => {
    setFilters({
      category: "",
      condition: "",
      itemType: "all",
      minPrice: "",
      maxPrice: "",
      search: "",
    });
  };

  return (
    <main className="min-h-screen bg-white dark:bg-dark-900">
      {/* Hero */}
      <div className="bg-gradient-to-r from-primary-600 to-blue-600 text-white py-8">
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-4xl font-bold mb-2">Browse Listings</h1>
              <p className="text-blue-100">Find items to swap or purchase</p>
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

      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar - Filters */}
          <div className="lg:col-span-1">
            <div className="bg-white dark:bg-dark-800 rounded-2xl p-6 sticky top-4">
              <div className="flex justify-between items-center mb-6">
                <h3 className="font-bold text-lg">Filters</h3>
                <button
                  onClick={handleReset}
                  className="text-sm text-primary-600 hover:text-primary-700 font-semibold"
                >
                  Reset
                </button>
              </div>

              <div className="space-y-6">
                {/* Search */}
                <div>
                  <label className="block text-sm font-semibold text-gray-900 dark:text-white mb-2">
                    Search
                  </label>
                  <input
                    type="text"
                    name="search"
                    value={filters.search}
                    onChange={handleFilterChange}
                    placeholder="Search items..."
                    className="w-full px-3 py-2 border border-gray-300 dark:border-dark-600 rounded-lg bg-white dark:bg-dark-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>

                {/* Item Type */}
                <div>
                  <label className="block text-sm font-semibold text-gray-900 dark:text-white mb-2">
                    Item Type
                  </label>
                  <select
                    name="itemType"
                    value={filters.itemType}
                    onChange={handleFilterChange}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-dark-600 rounded-lg bg-white dark:bg-dark-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                  >
                    <option value="all">All Items</option>
                    <option value="digital">Digital</option>
                    <option value="tangible">Physical</option>
                  </select>
                </div>

                {/* Category */}
                <div>
                  <label className="block text-sm font-semibold text-gray-900 dark:text-white mb-2">
                    Category
                  </label>
                  <select
                    name="category"
                    value={filters.category}
                    onChange={handleFilterChange}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-dark-600 rounded-lg bg-white dark:bg-dark-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                  >
                    <option value="">All Categories</option>
                    {CATEGORIES.map((cat) => (
                      <option key={cat} value={cat}>
                        {cat}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Condition */}
                <div>
                  <label className="block text-sm font-semibold text-gray-900 dark:text-white mb-2">
                    Condition
                  </label>
                  <select
                    name="condition"
                    value={filters.condition}
                    onChange={handleFilterChange}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-dark-600 rounded-lg bg-white dark:bg-dark-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                  >
                    <option value="">All Conditions</option>
                    {CONDITIONS.map((cond) => (
                      <option key={cond} value={cond}>
                        {cond}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Price Range */}
                <div>
                  <label className="block text-sm font-semibold text-gray-900 dark:text-white mb-2">
                    Price Range
                  </label>
                  <div className="space-y-2">
                    <input
                      type="number"
                      name="minPrice"
                      value={filters.minPrice}
                      onChange={handleFilterChange}
                      placeholder="Min price"
                      className="w-full px-3 py-2 border border-gray-300 dark:border-dark-600 rounded-lg bg-white dark:bg-dark-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                    />
                    <input
                      type="number"
                      name="maxPrice"
                      value={filters.maxPrice}
                      onChange={handleFilterChange}
                      placeholder="Max price"
                      className="w-full px-3 py-2 border border-gray-300 dark:border-dark-600 rounded-lg bg-white dark:bg-dark-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Main Content - Listings */}
          <div className="lg:col-span-3">
            <div className="mb-6 flex items-center justify-between">
              <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                {filteredListings.length} results found
              </h2>
            </div>

            {isLoading ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {[1, 2, 3, 4].map((i) => (
                  <CardSkeleton key={i} />
                ))}
              </div>
            ) : filteredListings.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {filteredListings.map((listing) => (
                  <Link key={listing.id} href={`/listings/${listing.id}`}>
                    <div className="bg-white dark:bg-dark-800 rounded-2xl overflow-hidden hover:shadow-lg transition-shadow cursor-pointer">
                      {/* Image */}
                      <div className="relative h-48 bg-gray-200 dark:bg-dark-700 overflow-hidden">
                        {listing.images[0] ? (
                          <img
                            src={listing.images[0]}
                            alt={listing.title}
                            className="w-full h-full object-cover hover:scale-105 transition-transform"
                          />
                        ) : (
                          <div className="w-full h-full flex items-center justify-center text-4xl bg-gray-100 dark:bg-dark-700">
                            📦
                          </div>
                        )}
                        {listing.price && (
                          <div className="absolute top-3 right-3 bg-primary-600 text-white px-3 py-1 rounded-full text-sm font-semibold">
                            ${listing.price}
                          </div>
                        )}
                      </div>

                      {/* Content */}
                      <div className="p-4">
                        <h3 className="font-bold text-lg text-gray-900 dark:text-white mb-1 line-clamp-2">
                          {listing.title}
                        </h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400 mb-3 line-clamp-2">
                          {listing.description}
                        </p>

                        {/* Tags */}
                        <div className="flex flex-wrap gap-2 mb-4">
                          <span className="text-xs bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 px-2 py-1 rounded">
                            {listing.category}
                          </span>
                          <span className="text-xs bg-gray-100 dark:bg-dark-700 text-gray-700 dark:text-gray-300 px-2 py-1 rounded capitalize">
                            {listing.condition}
                          </span>
                        </div>

                        {/* Footer */}
                        <div className="flex items-center justify-between pt-3 border-t border-gray-200 dark:border-dark-700">
                          <span className="text-xs text-gray-500 dark:text-gray-400">
                            📍 Posted 2 days ago
                          </span>
                          <span className="text-primary-600 font-semibold text-sm hover:text-primary-700">
                            View →
                          </span>
                        </div>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            ) : (
              <EmptyState
                title="No listings found"
                description="Try adjusting your filters or create your first listing!"
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
        </div>
      </div>
    </main>
  );
}
