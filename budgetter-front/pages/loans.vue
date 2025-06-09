<template>
  <v-container>
    <!-- スナックバー -->
    <MessageSnackbar ref="snackbarRef" />

    <v-progress-linear v-if="loading" indeterminate color="primary" />
    <div v-else>
      <!-- 削除確認ダイアログ -->
      <ConfirmDialog ref="confirmDialog" />

      <v-col cols="12">
        <div class="text-center">
          <v-btn color="red" @click="deleteAllRecords">
            <v-icon left>mdi-delete</v-icon> 全ての貸し借り履歴を削除
          </v-btn>
        </div>
      </v-col>

      <!-- 編集案内 -->
      <p class="text-caption mb-4">※貸し借り履歴はタップで編集できます。</p>

      <!-- レコード一覧 -->
      <!-- 貸しの一覧 -->
      <h3>貸した一覧</h3>
      <v-row no-gutters class="mb-8">
        <v-col v-for="record in loans.filter(r => r.loan_type === 0)" :key="record.id" cols="12" md="6" lg="4">
          <v-card class="mb-3  mx-1 record-card" @click="toggleEdit(record.id)"
            :elevation="editingId === record.id ? 12 : 2" style="cursor: pointer;" :ripple="false">
            <!-- 中身は元のコードのまま -->
            <v-card-title>
              {{ record.detail }}：<br />
              {{ record.name }} で{{ record.price.toLocaleString() }}円 貸し
            </v-card-title>
            <v-card-subtitle>{{ formatDate(record.date) }}</v-card-subtitle>

            <v-expand-transition>
              <div v-if="editingId === record.id" @click.stop class="pa-4" style="background-color: #f9f9f9;">
                <v-text-field v-model="editRecord.partner" label="相手" dense outlined />
                <v-text-field v-model="editRecord.name" label="項目" dense outlined />
                <v-select v-model="editRecord.loanType" :items="[
                  { text: '貸した', value: 0 },
                  { text: '借りた', value: 1 }
                ]" label="貸し借りの種類" item-title="text" item-value="value" outlined />
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

      <!-- 借りの一覧 -->
      <h3>借りた一覧</h3>
      <v-row no-gutters>
        <v-col v-for="record in loans.filter(r => r.loan_type === 1)" :key="record.id" cols="12" md="6" lg="4">
          <v-card class="mb-3 record-card" @click="toggleEdit(record.id)" :elevation="editingId === record.id ? 12 : 2"
            style="cursor: pointer;" :ripple="false">
            <!-- 中身は元のコードのまま -->
            <v-card-title>
              {{ record.detail }}：<br />
              {{ record.name }} で{{ record.price.toLocaleString() }}円 借り
            </v-card-title>
            <v-card-subtitle>{{ formatDate(record.date) }}</v-card-subtitle>

            <v-expand-transition>
              <div v-if="editingId === record.id" @click.stop class="pa-4" style="background-color: #f9f9f9;">
                <v-text-field v-model="editRecord.partner" label="相手" dense outlined />
                <v-text-field v-model="editRecord.name" label="項目" dense outlined />
                <v-select v-model="editRecord.loanType" :items="[
                  { text: '貸した', value: 0 },
                  { text: '借りた', value: 1 }
                ]" label="貸し借りの種類" item-title="text" item-value="value" outlined />
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
    </div>
  </v-container>
</template>

<script setup>
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import MessageSnackbar from '@/components/MessageSnackbar.vue'
import { ref, reactive, onMounted } from 'vue'

const { $api } = useNuxtApp()

const snackbarRef = ref()
const loading = ref(false)

// ===== States =====
const loans = ref([])
const editingId = ref(null)
const deletingId = ref(null)

// 登録ダイアログ
const confirmDialog = ref(null)

// ===== Formatters =====
const formatDate = (dateStr) => {
  const d = new Date(dateStr)
  return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`
}

// ===== Edit Form =====
const editRecord = reactive({
  id: null,
  name: '',
  partner: '',
  loanType: 0,
  price: 0,
  date: ''
})

onMounted(async () => {
  await fetchData()
})

// ===== Data Fetching =====
async function fetchData() {
  loading.value = true
  loans.value = []

  try {
    const [resRecords, resMonth] = await Promise.all([
      $api.get('/api/loans/'),
    ])

    loans.value = resRecords
  } catch (err) {
    console.error('データ取得エラー:', err)
  }

  loading.value = false
}

function resetEditForm() {
  Object.assign(editRecord, { id: null, name: '', partner: '', loanType: 0, price: 0, date: '' })
  editingId.value = null
  deletingId.value = null
}

// ===== Record Actions =====
function toggleEdit(id) {
  if (editingId.value === id) {
    resetEditForm()
    return
  }

  const record = loans.value.find(r => r.id === id)
  if (record) {
    Object.assign(editRecord, {
      id: record.id,
      name: record.name,
      partner: record.detail,
      loanType: record.loan_type,
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
    await $api.patch(`/api/loans/${editRecord.id}/`, {
      name: editRecord.name,
      detail: editRecord.partner,
      loan_type: editRecord.loanType,
      price: editRecord.price,
      date: editRecord.date,
    })
    await fetchData()
    resetEditForm()
  } catch (err) {
    console.error('更新エラー:', err)
    snackbarRef.value?.showApiErrorMessages(err.data)
  }
}

async function deleteRecord() {
  deletingId.value = editingId.value
  if (!deletingId.value) return

  const result = await confirmDialog.value.open('この貸し借り履歴を削除しますか？')
  if (!result) {
    return
  }

  try {
    await $api.patch(`/api/loans/${deletingId.value}/`, { is_active: false })
    deletingId.value = null
    resetEditForm()
    await fetchData()
  } catch (err) {
    console.error('削除エラー:', err)
  }
}

async function deleteAllRecords() {
  if (loans.value.length === 0) {
    snackbarRef.value?.showSnackbar('error', '貸し借り履歴がありません')
    return
  }

  const result = await confirmDialog.value.open('全ての貸し借り履歴を削除しますか？')
  if (!result) {
    return
  }

  try {
    await Promise.all(
      loans.value.map(record =>
        $api.patch(`/api/loans/${record.id}/`, { is_active: false })
      )
    )
    await fetchData()
    snackbarRef.value?.showSnackbar('success', '全ての貸し借り履歴を削除しました')
  } catch (err) {
    console.error('一括無効化エラー:', err)
    snackbarRef.value?.showSnackbar('error', '一部のレコードの削除に失敗しました')
  }
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
