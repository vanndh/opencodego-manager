/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        bg: 'rgb(var(--bg-rgb) / <alpha-value>)',
        surface: 'rgb(var(--surface-rgb) / <alpha-value>)',
        'surface-2': 'rgb(var(--surface-2-rgb) / <alpha-value>)',
        border: 'rgb(var(--border-rgb) / <alpha-value>)',
        'border-muted': 'rgb(var(--border-muted-rgb) / <alpha-value>)',
        'text-primary': 'rgb(var(--text-primary-rgb) / <alpha-value>)',
        'text-secondary': 'rgb(var(--text-secondary-rgb) / <alpha-value>)',
        'text-muted': 'rgb(var(--text-muted-rgb) / <alpha-value>)',
        accent: 'rgb(var(--accent-primary-rgb) / <alpha-value>)',
        'accent-2': 'rgb(var(--accent-secondary-rgb) / <alpha-value>)',
        danger: 'rgb(var(--accent-danger-rgb) / <alpha-value>)',
        info: 'rgb(var(--accent-info-rgb) / <alpha-value>)',
      },
      fontFamily: {
        ui: 'var(--font-ui)',
        mono: 'var(--font-mono)',
      },
      fontSize: {
        body: ['13px', '20px'],
        h1: ['15px', '22px'],
        h2: ['13px', '18px'],
        mono: ['12px', '18px'],
        tiny: ['11px', '16px'],
      },
      borderRadius: {
        sm: '3px',
        md: '4px',
        lg: '6px',
      },
    },
  },
  plugins: [],
}
