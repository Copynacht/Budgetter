<template>
  <v-container>
    <!-- スナックバー -->
    <MessageSnackbar ref="snackbarRef" />

    <v-progress-linear v-if="loading" indeterminate color="primary" />
    <div v-else>
      <v-row>
        <v-col cols="6">
          <p class="text-h5 mb-4">{{ slideTitle[slide] }}</p>
        </v-col>
        <v-col cols="6">
          <v-btn cols="6" v-if="slide === 0" color="success" @click="loan()">
            貸し借りを記録
          </v-btn>
          <v-btn cols="3" v-if="slide !== 0 && slide !== 5" color="success" @click="back()">
            戻る
          </v-btn>
          <v-btn cols="3" v-if="slide === 4 || slide === 5" class="ma-1" color="success" @click="reset()">
            リセット
          </v-btn>
        </v-col>
      </v-row>

      <v-carousel v-model="slide" height="100%" hide-delimiters :show-arrows="false" :touch="false">
        <v-carousel-item>
          <v-row no-gutters>
            <v-col v-for="category in activeCategories" :key="category.id" cols="12" md="6" lg="4">
              <v-card class="ma-2 pa-2 custom-card" outlined @click="moveCategoryDetailSelect(category.id)">
                <v-card-title>
                  <v-icon :icon="category.icon" class="mr-2" size="32" />
                  {{ category.name }}
                </v-card-title>
              </v-card>
            </v-col>
            <v-col v-if="activeCategories.length === 0">
              カテゴリを最低1つ登録してください。<br />
              左のタブの「カテゴリ管理」より追加できます。
            </v-col>
          </v-row>
        </v-carousel-item>

        <v-carousel-item>
          <v-row no-gutters>
            <v-col v-if="selectedCategory" v-for="categoryDetail in activeCategoryDetails" :key="categoryDetail.id"
              cols="12" md="6" lg="4">
              <v-card class="ma-2 pa-2 custom-card" outlined @click="movePaymentSelect(categoryDetail.id)">
                <v-card-title>
                  <v-icon :icon="selectedCategory.icon" class="mr-2" size="32" />
                  {{ categoryDetail.name }}
                </v-card-title>
              </v-card>
            </v-col>
          </v-row>
        </v-carousel-item>

        <v-carousel-item>
          <v-row no-gutters>
            <v-col v-for="payment in activePayments" :key="payment.id" cols="12" md="6" lg="4">
              <v-card class="ma-2 pa-2 custom-card" outlined @click="movePaymentDetailSelect(payment.id)">
                <v-card-title>
                  <v-icon :icon="payment.icon" class="mr-2" size="32" />
                  {{ payment.name }}
                </v-card-title>
              </v-card>
            </v-col>
            <v-col v-if="activePayments.length === 0">
              支払い方法を最低1つ登録してください。<br />
              左のタブの「支払方法管理」より追加できます。
            </v-col>
          </v-row>
        </v-carousel-item>

        <v-carousel-item>
          <v-row no-gutters>
            <v-col v-if="selectedPayment" v-for="paymentDetail in activePaymentDetails" :key="paymentDetail.id"
              cols="12" md="6" lg="4">
              <v-card class="ma-2 pa-2 custom-card" outlined @click="moveRegister(paymentDetail.id)">
                <v-card-title>
                  <v-icon :icon="selectedPayment.icon" class="mr-2" size="32" />
                  {{ paymentDetail.name }}
                </v-card-title>
              </v-card>
            </v-col>
            <v-col cols="12">
            </v-col>
          </v-row>
        </v-carousel-item>

        <v-carousel-item>
          <v-row class="fill-height" justify="center">
            <v-col>
              <v-card class="pa-4 custom-card mx-auto" max-width="600">
                <v-card v-if="selectedCategory" class="mb-4">
                  <v-card-title>
                    <v-icon :icon="selectedCategory.icon" class="mr-2" size="32" />
                    {{ selectedCategory.name }}
                  </v-card-title>
                  <v-card-text>
                    <v-card v-if="selectedCategoryDetail" class="mb-4">
                      <v-card-title>
                        {{ selectedCategoryDetail.name }}
                      </v-card-title>
                    </v-card>
                  </v-card-text>
                </v-card>

                <v-card v-if="selectedPayment" class="mb-4">
                  <v-card-title>
                    <v-icon :icon="selectedPayment.icon" class="mr-2" size="32" />
                    {{ selectedPayment.name }}
                  </v-card-title>
                  <v-card-text>
                    <v-card v-if="selectedPaymentDetail" class="mb-4">
                      <v-card-title>
                        {{ selectedPaymentDetail.name }}
                      </v-card-title>
                    </v-card>
                  </v-card-text>
                </v-card>

                <!-- サブスクチェックボックス -->
                <v-checkbox v-model="isSubscription" label="サブスクですか？"></v-checkbox>

                <v-row justify="center" class="mb-4">
                  <v-col cols="auto">
                    <div class="text-h6">{{ displayDate }}</div>
                  </v-col>
                  <v-col cols="auto">
                    <v-btn color="primary" @click="showDatePicker = true" :disabled="isSubscription">
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

                <v-form ref="formRef" v-model="formValid">
                  <v-text-field v-model="inputDetail" label="詳細" prepend-icon="mdi-tag" outlined class="mb-4" :rules="[
                    v => !!v || '詳細は必須です',
                    v => v.length <= 255 || '255文字以内で入力してください'
                  ]" />

                  <v-text-field v-model="inputPrice" label="金額" prepend-icon="mdi-currency-jpy" type="number" outlined
                    class="mb-4" :rules="[
                      v => !!v || '金額は必須です',
                      v => !v || Number.isInteger(+v) || '整数を入力してください',
                      v => +v >= 1 || '1以上の金額を入力してください'
                    ]" />

                  <v-row justify="center">
                    <v-col cols="auto">
                      <v-btn color="primary" @click="register" :disabled="!formValid">
                        登録
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-form>
              </v-card>
            </v-col>
          </v-row>
        </v-carousel-item>

        <v-carousel-item>
          <v-row class="fill-height" justify="center">
            <v-col>
              <v-card class="pa-4 custom-card mx-auto" max-width="600">
                <v-row justify="center" class="mb-4">
                  <v-col cols="auto">
                    <div class="text-h6">{{ displayDate }}</div>
                  </v-col>
                  <v-col cols="auto">
                    <v-btn color="primary" @click="showDatePicker = true" :disabled="isSubscription">
                      日付を変更
                    </v-btn>
                  </v-col>
                </v-row>

                <v-select v-model="loanType" :items="[
                  { text: '貸した', value: 0 },
                  { text: '借りた', value: 1 }
                ]" label="貸し借りの種類" prepend-icon="mdi-swap-horizontal" item-title="text" item-value="value" outlined
                  class="mb-4" />

                <v-text-field v-model="loanPartner" label="相手の名前" prepend-icon="mdi-account" outlined class="mb-4"
                  :rules="[v => !!v || '相手の名前は必須です']" />

                <v-dialog v-model="showDatePicker" persistent width="350">
                  <v-card>
                    <v-date-picker v-model="selectedDate" @update:model-value="handleDateSelected" />
                    <v-card-actions>
                      <v-spacer />
                      <v-btn text @click="showDatePicker = false">閉じる</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>

                <v-form ref="formRef" v-model="formValid">
                  <v-text-field v-model="inputDetail" label="詳細" prepend-icon="mdi-tag" outlined class="mb-4" :rules="[
                    v => !!v || '詳細は必須です',
                    v => v.length <= 255 || '255文字以内で入力してください'
                  ]" />

                  <v-text-field v-model="inputPrice" label="金額" prepend-icon="mdi-currency-jpy" type="number" outlined
                    class="mb-4" :rules="[
                      v => !!v || '金額は必須です',
                      v => !v || Number.isInteger(+v) || '整数を入力してください',
                      v => +v >= 1 || '1以上の金額を入力してください'
                    ]" />

                  <v-row justify="center">
                    <v-col cols="auto">
                      <v-btn color="primary" @click="registerLoan" :disabled="!formValid">
                        登録
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-form>
              </v-card>
            </v-col>
          </v-row>
        </v-carousel-item>
      </v-carousel>
    </div>
  </v-container>
