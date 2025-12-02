import Link from "next/link";

export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-gray-200 dark:border-dark-700 bg-white dark:bg-dark-900 shadow-sm">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <Link
          href="/"
          className="font-bold text-2xl text-primary-600 dark:text-primary-400"
        >
          🔄 Swap
        </Link>

        <nav className="hidden md:flex items-center gap-6">
          <Link
            href="/listings"
            className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
          >
            Browse
          </Link>
          <Link
            href="/offers"
            className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
          >
            Offers
          </Link>
          <Link
            href="/chat"
            className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
          >
            Chat
          </Link>
          <Link
            href="/wallet"
            className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
          >
            Wallet
          </Link>
          <Link
            href="/auth/login"
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            Login
          </Link>
        </nav>

        {/* Mobile menu button */}
        <button className="md:hidden text-gray-600 dark:text-gray-300">
          ☰
        </button>
      </div>
    </header>
  );
}
