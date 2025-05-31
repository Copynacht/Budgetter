import axios from 'axios'

export default defineNuxtPlugin((nuxtApp) => {
  const api = axios.create({
    baseURL: useRuntimeConfig().public.apiBase,
    withCredentials: true,
  })

  api.interceptors.request.use((config) => {
    const accessToken = useCookie('access_token').value
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`
    }
    return config
  })

  api.interceptors.response.use(
    (response) => response,
    async (error) => {
      const originalRequest = error.config

      // 401 エラーかつリトライでない場合
      if (error.response?.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true

        const refreshToken = useCookie('refresh_token').value
        if (!refreshToken) {
          useCookie('access_token').value = null
          useCookie('refresh_token').value = null
          return Promise.reject(error)
        }

        try {
          const rawAxios = axios.create({
            baseURL: useRuntimeConfig().public.apiBase,
            withCredentials: true,
          })

          const res = await rawAxios.post('/api/token/refresh/', {
            refresh: refreshToken,
          })

          const newAccessToken = res.data.access
          useCookie('access_token').value = newAccessToken
          api.defaults.headers.common['Authorization'] = `Bearer ${newAccessToken}`
          originalRequest.headers.Authorization = `Bearer ${newAccessToken}`

          return api(originalRequest)
        } catch (refreshError) {
          useCookie('access_token').value = null
          useCookie('refresh_token').value = null

          return Promise.reject(refreshError)
        }
      }

      return Promise.reject(error)
    }
  )

  nuxtApp.provide('api', api)
})
