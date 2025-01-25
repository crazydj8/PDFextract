module.exports = {
  reactStrictMode: true,
  env: {
    API_URL: process.env.API_URL || 'http://127.0.0.1:8080',
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://127.0.0.1:8080/api/:path*', // Proxy to Backend
      },
    ];
  },
};