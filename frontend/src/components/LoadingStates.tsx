export function LoadingSpinner() {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="relative w-16 h-16">
        <div className="absolute inset-0 bg-gradient-to-r from-primary-400 to-blue-600 rounded-full animate-spin"></div>
        <div className="absolute inset-2 bg-white dark:bg-dark-900 rounded-full"></div>
      </div>
    </div>
  );
}

export function CardSkeleton() {
  return (
    <div className="bg-gray-200 dark:bg-dark-700 rounded-2xl p-4 animate-pulse">
      <div className="h-48 bg-gray-300 dark:bg-dark-600 rounded-xl mb-4"></div>
      <div className="h-4 bg-gray-300 dark:bg-dark-600 rounded mb-2"></div>
      <div className="h-4 bg-gray-300 dark:bg-dark-600 rounded mb-4 w-5/6"></div>
      <div className="h-8 bg-gray-300 dark:bg-dark-600 rounded"></div>
    </div>
  );
}

export function EmptyState({
  title,
  description,
  action,
}: {
  title: string;
  description: string;
  action?: React.ReactNode;
}) {
  return (
    <div className="flex flex-col items-center justify-center min-h-96 text-center">
      <div className="text-6xl mb-4">📭</div>
      <h3 className="text-2xl font-semibold mb-2">{title}</h3>
      <p className="text-gray-600 dark:text-gray-400 mb-6 max-w-md">
        {description}
      </p>
      {action}
    </div>
  );
}
