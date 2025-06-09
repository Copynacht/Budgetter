<template>
  <v-container>
    <!-- スナックバー -->
    <MessageSnackbar ref="snackbarRef" />

    <v-progress-linear v-if="loading" indeterminate color="primary" />
    <div v-else>
      <!-- 確認ダイアログ -->
      <ConfirmDialog ref="confirmDialog" />

      <v-row>
        <v-col cols="12">
          <div class="text-center">
            <v-btn color="primary" @click="addAllCategories">
              <v-icon left>mdi-plus</v-icon> カテゴリの候補をすべて追加
            </v-btn>
          </div>
        </v-col>

        ※アイテムはドラッグ＆ドロップで並び替えできます

        <v-col cols="12">
          <!-- Categoryの並び替え -->
          <draggable :delay="300" :delayOnTouchOnly="false" v-model="categories"
            :group="{ name: 'categories', pull: true, put: false }" item-key="id" @delayStart="handleDragStart"
            @end="onCategoryOrderChange" :move="checkMoveParent">
            <template #item="{ element: category }">
              <v-card class="mb-4 custom-p-card">
                <v-card-title class="d-flex justify-space-between align-center">
                  <div>
                    <v-icon class="me-2">{{ category.icon || 'mdi-information-outline' }}</v-icon>
                    {{ category.name }}
                  </div>

                  <v-spacer />

                  <v-btn icon @click="openEditCategoryDialog(category)" class="mx-1">
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                  <v-btn icon @click="deleteCategory(category)" class="mx-1">
                    <v-icon color="red">mdi-trash-can-outline</v-icon>
                  </v-btn>
                </v-card-title>

                <v-card-text>
                  <!-- CategoryDetailドラッグ -->
                  <draggable :delay="300" :delayOnTouchOnly="false" v-model="category.category_details"
                    :group="{ name: 'category_details', pull: true, put: true }" item-key="id"
                    @delayStart="handleDragStart" @end="onCategoryDetailOrderChangeAll" :animation="100"
                    :fallbackOnBody="true" :ghost-class="'ghost-style'">
                    <template #item="{ element: detail }">
                      <v-card class="mb-2 pa-3 custom-pd-card" outlined>
                        <div class="d-flex align-center justify-space-between w-100">
                          <div class="d-flex align-center">
                            <v-icon class="me-2">{{ category.icon || 'mdi-information-outline' }}</v-icon>
                            <span>{{ detail.name }}</span>
                          </div>

                          <div class="d-flex">
                            <v-btn icon @click="openEditCategoryDetailDialog(detail)" density="compact" class="mx-1">
                              <v-icon>mdi-pencil</v-icon>
                            </v-btn>
                            <v-btn icon @click="deleteCategoryDetail(detail)" density="compact" class="mx-1">
                              <v-icon color="red">mdi-trash-can-outline</v-icon>
                            </v-btn>
                          </div>
                        </div>
                      </v-card>
                    </template>
                  </draggable>

                  <!-- CategoryDetail追加ボタン -->
                  <div class="d-flex justify-center mt-4">
                    <v-btn class="add-detail-btn" outlined @click="openCategoryDetailDialog(category)">
                      <v-icon>mdi-plus</v-icon>
                      <span>カテゴリ詳細を追加</span>
                    </v-btn>
                  </div>
                </v-card-text>
              </v-card>
            </template>
          </draggable>

          <!-- Category追加ボタン -->
          <div class="text-center mt-4">
            <v-btn color="primary" @click="openCategoryDialog">
              <v-icon left>mdi-plus</v-icon> カテゴリ追加
            </v-btn>
          </div>
        </v-col>
      </v-row>

      <!-- Category作成ダイアログ -->
      <v-dialog v-model="pRegDialog" max-width="500">
        <v-card>
          <v-card-title class="text-h6">新しいカテゴリの追加</v-card-title>
          <v-card-text>
            <v-autocomplete v-model="newCategory.icon" :items="iconOptions" item-title="label" item-value="value"
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

            <v-text-field v-model="newCategory.name" label="名前" required />
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn text @click="pRegDialog = false">キャンセル</v-btn>
            <v-btn color="primary" @click="submitNewCategory">登録</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <!-- Category編集ダイアログ -->
      <v-dialog v-model="pEditDialog" max-width="500">
        <v-card>
          <v-card-title class="text-h6">カテゴリの編集</v-card-title>
          <v-card-text>
            <v-autocomplete v-model="editCategory.icon" :items="iconOptions" item-title="label" item-value="value"
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

            <v-text-field v-model="editCategory.name" label="名前" required />
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn text @click="pEditDialog = false">キャンセル</v-btn>
            <v-btn color="primary" @click="submitEditCategory">保存</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <!-- Category-detail追加ダイアログ -->
      <v-dialog v-model="pdRegDialog" max-width="500">
        <v-card>
          <v-card-title class="text-h6">カテゴリ詳細の登録</v-card-title>
          <v-card-text>
            <v-text-field v-model="newCategoryDetail.name" label="名前" required />
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn text @click="pdRegDialog = false">キャンセル</v-btn>
            <v-btn color="primary" @click="submitNewCategoryDetail">登録</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <!-- CategoryDetail編集ダイアログ -->
      <v-dialog v-model="pdEditDialog" max-width="500">
        <v-card>
          <v-card-title class="text-h6">カテゴリ詳細の編集</v-card-title>
          <v-card-text>
            <v-text-field v-model="editCategoryDetail.name" label="名前" required />
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn text @click="pdEditDialog = false">キャンセル</v-btn>
            <v-btn color="primary" @click="submitEditCategoryDetail">保存</v-btn>
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

