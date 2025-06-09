<template>
  <v-container>
    <!-- スナックバー -->
    <MessageSnackbar ref="snackbarRef" />

    <v-progress-linear v-if="loadingAll" indeterminate color="primary" />
    <div v-else>
      <!-- 削除確認ダイアログ -->
      <ConfirmDialog ref="confirmDialog" />

      <!-- 合計カード -->
      <v-card class="mb-5 custom-card">
        <v-card-title>
          毎月合計 {{ Math.floor(monthlyTotalPrice) }} 円のサブスク利用
          <!-- サブスクレコード登録ボタン -->
        </v-card-title>
        <v-card-actions>
          <v-btn color="green" @click="openSubscriptionRegDialog">
            <v-icon left>mdi-plus</v-icon> サブスク利用料を今月の支払いに反映
          </v-btn>
        </v-card-actions>
      </v-card>

      <!-- 編集案内 -->
      <p class="text-caption mb-4">※サブスクはタップで編集できます。</p>

      <!-- レコード一覧 -->
      <v-progress-linear v-if="loadingAll" indeterminate color="primary" />
      <v-row v-else no-gutters>
        <v-col v-for="record in subscriptions" :key="record.id" cols="12" md="6" lg="4">
          <v-card class="mb-3 mx-1 record-card" @click="toggleEdit(record.id)"
            :elevation="editingId === record.id ? 12 : 2" style="cursor: pointer;" :ripple="false">
            <!-- 上部情報 -->
            <v-card-subtitle class="text-caption">
              <div class="d-flex align-center" style="gap: 8px;">
                <template v-if="record.category">
                  <v-icon small>{{ record.category.icon }}</v-icon>
                  <span>{{ record.category.name }}</span>
                </template>
                <template v-if="record.category_detail">
                  <span>></span>
                  <span>{{ record.category_detail.name }}</span>
                </template>
              </div>

              <div class="d-flex align-center" style="gap: 8px;">
                <template v-if="record.payment">
                  <v-icon small>{{ record.payment.icon }}</v-icon>
                  <span>{{ record.payment.name }}</span>
                </template>
                <template v-if="record.payment_detail">
                  <span>></span>
                  <span>{{ record.payment_detail.name }}</span>
                </template>
              </div>
            </v-card-subtitle>

            <!-- タイトル -->
            <v-card-title>
              <div class="d-flex justify-space-between w-100">
                <span>{{ record.name }}</span>
                <span>{{ record.price.toLocaleString() }} 円</span>
              </div>
            </v-card-title>

            <!-- 編集フォーム -->
            <v-expand-transition>
              <div v-if="editingId === record.id" @click.stop class="pa-4" style="background-color: #f9f9f9;">
                <v-text-field v-model="editRecord.name" label="名前" dense outlined />
                <v-text-field v-model.number="editRecord.price" label="価格" type="number" dense outlined />

                <v-btn color="primary" class="mr-2" @click.stop="updateRecord">更新</v-btn>
                <v-btn color="error" class="mr-6" @click.stop="deleteRecord">削除</v-btn>
                <v-btn text @click.stop="cancelEdit">キャンセル</v-btn>
              </div>
            </v-expand-transition>
          </v-card>
        </v-col>
      </v-row>

      <!-- サブスクレコード登録ダイアログ -->
      <v-dialog v-model="sRegDialog" max-width="500">
        <v-card>
          <v-card-title class="text-h6">サブスク利用料を支払いレコードに登録</v-card-title>
          <v-card-text>
            次で指定した日付で登録します
            <v-row justify="center" class="mb-4">
              <v-col cols="auto">
                <div class="text-h6">{{ displayDate }}</div>
              </v-col>
              <v-col cols="auto">
                <v-btn color="primary" @click="showDatePicker = true">
                  日付を変更
                </v-btn>
              </v-col>
            </v-row>

            <v-dialog v-model="showDatePicker" persistent width="350">
              <v-card>
                <v-date-picker v-model="selectedDate" @update:model-value="handleDateSelected" />
                <v-card-actions>
                  <v-spacer />
                  <v-btn text @click="showDatePicker = false">閉じる</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn text @click="sRegDialog = false">キャンセル</v-btn>
            <v-btn color="primary" @click="registerSubscriptionRecords">登録</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
  </v-container>
</template>

<script setup>
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import MessageSnackbar from '@/components/MessageSnackbar.vue'
import { ref, reactive, onMounted } from 'vue'
import dayjs from 'dayjs'

const { $api } = useNuxtApp()

const snackbarRef = ref()
const loadingAll = ref(false)
const loadingRecord = ref(false)

