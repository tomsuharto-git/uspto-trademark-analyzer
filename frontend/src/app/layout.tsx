import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'USPTO Trademark Risk Analyzer',
  description: 'AI-powered trademark conflict analysis using USPTO data',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen bg-gradient-radial bg-grid-pattern">
          {children}
        </div>
      </body>
    </html>
  )
}
