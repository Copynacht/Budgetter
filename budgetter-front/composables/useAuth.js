export const useAuth = () => {
    const login = async (email, password) => {
        const { $api } = useNuxtApp()
        const res = await $api.post('/api/token/', {
            email,
            password,
        })

        useCookie('access_token').value = res.data.access
        useCookie('refresh_token').value = res.data.refresh
        await navigateTo('/')
    }

    const logout = async () => {
        useCookie('access_token').value = null
        useCookie('refresh_token').value = null
        await navigateTo('/login')
    }

    return { login, logout }
}
