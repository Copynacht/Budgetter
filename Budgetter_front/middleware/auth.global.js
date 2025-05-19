export default defineNuxtRouteMiddleware(async (to) => {
  if (to.path === '/login') {
    // ログインページならチェック不要
    return
  }

  const { $api } = useNuxtApp()
  const token = useCookie('access_token').value

  if (!token) {
    return navigateTo('/login')
  }

  try {
    await $api.get('/api/me')
  } catch (e) {
    return navigateTo('/login')
  }
})
