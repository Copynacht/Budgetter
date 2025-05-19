<template>
    <v-container>
        <v-row>
            ※アイテムはドラッグ＆ドロップで並び替えできます
            <v-col cols="12">
                <div class="text-center">
                    <v-btn color="primary" @click="addAllCategories">
                        <v-icon left>mdi-plus</v-icon> カテゴリ候補をすべて追加
                    </v-btn>
                </div>
            </v-col>
            <v-col cols="12">
                <v-alert v-if="errorMessage" type="error">{{ errorMessage }}</v-alert>
            </v-col>

            <v-col cols="12" v-if="loading">
                <v-progress-linear indeterminate color="primary" />
            </v-col>

            <v-col cols="12" v-else>
                <!-- Categoryの並び替え -->
                <draggable v-model="categories" :group="{ name: 'categories', pull: true, put: false }" item-key="id"
                    @end="onCategoryOrderChange">
                    <template #item="{ element: categorie }">
                        <v-card class="mb-4 custom-p-card">
                            <v-card-title class="d-flex justify-space-between align-center">
                                <div>
                                    <v-icon class="me-2">{{ categorie.icon || 'mdi-information-outline' }}</v-icon>
                                    {{ categorie.name }}
                                </div>

                                <v-spacer />

                                <v-btn icon @click="openEditCategoryDialog(categorie)" class="mx-1">
                                    <v-icon>mdi-pencil</v-icon>
                                </v-btn>
                                <v-btn icon @click="deleteCategory(categorie)" class="mx-1">
                                    <v-icon color="red">mdi-trash-can-outline</v-icon>
                                </v-btn>
                            </v-card-title>
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
                    <v-autocomplete v-model="newCategory.icon" :items="iconOptions" item-title="label"
                        item-value="value" label="アイコン" clearable prepend-inner-icon="mdi-magnify">
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
                    <v-autocomplete v-model="editCategory.icon" :items="iconOptions" item-title="label"
                        item-value="value" label="アイコン" clearable prepend-inner-icon="mdi-magnify">
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

        <!-- エラースナックバー -->
        <v-snackbar v-model="snackbarE.show" location="top center" color="error" timeout="3000">
            {{ snackbarE.message }}
        </v-snackbar>

        <!-- 成功スナックバー -->
        <v-snackbar v-model="snackbarS.show" location="top center" color="success" timeout="3000">
            {{ snackbarS.message }}
        </v-snackbar>
    </v-container>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import draggable from 'vuedraggable'

const categories = ref([])
const loading = ref(false)
const errorMessage = ref('')
const { $api } = useNuxtApp()

// 登録・編集ダイアログ関連
const pRegDialog = ref(false)
const newCategory = ref({ name: '', icon: '' })
const pEditDialog = ref(false)
const editCategory = ref({ id: null, name: '', icon: '' })

const snackbarE = ref({ show: false, message: '' })
const snackbarS = ref({ show: false, message: '' })

const iconOptions = [
    { label: '物', value: 'mdi-cube' },
    { label: '日用品', value: 'mdi-basket' },
    { label: 'スーパー', value: 'mdi-cart' },
    { label: 'コンビニ', value: 'mdi-store-outline' },
    { label: '食材', value: 'mdi-food' },
    { label: 'お酒', value: 'mdi-glass-cocktail' },
    { label: '外食', value: 'mdi-silverware-fork-knife' },
    { label: '車関連', value: 'mdi-car' },
    { label: 'ガソリン', value: 'mdi-fuel' },
    { label: '高速料金', value: 'mdi-road-variant' },
    { label: '旅行', value: 'mdi-airplane' },
    { label: '宿泊', value: 'mdi-bed' },
    { label: '仕事', value: 'mdi-domain' },
    { label: '交通費', value: 'mdi-train-car' },
    { label: '家賃', value: 'mdi-home-city' },
    { label: '電気', value: 'mdi-flash' },
    { label: '水道', value: 'mdi-water-pump' },
    { label: 'ガス', value: 'mdi-fire' },
    { label: 'PC・スマホ関連', value: 'mdi-laptop' },
    { label: '通信費', value: 'mdi-wifi' },
    { label: '医療・健康', value: 'mdi-hospital-box-outline' },
    { label: '保険', value: 'mdi-shield-check' },
    { label: '育児・子ども', value: 'mdi-human-male-child' },
    { label: '趣味・娯楽', value: 'mdi-gamepad-variant' },
    { label: '教育', value: 'mdi-school' },
    { label: '寄付・贈与', value: 'mdi-gift' },
    { label: 'ペット', value: 'mdi-dog' },
    { label: '服・ファッション', value: 'mdi-tshirt-crew' },
    { label: '投資', value: 'mdi-chart-line' },
    { label: 'ライフイベント', value: 'mdi-ring' },
    { label: 'その他', value: 'mdi-dots-horizontal-circle-outline' }
];

