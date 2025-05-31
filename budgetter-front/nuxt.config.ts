export default defineNuxtConfig({
  ssr: false,
  devtools: { enabled: false },

  app: {
    baseURL: '/budgetter/',
    head: {
      meta: [
        { name: "theme-color", content: "#4CAF50" },
      ],
      link: [
        { rel: 'icon', href: '/budgetter/favicon.ico', sizes: '192x192' },
        { rel: 'apple-touch-icon', href: '/budgetter/icon-192.jpg' },
        { rel: 'manifest', href: '/budgetter/manifest.webmanifest' },
      ],
    },
  },

  modules: [
    "@nuxt/eslint",
    '@vite-pwa/nuxt',
  ],

  pwa: {
    registerType: "autoUpdate",
    includeAssets: ["favicon.ico", "icon-192.png", "icon-512.png"],
    client: {
      installPrompt: true,
    },
    manifest: {
      name: "Budgetter",
      short_name: "Budgetter",
      start_url: "/budgetter/",
      scope: "/budgetter/",
      display: "standalone",
      background_color: "#ffffff",
      theme_color: "#4CAF50",
      icons: [
        {
          src: '/budgetter/icon-192.png',
          sizes: '192x192',
          type: 'image/png',
        },
        {
          src: '/budgetter/icon-512.png',
          sizes: '512x512',
          type: 'image/png',
        },
      ],
    },
    workbox: {
      navigateFallback: null,
    },
  },

  css: [
    "vuetify/styles",
    "@mdi/font/css/materialdesignicons.min.css",
    "~/assets/css/global.css"
  ],

  components: true,

  build: {
    transpile: ["vuetify"],
  },

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE_URL,
    },
  },

  compatibilityDate: "2025-04-22",
});
