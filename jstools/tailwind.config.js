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
    maxWidth: {
      '1/4': '25%',
      '1/2': '50%',
      '3/4': '75%',
      '1/8': '12.5%',
      '1/6': '16.666667%',
      '5/6': '83.333333%',
      '7/8': '87.5%',
      '3/5': '60%',
    },
    extend: {},
  },
  plugins: [],
}

