import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,  // Helps catch potential bugs in development
  swcMinify: true,        // Enables faster minification for production builds
};

export default nextConfig;