const categories = ref([])
const confirmDialog = ref(null)
const snackbarRef = ref()
const loading = ref(false)

const { $api } = useNuxtApp()

// 登録・編集ダイアログ関連
const pRegDialog = ref(false)
const newCategory = ref({ name: '', icon: '' })
const pEditDialog = ref(false)
const editCategory = ref({ id: null, name: '', icon: '' })
const pdRegDialog = ref(false)
const newCategoryDetail = ref({ name: '', category: '' })
const pdEditDialog = ref(false)
const editCategoryDetail = ref({ id: null, name: '' })

const iconOptions = [
  { label: '物', value: 'mdi-cube' },
  { label: '生活', value: 'mdi-basket' },
  { label: '移動', value: 'mdi-train-bus' },
  { label: '食事', value: 'mdi-food-fork-drink' },
  { label: '趣味・娯楽', value: 'mdi-gamepad-variant' },
  { label: 'ファッション', value: 'mdi-tshirt-crew' },
  { label: '車', value: 'mdi-car' },
  { label: '旅行', value: 'mdi-airplane' },
  { label: '仕事', value: 'mdi-domain' },
  { label: '医療・健康', value: 'mdi-hospital-box-outline' },
  { label: '家賃・水道光熱費・通信費', value: 'mdi-home-account' },
  { label: '育児・子ども', value: 'mdi-human-male-child' },
  { label: 'PC・スマホ', value: 'mdi-laptop' },
  { label: '税金', value: 'mdi-currency-usd' },
  { label: '教育', value: 'mdi-school' },
  { label: '寄付・贈与', value: 'mdi-gift' },
  { label: 'ペット', value: 'mdi-dog' },
  { label: '投資', value: 'mdi-chart-line' },
  { label: 'ライフイベント', value: 'mdi-ring' },
  { label: 'その他', value: 'mdi-dots-horizontal-circle-outline' }
]

onMounted(async () => {
  await fetchData()
})

watch(() => newCategory.value.icon, (newIcon) => {
  const value = typeof newIcon === 'object' ? newIcon?.value : newIcon
  const found = iconOptions.find(i => i.value === value)
  if (found) {
    newCategory.value.name = found.label
  }
})

function handleDragStart() {
  if (navigator.vibrate) {
    navigator.vibrate(50);
  }
}

// Categoryの登録ダイアログ表示
function openCategoryDialog() {
  newCategory.value = { name: '', icon: '' }
  pRegDialog.value = true
}

// Categoryの編集ダイアログ表示
function openEditCategoryDialog(category) {
  editCategory.value = { id: category.id, name: category.name, icon: category.icon }
  pEditDialog.value = true
}

