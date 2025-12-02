"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { userApi, paymentApi } from "@/lib/api-client";
import { LoadingSpinner } from "@/components/LoadingStates";

interface WalletData {
  id: string;
  balance: number;
  locked_balance: number;
  currency: string;
}

interface Transaction {
  id: string;
  type: string;
  amount: number;
  description: string;
  status: string;
  created_at: string;
}

export default function WalletPage() {
  const [wallet, setWallet] = useState<WalletData | null>(null);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<"overview" | "topup" | "withdraw">(
    "overview"
  );
  const [amount, setAmount] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);

  useEffect(() => {
    const fetchWalletData = async () => {
      try {
        const walletResponse = await userApi.getWallet();
        setWallet(walletResponse.data);

        const historyResponse = await paymentApi.getPaymentHistory();
        setTransactions(historyResponse.data.data || []);
      } catch (error) {
        console.error("Failed to fetch wallet data:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchWalletData();
  }, []);

  const handleTopup = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!amount || parseFloat(amount) <= 0) return;

    setIsProcessing(true);
    try {
      await userApi.topupWallet(parseFloat(amount));
      setAmount("");
      setActiveTab("overview");
      // Refresh wallet data
      const walletResponse = await userApi.getWallet();
      setWallet(walletResponse.data);
    } catch (error) {
      console.error("Topup failed:", error);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleWithdraw = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!amount || parseFloat(amount) <= 0) return;

    setIsProcessing(true);
    try {
      await userApi.withdrawWallet(parseFloat(amount));
      setAmount("");
      setActiveTab("overview");
      // Refresh wallet data
      const walletResponse = await userApi.getWallet();
      setWallet(walletResponse.data);
    } catch (error) {
      console.error("Withdrawal failed:", error);
    } finally {
      setIsProcessing(false);
    }
  };

  if (isLoading) return <LoadingSpinner />;

  return (
    <main className="min-h-screen bg-white dark:bg-dark-900">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary-600 to-blue-600 text-white py-8">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl font-bold mb-2">Your Wallet</h1>
          <p className="text-blue-100">Manage your funds and payments</p>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2">
            {/* Tabs */}
            <div className="bg-white dark:bg-dark-800 rounded-2xl shadow-lg overflow-hidden mb-8">
              <div className="flex border-b border-gray-200 dark:border-dark-700">
                <button
                  onClick={() => setActiveTab("overview")}
                  className={`flex-1 px-6 py-4 font-semibold transition-colors ${
                    activeTab === "overview"
                      ? "bg-primary-600 text-white"
                      : "text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-dark-700"
                  }`}
                >
                  Overview
                </button>
                <button
                  onClick={() => setActiveTab("topup")}
                  className={`flex-1 px-6 py-4 font-semibold transition-colors ${
                    activeTab === "topup"
                      ? "bg-primary-600 text-white"
                      : "text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-dark-700"
                  }`}
                >
                  Add Funds
                </button>
                <button
                  onClick={() => setActiveTab("withdraw")}
                  className={`flex-1 px-6 py-4 font-semibold transition-colors ${
                    activeTab === "withdraw"
                      ? "bg-primary-600 text-white"
                      : "text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-dark-700"
                  }`}
                >
                  Withdraw
                </button>
              </div>

              <div className="p-8">
                {activeTab === "overview" && (
                  <div className="space-y-6">
                    <div>
                      <p className="text-gray-600 dark:text-gray-400 text-sm mb-2">
                        Available Balance
                      </p>
                      <p className="text-5xl font-bold text-primary-600">
                        ${wallet?.balance.toFixed(2) || "0.00"}
                      </p>
                    </div>
                    {wallet?.locked_balance ? (
                      <div className="p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border border-yellow-200 dark:border-yellow-800">
                        <p className="text-sm text-yellow-700 dark:text-yellow-300">
                          🔒{" "}
                          <strong>${wallet.locked_balance.toFixed(2)}</strong>{" "}
                          locked in escrow
                        </p>
                      </div>
                    ) : null}
                  </div>
                )}

                {activeTab === "topup" && (
                  <form onSubmit={handleTopup} className="max-w-md space-y-4">
                    <div>
                      <label className="block text-sm font-semibold text-gray-900 dark:text-white mb-2">
                        Amount to Add
                      </label>
                      <div className="relative">
                        <span className="absolute left-4 top-3 text-gray-600 dark:text-gray-400 text-lg">
                          $
                        </span>
                        <input
                          type="number"
                          step="0.01"
                          min="0.01"
                          value={amount}
                          onChange={(e) => setAmount(e.target.value)}
                          placeholder="0.00"
                          className="w-full pl-8 pr-4 py-3 border border-gray-300 dark:border-dark-600 rounded-lg bg-white dark:bg-dark-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                        />
                      </div>
                    </div>
                    <button
                      type="submit"
                      disabled={isProcessing}
                      className="w-full py-3 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 disabled:opacity-50 transition-colors"
                    >
                      {isProcessing ? "Processing..." : "Add Funds"}
                    </button>
                  </form>
                )}

                {activeTab === "withdraw" && (
                  <form
                    onSubmit={handleWithdraw}
                    className="max-w-md space-y-4"
                  >
                    <div>
                      <label className="block text-sm font-semibold text-gray-900 dark:text-white mb-2">
                        Amount to Withdraw
                      </label>
                      <div className="relative">
                        <span className="absolute left-4 top-3 text-gray-600 dark:text-gray-400 text-lg">
                          $
                        </span>
                        <input
                          type="number"
                          step="0.01"
                          min="0.01"
                          max={wallet?.balance || 0}
                          value={amount}
                          onChange={(e) => setAmount(e.target.value)}
                          placeholder="0.00"
                          className="w-full pl-8 pr-4 py-3 border border-gray-300 dark:border-dark-600 rounded-lg bg-white dark:bg-dark-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                        />
                      </div>
                      <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
                        Maximum: ${wallet?.balance.toFixed(2) || "0.00"}
                      </p>
                    </div>
                    <button
                      type="submit"
                      disabled={isProcessing}
                      className="w-full py-3 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 disabled:opacity-50 transition-colors"
                    >
                      {isProcessing ? "Processing..." : "Withdraw Funds"}
                    </button>
                  </form>
                )}
              </div>
            </div>
          </div>

          {/* Sidebar - Quick Stats */}
          <div className="space-y-4">
            <div className="bg-white dark:bg-dark-800 rounded-2xl p-6 shadow-lg">
              <h3 className="font-bold text-lg mb-4">Quick Stats</h3>
              <div className="space-y-4">
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                    Total Transactions
                  </p>
                  <p className="text-3xl font-bold text-gray-900 dark:text-white">
                    {transactions.length}
                  </p>
                </div>
                <div className="pt-4 border-t border-gray-200 dark:border-dark-700">
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                    Account Status
                  </p>
                  <p className="text-lg font-semibold text-green-600">
                    ✓ Active
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Transaction History */}
        <div className="mt-8 bg-white dark:bg-dark-800 rounded-2xl shadow-lg overflow-hidden">
          <div className="p-6 border-b border-gray-200 dark:border-dark-700">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
              Transaction History
            </h2>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200 dark:border-dark-700 bg-gray-50 dark:bg-dark-700">
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">
                    Type
                  </th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">
                    Amount
                  </th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">
                    Description
                  </th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">
                    Date
                  </th>
                </tr>
              </thead>
              <tbody>
                {transactions.length > 0 ? (
                  transactions.map((tx) => (
                    <tr
                      key={tx.id}
                      className="border-b border-gray-200 dark:border-dark-700 hover:bg-gray-50 dark:hover:bg-dark-700 transition-colors"
                    >
                      <td className="px-6 py-4 text-sm font-medium text-gray-900 dark:text-white capitalize">
                        {tx.type}
                      </td>
                      <td className="px-6 py-4 text-sm font-bold text-gray-900 dark:text-white">
                        ${tx.amount.toFixed(2)}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600 dark:text-gray-400">
                        {tx.description}
                      </td>
                      <td className="px-6 py-4 text-sm">
                        <span
                          className={`px-2 py-1 rounded-full text-xs font-semibold ${
                            tx.status === "completed"
                              ? "bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300"
                              : "bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300"
                          }`}
                        >
                          {tx.status}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600 dark:text-gray-400">
                        {new Date(tx.created_at).toLocaleDateString()}
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td
                      colSpan={5}
                      className="px-6 py-8 text-center text-gray-500 dark:text-gray-400"
                    >
                      No transactions yet
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>
  );
}
