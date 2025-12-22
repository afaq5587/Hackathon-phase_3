/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  serverExternalPackages: ["better-auth", "better-sqlite3"],
}

module.exports = nextConfig
