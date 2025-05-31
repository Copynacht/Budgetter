<template>
  <v-snackbar v-model="show" :color="color" location="top center" timeout="3000">
    {{ message }}
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

// 普通のスナックバー
function showSnackbar(type, msg) {
  if (!['success', 'error'].includes(type)) return
  color.value = type
  message.value = msg
  show.value = true
}

// エラー表示特化スナックバー
function showApiErrorMessages(errorResponse) {
  if (!errorResponse || typeof errorResponse !== 'object') {
    showSnackbar('error', '不明なエラーが発生しました。')
    return
  }

  const messages = []
  for (const key in errorResponse) {
    if (Array.isArray(errorResponse[key])) {
      errorResponse[key].forEach(msg => messages.push(
        msg.replace("name", "[名前]").replace("payment", "[支払い方法]")
      ))
    } else if (typeof errorResponse[key] === 'string') {
      messages.push(errorResponse[key])
    }
  }

  showSnackbar('error', messages.join('\n'))
}

defineExpose({ showSnackbar, showApiErrorMessages })
</script>
