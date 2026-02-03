import { cn } from "@/lib/utils";

interface CardProps {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
  variant?: "default" | "elevated" | "flat" | "accent";
}

const variants = {
  default: "bg-white rounded-lg border border-gray-200 p-6 shadow-sm",
  elevated: "bg-white rounded-lg border-2 border-navy/10 p-6 shadow-lg",
  flat: "bg-gray-50 rounded-lg border border-gray-200 p-6",
  accent: "bg-white rounded-lg border-l-4 p-6 shadow-sm",
};

export function Card({ children, className, hover = false, variant = "default" }: CardProps) {
  return (
    <div
      className={cn(
        variants[variant],
        hover && "hover:shadow-md hover:border-teal/50 transition-all",
        className
      )}
    >
      {children}
    </div>
  );
}
