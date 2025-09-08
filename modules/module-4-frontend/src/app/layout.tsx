import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Providers } from '../components/providers'
import { Navigation } from '../components/navigation'
import { Toaster } from '../components/ui/toaster'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Knowledge Graph Lab',
  description: 'AI-powered autonomous research and knowledge management system',
  keywords: ['AI', 'knowledge graph', 'research', 'creator economy', 'automation'],
  authors: [{ name: 'KGL Team' }],
  viewport: 'width=device-width, initial-scale=1',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} min-h-screen bg-background antialiased`}>
        <Providers>
          <div className="flex min-h-screen flex-col">
            <Navigation />
            <main className="flex-1">
              {children}
            </main>
            <Toaster />
          </div>
        </Providers>
      </body>
    </html>
  )
}