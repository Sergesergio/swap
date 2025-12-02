"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { authApi } from "@/lib/api-client";
import { useAuthStore } from "@/stores/auth.store";

export default function LoginPage() {
  const router = useRouter();
  const setUser = useAuthStore((state) => state.setUser);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      const response = await authApi.login(formData);
      const userData = response.data?.user || response.data;

      // Set user in store
      if (userData) {
        setUser(userData);
      }

      // Redirect to dashboard
      router.push("/dashboard");
    } catch (err: any) {
      setError(
        err.response?.data?.message || "Login failed. Please try again."
      );
      console.error("Login error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-dark-900 dark:to-dark-800 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        {/* Card */}
        <div className="bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-8">
          {/* Logo */}
          <div className="text-center mb-8">
            <div className="text-5xl mb-3">🔄</div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
              Swap
            </h1>
            <p className="text-gray-600 dark:text-gray-400 mt-2">
              Welcome back
            </p>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
              <p className="text-red-600 dark:text-red-400 text-sm">{error}</p>
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Email */}
            <div>
              <label
                htmlFor="email"
                className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
              >
                Email Address
              </label>
              <input
                id="email"
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="you@example.com"
                required
                className="w-full px-4 py-2 border border-gray-300 dark:border-dark-600 rounded-lg bg-white dark:bg-dark-700 text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 transition-colors"
              />
            </div>

            {/* Password */}
            <div>
              <label
                htmlFor="password"
                className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
              >
                Password
              </label>
              <input
                id="password"
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="••••••••"
                required
                className="w-full px-4 py-2 border border-gray-300 dark:border-dark-600 rounded-lg bg-white dark:bg-dark-700 text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 transition-colors"
              />
            </div>

            {/* Remember me & Forgot password */}
            <div className="flex items-center justify-between text-sm">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  className="w-4 h-4 text-primary-600 rounded"
                />
                <span className="ml-2 text-gray-600 dark:text-gray-400">
                  Remember me
                </span>
              </label>
              <Link
                href="/auth/forgot-password"
                className="text-primary-600 hover:text-primary-700 font-medium"
              >
                Forgot password?
              </Link>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-2 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors mt-6"
            >
              {isLoading ? "Signing in..." : "Sign In"}
            </button>
          </form>

          {/* Divider */}
          <div className="my-6 relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-300 dark:border-dark-600"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-white dark:bg-dark-800 text-gray-500">
                Or continue with
              </span>
            </div>
          </div>

          {/* Social Login (Placeholder) */}
          <div className="grid grid-cols-2 gap-4">
            <button className="py-2 px-4 border border-gray-300 dark:border-dark-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-dark-700 transition-colors">
              Google
            </button>
            <button className="py-2 px-4 border border-gray-300 dark:border-dark-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-dark-700 transition-colors">
              GitHub
            </button>
          </div>

          {/* Sign Up Link */}
          <p className="text-center mt-6 text-gray-600 dark:text-gray-400">
            Don't have an account?{" "}
            <Link
              href="/auth/register"
              className="text-primary-600 hover:text-primary-700 font-semibold"
            >
              Sign up
            </Link>
          </p>
        </div>

        {/* Footer */}
        <p className="text-center text-gray-600 dark:text-gray-400 text-sm mt-6">
          By signing in, you agree to our{" "}
          <Link href="/terms" className="text-primary-600 hover:underline">
            Terms
          </Link>{" "}
          and{" "}
          <Link href="/privacy" className="text-primary-600 hover:underline">
            Privacy Policy
          </Link>
        </p>
      </div>
    </div>
  );
}
