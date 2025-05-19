import axios from 'axios'

export default defineNuxtPlugin((nuxtApp) => {
  const api = axios.create({
    baseURL: useRuntimeConfig().public.apiBase,
    withCredentials: true,
  })

  // リクエスト時にJWTを付与
  api.interceptors.request.use((config) => {
    const accessToken = useCookie('access_token').value
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`
    }
    return config
  })

  // レスポンスで401 → リフレッシュトークン使用
  api.interceptors.response.use(
    (response) => response,
    async (error) => {
      const originalRequest = error.config

      // 401エラー（認証エラー）が発生した場合、リフレッシュトークンを使って再認証
      if (error.response?.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true
        const refreshToken = useCookie('refresh_token').value

        try {
          const res = await api.post('/api/token/refresh/', {
            refresh: refreshToken,
          })

          // 新しいアクセストークンをcookieに保存
          useCookie('access_token').value = res.data.access
          api.defaults.headers.common['Authorization'] = `Bearer ${res.data.access}`

          return api(originalRequest) // 元のリクエストを再送
        } catch (refreshError) {
          // リフレッシュトークンが無効（期限切れ）の場合、ログアウト
          useCookie('access_token').value = null
          useCookie('refresh_token').value = null

          // ログインページにリダイレクト
          return navigateTo('/login')
        }
      }

      // 他のエラーはそのまま返す
      return Promise.reject(error)
    }
  )

  nuxtApp.provide('api', api)
})
