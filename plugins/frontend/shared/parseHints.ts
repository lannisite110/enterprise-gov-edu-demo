export function parseHints(hints: string[] | undefined): Record<string, string> {
  const map: Record<string, string> = {}
  for (const line of hints ?? []) {
    const idx = line.indexOf('=')
    if (idx <= 0) continue
    map[line.slice(0, idx)] = line.slice(idx + 1)
  }
  return map
}

export function hintNumber(map: Record<string, string>, key: string, fallback = 0): number {
  const n = Number(map[key])
  return Number.isFinite(n) ? n : fallback
}

export function hintBool(map: Record<string, string>, key: string): boolean {
  return map[key] === 'true'
}
