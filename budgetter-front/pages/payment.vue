<template>
  <v-container>
    <v-progress-linear v-if="loading" indeterminate color="primary" />
    <div v-else>
      <!-- スナックバー -->
      <MessageSnackbar ref="snackbarRef" />

      <!-- 確認ダイアログ -->
      <ConfirmDialog ref="confirmDialog" />

      <v-row>
        <v-col cols="12">
          <div class="text-center">
            <v-btn color="primary" @click="addAllPayments">
              <v-icon left>mdi-plus</v-icon> 支払い方法の候補をすべて追加
            </v-btn>
          </div>
        </v-col>

        ※アイテムはドラッグ＆ドロップで並び替えできます

        <v-col cols="12">
          <!-- Paymentの並び替え -->
          <draggable :delay="300" :delayOnTouchOnly="false" v-model="payments"
            :group="{ name: 'payments', pull: true, put: false }" item-key="id" @delayStart="handleDragStart"
            @end="onPaymentOrderChange" :move="checkMoveParent">
            <template #item="{ element: payment }">
              <v-card class="mb-4 custom-p-card">
                <v-card-title class="d-flex justify-space-between align-center">
                  <div>
                    <v-icon class="me-2">{{ payment.icon || 'mdi-currency-usd' }}</v-icon>
                    {{ payment.name }}
                  </div>

                  <v-spacer />

                  <v-btn icon @click="openEditPaymentDialog(payment)" class="mx-1">
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                  <v-btn icon @click="deletePayment(payment)" class="mx-1">
                    <v-icon color="red">mdi-trash-can-outline</v-icon>
                  </v-btn>
                </v-card-title>

                <v-card-text>
                  <!-- PaymentDetailドラッグ -->
                  <draggable :delay="300" :delayOnTouchOnly="false" v-model="payment.payment_details"
                    :group="{ name: 'payment_details', pull: true, put: true }" item-key="id"
                    @delayStart="handleDragStart" @end="onPaymentDetailOrderChangeAll" :animation="100"
                    :fallbackOnBody="true" :ghost-class="'ghost-style'">
                    <template #item="{ element: detail }">
                      <v-card class="mb-2 pa-3 custom-pd-card" outlined>
                        <div class="d-flex align-center justify-space-between w-100">
                          <div class="d-flex align-center">
                            <v-icon class="me-2">{{ payment.icon || 'mdi-currency-usd' }}</v-icon>
                            <span>{{ detail.name }}</span>
                          </div>

                          <div class="d-flex">
                            <v-btn icon @click="openEditPaymentDetailDialog(detail)" density="compact" class="mx-1">
                              <v-icon>mdi-pencil</v-icon>
                            </v-btn>
                            <v-btn icon @click="deletePaymentDetail(detail)" density="compact" class="mx-1">
                              <v-icon color="red">mdi-trash-can-outline</v-icon>
                            </v-btn>
                          </div>
                        </div>
                      </v-card>
                    </template>
                  </draggable>

                  <!-- PaymentDetail追加ボタン -->
                  <div class="d-flex justify-center mt-4">
                    <v-btn class="add-detail-btn" outlined @click="openPaymentDetailDialog(payment)">
                      <v-icon>mdi-plus</v-icon>
                      <span>支払い詳細を追加</span>
                    </v-btn>
                  </div>
                </v-card-text>
              </v-card>
            </template>
          </draggable>

          <!-- Payment追加ボタン -->
          <div class="text-center mt-4">
            <v-btn color="primary" @click="openPaymentDialog">
              <v-icon left>mdi-plus</v-icon> 支払い方法追加
            </v-btn>
          </div>
        </v-col>
      </v-row>

      <!-- Payment作成ダイアログ -->
      <v-dialog v-model="pRegDialog" max-width="500">
        <v-card>
          <v-card-title class="text-h6">新しい支払い方法の追加</v-card-title>
          <v-card-text>
            <v-autocomplete v-model="newPayment.icon" :items="iconOptions" item-title="label" item-value="value"
              label="アイコン" clearable prepend-inner-icon="mdi-magnify">
              <template #item="{ item, props }">
                <v-list-item v-bind="props">
                  <v-icon :icon="item.value" />
                  <v-list-item-title>{{ item.label }}</v-list-item-title>
                </v-list-item>
              </template>

              <template #selection="{ item, index }">
                <div class="d-flex align-center">
                  <v-icon class="mr-2" :icon="item.value" />
                  <span>{{ item.label }}</span>
                </div>
              </template>
            </v-autocomplete>

            <v-text-field v-model="newPayment.name" label="名前" required />
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn text @click="pRegDialog = false">キャンセル</v-btn>
            <v-btn color="primary" @click="submitNewPayment">登録</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <!-- Payment編集ダイアログ -->
      <v-dialog v-model="pEditDialog" max-width="500">
        <v-card>
          <v-card-title class="text-h6">支払い方法の編集</v-card-title>
          <v-card-text>
            <v-autocomplete v-model="editPayment.icon" :items="iconOptions" item-title="label" item-value="value"
              label="アイコン" clearable prepend-inner-icon="mdi-magnify">
              <template #item="{ item, props }">
                <v-list-item v-bind="props">
                  <v-icon :icon="item.value" />
                  <v-list-item-title>{{ item.label }}</v-list-item-title>
                </v-list-item>
              </template>

              <template #selection="{ item }">
                <div class="d-flex align-center">
                  <v-icon class="mr-2" :icon="item.value" />
                  <span>{{ item.label }}</span>
                </div>
              </template>
            </v-autocomplete>

            <v-text-field v-model="editPayment.name" label="名前" required />
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn text @click="pEditDialog = false">キャンセル</v-btn>
            <v-btn color="primary" @click="submitEditPayment">保存</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <!-- Payment-detail追加ダイアログ -->
      <v-dialog v-model="pdRegDialog" max-width="500">
        <v-card>
          <v-card-title class="text-h6">支払い詳細の登録</v-card-title>
          <v-card-text>
            <v-text-field v-model="newPaymentDetail.name" label="名前" required />
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn text @click="pdRegDialog = false">キャンセル</v-btn>
            <v-btn color="primary" @click="submitNewPaymentDetail">登録</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <!-- PaymentDetail編集ダイアログ -->
      <v-dialog v-model="pdEditDialog" max-width="500">
        <v-card>
          <v-card-title class="text-h6">支払い詳細の編集</v-card-title>
          <v-card-text>
            <v-text-field v-model="editPaymentDetail.name" label="名前" required />
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn text @click="pdEditDialog = false">キャンセル</v-btn>
            <v-btn color="primary" @click="submitEditPaymentDetail">保存</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
  </v-container>
