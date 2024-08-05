import { defineConfig } from "vite";
import { resolve } from "path";

export default defineConfig({
  base: "/static/",
  build: {
    manifest: "manifest.json",
    outDir: resolve("../public"),
    rollupOptions: {
      input: {
        main: "./ts/main.ts",
      },
    },
  },
});
