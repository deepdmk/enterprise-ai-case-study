import { cn } from "@/lib/utils";

interface Stat {
  label: string;
  value: string;
  color?: "teal" | "amber" | "magenta" | "navy";
}

interface StatsBarProps {
  stats: Stat[];
  className?: string;
  variant?: "light" | "dark";
}

export function StatsBar({ stats, className, variant = "light" }: StatsBarProps) {
  const colorMap = {
    light: {
      teal: "text-teal",
      amber: "text-amber",
      magenta: "text-magenta",
      navy: "text-navy",
    },
    dark: {
      teal: "bg-teal/10 border-2 border-teal/30",
      amber: "bg-amber/10 border-2 border-amber/30",
      magenta: "bg-magenta/10 border-2 border-magenta/30",
      navy: "bg-white/10 border-2 border-white/30",
    },
  };

  const colorAccent = {
    teal: "border-l-4 border-teal",
    amber: "border-l-4 border-amber",
    magenta: "border-l-4 border-magenta",
    navy: "border-l-4 border-white",
  };

  return (
    <div
      className={cn(
        "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 py-8",
        className
      )}
    >
      {stats.map((stat, index) => (
        <div
          key={index}
          className={cn(
            "text-center p-4 rounded-lg",
            variant === "dark" && stat.color && colorMap.dark[stat.color],
            variant === "dark" && stat.color && colorAccent[stat.color]
          )}
        >
          <div
            className={cn(
              "text-2xl md:text-3xl font-bold mb-2",
              variant === "light" && stat.color ? colorMap.light[stat.color] : "text-white"
            )}
          >
            {stat.value}
          </div>
          <div
            className={cn(
              "text-base font-medium",
              variant === "light" ? "text-gray-600" : "text-white/90"
            )}
          >
            {stat.label}
          </div>
        </div>
      ))}
    </div>
  );
}