</template>

<script setup>
import MessageSnackbar from '@/components/MessageSnackbar.vue'
import { ref, onMounted, computed } from 'vue'
import dayjs from 'dayjs'

const { $api } = useNuxtApp()

const snackbarRef = ref()
const loading = ref(false)

const payments = ref([])
const paymentDetails = ref([])
const categories = ref([])
const categoryDetails = ref([])

const pSelected = ref(-1)
const pdSelected = ref(-1)
const cSelected = ref(-1)
const cdSelected = ref(-1)

const activePayments = computed(() => payments.value)
const activePaymentDetails = computed(() => paymentDetails.value)
const activeCategories = computed(() => categories.value)
const activeCategoryDetails = computed(() => categoryDetails.value)

const selectedPayment = computed(() => activePayments.value.find(p => p.id === pSelected.value))
const selectedPaymentDetail = computed(() => activePaymentDetails.value.find(pd => pd.id === pdSelected.value))
const selectedCategory = computed(() => activeCategories.value.find(c => c.id === cSelected.value))
const selectedCategoryDetail = computed(() => activeCategoryDetails.value.find(cd => cd.id === cdSelected.value))

const slide = ref(0)
const slideTitle = [
  'カテゴリ',
  'カテゴリ詳細',
  '支払い方法',
  '支払い詳細',
  '登録内容',
  '貸し借り登録',
]

