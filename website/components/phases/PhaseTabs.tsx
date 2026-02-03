"use client";

import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui";

interface PhaseTabsProps {
  vision: React.ReactNode;
  approach: React.ReactNode;
  technical: React.ReactNode;
}

export function PhaseTabs({ vision, approach, technical }: PhaseTabsProps) {
  return (
    <Tabs defaultValue="vision">
      <TabsList className="w-full bg-navy/10 p-2 rounded-lg mb-6">
        <TabsTrigger
          value="vision"
          className="flex-1 text-2xl py-3 data-[state=active]:bg-navy data-[state=active]:text-white data-[state=active]:shadow-sm text-navy"
        >
          Vision
        </TabsTrigger>
        <TabsTrigger
          value="approach"
          className="flex-1 text-2xl py-3 data-[state=active]:bg-navy data-[state=active]:text-white data-[state=active]:shadow-sm text-navy"
        >
          Approach
        </TabsTrigger>
        <TabsTrigger
          value="technical"
          className="flex-1 text-2xl py-3 data-[state=active]:bg-navy data-[state=active]:text-white data-[state=active]:shadow-sm text-navy"
        >
          Technical Implementation
        </TabsTrigger>
      </TabsList>

      <TabsContent value="vision">
        <div className="border border-gray-200 rounded-lg p-6 bg-white border-t-4 border-t-navy">
          {vision}
        </div>
      </TabsContent>
      <TabsContent value="approach">{approach}</TabsContent>
      <TabsContent value="technical">
        <div className="border border-gray-200 rounded-lg p-6 bg-white border-t-4 border-t-navy">
          {technical}
        </div>
      </TabsContent>
    </Tabs>
  );
}
