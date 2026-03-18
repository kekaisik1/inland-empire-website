/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./mysite/templates/**/*.html",
    "./home/templates/**/*.html",
    "./services/templates/**/*.html",
    "./locations/templates/**/*.html",
    "./blog/templates/**/*.html",
    "./pages/templates/**/*.html",
    "./search/templates/**/*.html",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#FFD504",
          hover: "#e6c003",
          light: "#ffe34d",
          pale: "rgba(255,213,4,0.08)",
        },
        text: {
          DEFAULT: "#ffffff",
          muted: "#A0A0A5",
          dark: "#121212",
        },
        border: "rgba(255,255,255,0.1)",
        background: "#1A1B20",
        surface: "#25262C",
        "surface-hover": "#2d2e35",
        footer: "#15161A",
        success: "#22c55e",
        warning: "#f59e0b",
        error: "#ef4444",
        glow: "#00FF94",
      },
      fontFamily: {
        display: ["'Montserrat'", "system-ui", "sans-serif"],
        sans: ["'Inter'", "system-ui", "-apple-system", "sans-serif"],
        script: ["'Sacramento'", "cursive"],
      },
      borderRadius: {
        card: "24px",
        button: "50px",
        input: "8px",
      },
      maxWidth: {
        container: "1280px",
      },
      boxShadow: {
        glow: "0 0 10px #00FF94",
        card: "0 20px 40px rgba(0,0,0,0.3)",
        "card-hover": "0 25px 50px rgba(0,0,0,0.4)",
        button: "0 10px 30px rgba(0,0,0,0.3)",
        "button-hover": "0 15px 40px rgba(0,0,0,0.4)",
        widget: "0 25px 50px -12px rgba(0,0,0,0.5)",
      },
      keyframes: {
        float: {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-10px)" },
        },
        "success-pop": {
          from: { opacity: "0", transform: "scale(0.8)" },
          to: { opacity: "1", transform: "scale(1)" },
        },
      },
      animation: {
        float: "float 3s ease-in-out infinite",
        "success-pop":
          "success-pop 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) forwards",
      },
    },
  },
  plugins: [],
};