// CategoryDetailの登録ダイアログ表示
function openCategoryDetailDialog(category) {
  newCategoryDetail.value = { name: '', category: category }
  pdRegDialog.value = true
}

// CategoryDetailの編集ダイアログ表示
function openEditCategoryDetailDialog(categoryDetail) {
  editCategoryDetail.value = { id: categoryDetail.id, name: categoryDetail.name }
  pdEditDialog.value = true
}

// 同じリスト内の移動だけ許可し、別リストへの移動は禁止
function checkMoveParent(evt) {
  return evt.from === evt.to;
}

// Categories一覧の取得
async function fetchData() {
  loading.value = true

  try {
    const res = await $api.get('/api/categories/')
    const list = Array.isArray(res) ? res : res.results || []
    categories.value = list.map(p => ({
      ...p,
      category_details: p.details || []
    }))
  } catch (err) {
    if (err.data) {
      snackbarRef.value?.showApiErrorMessages(err.data)
    } else {
      snackbarRef.value?.showSnackbar('error', 'カテゴリの取得に失敗：サーバーエラー')
    }
    console.error('カテゴリの取得に失敗:', err)
  }

  loading.value = false
}

// 候補のカテゴリを全件登録
async function addAllCategories() {
  const existingNames = categories.value.map(p => p.name)

  const newCategories = iconOptions.filter(option => !existingNames.includes(option.label))

  if (newCategories.length === 0) {
    snackbarRef.value?.showSnackbar('error', '全てのカテゴリの候補を追加済みです')
    return
  }

  const result = await confirmDialog.value.open(`新規のカテゴリ ${newCategories.length} 件を追加しますか？`)
  if (!result) {
    return
  }

  for (const [index, p] of newCategories.entries()) {
    try {
      await $api.post('/api/categories/', {
        name: p.label,
        icon: p.value,
        details: null,
        order: Math.max(0, ...categories.value.map(p => p.order)) + index + 1,
      })
    } catch (err) {
      console.error(`カテゴリ「${p.label}」の追加に失敗`, err)
    }
  }
  snackbarRef.value?.showSnackbar('success', `${newCategories.length} 件のカテゴリを追加しました`)

  await fetchData()
}

async function onCategoryOrderChange() {
  try {
    await Promise.all(
      categories.value.map((p, idx) =>
        $api.patch(`/api/categories/${p.id}/`, { order: idx + 1 })
      )
    )
  } catch (err) {
    if (err.data) {
      snackbarRef.value?.showApiErrorMessages(err.data)
    } else {
      snackbarRef.value?.showSnackbar('error', 'カテゴリの並び替えに失敗：サーバーエラー')
    }
    console.error('カテゴリの並び替えに失敗:', err)
  }
}

async function onCategoryDetailOrderChangeAll() {
  try {
    const allDetails = []
    categories.value.forEach((p) => {
      p.category_details.forEach((d, i) => {
        allDetails.push({
          id: d.id,
          order: i + 1,
          category: p.id
        })
      })
    })

    await Promise.all(
      allDetails.map(d =>
        $api.patch(`/api/category-details/${d.id}/`, {
          order: d.order,
          category: d.category
        })
      )
    )
  } catch (err) {
    if (err.data) {
      snackbarRef.value?.showApiErrorMessages(err.data)
    } else {
      snackbarRef.value?.showSnackbar('error', 'カテゴリ詳細の並び替えに失敗：サーバーエラー')
    }
    console.error('カテゴリ詳細の並び替えに失敗:', err)
  }
}

// Categoryの登録
async function submitNewCategory() {
  try {
    const iconValue = typeof newCategory.value.icon === 'object' && newCategory.value.icon !== null
      ? newCategory.value.icon.value
      : newCategory.value.icon

    await $api.post('/api/categories/', {
      name: newCategory.value.name,
      icon: iconValue,
      order: Math.max(...categories.value.map(p => p.order), 0) + 1,
    })
    pRegDialog.value = false
    snackbarRef.value?.showSnackbar('success', 'カテゴリを追加しました')
    await fetchData()
  } catch (err) {
    if (err.data) {
      snackbarRef.value?.showApiErrorMessages(err.data)
    } else {
      snackbarRef.value?.showSnackbar('error', 'カテゴリの追加に失敗：サーバーエラー')
    }
    console.error('カテゴリの追加に失敗:', err)
  }
}

