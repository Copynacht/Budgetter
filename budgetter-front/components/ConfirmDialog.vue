<template>
  <v-dialog v-model="visible" max-width="450">
    <v-card>
      <v-card-title class="headline">
        {{ message }}
      </v-card-title>
      <v-card-text>この操作は取り消せません。</v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="cancel">キャンセル</v-btn>
        <v-btn text color="error" @click="confirm">はい</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref } from 'vue'

const visible = ref(false)
const message = ref('')
let resolveFn = () => {}

function open(msg) {
  message.value = msg
  visible.value = true
  return new Promise((resolve) => {
    resolveFn = resolve
  })
}

function confirm() {
  visible.value = false
  resolveFn(true)
}

function cancel() {
  visible.value = false
  resolveFn(false)
}

defineExpose({ open })
</script>
