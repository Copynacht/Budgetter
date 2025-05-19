<template>
    <v-container>
        <v-snackbar v-model="snackbar" location="top center" :timeout="3000" color="success">
            登録に成功しました！
            <template #actions>
                <v-btn icon @click="snackbar = false">
                    <v-icon icon="mdi-close" />
                </v-btn>
            </template>
        </v-snackbar>

        <!-- 削除確認ダイアログ -->
        <v-dialog v-model="deletingId" max-width="400">
            <v-card>
                <v-card-title class="headline">サブスクを削除しますか？</v-card-title>
                <v-card-text>この操作は取り消せません。</v-card-text>
                <v-card-actions>
                    <v-spacer />
                    <v-btn text @click="cancelDelete">キャンセル</v-btn>
                    <v-btn color="error" text @click="deleteRecord">削除する</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <!-- 合計カード -->
        <v-card class="mb-5 custom-card">
            <v-card-title>
                毎月 {{ Math.floor(monthlyTotalPrice) }} 円のサブスク利用があります
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
        <v-row no-gutters>
            <v-col v-for="record in subscriptions" :key="record.id" cols="12" md="6" lg="4">
                <v-card class="mb-3 record-card" @click="toggleEdit(record.id)"
                    :elevation="editingId === record.id ? 12 : 2" style="cursor: pointer;" :ripple="false">
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

                    <!-- 編集フォーム -->
                    <v-expand-transition>
                        <div v-if="editingId === record.id" @click.stop class="pa-4" style="background-color: #f9f9f9;">
                            <v-text-field v-model="editRecord.name" label="名前" dense outlined />
                            <v-text-field v-model.number="editRecord.price" label="価格" type="number" dense outlined />

                            <v-btn color="primary" class="mr-2" @click.stop="updateRecord">更新</v-btn>
                            <v-btn color="error" class="mr-6" @click.stop="confirmDelete">削除</v-btn>
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
    </v-container>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import dayjs from 'dayjs'

const { $api } = useNuxtApp()

// ===== States =====
const subscriptions = ref([])
const payments = ref([])
const categories = ref([])
const editingId = ref(null)
const deletingId = ref(null)
const monthlyTotalPrice = ref(0)
const annualTotalPrice = ref(0)

// 登録ダイアログ
const sRegDialog = ref(false)

const showDatePicker = ref(false)
const selectedDate = ref(dayjs().format('YYYY-MM-DD'))

const displayDate = ref(dayjs().format('YYYY年MM月DD日'))

const handleDateSelected = (dateStr) => {
    displayDate.value = dayjs(dateStr).format('YYYY年MM月DD日')
    selectedDate.value = dateStr
    showDatePicker.value = false
}

const snackbar = ref(false)
const showSuccessMessage = () => {
  snackbar.value = true
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
    subscriptions.value = []
    monthlyTotalPrice.value = 0
    annualTotalPrice.value = 0

    try {
        const [resRecords, resMonth] = await Promise.all([
            $api.get('/api/subscriptions/'),
            $api.get('/api/subscriptions/sum-all-prices')
        ])

        subscriptions.value = resRecords.data
        monthlyTotalPrice.value = resMonth.data.total_price ?? 0
    } catch (err) {
        console.error('データ取得エラー:', err)
    }
}

// 登録ウィンドウ表示
function openSubscriptionRegDialog() {
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
        await $api.patch(`/api/subscriptions/${deletingId.value}/`, { is_active: false })
        deletingId.value = null
        resetEditForm()
        await fetchData()
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
            }

            await $api.post('/api/records/', payload)

        } catch (error) {
            console.error(`投稿失敗: ${sub.name}`, error)
        }
    }
    sRegDialog.value = false
    showSuccessMessage()
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
