import { defineNuxtPlugin } from '#app'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import { VPullToRefresh } from 'vuetify/labs/VPullToRefresh'

export default defineNuxtPlugin(nuxtApp => {
  const vuetify = createVuetify({
    components: {
      ...components,
      VPullToRefresh,
    },
  })

  nuxtApp.vueApp.use(vuetify)
})
