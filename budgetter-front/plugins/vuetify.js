import { defineNuxtPlugin } from '#app'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'

export default defineNuxtPlugin(nuxtApp => {
  const vuetify = createVuetify({
    components: {
      ...components,
    },
  })

  nuxtApp.vueApp.use(vuetify)
})
