export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-dark-900 dark:to-dark-800">
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl font-bold mb-4 text-gray-900 dark:text-white">
            Welcome to Swap Platform
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-8">
            Buy, sell, and swap items securely with real-time messaging and
            escrow payments
          </p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
            <div className="bg-white dark:bg-dark-800 p-6 rounded-2xl shadow-lg hover:shadow-xl transition-shadow">
              <div className="text-4xl mb-4">🛍️</div>
              <h2 className="text-2xl font-semibold mb-2">Browse Listings</h2>
              <p className="text-gray-600 dark:text-gray-400">
                Explore thousands of items available for swap or purchase
              </p>
            </div>

            <div className="bg-white dark:bg-dark-800 p-6 rounded-2xl shadow-lg hover:shadow-xl transition-shadow">
              <div className="text-4xl mb-4">💬</div>
              <h2 className="text-2xl font-semibold mb-2">Real-time Chat</h2>
              <p className="text-gray-600 dark:text-gray-400">
                Communicate instantly with buyers and sellers
              </p>
            </div>

            <div className="bg-white dark:bg-dark-800 p-6 rounded-2xl shadow-lg hover:shadow-xl transition-shadow">
              <div className="text-4xl mb-4">🔒</div>
              <h2 className="text-2xl font-semibold mb-2">Secure Payments</h2>
              <p className="text-gray-600 dark:text-gray-400">
                Escrow-backed transactions for your peace of mind
              </p>
            </div>
          </div>

          <div className="mt-12 space-y-4 space-y-4">
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Frontend is loading... API endpoints available at
              http://localhost:8080/api/
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}
