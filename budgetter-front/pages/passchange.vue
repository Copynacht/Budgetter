<template>
  <v-container class="d-flex justify-center align-center fill-height">
    <!-- スナックバー -->
    <MessageSnackbar ref="snackbarRef" />

    <v-card class="pa-6" width="400" elevation="5" rounded="xl">
      <v-card-title class="text-h5 mb-4">パスワード変更</v-card-title>
      <v-form @submit.prevent="handleChangePassword" ref="form" fast-fail>
        <v-text-field
          v-model="currentPassword"
          label="現在のパスワード"
          type="password"
          prepend-icon="mdi-lock"
          :rules="passwordRules"
          required
        />

        <v-text-field
          v-model="newPassword"
          label="新しいパスワード"
          type="password"
          prepend-icon="mdi-lock-reset"
          :rules="passwordRules"
          required
        />

        <v-text-field
          v-model="newPasswordConfirm"
          label="新しいパスワード（確認）"
          type="password"
          prepend-icon="mdi-lock-check"
          :rules="passwordConfirmRules"
          required
        />

        <v-btn type="submit" color="primary" class="mt-4" block :loading="loading">
          変更する
        </v-btn>
      </v-form>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import MessageSnackbar from '@/components/MessageSnackbar.vue'
import { useNuxtApp } from '#app'

const snackbarRef = ref()
const currentPassword = ref('')
const newPassword = ref('')
const newPasswordConfirm = ref('')
const loading = ref(false)

const router = useRouter()

const passwordRules = [
  v => !!v || 'パスワードを入力してください',
  v => v.length >= 6 || '6文字以上のパスワードを入力してください',
]

const passwordConfirmRules = [
  v => !!v || '確認用パスワードを入力してください',
  v => v === newPassword.value || '新しいパスワードと一致しません',
]

const { $api } = useNuxtApp()

const handleChangePassword = async () => {
  loading.value = true
  try {
    await $api.post('/api/password-change/', {
      current_password: currentPassword.value,
      new_password: newPassword.value,
      new_password_confirm: newPasswordConfirm.value,
    })
    snackbarRef.value?.showSnackbar('success', 'パスワードを変更しました')

    router.push('/profile')
  } catch (err) {
    if (err.data) {
      snackbarRef.value?.showApiErrorMessages(err.data)
    } else {
      snackbarRef.value?.showSnackbar('error', 'パスワード変更に失敗しました')
    }
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
