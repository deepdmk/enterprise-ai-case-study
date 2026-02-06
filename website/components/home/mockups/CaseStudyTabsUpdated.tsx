"use client";

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/Tabs";
import { JourneyGraphicResponsive } from "@/components/home/mockups/JourneyGraphicResponsive";
import { DemonstratesSectionBalanced } from "@/components/home/mockups/DemonstratesSection";

/**
 * Updated CaseStudyTabs using the responsive journey graphic
 *
 * Changes:
 * - "The Journey" tab now uses JourneyGraphicResponsive (no horizontal scroll)
 * - "What This Demonstrates" tab remains unchanged (already well designed)
 */
export function CaseStudyTabsUpdated() {
  return (
    <div className="bg-gray-200 rounded-b-lg">
      <Tabs defaultValue="journey" className="w-full">
        <TabsList className="w-full justify-start bg-gray-300/50 rounded-none p-0 h-auto border-b border-gray-400">
          <TabsTrigger
            value="journey"
            className="rounded-none data-[state=active]:bg-gray-200 data-[state=active]:shadow-none px-8 py-4 text-base font-semibold data-[state=active]:border-b-2 data-[state=active]:border-navy"
          >
            The Journey
          </TabsTrigger>
          <TabsTrigger
            value="demonstrates"
            className="rounded-none data-[state=active]:bg-gray-200 data-[state=active]:shadow-none px-8 py-4 text-base font-semibold data-[state=active]:border-b-2 data-[state=active]:border-navy"
          >
            What This Demonstrates
          </TabsTrigger>
        </TabsList>

        <TabsContent value="journey" className="p-10 mt-0">
          <h3 className="text-xl font-bold text-navy text-center mb-6">
            Enterprise 18-month Journey from Strategy &rarr; Transformation
            &rarr; Deployment
          </h3>
          <JourneyGraphicResponsive />
        </TabsContent>

        <TabsContent value="demonstrates" className="p-10 mt-0">
          {/* Updated: Using balanced 2x2 layout */}
          <DemonstratesSectionBalanced />
        </TabsContent>
      </Tabs>
    </div>
  );
}