</template>

<script setup>
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import MessageSnackbar from '@/components/MessageSnackbar.vue'
import { ref, onMounted, watch } from 'vue'
import draggable from 'vuedraggable'

const payments = ref([])
const confirmDialog = ref(null)
const snackbarRef = ref()
const loading = ref(false)

const { $api } = useNuxtApp()

// 登録・編集ダイアログ関連
const pRegDialog = ref(false)
const newPayment = ref({ name: '', icon: '' })
const pEditDialog = ref(false)
const editPayment = ref({ id: null, name: '', icon: '' })
const pdRegDialog = ref(false)
const newPaymentDetail = ref({ name: '', payment: '' })
const pdEditDialog = ref(false)
const editPaymentDetail = ref({ id: null, name: '' })

const iconOptions = [
  { label: 'ドル', value: 'mdi-currency-usd' },
  { label: 'プリペイドカード', value: 'mdi-card-bulleted' },
  { label: 'クレジットカード', value: 'mdi-credit-card' },
  { label: '現金', value: 'mdi-cash' },
  { label: 'QRコード決済', value: 'mdi-qrcode-scan' },
  { label: '交通系IC', value: 'mdi-train' },
  { label: '銀行', value: 'mdi-bank' },
  { label: '電子マネー', value: 'mdi-cellphone' },
  { label: 'ギフトカード', value: 'mdi-gift' },
  { label: 'ポイント払い', value: 'mdi-star-circle-outline' },
  { label: 'ビットコイン', value: 'mdi-bitcoin' },
]

onMounted(async () => {
  await fetchData()
})

watch(() => newPayment.value.icon, (newIcon) => {
  const value = typeof newIcon === 'object' ? newIcon?.value : newIcon
  const found = iconOptions.find(i => i.value === value)
  if (found) {
    newPayment.value.name = found.label
  }
})

function handleDragStart() {
  if (navigator.vibrate) {
    navigator.vibrate(50);
  }
}

// Paymentの登録ダイアログ表示
function openPaymentDialog() {
  newPayment.value = { name: '', icon: '' }
  pRegDialog.value = true
}

