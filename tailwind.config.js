/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './static/**/*.js',
    './**/templates/**/*.html',
    './**/static/**/*.js',
  ],
  theme: {
    extend: {
      height: {
        '500px': '500px',
      },
      colors: {
        mapBackground: '#e5f3ff',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}

