import { cn } from "@/lib/utils";

interface KeyInsightCalloutProps {
  children: React.ReactNode;
  className?: string;
}

export function KeyInsightCallout({ children, className }: KeyInsightCalloutProps) {
  return (
    <div
      className={cn(
        "bg-blue-50 border-l-4 border-blue-500 p-4 rounded-r-lg mt-6",
        className
      )}
    >
      <p className="text-sm font-semibold text-blue-900 mb-1">Key Insight:</p>
      <p className="text-gray-700">{children}</p>
    </div>
  );
}
