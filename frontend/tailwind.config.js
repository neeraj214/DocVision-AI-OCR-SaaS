/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          base: "#0F172A", // Backgrounds / Dark Mode Sidebar (Deep Navy)
        },
        action: {
          primary: "#6366F1", // Primary Buttons / Links (Electric Indigo)
          hover: "#4F46E5",
        },
        ai: {
          highlight1: "#D8B4FE", // Soft Purple for Entities or Selected Text
          highlight2: "#86EFAC", // Mint Green for Sentiment (Positive) or Success
        },
        text: {
          neutral: "#F8FAFC", // Primary Typography (Off-White)
          secondary: "#94A3B8", // Descriptions / Metadata (Muted Slate)
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-out',
        'slide-up': 'slideUp 0.5s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      }
    },
  },
  plugins: [],
}
