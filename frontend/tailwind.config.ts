import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        bg: "#0b1220",
        panel: "#111827",
        border: "#1f2937",
        muted: "#9ca3af",
        accent: "rgb(var(--accent) / <alpha-value>)",
        ok: "#10b981",
        warn: "#f59e0b",
        err: "#ef4444",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "ui-monospace", "monospace"],
      },
    },
  },
  plugins: [],
};
export default config;
