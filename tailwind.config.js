/** @type {import('tailwindcss').Config} */
const forms = require('@tailwindcss/forms');
// Removed incorrect crispyTailwind require

module.exports = {
  content: [
    './templates/**/*.html',
    './static/**/*.js',
    './**/templates/**/*.html',
    './users/templates/users/**/*.html',
    './activities/templates/**/*.html',
    // Removed incorrect crispyTailwind content path
  ],
  theme: {
    extend: {
      colors: {
        'coffee-bean': '#3D2B1F', // Dark brown
        'espresso': '#4B3832',    // Slightly lighter dark brown
        'latte': '#A0785A',      // Medium brown
        'cream': '#FFF8DC',       // Changed to Cornsilk for a warmer off-white
        'paper-cup': '#F5F5F5',   // Changed to WhiteSmoke for a slightly cooler off-white
        'accent-green': '#4CAF50', // A complementary green
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', '-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', 'Roboto', '"Helvetica Neue"', 'Arial', '"Noto Sans"', 'sans-serif', '"Apple Color Emoji"', '"Segoe UI Emoji"', '"Segoe UI Symbol"', '"Noto Color Emoji"'], // Example using Inter
      }
    },
  },
  plugins: [
      forms, // Use imported variable
      // Removed incorrect crispyTailwind plugin
  ],
}

