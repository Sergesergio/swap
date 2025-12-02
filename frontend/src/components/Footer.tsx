export function Footer() {
  return (
    <footer className="border-t border-gray-200 dark:border-dark-700 bg-gray-50 dark:bg-dark-900 py-12 mt-16">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          <div>
            <h3 className="font-bold text-lg mb-4">Swap Platform</h3>
            <p className="text-gray-600 dark:text-gray-400">
              Buy, sell, and swap items securely with real-time messaging.
            </p>
          </div>

          <div>
            <h4 className="font-semibold mb-4">Browse</h4>
            <ul className="space-y-2 text-gray-600 dark:text-gray-400">
              <li>
                <a
                  href="/listings"
                  className="hover:text-gray-900 dark:hover:text-white"
                >
                  All Listings
                </a>
              </li>
              <li>
                <a
                  href="/listings?type=digital"
                  className="hover:text-gray-900 dark:hover:text-white"
                >
                  Digital Items
                </a>
              </li>
              <li>
                <a
                  href="/listings?type=tangible"
                  className="hover:text-gray-900 dark:hover:text-white"
                >
                  Physical Items
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold mb-4">Account</h4>
            <ul className="space-y-2 text-gray-600 dark:text-gray-400">
              <li>
                <a
                  href="/profile"
                  className="hover:text-gray-900 dark:hover:text-white"
                >
                  Profile
                </a>
              </li>
              <li>
                <a
                  href="/wallet"
                  className="hover:text-gray-900 dark:hover:text-white"
                >
                  Wallet
                </a>
              </li>
              <li>
                <a
                  href="/settings"
                  className="hover:text-gray-900 dark:hover:text-white"
                >
                  Settings
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold mb-4">Legal</h4>
            <ul className="space-y-2 text-gray-600 dark:text-gray-400">
              <li>
                <a
                  href="/privacy"
                  className="hover:text-gray-900 dark:hover:text-white"
                >
                  Privacy
                </a>
              </li>
              <li>
                <a
                  href="/terms"
                  className="hover:text-gray-900 dark:hover:text-white"
                >
                  Terms
                </a>
              </li>
              <li>
                <a
                  href="/contact"
                  className="hover:text-gray-900 dark:hover:text-white"
                >
                  Contact
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-200 dark:border-dark-700 pt-8 text-center text-gray-600 dark:text-gray-400">
          <p>&copy; 2025 Swap Platform. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}
