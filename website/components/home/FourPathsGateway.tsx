'use client';

import Link from 'next/link';

export default function FourPathsGateway() {
  return (
    <div className="bg-gradient-to-br from-slate-800 to-slate-900 p-10">
      <div className="text-center mb-6">
        <h2 className="text-4xl font-bold text-white mb-2">Pick Your Case Path</h2>
        <p className="text-xl text-slate-300">Explore the case study from the angle that matters most to you</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Case Summary - Slate */}
        <Link href="/summary" className="group block h-full">
          <div className="bg-white rounded-xl h-full">
            <div className="rounded-xl p-4 h-full shadow-lg hover:shadow-xl transition-all duration-300 group-hover:-translate-y-1 border-b-4 border-slate-500" style={{ backgroundColor: 'rgba(100, 116, 139, 0.15)' }}>
              <div className="flex items-center gap-3 mb-2">
                <div className="w-10 h-10 bg-slate-200 rounded-lg flex items-center justify-center shadow-md flex-shrink-0">
                  <svg className="w-5 h-5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                  </svg>
                </div>
                <h3 className="text-lg font-bold text-slate-700">Case Summary</h3>
              </div>
              <div className="flex items-center justify-between">
                <p className="text-gray-700 text-base">See the Case at a Glance</p>
                <svg className="w-5 h-5 flex-shrink-0 ml-2 text-slate-500 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7"/>
                </svg>
              </div>
            </div>
          </div>
        </Link>

        {/* Strategic Analysis - Navy */}
        <Link href="/strategy" className="group block h-full">
          <div className="bg-white rounded-xl h-full">
            <div className="rounded-xl p-4 h-full shadow-lg hover:shadow-xl transition-all duration-300 group-hover:-translate-y-1 border-b-4" style={{ borderColor: '#1e3a5f', backgroundColor: 'rgba(30, 58, 95, 0.15)' }}>
              <div className="flex items-center gap-3 mb-2">
                <div className="w-10 h-10 rounded-lg flex items-center justify-center shadow-md flex-shrink-0" style={{ backgroundColor: 'rgba(30, 58, 95, 0.2)' }}>
                  <svg className="w-5 h-5" style={{ color: '#1e3a5f' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
                  </svg>
                </div>
                <h3 className="text-lg font-bold" style={{ color: '#1e3a5f' }}>Strategic Analysis</h3>
              </div>
              <div className="flex items-center justify-between">
                <p className="text-gray-700 text-base">See how we determined the Strategic Approach</p>
                <svg className="w-5 h-5 flex-shrink-0 ml-2 group-hover:translate-x-1 transition-transform" style={{ color: '#1e3a5f' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7"/>
                </svg>
              </div>
            </div>
          </div>
        </Link>

        {/* Transformation Approach - Teal */}
        <Link href="/transformation" className="group block h-full">
          <div className="bg-white rounded-xl h-full">
            <div className="rounded-xl p-4 h-full shadow-lg hover:shadow-xl transition-all duration-300 group-hover:-translate-y-1 border-b-4" style={{ borderColor: '#14b8a6', backgroundColor: 'rgba(20, 184, 166, 0.15)' }}>
              <div className="flex items-center gap-3 mb-2">
                <div className="w-10 h-10 rounded-lg flex items-center justify-center shadow-md flex-shrink-0" style={{ backgroundColor: 'rgba(20, 184, 166, 0.2)' }}>
                  <svg className="w-5 h-5" style={{ color: '#085C4F' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                  </svg>
                </div>
                <h3 className="text-lg font-bold" style={{ color: '#085C4F' }}>Transformation Approach</h3>
              </div>
              <div className="flex items-center justify-between">
                <p className="text-gray-700 text-base">Explore how we built the Transformation Path</p>
                <svg className="w-5 h-5 flex-shrink-0 ml-2 group-hover:translate-x-1 transition-transform" style={{ color: '#085C4F' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7"/>
                </svg>
              </div>
            </div>
          </div>
        </Link>

        {/* Technical Solution - Amber */}
        <Link href="/solution" className="group block h-full">
          <div className="bg-white rounded-xl h-full">
            <div className="rounded-xl p-4 h-full shadow-lg hover:shadow-xl transition-all duration-300 group-hover:-translate-y-1 border-b-4" style={{ borderColor: '#f59e0b', backgroundColor: 'rgba(245, 158, 11, 0.15)' }}>
              <div className="flex items-center gap-3 mb-2">
                <div className="w-10 h-10 rounded-lg flex items-center justify-center shadow-md flex-shrink-0" style={{ backgroundColor: 'rgba(245, 158, 11, 0.2)' }}>
                  <svg className="w-5 h-5" style={{ color: '#92400E' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"/>
                  </svg>
                </div>
                <h3 className="text-lg font-bold" style={{ color: '#92400E' }}>Technical Solution</h3>
              </div>
              <div className="flex items-center justify-between">
                <p className="text-gray-700 text-base">Deep dive into the Technical Solutions we developed</p>
                <svg className="w-5 h-5 flex-shrink-0 ml-2 group-hover:translate-x-1 transition-transform" style={{ color: '#92400E' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7"/>
                </svg>
              </div>
            </div>
          </div>
        </Link>
      </div>
    </div>
  );
}
