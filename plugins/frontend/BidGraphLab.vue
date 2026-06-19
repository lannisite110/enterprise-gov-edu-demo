<script setup lang="ts">
import { ref } from 'vue'

const loading = ref(false)
const error = ref('')
const result = ref<Record<string, unknown> | null>(null)

async function runAnalysis() {
  loading.value = true
  error.value = ''
  result.value = null
  try {
    const res = await fetch('/api/v1/labs/edu.cn.gov.bid-graph/simulate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_prompt: '招投标关联图谱分析',
        params: { graph: 'sample' },
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
    <h1>招投标关联图谱</h1>
    <p class="muted">虚构供应商节点 · 纯图算法教学 · 不对接政府采购网</p>
    <button class="primary" :disabled="loading" @click="runAnalysis">
      {{ loading ? '分析中…' : '运行关联分析' }}
    </button>
    <p v-if="error" class="error">{{ error }}</p>
    <pre v-if="result" class="result">{{ JSON.stringify(result, null, 2) }}</pre>
  </section>
</template>
