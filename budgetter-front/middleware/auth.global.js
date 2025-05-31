// middleware/auth.global.js
export default defineNuxtRouteMiddleware(async (to) => {
  const { $api } = useNuxtApp()
  const token = useCookie('access_token').value

  if (!token) {
    if (to.path !== '/login') {
      return navigateTo('/login')
    }
    return
  }

  try {
    await $api.get('/api/me')

    if (to.path === '/login') {
      return navigateTo('/')
    }
  } catch (e) {
    useCookie('access_token').value = null
    useCookie('refresh_token').value = null
    if (to.path !== '/login') {
      return navigateTo('/login')
    }
  }
})
