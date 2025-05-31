<template>
  <v-container>
    <v-progress-linear v-if="loadingAll" indeterminate color="primary" />
    <div v-else>
      <!-- スナックバー -->
      <MessageSnackbar ref="snackbarRef" />
      <!-- 確認ダイアログ -->
      <ConfirmDialog ref="confirmDialog" />

      <v-row>
        <v-col cols="12">
          <!-- フィルター -->
          <v-row class="mb-2" no-gutters>
            <v-col cols="6" sm="3" class="px-2">
              <v-select v-model="selectedYear" :items="yearOptions" label="年" outlined dense />
            </v-col>
            <v-col cols="6" sm="3" class="px-2">
              <v-select v-model="selectedMonth" :items="monthOptions" label="月" outlined dense />
            </v-col>
            <v-col cols="6" sm="3" class="px-2">
              <v-select v-model="selectedCategory" :items="categories" item-title="name" item-value="id" label="カテゴリ"
                clearable />
            </v-col>
            <v-col cols="6" sm="3" class="px-2" v-if="selectedPayment && !selectedCategory">
            </v-col>
            <v-col cols="6" sm="3" class="px-2" v-if="selectedCategory">
              <v-select v-model="selectedCategoryDetail" :items="categoryDetailOptions" item-title="name"
                item-value="id" label="カテゴリ詳細" clearable :disabled="categoryDetailOptions.length === 0" />
            </v-col>
            <v-col cols="6" sm="3" class="px-2">
              <v-select v-model="selectedPayment" :items="payments" item-title="name" item-value="id" label="支払い方法"
                clearable />
            </v-col>
            <v-col cols="6" sm="3" class="px-2" v-if="selectedPayment">
              <v-select v-model="selectedPaymentDetail" :items="paymentDetailOptions" item-title="name" item-value="id"
                label="支払い方法詳細" clearable :disabled="paymentDetailOptions.length === 0" />
            </v-col>
          </v-row>

          <!-- 合計カード -->
          <v-card class="mb-2 custom-card">
            <v-card-title>
              {{ selectedYear }}年{{ selectedMonth }}月の支出合計: {{ monthlyTotalPrice.toLocaleString() }} 円<br />
              1日あたり {{ Math.floor(monthlyTotalPrice / daysUsed) }} 円の利用です
            </v-card-title>
            <v-card-text>
              {{ selectedYear }}年の支出合計: {{ annualTotalPrice.toLocaleString() }} 円
            </v-card-text>
          </v-card>
          <div class="d-flex justify-end mb-4">
            <v-btn color="primary" @click="exportRecordsToCSV">
              CSVエクスポート
            </v-btn>
          </div>

          <!-- 編集案内 -->
          <p class="text-caption mb-4">※レコードはタップで編集できます。</p>


          <v-progress-linear v-if="loadingRecord" indeterminate color="primary" />
          <!-- レコード一覧 -->
          <v-row v-else no-gutters>
            <v-col v-for="record in records" :key="record.id" cols="12" md="6" lg="4">
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
                <v-card-subtitle>{{ formatDate(record.date) }}</v-card-subtitle>

                <!-- 編集フォーム -->
                <v-expand-transition>
                  <div v-if="editingId === record.id" @click.stop class="pa-4" style="background-color: #f9f9f9;">
                    <v-text-field v-model="editRecord.name" label="名前" dense outlined />
                    <v-text-field v-model.number="editRecord.price" label="価格" type="number" dense outlined />
                    <v-text-field v-model="editRecord.date" label="日付" type="date" dense outlined />

                    <v-btn color="primary" class="mr-2" @click.stop="updateRecord">更新</v-btn>
                    <v-btn color="error" class="mr-6" @click.stop="deleteRecord">削除</v-btn>
                    <v-btn text @click.stop="cancelEdit">キャンセル</v-btn>
                  </div>
                </v-expand-transition>
              </v-card>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<script setup>
import MessageSnackbar from '@/components/MessageSnackbar.vue'
import { ref, reactive, computed, onMounted, watch } from 'vue'
import ConfirmDialog from '@/components/ConfirmDialog.vue'

const { $api } = useNuxtApp()

const snackbarRef = ref()
const loadingAll = ref(false)
const loadingRecord = ref(false)

// ===== States =====
const records = ref([])
const payments = ref([])
const categories = ref([])
const editingId = ref(null)
const selectedYear = ref(new Date().getFullYear())
const selectedMonth = ref(new Date().getMonth() + 1)
const selectedPayment = ref(null)
const selectedPaymentDetail = ref(null)
const selectedCategory = ref(null)
const selectedCategoryDetail = ref(null)
const monthlyTotalPrice = ref(0)
const annualTotalPrice = ref(0)
const confirmDialog = ref(null)

// ===== Options =====
const yearOptions = Array.from({ length: 6 }, (_, i) => selectedYear.value - i)
const monthOptions = Array.from({ length: 12 }, (_, i) => i + 1)

// detailの選択肢はselectedに依存
const paymentDetailOptions = computed(() => {
  if (!selectedPayment.value) return []
  const payment = payments.value.find(p => p.id === selectedPayment.value)
  return payment?.details ?? []
})
const categoryDetailOptions = computed(() => {
  if (!selectedCategory.value) return []
  const category = categories.value.find(c => c.id === selectedCategory.value)
  return category?.details ?? []
})

