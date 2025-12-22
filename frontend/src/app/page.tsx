'use client';

import dynamic from 'next/dynamic';

const HomeContent = dynamic(() => import('@/components/home/HomeContent'), {
  ssr: false,
  loading: () => (
    <div className="min-h-screen flex items-center justify-center bg-neon-dark">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-neon-cyan shadow-[0_0_15px_#00f3ff]"></div>
    </div>
  ),
});

export default function HomePage() {
  return <HomeContent />;
}
