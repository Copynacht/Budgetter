export default defineNuxtRouteMiddleware(async (to) => {
  const { $api } = useNuxtApp()

  try {
    await $api.get('/api/me')
    if (to.path === '/login') {
      return navigateTo('/')
    }
  } catch (e) {
    if (to.path !== '/login') {
      return navigateTo('/login')
    }
  }
})
