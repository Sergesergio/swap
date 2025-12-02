"use client";

import { useState, useEffect } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import Link from "next/link";
import { authApi } from "@/lib/api-client";

export default function VerifyEmailPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [message, setMessage] = useState("Verifying your email address...");

  useEffect(() => {
    const verifyEmail = async () => {
      const token = searchParams.get("token");

      if (!token) {
        setMessage("Waiting for verification link...");
        return;
      }

      setIsLoading(true);
      try {
        await authApi.verifyEmail(token);
        setSuccess(true);
        setMessage("Email verified successfully! Redirecting...");

        setTimeout(() => {
          router.push("/dashboard");
        }, 2000);
      } catch (err: any) {
        setError(err.response?.data?.message || "Email verification failed");
      } finally {
        setIsLoading(false);
      }
    };

    verifyEmail();
  }, [searchParams, router]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-dark-900 dark:to-dark-800 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-8 text-center">
          {/* Icon */}
          <div className="text-6xl mb-4">
            {success ? "✅" : isLoading ? "⏳" : "📧"}
          </div>

          {/* Title */}
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
            {success ? "Email Verified" : "Verify Your Email"}
          </h2>

          {/* Message */}
          <p className="text-gray-600 dark:text-gray-400 mb-6">{message}</p>

          {/* Error */}
          {error && (
            <div className="mb-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
              <p className="text-red-600 dark:text-red-400 text-sm">{error}</p>
              <div className="mt-4 space-y-2">
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Didn't receive the email?
                </p>
                <button className="text-primary-600 hover:text-primary-700 font-semibold text-sm">
                  Resend verification link
                </button>
              </div>
            </div>
          )}

          {/* Actions */}
          {!isLoading && !success && (
            <div className="space-y-4">
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Check your email for a verification link. Click the link to
                confirm your account.
              </p>
              <Link
                href="/auth/login"
                className="inline-block py-2 px-6 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 transition-colors"
              >
                Back to Login
              </Link>
            </div>
          )}

          {success && (
            <Link
              href="/dashboard"
              className="inline-block py-2 px-6 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 transition-colors mt-4"
            >
              Go to Dashboard
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}
