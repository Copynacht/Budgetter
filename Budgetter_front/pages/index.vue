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

    <v-col cols="12">
      <p class="text-h4 mb-4">{{ slideTitle[slide] }}</p>
    </v-col>
    <v-carousel v-model="slide" height="100%" hide-delimiters :show-arrows="false" :touch="false">
      <v-carousel-item>
        <v-row no-gutters>
          <v-col v-for="payment in activePayments" :key="payment.id" cols="12" md="6" lg="4">
            <v-card class="ma-2 pa-2 custom-card" outlined @click="moveDetailSelect(payment.id)">
              <v-card-title>
                <v-icon :icon="payment.icon" class="mr-2" size="32" />
                {{ payment.name }}
              </v-card-title>
            </v-card>
          </v-col>
          <v-col v-if="activePayments.length === 0">
            支払い方法を最低1つ登録してください。
          </v-col>
        </v-row>
      </v-carousel-item>

      <v-carousel-item>
        <v-row no-gutters>
          <v-col v-if="selectedPayment" v-for="paymentDetail in activePaymentDetails" :key="paymentDetail.id" cols="12"
            md="6" lg="4">
            <v-card class="ma-2 pa-2 custom-card" outlined @click="moveCategorySelect(paymentDetail.id)">
              <v-card-title>
                <v-icon :icon="selectedPayment.icon" class="mr-2" size="32" />
                {{ paymentDetail.name }}
              </v-card-title>
            </v-card>
          </v-col>
          <v-col cols="12">
            <v-btn size="x-large" class="ml-5 my-5" color="success" @click="back()">
              戻る
            </v-btn>
          </v-col>
        </v-row>
      </v-carousel-item>

      <v-carousel-item>
        <v-row no-gutters>
          <v-col v-for="category in activeCategories" :key="category.id" cols="12" md="6" lg="4">
            <v-card class="ma-2 pa-2 custom-card" outlined @click="moveRegister(category.id)">
              <v-card-title>
                <v-icon :icon="category.icon" class="mr-2" size="32" />
                {{ category.name }}
              </v-card-title>
            </v-card>
          </v-col>
          <v-col v-if="activeCategories.length === 0">
            カテゴリを最低1つ登録してください。
          </v-col>
          <v-col cols="12">
            <v-btn size="x-large" class="ml-5 my-5" color="success" @click="back()">
              戻る
            </v-btn>
          </v-col>
        </v-row>
      </v-carousel-item>

      <v-carousel-item>
        <v-row class="fill-height" justify="center">
          <v-col>
            <v-card class="pa-4 custom-card mx-auto" max-width="600">
              <v-card v-if="selectedPayment" class="mb-4">
                <v-card-title>
                  <v-icon :icon="selectedPayment.icon" class="mr-2" size="32" />
                  {{ selectedPayment.name }}
                </v-card-title>
              </v-card>

              <v-card v-if="selectedPaymentDetail" class="mb-4">
                <v-card-title>
                  <v-icon :icon="selectedPayment.icon" class="mr-2" size="32" />
                  {{ selectedPaymentDetail.name }}
                </v-card-title>
              </v-card>

              <v-card v-if="selectedCategory" class="mb-4">
                <v-card-title>
                  <v-icon :icon="selectedCategory.icon" class="mr-2" size="32" />
                  {{ selectedCategory.name }}
                </v-card-title>
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
          <v-col cols="12">
            <v-btn size="x-large" class="ml-5 my-5" color="success" @click="back()">
              戻る
            </v-btn>
            <v-btn size="x-large" class="mx-5 my-5" color="success" @click="next()">
              最初から
            </v-btn>
          </v-col>
        </v-row>
      </v-carousel-item>
    </v-carousel>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import dayjs from 'dayjs'

const { $api } = useNuxtApp()

const payments = ref([])
const pSelected = ref(-1)

const paymentDetails = ref([])
const pdSelected = ref(-1)

const categories = ref([])
const cSelected = ref(-1)

const activePayments = computed(() => payments.value)
const activePaymentDetails = computed(() => paymentDetails.value)
const activeCategories = computed(() => categories.value)

const selectedPayment = computed(() => activePayments.value.find(p => p.id === pSelected.value))
const selectedPaymentDetail = computed(() => activePaymentDetails.value.find(pd => pd.id === pdSelected.value))
const selectedCategory = computed(() => activeCategories.value.find(c => c.id === cSelected.value))

const slide = ref(0)
const slideTitle = [
  '支払い方法',
  '支払い方法詳細',
  'カテゴリー選択',
  '登録情報',
]

const isSubscription = ref(false)
const inputPrice = ref("")
const inputDetail = ref("")

const showDatePicker = ref(false)
const selectedDate = ref(dayjs().format('YYYY-MM-DD'))

const displayDate = ref(dayjs().format('YYYY年MM月DD日'))

const handleDateSelected = (dateStr) => {
  displayDate.value = dayjs(dateStr).format('YYYY年MM月DD日')
  selectedDate.value = dateStr
  showDatePicker.value = false
}

const formValid = ref(false)
const formRef = ref(null)

const snackbar = ref(false)
const showSuccessMessage = () => {
  snackbar.value = true
}

onMounted(async () => {
  try {
    const [resPayments, resCategories] = await Promise.all([
      $api.get('/api/payments/'),
      $api.get('/api/categories/')
    ])
    payments.value = resPayments.data
    categories.value = resCategories.data
  } catch (err) {
    console.error('Failed to fetch data:', err)
  }
})

const moveDetailSelect = (id) => {
  pSelected.value = id
  paymentDetails.value = payments.value.find(payment => payment.id === id).details
  if (paymentDetails.value.length === 0) {
    slide.value += 2
  } else {
    slide.value += 1
  }
}

const moveCategorySelect = (id) => {
  pdSelected.value = id
  slide.value += 1
}

const moveRegister = (id) => {
  cSelected.value = id
  slide.value += 1
}

const reset = () => {
  slide.value = 0
  pSelected.value = -1
  pdSelected.value = -1
  cSelected.value = -1
  inputPrice.value = ""
  inputDetail.value = ""
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
    }
    if (pdSelected.value === -1) {
      payload.payment_detail_id = null;
    }
    if (isSubscription.value === true) {
      delete payload.date;
      await $api.post('/api/subscriptions/', payload)
    }
    else {
      await $api.post('/api/records/', payload)
    }
    showSuccessMessage()
    reset()
  } catch (error) {
    console.error('Failed:', error)
  }
}

const back = () => {
  if (slide.value === 2 && paymentDetails.value.length === 0) {
    slide.value -= 2
  } else {
    slide.value -= 1
    if (slide.value === 0) {
      reset()
    }
  }
}

const next = () => {
  slide.value += 1
  if (slide.value === 4) {
    reset()
  }
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