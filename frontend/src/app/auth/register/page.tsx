"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { authApi } from "@/lib/api-client";
import { useAuthStore } from "@/stores/auth.store";

export default function RegisterPage() {
  const router = useRouter();
  const setUser = useAuthStore((state) => state.setUser);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [formData, setFormData] = useState({
    email: "",
    username: "",
    password: "",
    confirmPassword: "",
    terms: false,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, type, value, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const validateForm = () => {
    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match");
      return false;
    }
    if (formData.password.length < 8) {
      setError("Password must be at least 8 characters");
      return false;
    }
    if (!formData.terms) {
      setError("You must agree to the terms and conditions");
      return false;
    }
    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!validateForm()) return;

    setIsLoading(true);

    try {
      const response = await authApi.register({
        email: formData.email,
        username: formData.username,
        password: formData.password,
      });

      const userData = response.data?.user || response.data;
      if (userData) {
        setUser(userData);
      }

      setSuccess(true);

      // Redirect to verify email or dashboard after 2 seconds
      setTimeout(() => {
        router.push("/auth/verify-email");
      }, 2000);
    } catch (err: any) {
      const message =
        err.response?.data?.message ||
        err.response?.data?.detail ||
        "Registration failed";
      setError(message);
      console.error("Registration error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  if (success) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-dark-900 dark:to-dark-800 flex items-center justify-center px-4">
        <div className="text-center">
          <div className="text-6xl mb-4">✅</div>
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Account Created!
          </h2>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            Redirecting you to verify your email...
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-dark-900 dark:to-dark-800 flex items-center justify-center px-4 py-8">
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
              Create your account
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

            {/* Username */}
            <div>
              <label
                htmlFor="username"
                className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
              >
                Username
              </label>
              <input
                id="username"
                type="text"
                name="username"
                value={formData.username}
                onChange={handleChange}
                placeholder="johndoe"
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
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                At least 8 characters
              </p>
            </div>

            {/* Confirm Password */}
            <div>
              <label
                htmlFor="confirmPassword"
                className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
              >
                Confirm Password
              </label>
              <input
                id="confirmPassword"
                type="password"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                placeholder="••••••••"
                required
                className="w-full px-4 py-2 border border-gray-300 dark:border-dark-600 rounded-lg bg-white dark:bg-dark-700 text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 transition-colors"
              />
            </div>

            {/* Terms Agreement */}
            <div className="flex items-start">
              <input
                id="terms"
                type="checkbox"
                name="terms"
                checked={formData.terms}
                onChange={handleChange}
                className="w-4 h-4 text-primary-600 rounded mt-1"
              />
              <label
                htmlFor="terms"
                className="ml-2 text-sm text-gray-600 dark:text-gray-400"
              >
                I agree to the{" "}
                <Link
                  href="/terms"
                  className="text-primary-600 hover:underline"
                >
                  Terms and Conditions
                </Link>{" "}
                and{" "}
                <Link
                  href="/privacy"
                  className="text-primary-600 hover:underline"
                >
                  Privacy Policy
                </Link>
              </label>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-2 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors mt-6"
            >
              {isLoading ? "Creating account..." : "Create Account"}
            </button>
          </form>

          {/* Sign In Link */}
          <p className="text-center mt-6 text-gray-600 dark:text-gray-400">
            Already have an account?{" "}
            <Link
              href="/auth/login"
              className="text-primary-600 hover:text-primary-700 font-semibold"
            >
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
