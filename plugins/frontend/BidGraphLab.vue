<script setup lang="ts">
import { computed, ref } from 'vue'
import { useLabSimulate } from './shared/useLabSimulate'
import { parseHints, hintNumber } from './shared/parseHints'
import LabAssistDrawer from '@/components/LabAssistDrawer.vue'

const scenario = ref('sample')
const { loading, error, result, taskStatus, taskReport, runSimulate, parseEvaluation } =
  useLabSimulate('edu.cn.gov.bid-graph', ['fabric-local'])

const evaluation = computed(() => parseEvaluation(result.value?.evaluation))
const hints = computed(() => parseHints(evaluation.value?.audit_hints))
const suspicionScore = computed(() => hintNumber(hints.value, 'suspicion_score'))
const riskLevel = computed(() => hints.value.risk_level ?? 'low')

const graphNodes = [
  { id: 'sup-a', name: '华东虚构建材', x: 12, y: 20, rep: '张某某' },
  { id: 'sup-b', name: '浦东虚构工程', x: 42, y: 15, rep: '张某某' },
  { id: 'sup-c', name: '长三角虚构IT', x: 72, y: 25, rep: '李某某' },
  { id: 'sup-d', name: '西湖虚构设备', x: 55, y: 55, rep: '王某某' },
  { id: 'sup-e', name: '独立虚构贸易', x: 18, y: 65, rep: '赵某某' },
]

const graphEdges = [
  { from: 'sup-a', to: 'sup-b' },
  { from: 'sup-b', to: 'sup-c' },
  { from: 'sup-a', to: 'sup-d' },
  { from: 'sup-c', to: 'sup-d' },
]

const structuredKeys = new Set([
  'suspicion_score', 'risk_level', 'nodes', 'edges', 'graph_source',
])

const textFindings = computed(() =>
  (evaluation.value?.audit_hints ?? []).filter((h) => {
    const key = h.includes('=') ? h.slice(0, h.indexOf('=')) : ''
    return !structuredKeys.has(key)
  }),
)

const scorePercent = computed(() => Math.min(100, Math.max(0, suspicionScore.value)))

function nodeById(id: string) {
  return graphNodes.find((n) => n.id === id)
}

function runAnalysis() {
  runSimulate(
    '招投标关联图谱分析',
    { graph: 'sample', scenario: scenario.value },
    { taskType: 'CN_BID_GRAPH_SIM' },
  )
}

const assistParams = computed(() => ({ graph: 'sample', scenario: scenario.value }))
</script>

<template>
  <section class="lab-panel">
    <header class="lab-header">
      <img src="/assets/icon.png" alt="" width="32" height="32" />
      <div>
        <h1>招投标关联图谱</h1>
        <p class="muted">虚构供应商节点 · 纯图算法教学 · 不对接政府采购网</p>
      </div>
    </header>

    <div v-if="evaluation" class="eval-card">
      <h2>规则评估</h2>
      <p class="ok">✓ 合规通过 · {{ evaluation.recommended_language }}</p>
      <p>
        <strong>教学评分:</strong> {{ suspicionScore }}/100
        · <strong>风险:</strong> {{ riskLevel }}
        · 节点 {{ hints.nodes }} / 边 {{ hints.edges }}
      </p>
      <div class="score-bar">
        <div class="score-fill" :style="{ width: scorePercent + '%' }" :class="riskLevel" />
      </div>
    </div>

    <div class="lab-grid">
      <div class="card">
        <h2>分析控制</h2>
        <label>
          场景
          <select v-model="scenario">
            <option value="sample">sample-graph（默认）</option>
          </select>
        </label>
        <button :disabled="loading" @click="runAnalysis">
          {{ loading ? '分析中…' : '运行关联分析' }}
        </button>
        <p v-if="taskStatus" class="status">任务状态: {{ taskStatus }}</p>
        <p v-if="error" class="error">{{ error }}</p>
      </div>

      <div class="card graph-card">
        <h2>关联图谱（示意）</h2>
        <svg viewBox="0 0 100 80" class="graph-svg">
          <line
            v-for="(e, i) in graphEdges"
            :key="i"
            :x1="nodeById(e.from)?.x"
            :y1="nodeById(e.from)?.y"
            :x2="nodeById(e.to)?.x"
            :y2="nodeById(e.to)?.y"
            stroke="#94a3b8"
            stroke-width="0.8"
          />
          <g v-for="n in graphNodes" :key="n.id">
            <circle :cx="n.x" :cy="n.y" r="4" :class="n.rep === '张某某' ? 'hot' : 'node'" />
            <text :x="n.x" :y="n.y + 8" text-anchor="middle" class="node-label">{{ n.id }}</text>
          </g>
        </svg>
        <p class="muted">橙色：共享法人「张某某」节点</p>
      </div>

      <div class="card">
        <h2>评分解释</h2>
        <ul v-if="textFindings.length" class="findings">
          <li v-for="(f, i) in textFindings" :key="i">{{ f }}</li>
        </ul>
        <p v-else class="muted">提交分析后显示 findings</p>
      </div>
    </div>

    <pre v-if="taskReport" class="result">{{ JSON.stringify(taskReport, null, 2) }}</pre>
    <pre v-else-if="result" class="result">{{ JSON.stringify(result, null, 2) }}</pre>

    <LabAssistDrawer
      plugin-id="edu.cn.gov.bid-graph"
      :params="assistParams"
      :audit-hints="evaluation?.audit_hints"
    />
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
.muted { color: #64748b; font-size: 0.875rem; }
.status { color: #2563eb; font-size: 0.875rem; margin-top: 0.5rem; }
.error { color: #dc2626; }
.score-bar { height: 8px; background: #e2e8f0; border-radius: 4px; margin-top: 0.5rem; overflow: hidden; }
.score-fill { height: 100%; transition: width 0.3s; }
.score-fill.high { background: #dc2626; }
.score-fill.medium { background: #f59e0b; }
.score-fill.low { background: #22c55e; }
.graph-svg { width: 100%; height: 180px; background: #fff; border-radius: 4px; }
.node { fill: #3b82f6; }
.hot { fill: #f59e0b; }
.node-label { font-size: 3px; fill: #475569; }
.findings { padding-left: 1.1rem; font-size: 0.85rem; }
.findings li { margin-bottom: 0.35rem; }
.result { margin-top: 1rem; background: #1e293b; color: #e2e8f0; padding: 1rem; border-radius: 8px; overflow: auto; font-size: 0.8rem; }
select, input { display: block; width: 100%; margin: 0.5rem 0; padding: 0.5rem; border: 1px solid #cbd5e1; border-radius: 4px; }
button { margin-top: 0.5rem; padding: 0.5rem 1rem; background: #2563eb; color: white; border: none; border-radius: 4px; cursor: pointer; }
button:disabled { opacity: 0.6; cursor: not-allowed; }
</style>
