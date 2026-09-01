/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        terrain: {
          900: '#1c1917', // stone-900
          800: '#292524', // stone-800
          700: '#44403c', // stone-700
          600: '#57534e', // stone-600
        },
        status: {
          visible: '#10b981', // emerald-500
          uncertain: '#f59e0b', // amber-500
          blocked: '#ef4444', // red-500
        }
      }
    },
  },
  plugins: [],
}
