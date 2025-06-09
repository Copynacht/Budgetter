export const useAuth = () => {
  const { $api } = useNuxtApp()
  const router = useRouter()

  const login = async (email, password) => {
    try {
      await $api.post('/api/token/', { email, password })
      await router.push('/')
    } catch (error) {
      console.error('ログイン失敗', error)
      throw error
    }
  }

  const logout = async () => {
    try {
      await $api.post('/api/logout/')
      await router.push('/login')
    } catch (error) {
      console.error('ログアウト失敗', error)
    }
  }

  return { login, logout }
}
