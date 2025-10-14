import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'LectureKit - Teacher Dashboard',
  description: 'Production-grade lecture recording and management platform for educators',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
