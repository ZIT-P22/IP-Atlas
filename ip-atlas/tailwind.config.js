/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  content: ["./templates/**/*.{html,htm}"],
  theme: {
    extend: {
      borderColor: theme => ({
        DEFAULT: theme('colors.gray.700'),
      }),
    },
  },
  plugins: [],
}


