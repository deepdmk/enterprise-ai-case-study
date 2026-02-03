import { cn } from "@/lib/utils";

type Intensity = "HIGH" | "MOD-HIGH" | "MODERATE";

interface IntensityBadgeProps {
  intensity: Intensity;
  className?: string;
}

const intensityColors: Record<Intensity, string> = {
  HIGH: "bg-red-500",
  "MOD-HIGH": "bg-orange-500",
  MODERATE: "bg-amber-500",
};

export function IntensityBadge({ intensity, className }: IntensityBadgeProps) {
  return (
    <span
      className={cn(
        "text-white px-3 py-1 rounded-full text-xs font-semibold whitespace-nowrap",
        intensityColors[intensity],
        className
      )}
    >
      {intensity}
    </span>
  );
}
