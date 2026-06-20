<script setup lang="ts">
import { computed, ref } from 'vue'
import { useLabI18n } from '@/composables/useLabI18n'
import { useLabSimulate } from './shared/useLabSimulate'
import { parseHints, hintBool, hintNumber } from './shared/parseHints'

const { t } = useLabI18n('edu.cn.gov.supply')

const simulateBreak = ref(false)
const assetId = ref('MAT-2024-DEMO-001')

const { loading, error, result, taskStatus, taskReport, runSimulate, parseEvaluation } =
  useLabSimulate('edu.cn.gov.supply', ['fabric-local'])

const evaluation = computed(() => parseEvaluation(result.value?.evaluation))
const hints = computed(() => parseHints(evaluation.value?.audit_hints))
const chainIntact = computed(() => hintBool(hints.value, 'chain_intact'))
const balance = computed(() => hintNumber(hints.value, 'balance'))

const demoEvents = [
  { seq: 1, type: 'inbound', warehouse: 'WH-DEMO-A', quantity: 100, delta: 100 },
  { seq: 2, type: 'transfer', warehouse: 'WH-DEMO-B', quantity: 40, delta: 0 },
  { seq: 3, type: 'outbound', warehouse: 'WH-DEMO-B', quantity: 15, delta: -15 },
]

function eventTypeLabel(type: string) {
  if (type === 'inbound') return t('type_inbound')
  if (type === 'transfer') return t('type_transfer')
  if (type === 'outbound') return t('type_outbound')
  return type
}

const inventoryTimeline = computed(() => {
  let stock = 0
  return demoEvents.map((e) => {
    stock += e.delta
    return { ...e, stock, typeLabel: eventTypeLabel(e.type) }
  })
})

const fabricSandbox = {
  chainId: 'fabric-local',
  channel: 'edu-cn-gov-sandbox',
  org: 'OrgEduDemo',
}

function runVerify() {
  runSimulate(
    '物资出入库存证校验',
    {
      ledger: 'sample',
      asset_id: assetId.value,
      simulate_break: simulateBreak.value,
    },
    { taskType: 'CN_SUPPLY_CHAIN_DEMO' },
  )
}
</script>

<template>
  <section class="lab-panel">
    <header class="lab-header">
      <img src="/assets/icon.png" alt="" width="32" height="32" />
      <div>
        <h1>{{ t('title') }}</h1>
        <p class="muted">{{ t('subtitle') }}</p>
      </div>
    </header>

    <div v-if="evaluation" class="eval-card" :class="{ broken: !chainIntact }">
      <h2>{{ t('ruleEval') }}</h2>
      <p v-if="chainIntact" class="ok">{{ t('compliancePass') }} · {{ evaluation.recommended_language }}</p>
      <p v-else class="warn">{{ t('chainBroken') }}</p>
      <p>
        <strong>{{ t('stock') }}:</strong> {{ balance }} {{ t('pieces') }}
        · <strong>{{ t('events') }}:</strong> {{ hints.event_count }}
      </p>
      <p v-if="hints.merkle_root"><strong>{{ t('merkleRoot') }}:</strong> <code>{{ hints.merkle_root }}</code></p>
    </div>

    <div class="lab-grid">
      <div class="card">
        <h2>{{ t('verifySection') }}</h2>
        <label>{{ t('assetId') }} <input v-model="assetId" /></label>
        <label class="check-row">
          <input v-model="simulateBreak" type="checkbox" />
          {{ t('simulateBreak') }}
        </label>
        <button :disabled="loading" @click="runVerify">
          {{ loading ? t('verifying') : t('runVerify') }}
        </button>
        <p v-if="taskStatus" class="status">{{ t('taskStatus') }}: {{ taskStatus }}</p>
        <p v-if="error" class="error">{{ error }}</p>
      </div>

      <div class="card">
        <h2>{{ t('eventTimeline') }}</h2>
        <table>
          <thead>
            <tr><th>{{ t('seq') }}</th><th>{{ t('type') }}</th><th>{{ t('warehouse') }}</th><th>Δ</th><th>{{ t('stock') }}</th></tr>
          </thead>
          <tbody>
            <tr v-for="e in inventoryTimeline" :key="e.seq">
              <td>{{ e.seq }}</td>
              <td>{{ e.typeLabel }}</td>
              <td>{{ e.warehouse }}</td>
              <td>{{ e.delta > 0 ? '+' + e.delta : e.delta }}</td>
              <td><strong>{{ e.stock }}</strong></td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="card">
        <h2>{{ t('chain') }}</h2>
        <ol class="hash-chain">
          <li v-for="e in demoEvents" :key="e.seq" :class="{ broken: simulateBreak && e.seq === 3 }">
            #{{ e.seq }} {{ eventTypeLabel(e.type) }}
            <span v-if="simulateBreak && e.seq === 3" class="warn-tag">prev_hash ✗</span>
            <span v-else class="ok-tag">→</span>
          </li>
        </ol>
        <p class="muted">Fabric {{ fabricSandbox.channel }}</p>
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
.eval-card.broken { background: #fffbeb; border-color: #fcd34d; }
.eval-card h2 { margin: 0 0 0.5rem; font-size: 1rem; }
.eval-card .ok { color: #15803d; margin: 0 0 0.5rem; }
.eval-card .warn { color: #d97706; font-weight: 600; margin: 0 0 0.5rem; }
.lab-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; }
.card { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 1rem; }
.muted { color: #64748b; font-size: 0.875rem; }
.status { color: #2563eb; font-size: 0.875rem; margin-top: 0.5rem; }
.error { color: #dc2626; }
code { font-family: monospace; font-size: 0.75rem; color: #0f766e; }
.check-row { display: flex; align-items: center; gap: 0.5rem; margin: 0.5rem 0; font-size: 0.875rem; }
.hash-chain { padding-left: 1.25rem; font-size: 0.85rem; }
.hash-chain li.broken { color: #dc2626; font-weight: 600; }
.ok-tag { color: #16a34a; margin-left: 0.25rem; }
.warn-tag { color: #dc2626; margin-left: 0.25rem; font-size: 0.75rem; }
.result { margin-top: 1rem; background: #1e293b; color: #e2e8f0; padding: 1rem; border-radius: 8px; overflow: auto; font-size: 0.8rem; }
table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
th, td { border: 1px solid #e2e8f0; padding: 0.4rem 0.5rem; text-align: left; }
input[type="text"] { display: block; width: 100%; margin: 0.35rem 0 0.75rem; padding: 0.5rem; border: 1px solid #cbd5e1; border-radius: 4px; }
button { margin-top: 0.5rem; padding: 0.5rem 1rem; background: #2563eb; color: white; border: none; border-radius: 4px; cursor: pointer; }
button:disabled { opacity: 0.6; cursor: not-allowed; }
</style>