watch(() => newCategory.value.icon, (newIcon) => {
    const value = typeof newIcon === 'object' ? newIcon?.value : newIcon
    const found = iconOptions.find(i => i.value === value)
    if (found) {
        newCategory.value.name = found.label
    }
})

// Categorys一覧の取得
async function fetchCategorys() {
    loading.value = true
    errorMessage.value = ''
    try {
        const res = await $api.get('/api/categories/')
        const list = Array.isArray(res.data) ? res.data : res.data.results || []
        categories.value = list.map(p => ({
            ...p,
            categorie_details: p.details || []
        }))
    } catch (err) {
        errorMessage.value = 'カテゴリの取得に失敗しました'
        console.error(err)
    } finally {
        loading.value = false
    }
}

async function onCategoryOrderChange() {
    try {
        await Promise.all(
            categories.value.map((p, idx) =>
                $api.patch(`/api/categories/${p.id}/`, { order: idx + 1 })
            )
        )
    } catch (err) {
        console.error('Categoryの並び順更新失敗:', err)
    }
}

// Categoryの登録ウィンドウ表示
function openCategoryDialog() {
    newCategory.value = { name: '', icon: '' }
    pRegDialog.value = true
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
            order: categories.value.length + 1,
        })
        pRegDialog.value = false
        await fetchCategorys()
    } catch (err) {
        if (err.response && err.response.data) {
            showApiErrorMessages(err.response.data)
        } else {
            snackbarE.value.message = 'カテゴリの追加に失敗：サーバーエラー'
            snackbarE.value.show = true
        }
        console.error('カテゴリの追加に失敗:', err)
    }
}

// 候補カテゴリ全件登録
async function addAllCategories() {
    const existingNames = categories.value.map(c => c.name)

    const newCategories = iconOptions.filter(option => !existingNames.includes(option.label))

    if (newCategories.length === 0) {
        snackbarE.value.message = '追加可能なカテゴリはありません'
        snackbarE.value.show = true
        return
    }

    const confirmed = confirm(`新規カテゴリ ${newCategories.length} 件を追加しますか？`)
    if (!confirmed) return

    for (const [index, cat] of newCategories.entries()) {
        try {
            await $api.post('/api/categories/', {
                name: cat.label,
                icon: cat.value,
                order: categories.value.length + index + 1,
            })
        } catch (err) {
            console.error(`カテゴリ「${cat.label}」の追加に失敗`, err)
        }
    }

    snackbarS.value.message = `${newCategories.length} 件のカテゴリを追加しました`
    snackbarS.value.show = true

    await fetchCategorys()
}

// Category編集ダイアログ表示
function openEditCategoryDialog(categorie) {
    editCategory.value = { id: categorie.id, name: categorie.name, icon: categorie.icon }
    pEditDialog.value = true
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
        await fetchCategorys()
    } catch (err) {
        if (err.response && err.response.data) {
            showApiErrorMessages(err.response.data)
        } else {
            snackbarE.value.message = 'カテゴリの編集に失敗：サーバーエラー'
            snackbarE.value.show = true
        }
        console.error('カテゴリの編集に失敗:', err)
    }
}

// Categoryの削除
async function deleteCategory(categorie) {
    const confirmed = window.confirm('このカテゴリを削除しますか？');
    if (!confirmed) return;

    try {
        await $api.patch(`/api/categories/${categorie.id}/`, {
            is_active: false,
        });
        await fetchCategorys()
    } catch (error) {
        console.error('削除に失敗しました', error);
    }
};

// API空のエラー表示特化関数
function showApiErrorMessages(errorResponse) {
    if (!errorResponse || typeof errorResponse !== 'object') {
        snackbarE.value.message = '不明なエラーが発生しました。'
        snackbarE.value.show = true
        return
    }

    const messages = []
    for (const key in errorResponse) {
        if (Array.isArray(errorResponse[key])) {
            errorResponse[key].forEach(msg => messages.push(`${msg.replace("name", "[名前]")}`))
        } else if (typeof errorResponse[key] === 'string') {
            messages.push(`${errorResponse[key]}`)
        }
    }

    snackbarE.value.message = messages.join('\n')
    snackbarE.value.show = true
}

onMounted(fetchCategorys)
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
