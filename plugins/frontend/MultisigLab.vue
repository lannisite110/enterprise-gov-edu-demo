<script setup lang="ts">
import { ref } from 'vue'

const threshold = ref(2)
const loading = ref(false)
const error = ref('')
const result = ref<Record<string, unknown> | null>(null)

async function runApproval() {
  loading.value = true
  error.value = ''
  result.value = null
  try {
    const res = await fetch('/api/v1/labs/edu.cn.gov.multisig/simulate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_prompt: '多级多签审批演示',
        params: {
          threshold: threshold.value,
          confirmations: [
            '0x1111111111111111111111111111111111111111',
            '0x2222222222222222222222222222222222222222',
          ],
        },
        allowed_chain_ids: [11155111],
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
    <h1>多级多签审批</h1>
    <p class="muted">Sepolia 测试网合约模板 · 权限模型教学 · 非真实 OA 系统</p>
    <label class="field">
      签名阈值（2-of-3 示例）
      <input v-model.number="threshold" type="number" min="1" max="3" />
    </label>
    <button class="primary" :disabled="loading" @click="runApproval">
      {{ loading ? '模拟中…' : '模拟审批流' }}
    </button>
    <p v-if="error" class="error">{{ error }}</p>
    <pre v-if="result" class="result">{{ JSON.stringify(result, null, 2) }}</pre>
  </section>
</template>
