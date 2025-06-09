<template>
  <v-container class="fill-height d-flex justify-center align-center">
    <v-card class="pa-6" width="500" elevation="5" rounded="xl">
      <v-card-title class="text-h5 mb-4">ユーザー情報</v-card-title>

      <v-card-text v-if="user">
        <v-list dense>
          <v-list-item>
            <v-list-item-title class="font-weight-bold">ユーザー名</v-list-item-title>
            <v-list-item-subtitle class="custom-text">{{ user.username }}</v-list-item-subtitle>
          </v-list-item>

          <v-divider class="my-3" />

          <v-list-item>
            <v-list-item-title class="font-weight-bold">メールアドレス</v-list-item-title>
            <v-list-item-subtitle class="custom-text">{{ user.email }}</v-list-item-subtitle>
          </v-list-item>
        </v-list>

        <!-- パスワード変更ページへ遷移するボタン -->
        <v-btn class="mt-6" color="primary" block @click="goToPassChange">
          パスワード変更
        </v-btn>

        <!-- 管理者画面へ遷移するボタン -->
        <v-btn v-if="user.is_staff" class="mt-3" color="secondary" block @click="openAdminPanel">
          管理画面を開く
        </v-btn>
      </v-card-text>

      <v-card-text v-else>
        <v-progress-circular indeterminate color="primary" />
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter, useRuntimeConfig } from '#imports'

const user = ref(null)
const router = useRouter()
const config = useRuntimeConfig()
const { $api } = useNuxtApp()

onMounted(async () => {
  try {
    const res = await $api.get('/api/me')
    user.value = res
  } catch (e) {
    console.error('プロフィール情報の取得に失敗しました', e)
    return navigateTo('/login')
  }
})

const goToPassChange = () => {
  router.push('/passchange')
}

const openAdminPanel = () => {
  const adminUrl = `${config.public.apiBase}/admin`
  window.open(adminUrl, '_blank')
}
</script>


<style scoped>
.fill-height {
  height: 100vh;
}
</style>

<style scoped>
.custom-text {
  font-size: 16px;
  font-weight: 500;
  color: #212121;
  line-height: 1.6;
  padding-top: 2px;
}
</style>
