/**
 * ASCII primitives — фирменный визуальный язык OpenCode GO Manager.
 */

export type GlyphKind =
  | 'online' | 'offline' | 'limited' | 'error' | 'disabled'
  | 'logging_in' | 'reauth'

const GLYPHS: Record<GlyphKind, { ch: string; color: string; label: string }> = {
  online: { ch: '●', color: 'text-accent', label: 'ONLINE' },
  offline: { ch: '○', color: 'text-text-muted', label: 'OFFLINE' },
  limited: { ch: '!', color: 'text-accent-2', label: 'LIMITED' },
  error: { ch: '!', color: 'text-danger', label: 'ERROR' },
  disabled: { ch: '○', color: 'text-text-muted', label: 'DISABLED' },
  logging_in: { ch: '●', color: 'text-info', label: 'LOGGING IN' },
  reauth: { ch: '●', color: 'text-info', label: 'REAUTHENTICATING' },
}

export function Glyph({ kind }: { kind: GlyphKind }) {
  const g = GLYPHS[kind]
  return (
    <span className={`font-mono text-tiny uppercase tracking-wider ${g.color}`}>
      {g.ch} {g.label}
    </span>
  )
}

export function StatusDot({ kind }: { kind: GlyphKind }) {
  const g = GLYPHS[kind]
  return (
    <span className={`font-mono text-mono ${g.color}`} title={g.label}>
      {g.ch}
    </span>
  )
}
