import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { Sidebar } from '@/components/Sidebar';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Payment QA Platform',
  description: 'AI-powered test automation platform for payments',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-gray-50 flex h-screen overflow-hidden`}>
        <Sidebar />
        <main className="ml-64 flex-1 overflow-y-auto w-full">
          <div className="p-10">
            {children}
          </div>
        </main>
      </body>
    </html>
  );
}