// Paymentの編集ダイアログ表示
function openEditPaymentDialog(payment) {
  editPayment.value = { id: payment.id, name: payment.name, icon: payment.icon }
  pEditDialog.value = true
}

// PaymentDetailの登録ダイアログ表示
function openPaymentDetailDialog(payment) {
  newPaymentDetail.value = { name: '', payment: payment }
  pdRegDialog.value = true
}

// PaymentDetailの編集ダイアログ表示
function openEditPaymentDetailDialog(paymentDetail) {
  editPaymentDetail.value = { id: paymentDetail.id, name: paymentDetail.name }
  pdEditDialog.value = true
}

// 同じリスト内の移動だけ許可し、別リストへの移動は禁止
function checkMoveParent(evt) {
  return evt.from === evt.to;
}

// Payments一覧の取得
async function fetchData() {
  loading.value = true

  try {
    const res = await $api.get('/api/payments/')
    const list = Array.isArray(res.data) ? res.data : res.data.results || []
    payments.value = list.map(p => ({
      ...p,
      payment_details: p.details || []
    }))
  } catch (err) {
    if (err.response && err.response.data) {
      snackbarRef.value?.showApiErrorMessages(err.response.data)
    } else {
      snackbarRef.value?.showSnackbar('error', '支払い情報の取得に失敗：サーバーエラー')
    }
    console.error('支払い情報の取得に失敗:', err)
  }
  
  loading.value = false
}

// 候補の支払い方法を全件登録
async function addAllPayments() {
  const existingNames = payments.value.map(p => p.name)

  const newPayments = iconOptions.filter(option => !existingNames.includes(option.label))

  if (newPayments.length === 0) {
    snackbarRef.value?.showSnackbar('error', '全ての支払い方法の候補を追加済みです')
    return
  }

  const result = await confirmDialog.value.open(`新規の支払い方法 ${newPayments.length} 件を追加しますか？`)
  if (!result) {
    return
  }

  for (const [index, p] of newPayments.entries()) {
    try {
      await $api.post('/api/payments/', {
        name: p.label,
        icon: p.value,
        details: null,
        order: Math.max(0, ...payments.value.map(p => p.order)) + index + 1,
      })
    } catch (err) {
      console.error(`支払い方法「${p.label}」の追加に失敗`, err)
    }
  }

  snackbarRef.value?.showSnackbar('success', `${newPayments.length} 件のカテゴリを追加しました`)

  await fetchData()
}

async function onPaymentOrderChange() {
  try {
    await Promise.all(
      payments.value.map((p, idx) =>
        $api.patch(`/api/payments/${p.id}/`, { order: idx + 1 })
      )
    )
  } catch (err) {
    if (err.response && err.response.data) {
      snackbarRef.value?.showApiErrorMessages(err.response.data)
    } else {
      snackbarRef.value?.showSnackbar('error', '支払い方法の並び替えに失敗：サーバーエラー')
    }
    console.error('支払い方法の並び替えに失敗:', err)
  }
}

async function onPaymentDetailOrderChangeAll() {
  try {
    const allDetails = []
    payments.value.forEach((p) => {
      p.payment_details.forEach((d, i) => {
        allDetails.push({
          id: d.id,
          order: i + 1,
          payment: p.id
        })
      })
    })

    await Promise.all(
      allDetails.map(d =>
        $api.patch(`/api/payment-details/${d.id}/`, {
          order: d.order,
          payment: d.payment
        })
      )
    )
  } catch (err) {
    if (err.response && err.response.data) {
      snackbarRef.value?.showApiErrorMessages(err.response.data)
    } else {
      snackbarRef.value?.showSnackbar('error', '支払い詳細の並び替えに失敗：サーバーエラー')
    }
    console.error('支払い詳細の並び替えに失敗:', err)
  }
}

// Paymentの登録
async function submitNewPayment() {
  try {
    const iconValue = typeof newPayment.value.icon === 'object' && newPayment.value.icon !== null
      ? newPayment.value.icon.value
      : newPayment.value.icon

    await $api.post('/api/payments/', {
      name: newPayment.value.name,
      icon: iconValue,
      order: Math.max(...payments.value.map(p => p.order), 0) + 1,
    })
    pRegDialog.value = false
    snackbarRef.value?.showSnackbar('success', '支払い方法を追加しました')
    await fetchData()
  } catch (err) {
    if (err.response && err.response.data) {
      snackbarRef.value?.showApiErrorMessages(err.response.data)
    } else {
      snackbarRef.value?.showSnackbar('error', '支払い方法の追加に失敗：サーバーエラー')
    }
    console.error('支払い方法の追加に失敗:', err)
  }
}

