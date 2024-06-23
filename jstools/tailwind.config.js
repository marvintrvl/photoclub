/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '../**/templates/*.html',
    '../**/templates/**/*.html'
  ],
  theme: {
    colors: {
      'fblue': '#20283D',
      'forange': '#E5B083',
      'fgreen': '#426E5D',
      'fgray': '#F5F6F6',
    },
    extend: {},
  },
  plugins: [],
}

