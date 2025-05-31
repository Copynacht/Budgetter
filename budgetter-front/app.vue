<template>
  <v-app>
    <!-- Toolbar -->
    <v-app-bar color="white" height="48">
      <v-app-bar-title class="text-h6 ms-3">
        <v-icon icon="mdi-hamburger" @click="drawer = !drawer" />
        <span class="ms-3">{{ pageTitle }}</span>
      </v-app-bar-title>
      <v-btn v-if="!isLoginPage" @click="handleLogout" color="black" variant="outlined">
        <v-icon class="mr-2 mt-1">mdi-logout</v-icon>
        ログアウト
      </v-btn>
    </v-app-bar>

    <!-- Navigation Drawer -->
    <v-navigation-drawer v-model="drawer">
      <v-list>
        <v-list-item title="ホーム (登録)" prepend-icon="mdi-home" @click="navigateTo('/')" />
        <v-list-item title="支出明細" prepend-icon="mdi-clipboard-text-clock-outline" @click="navigateTo('/records')" />
        <v-list-item title="貸し借り履歴" prepend-icon="mdi-swap-horizontal" @click="navigateTo('/loans')" />
        <v-list-item title="サブスク管理" prepend-icon="mdi-calendar-sync-outline" @click="navigateTo('/subscription')" />
        <v-list-item title="カテゴリ管理" prepend-icon="mdi-information-outline" @click="navigateTo('/category')" />
        <v-list-item title="支払方法管理" prepend-icon="mdi-credit-card" @click="navigateTo('/payment')" />
        <v-list-item title="ユーザー情報" prepend-icon="mdi-face-man-profile" @click="navigateTo('/profile')" />
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <NuxtPage />
    </v-main>

    <!-- Footer -->
    <v-footer app color="white" height="30">
      <v-container class="text-caption text-center">
        © {{ new Date().getFullYear() }} Copynight - All Rights Reserved
      </v-container>
    </v-footer>
  </v-app>
</template>

<script setup>
import { computed, shallowRef } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const drawer = shallowRef(false)
const route = useRoute()
const router = useRouter()
const { logout } = useAuth()

const handleLogout = async () => {
  await logout()
}

const pageTitle = computed(() => {
  const path = route.path.replace(/\/$/, '')

  if (path.startsWith('/login')) return 'ログイン'
  if (path.startsWith('/passchange')) return 'パスワード変更'
  if (path.startsWith('/records')) return '支出明細'
  if (path.startsWith('/loans')) return '貸し借り履歴'
  if (path.startsWith('/subscription')) return 'サブスク管理'
  if (path.startsWith('/category')) return 'カテゴリ管理'
  if (path.startsWith('/payment')) return '支払方法管理'
  if (path.startsWith('/profile')) return 'プロフィール'
  return 'Budgetter'
})

function navigateTo(path) {
  router.push(path)
}

const isLoginPage = computed(() => route.path === '/login')
</script>