onMounted(async () => {
  await fetchData()
})

watch(selectedPayment, () => {
  selectedPaymentDetail.value = null
})

watch(selectedCategory, () => {
  selectedCategoryDetail.value = null
})


// ===== Computed =====
const daysUsed = computed(() => {
  const now = new Date()
  if (selectedYear.value === now.getFullYear() && selectedMonth.value === now.getMonth() + 1) {
    return now.getDate()
  }
  return new Date(selectedYear.value, selectedMonth.value, 0).getDate()
})

// ===== Formatters =====
const formatDate = (dateStr) => {
  const d = new Date(dateStr)
  return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`
}

// ===== Edit Form =====
const editRecord = reactive({
  id: null,
  name: '',
  price: 0,
  date: ''
})

function resetEditForm() {
  Object.assign(editRecord, { id: null, name: '', price: 0, date: '' })
  editingId.value = null
}

// ===== Data Fetching =====
async function fetchData() {
  loadingAll.value = true
  await Promise.all([
    fetchMasterData(),
    fetchRecordData()
  ])
  loadingAll.value = false
}


// ① 支払い方法・カテゴリだけ取得 ---------------------
async function fetchMasterData() {
  try {
    const [resPayments, resCategories] = await Promise.all([
      $api.get('/api/payments/'),
      $api.get('/api/categories/')
    ])
    payments.value = resPayments.data
    categories.value = resCategories.data
  } catch (err) {
    console.error('マスタデータ取得エラー:', err)
  }
}

// ② レコード & 集計だけ取得 ---------------------------
async function fetchRecordData() {
  loadingRecord.value = true

  const params = {
    year: selectedYear.value,
    month: selectedMonth.value,
    ...(selectedPayment.value && { payment: selectedPayment.value }),
    ...(selectedPaymentDetail.value && { payment_detail: selectedPaymentDetail.value }),
    ...(selectedCategory.value && { category: selectedCategory.value }),
    ...(selectedCategoryDetail.value && { category_detail: selectedCategoryDetail.value })
  }

  try {
    const [resRecords, resMonth, resYear] = await Promise.all([
      $api.get('/api/records/', { params }),
      $api.get('/api/records/sum-by-month/', { params }),
      $api.get('/api/records/sum-by-month/', { params: { ...params, month: 0 } })
    ])

    records.value = resRecords.data
    monthlyTotalPrice.value = resMonth.data.total_price ?? 0
    annualTotalPrice.value = resYear.data.total_price ?? 0
  } catch (err) {
    console.error('レコード取得エラー:', err)
  } finally {
    loadingRecord.value = false
  }
}

// ===== Record Actions =====
function toggleEdit(id) {
  if (editingId.value === id) {
    resetEditForm()
    return
  }

  const record = records.value.find(r => r.id === id)
  if (record) {
    Object.assign(editRecord, {
      id: record.id,
      name: record.name,
      price: record.price,
      date: record.date.slice(0, 10)
    })
    editingId.value = id
  }
}

function cancelEdit() {
  resetEditForm()
}

async function updateRecord() {
  try {
    await $api.patch(`/api/records/${editingId.value}/`, {
      name: editRecord.name,
      price: editRecord.price,
      date: editRecord.date
    })
    await fetchRecordData()
    resetEditForm()
  } catch (err) {
    if (err.response && err.response.data) {
      snackbarRef.value?.showApiErrorMessages(err.response.data)
    } else {
      snackbarRef.value?.showSnackbar('error', '更新に失敗：サーバーエラー')
    }
    console.error('更新に失敗:', err)
  }
}

async function deleteRecord() {
  const result = await confirmDialog.value.open('このレコードを削除しますか？')
  if (!result) {
    return
  }

  if (!editingId.value) return

  try {
    await $api.patch(`/api/records/${editingId.value}/`, { is_active: false })
    resetEditForm()
    await fetchRecordData()
  } catch (err) {
    if (err.response && err.response.data) {
      snackbarRef.value?.showApiErrorMessages(err.response.data)
    } else {
      snackbarRef.value?.showSnackbar('error', '削除に失敗：サーバーエラー')
    }
    console.error('削除に失敗:', err)
  }
}

function exportRecordsToCSV() {
  if (records.value.length === 0) {
    snackbarRef.value?.showSnackbar('error', 'レコードがありません')
    return
  }

  const headers = ['日付', '名前', '価格', '支払い方法', '支払い方法詳細', 'カテゴリ', 'カテゴリ詳細']
  const rows = records.value.map(r => [
    formatDate(r.date),
    r.name,
    r.price,
    r.payment?.name || '',
    r.payment_detail?.name || '',
    r.category?.name || '',
    r.category_detail?.name || ''
  ])

  const csvContent =
    '\uFEFF' +
    [headers, ...rows].map(row => row.map(field => `"${String(field).replace(/"/g, '""')}"`).join(',')).join('\n')

  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const now = new Date()
  const filename = `records_${selectedYear.value}_${selectedMonth.value}.csv`

  link.href = URL.createObjectURL(blob)
  link.setAttribute('download', filename)
  link.click()
  URL.revokeObjectURL(link.href)
}

// ===== Watch =====
watch(
  [selectedPayment, selectedPaymentDetail, selectedCategory, selectedCategoryDetail, selectedYear, selectedMonth],
  fetchRecordData
)
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
