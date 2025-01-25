module.exports = {
  reactStrictMode: true,
  env: {
    API_URL: process.env.API_URL || 'http://127.0.0.1:5000',
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://127.0.0.1:5000/:path*', // Proxy to Backend
      },
    ];
  },
};