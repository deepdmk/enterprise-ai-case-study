"use client";

import { Container } from "@/components/layout/Container";
import { Card } from "@/components/ui/Card";
import { HABITAT_PRINCIPLES } from "@/lib/constants";
import {
  Users,
  Target,
  ShieldCheck,
  Server,
  Eye,
  Network,
  DollarSign,
  LucideIcon,
} from "lucide-react";

const iconMap: Record<string, LucideIcon> = {
  users: Users,
  target: Target,
  "shield-check": ShieldCheck,
  server: Server,
  eye: Eye,
  network: Network,
  "dollar-sign": DollarSign,
};

export function PrinciplesSection() {
  return (
    <section className="py-20 bg-navy text-white">
      <Container>
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold mb-4">Design Philosophy</h2>
          <p className="text-xl text-white/80 max-w-3xl mx-auto">
            Foundational tenets that enable discovery-driven innovation while guaranteeing
            AI transformation
          </p>
        </div>

        <div className="space-y-6">
          {/* Top row - 4 cards */}
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {HABITAT_PRINCIPLES.slice(0, 4).map((principle, index) => {
              const Icon = iconMap[principle.icon];
              return (
                <Card
                  key={index}
                  className="bg-white/5 border-white/10 hover:bg-white/10 transition-colors"
                  hover
                >
                  <div className="flex flex-col items-center text-center">
                    <div className="p-3 bg-teal/20 rounded-lg mb-4">
                      <Icon className="w-8 h-8 text-teal" />
                    </div>
                    <h3 className="text-lg font-bold mb-2">{principle.title}</h3>
                    <p className="text-base text-white/70">{principle.description}</p>
                  </div>
                </Card>
              );
            })}
          </div>

          {/* Bottom row - 3 cards, centered/offset */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 lg:max-w-[75%] lg:mx-auto">
            {HABITAT_PRINCIPLES.slice(4, 7).map((principle, index) => {
              const Icon = iconMap[principle.icon];
              return (
                <Card
                  key={index + 4}
                  className="bg-white/5 border-white/10 hover:bg-white/10 transition-colors"
                  hover
                >
                  <div className="flex flex-col items-center text-center">
                    <div className="p-3 bg-teal/20 rounded-lg mb-4">
                      <Icon className="w-8 h-8 text-teal" />
                    </div>
                    <h3 className="text-lg font-bold mb-2">{principle.title}</h3>
                    <p className="text-base text-white/70">{principle.description}</p>
                  </div>
                </Card>
              );
            })}
          </div>
        </div>
      </Container>
    </section>
  );
}
