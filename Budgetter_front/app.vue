<template>
    <v-app>
        <!-- Toolbar at the top of the screen -->
        <v-app-bar color="white" height="48">
            <!-- Title of the application with adjusted margin and font size -->
            <v-app-bar-title class="text-h6 ms-3">
                <v-icon icon="mdi-hamburger" @click="drawer = !drawer" />

                <span class="ms-3">{{ pageTitle }}</span>
            </v-app-bar-title>

            <!-- Display logout button only if not on the /login page -->
            <v-btn v-if="!isLoginPage" @click="handleLogout" color="black" variant="outlined">
                <v-icon class="mr-2 mt-1">mdi-logout</v-icon>
                ログアウト
            </v-btn>
        </v-app-bar>

        <!-- Navigation drawer for menu actions -->
        <v-navigation-drawer v-model="drawer">
            <v-list>
                <!-- Menu items in the drawer with icons -->
                <v-list-item title="ホーム (登録)" prepend-icon="mdi-home" @click="navigateTo('/')" />
                
                <v-list-item title="支出明細" prepend-icon="mdi-clipboard-text-clock-outline" @click="navigateTo('/records')" />
                
                <v-list-item title="サブスク管理" prepend-icon="mdi-calendar-sync-outline" @click="navigateTo('/subscription')" />
                
                <v-list-item title="支払方法管理" prepend-icon="mdi-credit-card" @click="navigateTo('/payment')" />

                <v-list-item title="支払カテゴリ管理" prepend-icon="mdi-information-outline" @click="navigateTo('/category')" />

                <v-list-item title="ユーザー情報" prepend-icon="mdi-face-man-profile" @click="navigateTo('/profile')" />
            </v-list>
        </v-navigation-drawer>

        <!-- Main content of the application -->
        <v-main>
            <NuxtPage />
        </v-main>

        <!-- Smaller footer at the bottom of the screen -->
        <v-footer app color="secondary" height="30">
            <v-container class="text-caption text-center">
                © {{ new Date().getFullYear() }} Copynight - All Rights Reserved
            </v-container>
        </v-footer>
    </v-app>
</template>

<script setup>
// Importing `useRoute` to access route-related information
import { useRoute, useRouter } from "vue-router"
import { computed } from "vue"

// Drawer state to open/close the navigation drawer
const drawer = shallowRef(false)

// Get the current route
const route = useRoute()
const router = useRouter()

const { logout } = useAuth()

const handleLogout = async () => {
    await logout()
}

const pageTitle = computed(() => {
    const path = route.path.replace(/\/$/, "")

    if (path.startsWith("/login")) {
        return "ログイン"
    }
    else if (path.startsWith("/records")) {
        return "支出明細"
    }
    else if (path.startsWith("/subscription")) {
        return "サブスク管理"
    }
    else if (path.startsWith("/payment")) {
        return "支払方法管理"
    }
    else if (path.startsWith("/category")) {
        return "カテゴリ管理"
    }
    else if (path.startsWith("/profile")) {
        return "プロフィール"
    }
    else {
        return "Budgetter"
    }
})

// Function to navigate to a new route using `router.push`
function navigateTo(path) {
    router.push(path)
}

// Computed property to check if the current route is '/login'
const isLoginPage = computed(() => route.path === "/login")
</script>
