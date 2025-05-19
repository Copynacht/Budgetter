export default defineNuxtConfig({
  pages: true,
  ssr: false,
  devtools: { enabled: false },

  modules: [
    "@nuxt/eslint",
    '@vite-pwa/nuxt',
  ],

  css: [
    "vuetify/styles",
    "@mdi/font/css/materialdesignicons.min.css",
  ],

  components: true,

  build: {
    transpile: ["vuetify"],
  },

  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE_URL,
    },
  },

  compatibilityDate: "2025-04-22",
})