// Category編集結果Push
async function submitEditCategory() {
  try {
    const iconValue = typeof editCategory.value.icon === 'object' && editCategory.value.icon !== null
      ? editCategory.value.icon.value
      : editCategory.value.icon

    await $api.patch(`/api/categories/${editCategory.value.id}/`, {
      name: editCategory.value.name,
      icon: iconValue,
    })
    pEditDialog.value = false
    const index = categories.value.findIndex(p => p.id === editCategory.value.id)
    if (index !== -1) {
      categories.value[index].name = editCategory.value.name
      categories.value[index].icon = iconValue
    }
    snackbarRef.value?.showSnackbar('success', 'カテゴリを編集しました')
  } catch (err) {
    if (err.data) {
      snackbarRef.value?.showApiErrorMessages(err.data)
    } else {
      snackbarRef.value?.showSnackbar('error', 'カテゴリの編集に失敗：サーバーエラー')
    }
    console.error('カテゴリの編集に失敗:', err)
  }
}

// Categoryの削除
async function deleteCategory(category) {
  const result = await confirmDialog.value.open('このカテゴリを削除しますか？')
  if (!result) {
    return
  }

  try {
    await $api.patch(`/api/categories/${category.id}/`, {
      is_active: false,
    });
    categories.value = categories.value.filter(p => p.id !== category.id)
    snackbarRef.value?.showSnackbar('success', '削除しました')
  } catch (err) {
    if (err.data) {
      snackbarRef.value?.showApiErrorMessages(err.data)
    } else {
      snackbarRef.value?.showSnackbar('error', 'カテゴリ詳細の追加に失敗：サーバーエラー')
    }
    console.error('削除に失敗:', err)
  }
};


// CategoryDetailの登録
async function submitNewCategoryDetail() {
  try {
    await $api.post('/api/category-details/', {
      name: newCategoryDetail.value.name,
      order: newCategoryDetail.value.category.details.length + 1,
      category: newCategoryDetail.value.category.id
    })
    pdRegDialog.value = false
    snackbarRef.value?.showSnackbar('success', 'カテゴリ詳細を追加しました')
    await fetchData()
  } catch (err) {
    if (err.data) {
      snackbarRef.value?.showApiErrorMessages(err.data)
    } else {
      snackbarRef.value?.showSnackbar('error', 'カテゴリ詳細の追加に失敗：サーバーエラー')
    }
    console.error('カテゴリ詳細の追加に失敗:', err)
  }
}


// CategoryDetail編集結果Push
async function submitEditCategoryDetail() {
  try {
    await $api.patch(`/api/category-details/${editCategoryDetail.value.id}/`, {
      name: editCategoryDetail.value.name,
    })
    pdEditDialog.value = false
    snackbarRef.value?.showSnackbar('success', 'カテゴリ詳細を編集しました')
    await fetchData()
  } catch (err) {
    if (err.data) {
      snackbarRef.value?.showApiErrorMessages(err.data)
    } else {
      snackbarRef.value?.showSnackbar('error', 'カテゴリ詳細の編集に失敗：サーバーエラー')
    }
    console.error('カテゴリ詳細の編集に失敗:', err)
  }
}

// CategoryDetailの削除
async function deleteCategoryDetail(categoryDetail) {
  const result = await confirmDialog.value.open('このカテゴリ詳細を削除しますか？')
  if (!result) {
    return
  }

  try {
    await $api.patch(`/api/category-details/${categoryDetail.id}/`, {
      is_active: false,
    });
    snackbarRef.value?.showSnackbar('success', '削除しました')
    await fetchData()
  } catch (err) {
    if (err.data) {
      snackbarRef.value?.showApiErrorMessages(err.data)
    } else {
      snackbarRef.value?.showSnackbar('error', 'カテゴリ詳細の追加に失敗：サーバーエラー')
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
