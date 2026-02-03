import { cn } from "@/lib/utils";

interface ContainerProps {
  children: React.ReactNode;
  className?: string;
  size?: "content" | "reading";
}

export function Container({
  children,
  className,
  size = "content",
}: ContainerProps) {
  return (
    <div
      className={cn(
        "mx-auto px-4 sm:px-6 lg:px-8",
        size === "content" && "max-w-[1200px]",
        size === "reading" && "max-w-[800px]",
        className
      )}
    >
      {children}
    </div>
  );
}