// ===== States =====
const subscriptions = ref([])
const payments = ref([])
const categories = ref([])
const editingId = ref(null)
const deletingId = ref(null)
const monthlyTotalPrice = ref(0)

// 登録ダイアログ
const sRegDialog = ref(false)
const confirmDialog = ref(null)

const showDatePicker = ref(false)
const selectedDate = ref(dayjs().format('YYYY-MM-DD'))

const displayDate = ref(dayjs().format('YYYY年MM月DD日'))

onMounted(async () => {
  await fetchData()
})

const handleDateSelected = (dateStr) => {
  displayDate.value = dayjs(dateStr).format('YYYY年MM月DD日')
  selectedDate.value = dateStr
  showDatePicker.value = false
}

// ===== Edit Form =====
const editRecord = reactive({
  id: null,
  name: '',
  price: 0,
})

function resetEditForm() {
  Object.assign(editRecord, { id: null, name: '', price: 0 })
  editingId.value = null
  deletingId.value = null
}

async function fetchData() {
  loadingAll.value = true
  await Promise.all([
    fetchPaymentAndCategory(),
    fetchSubscriptionsAndSum()
  ])
  loadingAll.value = false
}


async function fetchPaymentAndCategory() {
  try {
    const [resPayments, resCategories] = await Promise.all([
      $api.get('/api/payments/'),
      $api.get('/api/categories/')
    ])
    payments.value = resPayments
    categories.value = resCategories
  } catch (err) {
    console.error('支払い方法・カテゴリの取得失敗:', err)
  }
}

async function fetchSubscriptionsAndSum() {
  loadingRecord.value = true
  try {
    const [resSubscriptions, resSumMonth] = await Promise.all([
      $api.get('/api/subscriptions/'),
      $api.get('/api/subscriptions/sum-all-prices/')
    ])
    subscriptions.value = resSubscriptions
    monthlyTotalPrice.value = resSumMonth.total_price ?? 0
  } catch (err) {
    console.error('サブスク・合計金額の取得失敗:', err)
  } finally {
    loadingRecord.value = false
  }
}

// 登録ウィンドウ表示
function openSubscriptionRegDialog() {
  if (subscriptions.value.length === 0) {
    snackbarRef.value?.showSnackbar('error', 'サブスクの登録がありません')
    return
  }
  sRegDialog.value = true
}

// ===== Record Actions =====
function toggleEdit(id) {
  if (editingId.value === id) {
    resetEditForm()
    return
  }

  const record = subscriptions.value.find(r => r.id === id)
  if (record) {
    Object.assign(editRecord, {
      id: record.id,
      name: record.name,
      price: record.price,
    })
    editingId.value = id
  }
}

function cancelEdit() {
  resetEditForm()
}

async function updateRecord() {
  try {
    await $api.patch(`/api/subscriptions/${editRecord.id}/`, {
      name: editRecord.name,
      price: editRecord.price,
    })
    await fetchSubscriptionsAndSum()
    resetEditForm()
  } catch (err) {
    snackbarRef.value?.showApiErrorMessages(err.data)
    console.error('更新エラー:', err)
  }
}

async function deleteRecord() {
  deletingId.value = editingId.value
  if (!deletingId.value) return

  const result = await confirmDialog.value.open('このサブスクを削除しますか？')
  if (!result) {
    return
  }

  try {
    await $api.patch(`/api/subscriptions/${deletingId.value}/`, { is_active: false })
    deletingId.value = null
    resetEditForm()
    await fetchSubscriptionsAndSum()
  } catch (err) {
    console.error('削除エラー:', err)
  }
}

async function registerSubscriptionRecords() {
  for (const sub of subscriptions.value) {
    try {
      let formattedDate = dayjs(selectedDate.value).format('YYYY-MM-DD')

      const payload = {
        name: sub.name,
        price: sub.price,
        date: formattedDate,
        payment_id: sub.payment?.id ?? sub.payment_id,
        payment_detail_id: sub.payment_detail?.id ?? sub.payment_detail_id ?? null,
        category_id: sub.category?.id ?? sub.category_id,
        category_detail_id: sub.category_detail?.id ?? sub.category_detail_id ?? null,
      }

      await $api.post('/api/records/', payload)
    } catch (error) {
      console.error(`投稿失敗: ${sub.name}`, error)
      return
    }
  }
  snackbarRef.value?.showSnackbar('success', '登録に成功しました')
  sRegDialog.value = false
}

</script>

<style scoped>
.custom-card {
  border: 2px solid green;
  transition: all 0.3s ease;
}

.custom-card:hover {
  border-color: green;
  box-shadow: 0 5px 8px rgba(0, 0, 0, 0.1);
}

.record-card {
  border: 1px solid gray;
  transition: box-shadow 0.1s ease;
}

.record-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
</style>
