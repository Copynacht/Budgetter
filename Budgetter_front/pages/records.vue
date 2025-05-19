<template>
  <v-container>
    <!-- 削除確認ダイアログ -->
    <v-dialog v-model="deletingId" max-width="400">
      <v-card>
        <v-card-title class="headline">レコードを削除しますか？</v-card-title>
        <v-card-text>この操作は取り消せません。</v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="cancelDelete">キャンセル</v-btn>
          <v-btn color="error" text @click="deleteRecord">削除する</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- フィルター -->
    <v-row class="mb-2" no-gutters>
      <v-col cols="6" sm="3" class="px-2">
        <v-select v-model="selectedYear" :items="yearOptions" label="年" outlined dense />
      </v-col>
      <v-col cols="6" sm="3" class="px-2">
        <v-select v-model="selectedMonth" :items="monthOptions" label="月" outlined dense />
      </v-col>
      <v-col cols="6" sm="3" class="px-2">
        <v-select
          v-model="selectedPayment"
          :items="payments"
          item-title="name"
          item-value="id"
          label="支払い方法"
          clearable
        />
      </v-col>
      <v-col cols="6" sm="3" class="px-2" v-if="selectedPayment">
        <v-select
          v-model="selectedPaymentDetail"
          :items="paymentDetailOptions"
          item-title="name"
          item-value="id"
          label="支払い方法詳細"
          clearable
        />
      </v-col>
      <v-col cols="12" md="6" class="px-2">
        <v-select v-model="selectedCategory" :items="categories" item-title="name" item-value="id" label="カテゴリ" clearable/>
      </v-col>
    </v-row>

    <!-- 合計カード -->
    <v-card class="mb-5 custom-card">
      <v-card-title>
        {{ selectedYear }}年{{ selectedMonth }}月の支出合計: {{ monthlyTotalPrice.toLocaleString() }} 円<br />
        1日あたり {{ Math.floor(monthlyTotalPrice / daysUsed) }} 円の利用です
      </v-card-title>
      <v-card-text>
        {{ selectedYear }}年の支出合計: {{ annualTotalPrice.toLocaleString() }} 円
      </v-card-text>
    </v-card>

    <!-- 編集案内 -->
    <p class="text-caption mb-4">※レコードはタップで編集できます。</p>

    <!-- レコード一覧 -->
    <v-row no-gutters>
      <v-col v-for="record in records" :key="record.id" cols="12" md="6" lg="4">
        <v-card
          class="mb-3 record-card"
          @click="toggleEdit(record.id)"
          :elevation="editingId === record.id ? 12 : 2"
          style="cursor: pointer;"
          :ripple="false"
        >
          <!-- 上部情報 -->
          <v-card-subtitle class="d-flex align-center text-caption" style="gap: 8px;">
            <template v-if="record.payment">
              <v-icon small>{{ record.payment.icon }}</v-icon>
              <span>{{ record.payment.name }}</span>
            </template>
            <template v-if="record.payment_detail">
              <span>></span>
              <span>{{ record.payment_detail.name }}</span>
            </template>
            <span>-</span>
            <template v-if="record.category">
              <v-icon small>{{ record.category.icon }}</v-icon>
              <span>{{ record.category.name }}</span>
            </template>
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
              <v-btn color="error" class="mr-6" @click.stop="confirmDelete">削除</v-btn>
              <v-btn text @click.stop="cancelEdit">キャンセル</v-btn>
            </div>
          </v-expand-transition>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'

const { $api } = useNuxtApp()

// ===== States =====
const records = ref([])
const payments = ref([])
const categories = ref([])
const editingId = ref(null)
const deletingId = ref(null)
const selectedYear = ref(new Date().getFullYear())
const selectedMonth = ref(new Date().getMonth() + 1)
const selectedPayment = ref(null)
const selectedPaymentDetail = ref(null)
const selectedCategory = ref(null)
const monthlyTotalPrice = ref(0)
const annualTotalPrice = ref(0)

// ===== Options =====
const yearOptions = Array.from({ length: 6 }, (_, i) => selectedYear.value - i)
const monthOptions = Array.from({ length: 12 }, (_, i) => i + 1)

// payment_detailの選択肢はselectedPaymentに依存
const paymentDetailOptions = computed(() => {
  if (!selectedPayment.value) return []
  const payment = payments.value.find(p => p.id === selectedPayment.value)
  return payment?.details ?? []
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
  deletingId.value = null
}

// ===== Lifecycle =====
onMounted(async () => {
  try {
    const [resPayments, resCategories] = await Promise.all([
      $api.get('/api/payments/'),
      $api.get('/api/categories/')
    ])
    payments.value = resPayments.data
    categories.value = resCategories.data
    await fetchData()
  } catch (err) {
    console.error('初期データ取得失敗:', err)
  }
})

// ===== Data Fetching =====
async function fetchData() {
  records.value = []
  monthlyTotalPrice.value = 0
  annualTotalPrice.value = 0

  const params = {
    year: selectedYear.value,
    month: selectedMonth.value,
    ...(selectedPayment.value && { payment: selectedPayment.value }),
    ...(selectedPaymentDetail.value && { payment_detail: selectedPaymentDetail.value }),
    ...(selectedCategory.value && { category: selectedCategory.value })
  }

  try {
    const [resRecords, resMonth, resYear] = await Promise.all([
      $api.get('/api/records/', { params }),
      $api.get('/api/records/sum-by-month', { params }),
      $api.get('/api/records/sum-by-month', { params: { ...params, month: 0 } })
    ])

    records.value = resRecords.data
    monthlyTotalPrice.value = resMonth.data.total_price ?? 0
    annualTotalPrice.value = resYear.data.total_price ?? 0
  } catch (err) {
    console.error('データ取得エラー:', err)
  }
}

// ===== Payment選択変更時にpayment_detailをリセット =====
function onPaymentChange() {
  selectedPaymentDetail.value = null
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
    await $api.patch(`/api/records/${editRecord.id}/`, {
      name: editRecord.name,
      price: editRecord.price,
      date: editRecord.date
    })
    await fetchData()
    resetEditForm()
  } catch (err) {
    console.error('更新エラー:', err)
  }
}

function confirmDelete() {
  deletingId.value = editingId.value
}

function cancelDelete() {
  deletingId.value = null
}

async function deleteRecord() {
  if (!deletingId.value) return

  try {
    await $api.patch(`/api/records/${deletingId.value}/`, { is_active: false })
    deletingId.value = null
    resetEditForm()
    await fetchData()
  } catch (err) {
    console.error('削除エラー:', err)
  }
}

// ===== Watch =====
watch(
  [selectedPayment, selectedPaymentDetail, selectedCategory, selectedYear, selectedMonth],
  fetchData
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
