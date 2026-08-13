import type { ReactNode } from 'react'

type PillKind = 'active' | 'amber' | 'danger' | 'muted'

const KINDS: Record<PillKind, string> = {
  active: 'pill-active',
  amber: 'pill-amber',
  danger: 'pill-danger',
  muted: 'pill-muted',
}

export function Pill({ children, kind = 'muted' }: { children: ReactNode; kind?: PillKind }) {
  return <span className={`pill ${KINDS[kind]}`}>[ {children} ]</span>
}
