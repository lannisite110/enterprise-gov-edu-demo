import { onUnmounted, ref } from 'vue'

export interface SimulateEvaluation {
  compliance_passed?: boolean
  recommended_template?: string
  recommended_language?: string
  rejection_reason?: string
  audit_hints?: string[]
}

export interface SimulateResult {
  plugin_id?: string
  evaluation?: SimulateEvaluation | string
  task?: {
    id?: string
    namespace?: string
    status?: string
    task_type?: string
  }
}

function parseEvaluation(raw: SimulateEvaluation | string | undefined): SimulateEvaluation | null {
  if (!raw) return null
  if (typeof raw === 'string') {
    try {
      return JSON.parse(raw) as SimulateEvaluation
    } catch {
      return null
    }
  }
  return raw
}

export function useLabSimulate(
  pluginId: string,
  defaultChainIds: (number | string)[] = ['fabric-local'],
  pollIntervalMs = 1500,
) {
  const loading = ref(false)
  const error = ref('')
  const result = ref<SimulateResult | null>(null)
  const taskStatus = ref('')
  const taskReport = ref<Record<string, unknown> | null>(null)
  let pollTimer: ReturnType<typeof setInterval> | null = null

  function stopPoll() {
    if (pollTimer) {
      clearInterval(pollTimer)
      pollTimer = null
    }
  }

  function startPoll(taskId: string) {
    stopPoll()
    taskStatus.value = 'pending'
    pollTimer = setInterval(async () => {
      try {
        const statusRes = await fetch(`/api/v1/labs/${pluginId}/status/${taskId}`)
        const statusData = await statusRes.json()
        taskStatus.value = (statusData.status as string) ?? 'unknown'
        if (taskStatus.value === 'completed' || taskStatus.value === 'failed') {
          stopPoll()
          const reportRes = await fetch(`/api/v1/labs/${pluginId}/report/${taskId}`)
          taskReport.value = await reportRes.json()
        }
      } catch {
        /* ignore transient poll errors */
      }
    }, pollIntervalMs)
  }

  async function runSimulate(
    userPrompt: string,
    params: Record<string, unknown>,
    options?: { taskType?: string },
  ) {
    loading.value = true
    error.value = ''
    result.value = null
    taskStatus.value = ''
    taskReport.value = null
    stopPoll()
    try {
      const body: Record<string, unknown> = {
        user_prompt: userPrompt,
        params,
        allowed_chain_ids: defaultChainIds,
      }
      if (options?.taskType) body.task_type = options.taskType

      const res = await fetch(`/api/v1/labs/${pluginId}/simulate`, {
        method: 'POST',
        headers: { 'Content-Type: application/json' },
        body: JSON.stringify(body),
      })
      const data = (await res.json()) as SimulateResult
      if (!res.ok) throw new Error((data as { error?: string }).error || res.statusText)
      result.value = data
      const evaluation = parseEvaluation(data.evaluation)
      if (evaluation && evaluation.compliance_passed === false) {
        throw new Error(evaluation.rejection_reason || 'compliance check failed')
      }
      const taskId = data.task?.id
      if (taskId) startPoll(taskId)
    } catch (e) {
      error.value = e instanceof Error ? e.message : String(e)
    } finally {
      loading.value = false
    }
  }

  onUnmounted(stopPoll)

  return { loading, error, result, taskStatus, taskReport, runSimulate, parseEvaluation }
}
