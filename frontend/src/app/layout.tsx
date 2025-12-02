import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Swap Platform - Exchange Items Securely",
  description:
    "Buy, sell, and swap items with ease. Secure escrow payments and real-time messaging.",
  keywords: "swap, exchange, marketplace, buy, sell, escrow",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-white dark:bg-dark-900 text-gray-900 dark:text-gray-100">
        {children}
      </body>
    </html>
  );
}
