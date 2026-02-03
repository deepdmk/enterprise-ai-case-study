import { Container } from "./Container";
import { cn } from "@/lib/utils";

interface PageHeaderProps {
  title: string;
  subtitle?: string;
  children?: React.ReactNode;
  className?: string;
}

export function PageHeader({
  title,
  subtitle,
  children,
  className,
}: PageHeaderProps) {
  return (
    <div className={cn("bg-navy text-white py-16", className)}>
      <Container>
        <h1 className="text-5xl md:text-6xl font-bold mb-4">{title}</h1>
        {subtitle && (
          <p className="text-xl text-white/80 max-w-3xl">{subtitle}</p>
        )}
        {children && <div className="mt-6">{children}</div>}
      </Container>
    </div>
  );
}
