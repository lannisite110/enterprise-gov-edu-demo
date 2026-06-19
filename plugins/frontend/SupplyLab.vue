<script setup lang="ts">
import { ref } from 'vue'

const loading = ref(false)
const error = ref('')
const result = ref<Record<string, unknown> | null>(null)

async function runVerify() {
  loading.value = true
  error.value = ''
  result.value = null
  try {
    const res = await fetch('/api/v1/labs/edu.cn.gov.supply/simulate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_prompt: '物资出入库存证校验',
        params: { ledger: 'sample' },
        allowed_chain_ids: ['fabric-local'],
      }),
    })
    const data = await res.json()
    if (!res.ok) throw new Error((data as { error?: string }).error || res.statusText)
    result.value = data
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="card">
    <h1>物资供应链存证</h1>
    <p class="muted">Fabric 沙箱 · 出入库哈希链 · 虚构批次数据</p>
    <button class="primary" :disabled="loading" @click="runVerify">
      {{ loading ? '校验中…' : '校验存证链' }}
    </button>
    <p v-if="error" class="error">{{ error }}</p>
    <pre v-if="result" class="result">{{ JSON.stringify(result, null, 2) }}</pre>
  </section>
</template>
