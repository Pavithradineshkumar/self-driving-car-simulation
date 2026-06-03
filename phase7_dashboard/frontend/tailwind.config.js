export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        dash: {
          bg:      "#0d0f14",
          card:    "#141720",
          border:  "#1e2330",
          accent:  "#00e5a0",
          warning: "#ff6b35",
          info:    "#3b9eff",
        }
      },
      fontFamily: {
        mono: ["JetBrains Mono", "monospace"],
      }
    }
  }
}