<script setup lang="ts">
import { computed, ref } from 'vue'
import { useLabSimulate } from './shared/useLabSimulate'
import { parseHints, hintBool, hintNumber } from './shared/parseHints'

const threshold = ref(2)
const proposalId = ref('PROPOSAL-DEMO-001')
const proposalTitle = ref('教学预算拨付提案')
const signed = ref<string[]>([])

const { loading, error, result, taskStatus, taskReport, runSimulate, parseEvaluation } =
  useLabSimulate('edu.cn.gov.multisig', [11155111])

const evaluation = computed(() => parseEvaluation(result.value?.evaluation))
const hints = computed(() => parseHints(evaluation.value?.audit_hints))
const approved = computed(() => hintBool(hints.value, 'approved'))
const confirmationCount = computed(() => hintNumber(hints.value, 'confirmations', signed.value.length))

const approvers = [
  { label: 'Owner 1', addr: '0x1111111111111111111111111111111111111111' },
  { label: 'Owner 2', addr: '0x2222222222222222222222222222222222222222' },
  { label: 'Owner 3', addr: '0x3333333333333333333333333333333333333333' },
]

const progressPct = computed(() =>
  Math.min(100, (signed.value.length / threshold.value) * 100),
)

function toggleSign(addr: string) {
  if (signed.value.includes(addr)) {
    signed.value = signed.value.filter((a) => a !== addr)
  } else {
    signed.value = [...signed.value, addr]
  }
}

function runApproval() {
  runSimulate(
    '多级多签审批演示',
    {
      proposal_id: proposalId.value,
      proposal_title: proposalTitle.value,
      threshold: threshold.value,
      confirmations: signed.value,
    },
    { taskType: 'CN_MULTISIG_APPROVAL_DEMO' },
  )
}
</script>

<template>
  <section class="lab-panel">
    <header class="lab-header">
      <img src="/assets/icon.png" alt="" width="32" height="32" />
      <div>
        <h1>多级多签审批</h1>
        <p class="muted">Sepolia 测试网合约模板 · 权限模型教学 · 非真实 OA 系统</p>
      </div>
    </header>

    <div v-if="evaluation" class="eval-card">
      <h2>规则评估</h2>
      <p class="ok">✓ 合规通过 · {{ evaluation.recommended_language }}</p>
      <p v-if="hints.proposal_id"><strong>提案:</strong> {{ hints.proposal_id }}</p>
      <p v-if="hints.threshold"><strong>阈值:</strong> {{ hints.threshold }}</p>
      <p><strong>已批准:</strong> {{ approved ? '是' : '否' }} · 确认 {{ confirmationCount }}</p>
    </div>

    <div class="lab-grid">
      <div class="card">
        <h2>提案信息</h2>
        <label>提案 ID <input v-model="proposalId" /></label>
        <label>标题 <input v-model="proposalTitle" /></label>
        <label>
          签名阈值
          <input v-model.number="threshold" type="number" min="1" max="3" />
        </label>
        <div class="progress">
          <div class="progress-fill" :style="{ width: progressPct + '%' }" />
        </div>
        <p class="muted">{{ signed.length }} / {{ threshold }} 签名</p>
        <button :disabled="loading" @click="runApproval">
          {{ loading ? '模拟中…' : '提交审批快照' }}
        </button>
        <p v-if="taskStatus" class="status">任务状态: {{ taskStatus }}</p>
        <p v-if="error" class="error">{{ error }}</p>
      </div>

      <div class="card">
        <h2>逐步签名</h2>
        <ul class="sign-list">
          <li v-for="a in approvers" :key="a.addr">
            <label>
              <input
                type="checkbox"
                :checked="signed.includes(a.addr)"
                @change="toggleSign(a.addr)"
              />
              {{ a.label }} <code>{{ a.addr.slice(0, 10) }}…</code>
            </label>
          </li>
        </ul>
        <p class="muted">勾选签名人后提交 · MultiSigApprovalDemo.sol</p>
      </div>

      <div class="card" :class="{ approved: approved }">
        <h2>审批状态</h2>
        <p v-if="!evaluation" class="muted">提交后显示规则评估</p>
        <p v-else-if="approved" class="ok">✓ 已达 {{ hints.threshold }} — approved</p>
        <p v-else class="info">pending — 需更多签名</p>
        <ol class="steps">
          <li :class="{ done: signed.length >= 1 }">1. 收集签名</li>
          <li :class="{ done: signed.length >= threshold }">2. 达阈值</li>
          <li :class="{ done: approved }">3. 可执行（教学）</li>
        </ol>
      </div>
    </div>

    <pre v-if="taskReport" class="result">{{ JSON.stringify(taskReport, null, 2) }}</pre>
    <pre v-else-if="result" class="result">{{ JSON.stringify(result, null, 2) }}</pre>
  </section>
</template>

<style scoped>
.lab-panel { padding: 1rem; }
.lab-header { display: flex; gap: 0.75rem; align-items: center; margin-bottom: 1rem; }
.eval-card { background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 1rem; margin-bottom: 1rem; }
.eval-card h2 { margin: 0 0 0.5rem; font-size: 1rem; }
.eval-card .ok { color: #15803d; margin: 0 0 0.5rem; }
.lab-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; }
.card { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 1rem; }
.card.approved { border-color: #86efac; background: #f0fdf4; }
.muted { color: #64748b; font-size: 0.875rem; }
.status { color: #2563eb; font-size: 0.875rem; margin-top: 0.5rem; }
.error { color: #dc2626; }
.ok { color: #16a34a; font-weight: 600; }
.info { color: #2563eb; }
code { font-family: monospace; font-size: 0.75rem; color: #0f766e; }
.progress { height: 8px; background: #e2e8f0; border-radius: 4px; margin: 0.5rem 0; overflow: hidden; }
.progress-fill { height: 100%; background: #2563eb; transition: width 0.25s; }
.sign-list { list-style: none; padding: 0; font-size: 0.85rem; }
.sign-list li { margin-bottom: 0.4rem; }
.steps { padding-left: 1.25rem; font-size: 0.85rem; }
.steps li.done { color: #16a34a; font-weight: 600; }
.result { margin-top: 1rem; background: #1e293b; color: #e2e8f0; padding: 1rem; border-radius: 8px; overflow: auto; font-size: 0.8rem; }
input[type="text"], input[type="number"] { display: block; width: 100%; margin: 0.35rem 0 0.75rem; padding: 0.5rem; border: 1px solid #cbd5e1; border-radius: 4px; }
button { margin-top: 0.5rem; padding: 0.5rem 1rem; background: #2563eb; color: white; border: none; border-radius: 4px; cursor: pointer; }
button:disabled { opacity: 0.6; cursor: not-allowed; }
</style>
