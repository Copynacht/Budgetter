<template>
  <v-container class="d-flex justify-center align-center fill-height">
    <!-- Snackbar -->
    <v-snackbar v-model="showError"  location="top center" color="error" timeout="3000">
      {{ errorMessage }}
    </v-snackbar>
    <v-card class="pa-6" width="400" elevation="5" rounded="xl">
      <v-card-title class="text-h5 mb-4">ログイン</v-card-title>
      <v-form @submit.prevent="handleLogin" ref="form" fast-fail>
        <v-text-field v-model="email" label="メールアドレス" type="email" prepend-icon="mdi-email" :rules="emailRules"
          required />

        <v-text-field v-model="password" label="パスワード" type="password" prepend-icon="mdi-lock" :rules="passwordRules"
          required />

        <v-btn type="submit" color="primary" class="mt-4" block :loading="loading">
          ログイン
        </v-btn>
      </v-form>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useAuth } from '~/composables/useAuth'

const email = ref('')
const password = ref('')
const loading = ref(false)
const showError = ref(false)
const errorMessage = ref('')

const { login } = useAuth()

const emailRules = [
  v => !!v || 'メールアドレスを入力してください',
  v => /.+@.+\..+/.test(v) || '有効なメールアドレスを入力してください',
]

const passwordRules = [
  v => !!v || 'パスワードを入力してください',
  v => v.length >= 6 || '6文字以上のパスワードを入力してください',
]

const handleLogin = async () => {
  loading.value = true
  try {
    await login(email.value, password.value)
  } catch (e) {
    errorMessage.value = 'ログインに失敗しました'
    showError.value = true
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.fill-height {
  height: 100vh;
}
</style>
