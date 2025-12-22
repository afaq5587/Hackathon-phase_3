/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Neon / Robotic palette
        neon: {
          cyan: '#00f3ff',
          magenta: '#ff00ff',
          lime: '#39ff14',
          blue: '#1e40af',
          dark: '#0a0a0c', // Deep charcoal
          surface: '#121217', // Lighter charcoal for cards
        },
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#00f3ff', // Primary is now Neon Cyan
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
        // Chat colors
        chat: {
          user: '#00f3ff',      // Neon Cyan for user messages
          assistant: '#121217', // Darker charcoal for assistant
          'user-text': '#0a0a0c',
          'assistant-text': '#f3f4f6',
        },
      },
      fontFamily: {
        sans: ['Inter', 'Outfit', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Menlo', 'monospace'],
      },
      // Responsive breakpoints per spec: 320px - 1920px
      screens: {
        'xs': '320px',
        'sm': '480px',
        'md': '768px',
        'lg': '1024px',
        'xl': '1280px',
        '2xl': '1536px',
        '3xl': '1920px',
      },
      animation: {
        'typing': 'typing 1.4s infinite',
        'fade-in': 'fadeIn 0.3s ease-in-out',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'float': 'float 3s ease-in-out infinite',
      },
      keyframes: {
        typing: {
          '0%, 60%, 100%': { opacity: '0.3' },
          '30%': { opacity: '1' },
        },
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        glow: {
          'from': { boxShadow: '0 0 5px #00f3ff, 0 0 10px #00f3ff' },
          'to': { boxShadow: '0 0 10px #00f3ff, 0 0 20px #00f3ff' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
      },
    },
  },
  plugins: [],
}
