<template>
  <v-snackbar v-model="show" :color="color" location="top center" timeout="3000">
    <span v-html="message" />
    <template #actions>
      <v-btn icon @click="show = false">
        <v-icon icon="mdi-close" />
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script setup>
import { ref } from 'vue'

const show = ref(false)
const color = ref('success')
const message = ref('')

function showSnackbar(type, msg) {
  if (!['success', 'error'].includes(type)) return
  color.value = type
  message.value = msg
  show.value = true
}

function convertFieldName(key) {
  const map = {
    name: '[名前]',
    payment: '[支払い方法]',
    email: '[メールアドレス]',
    password: '[パスワード]',
    price: '[値段]',
  }
  return map[key] || key
}

function showApiErrorMessages(errorResponse) {
  if (!errorResponse || typeof errorResponse !== 'object') {
    showSnackbar('error', '不明なエラーが発生しました。')
    return
  }

  if (errorResponse.detail === 'no refresh token') {
    showSnackbar('error', 'ログインに失敗しました。<br>メールアドレスやパスワードをお確かめください。')
    return
  }

  const messages = []

  for (const key in errorResponse) {
    const fieldLabel = convertFieldName(key)
    const value = errorResponse[key]

    if (Array.isArray(value)) {
      value.forEach(msg => {
        messages.push(`${fieldLabel}: ${msg}`)
      })
    } else if (typeof value === 'string') {
      messages.push(`${fieldLabel}: ${value}`)
    }
  }

  showSnackbar('error', messages.join('<br>'))
}

defineExpose({ showSnackbar, showApiErrorMessages })
</script>
