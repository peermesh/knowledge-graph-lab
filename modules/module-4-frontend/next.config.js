/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  env: {
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
    NEXT_PUBLIC_INGESTION_API: process.env.NEXT_PUBLIC_INGESTION_API || 'http://localhost:8001',
    NEXT_PUBLIC_KNOWLEDGE_API: process.env.NEXT_PUBLIC_KNOWLEDGE_API || 'http://localhost:8002',
    NEXT_PUBLIC_REASONING_API: process.env.NEXT_PUBLIC_REASONING_API || 'http://localhost:8003',
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: process.env.NEXT_PUBLIC_API_BASE_URL + '/api/:path*',
      },
    ];
  },
}

module.exports = nextConfig