const isSubscription = ref(false)
const loanType = ref(0)
const loanPartner = ref("")
const inputPrice = ref("")
const inputDetail = ref("")

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

const formValid = ref(false)
const formRef = ref(null)

const fetchData = async () => {
  loading.value = true
  try {
    const [resCategories, resPayments] = await Promise.all([
      $api.get('/api/categories/'),
      $api.get('/api/payments/')
    ])
    categories.value = resCategories
    payments.value = resPayments
  } catch (err) {
    console.error('Failed to fetch data:', err)
  }
  loading.value = false
}

const moveCategoryDetailSelect = (id) => {
  cSelected.value = id
  const details = categories.value.find(category => category.id === id).details
  if (details.length === 0) {
    slide.value += 2
  } else {
    categoryDetails.value = [{ id: -1, name: '指定しない' }, ...details]
    slide.value += 1
  }
}

const movePaymentSelect = (id) => {
  cdSelected.value = id
  slide.value += 1
}

const movePaymentDetailSelect = (id) => {
  pSelected.value = id
  paymentDetails.value = payments.value.find(payment => payment.id === id).details
  if (paymentDetails.value.length === 0) {
    slide.value += 2
  } else {
    slide.value += 1
  }
}

const moveRegister = (id) => {
  pdSelected.value = id
  slide.value += 1
}

const reset = () => {
  slide.value = 0
  pSelected.value = -1
  pdSelected.value = -1
  cSelected.value = -1
  cdSelected.value = -1
  isSubscription.value = false
  loanType.value = 0
  loanPartner.value = ""
  inputPrice.value = ""
  inputDetail.value = ""

  formRef.value?.reset()

  selectedDate.value = dayjs().format('YYYY-MM-DD')
  displayDate.value = dayjs().format('YYYY年MM月DD日')
}

const register = async () => {
  const isValid = await formRef.value?.validate()
  if (!isValid) return;

  try {
    let payload = {}
    let formattedDate = dayjs(selectedDate.value).format('YYYY-MM-DD')

    payload = {
      name: inputDetail.value,
      price: Number(inputPrice.value),
      date: formattedDate,
      payment_id: pSelected.value,
      payment_detail_id: pdSelected.value,
      category_id: cSelected.value,
      category_detail_id: cdSelected.value,
    }
    if (pdSelected.value === -1) {
      payload.payment_detail_id = null;
    }
    if (cdSelected.value === -1) {
      payload.category_detail_id = null;
    }
    if (isSubscription.value === true) {
      delete payload.date;
      await $api.post('/api/subscriptions/', payload)
    }
    else {
      await $api.post('/api/records/', payload)
    }
    snackbarRef.value?.showSnackbar('success', '登録に成功しました')
    reset()
  } catch (err) {
    if (err.data) {
      snackbarRef.value?.showApiErrorMessages(err.data)
    } else {
      snackbarRef.value?.showSnackbar('error', 'レコードの登録に失敗：サーバーエラー')
    }
    console.error('レコードの登録に失敗:', err)
  }
}

const registerLoan = async () => {
  const isValid = await formRef.value?.validate()
  if (!isValid) return;

  try {
    let payload = {}
    let formattedDate = dayjs(selectedDate.value).format('YYYY-MM-DD')

    payload = {
      name: inputDetail.value,
      price: Number(inputPrice.value),
      date: formattedDate,
      detail: loanPartner.value,
      loan_type: loanType.value
    }

    await $api.post('/api/loans/', payload)

    snackbarRef.value?.showSnackbar('success', '登録に成功しました')
    reset()
  } catch (err) {
    if (err.data) {
      snackbarRef.value?.showApiErrorMessages(err.data)
    } else {
      snackbarRef.value?.showSnackbar('error', '貸し借りレコードの登録に失敗：サーバーエラー')
    }
    console.error('貸し借りレコードの登録に失敗:', err)
  }
}

const back = () => {
  if (slide.value === 2 && categoryDetails.value.length === 0) {
    slide.value -= 2
  } else if (slide.value === 4 && paymentDetails.value.length === 0) {
    slide.value -= 2
  } else {
    slide.value -= 1
    if (slide.value === 0) {
      reset()
    }
  }
}

const loan = () => {
  slide.value = 5
}
</script>

<style scoped>
.custom-card {
  border: 2px solid green;
  /* 輪郭を強調するための色 */
  transition: all 0.3s ease;
  /* ホバー時のアニメーション */
}

.custom-card:hover {
  border-color: green;
  /* ホバー時のボーダーカラー */
  box-shadow: 0 5px 8px rgba(0, 0, 0, 0.1);
  /* ホバー時の影 */
}
</style>