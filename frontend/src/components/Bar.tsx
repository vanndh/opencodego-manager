/**
 * ASCII progress bar: [████████░░] 82%
 * Рисуется символами в mono — не CSS gradient.
 */
const WIDTH = 10

export function Bar({ pct, color = 'text-accent' }: { pct: number; color?: string }) {
  const p = Math.max(0, Math.min(100, pct))
  const filled = Math.round((p / 100) * WIDTH)
  const fill = '█'.repeat(filled)
  const rest = '░'.repeat(WIDTH - filled)
  return (
    <span className="ascii-bar text-text-secondary">
      <span className={`text-muted`}>[</span>
      <span className={color}>{fill}</span>
      <span className="text-border">{rest}</span>
      <span className="text-muted">]</span>
      <span className="ml-1 text-text-secondary">{p}%</span>
    </span>
  )
}