// Payment編集結果Push
async function submitEditPayment() {
  try {
    const iconValue = typeof editPayment.value.icon === 'object' && editPayment.value.icon !== null
      ? editPayment.value.icon.value
      : editPayment.value.icon

    await $api.patch(`/api/payments/${editPayment.value.id}/`, {
      name: editPayment.value.name,
      icon: iconValue,
    })
    pEditDialog.value = false
    const index = payments.value.findIndex(p => p.id === editPayment.value.id)
    if (index !== -1) {
      payments.value[index].name = editPayment.value.name
      payments.value[index].icon = iconValue
    }
    snackbarRef.value?.showSnackbar('success', '支払い方法を編集しました')
  } catch (err) {
    if (err.response && err.response.data) {
      snackbarRef.value?.showApiErrorMessages(err.response.data)
    } else {
      snackbarRef.value?.showSnackbar('error', '支払い方法の編集に失敗：サーバーエラー')
    }
    console.error('支払い方法の編集に失敗:', err)
  }
}

// Paymentの削除
async function deletePayment(payment) {
  const result = await confirmDialog.value.open('この支払い方法を削除しますか？')
  if (!result) {
    return
  }

  try {
    await $api.patch(`/api/payments/${payment.id}/`, {
      is_active: false,
    });
    payments.value = payments.value.filter(p => p.id !== payment.id)
    snackbarRef.value?.showSnackbar('success', '削除しました')
  } catch (err) {
    if (err.response && err.response.data) {
      snackbarRef.value?.showApiErrorMessages(err.response.data)
    } else {
      snackbarRef.value?.showSnackbar('error', '支払い詳細の追加に失敗：サーバーエラー')
    }
    console.error('削除に失敗:', err)
  }
};


// PaymentDetailの登録
async function submitNewPaymentDetail() {
  try {
    await $api.post('/api/payment-details/', {
      name: newPaymentDetail.value.name,
      order: newPaymentDetail.value.payment.details.length + 1,
      payment: newPaymentDetail.value.payment.id
    })
    pdRegDialog.value = false
    snackbarRef.value?.showSnackbar('success', '支払い詳細を追加しました')
    await fetchData()
  } catch (err) {
    if (err.response && err.response.data) {
      snackbarRef.value?.showApiErrorMessages(err.response.data)
    } else {
      snackbarRef.value?.showSnackbar('error', '支払い詳細の追加に失敗：サーバーエラー')
    }
    console.error('支払い詳細の追加に失敗:', err)
  }
}


// PaymentDetail編集結果Push
async function submitEditPaymentDetail() {
  try {
    await $api.patch(`/api/payment-details/${editPaymentDetail.value.id}/`, {
      name: editPaymentDetail.value.name,
    })
    pdEditDialog.value = false
    snackbarRef.value?.showSnackbar('success', '支払い詳細を編集しました')
    await fetchData()
  } catch (err) {
    if (err.response && err.response.data) {
      snackbarRef.value?.showApiErrorMessages(err.response.data)
    } else {
      snackbarRef.value?.showSnackbar('error', '支払い詳細の編集に失敗：サーバーエラー')
    }
    console.error('支払い詳細の編集に失敗:', err)
  }
}

// PaymentDetailの削除
async function deletePaymentDetail(paymentDetail) {
  const result = await confirmDialog.value.open('この支払い詳細を削除しますか？')
  if (!result) {
    return
  }

  try {
    await $api.patch(`/api/payment-details/${paymentDetail.id}/`, {
      is_active: false,
    });
    snackbarRef.value?.showSnackbar('success', '削除しました')
    await fetchData()
  } catch (err) {
    if (err.response && err.response.data) {
      snackbarRef.value?.showApiErrorMessages(err.response.data)
    } else {
      snackbarRef.value?.showSnackbar('error', '支払い詳細の追加に失敗：サーバーエラー')
    }
    console.error('削除に失敗:', err)
  }
};
</script>

<style scoped>
.custom-p-card {
  border: 2px solid gray;
}

.custom-pd-card {
  border: 2px solid lightgray;
}

.add-detail-btn {
  border: 2px dashed #1976d2;
  color: #1976d2;
  font-weight: bold;
}

.ghost-style {
  opacity: 0.6;
}
</style>
