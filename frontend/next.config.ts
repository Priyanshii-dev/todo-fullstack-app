import type { NextConfig } from "next";

const nextConfig = {
  output: "standalone",
  reactCompiler: true,
  experimental: {
    ppr: false,
  },
  images: {
    remotePatterns: [
      { protocol: "http", hostname: "127.0.0.1", port: "8000" },
      { protocol: "http", hostname: "localhost",    port: "8000" },
      { protocol: "https", hostname: "**" },
    ],
  },
};

export default nextConfig;
