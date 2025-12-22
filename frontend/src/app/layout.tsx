import type { Metadata } from 'next';
import '../styles/globals.css';

export const metadata: Metadata = {
  title: 'Todo Chatbot - AI-Powered Task Management',
  description: 'Manage your tasks with natural language using our AI-powered chatbot',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen">
        <div className="min-h-screen text-gray-100 selection:bg-neon-cyan/30">
          {children}
        </div>
      </body>
    </html>
  );
}
