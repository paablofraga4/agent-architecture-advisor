/** @type {import('next').NextConfig} */
const nextConfig = {
  // Disabled because StrictMode double-mounts effects in dev, which aborts
  // our long-running SSE stream and shows a spurious AbortError.
  reactStrictMode: false,
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8080"}/:path*`,
      },
    ];
  },
};
module.exports = nextConfig;
