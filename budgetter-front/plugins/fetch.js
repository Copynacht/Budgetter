export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()

  const apiFetch = async (url, options = {}) => {
    try {
      return await $fetch(url, {
        baseURL: config.public.apiBase,
        credentials: 'include',
        ...options,
      })
    } catch (error) {
      if (error?.response?.status === 401) {
        try {
          await $fetch('/api/token/refresh/', {
            method: 'POST',
            baseURL: config.public.apiBase,
            credentials: 'include',
          })
          return await $fetch(url, {
            baseURL: config.public.apiBase,
            credentials: 'include',
            ...options,
          })
        } catch (refreshError) {
          await navigateTo('/login')
          throw refreshError
        }
      }
      throw error
    }
  }

  apiFetch.get = (url, options = {}) => apiFetch(url, { ...options, method: 'GET' })
  apiFetch.post = (url, payload = {}, options = {}) =>
    apiFetch(url, { ...options, method: 'POST', body: payload })
  apiFetch.patch = (url, payload = {}, options = {}) =>
    apiFetch(url, { ...options, method: 'PATCH', body: payload })

  return {
    provide: {
      api: apiFetch,
    },
  }
})
