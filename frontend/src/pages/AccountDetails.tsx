import { useParams } from 'react-router-dom'
import { mockAccounts, pct } from '@/store/mock'
import { Glyph } from '@/components/Glyph'
import { Bar } from '@/components/Bar'

export default function AccountDetails() {
  const { id } = useParams()
  const a = mockAccounts.find((x) => x.id === id) ?? mockAccounts[0]

  return (
    <div className="p-6 max-w-3xl">
      <div className="flex items-center gap-3 mb-4">
        <h1 className="font-mono text-h1 uppercase tracking-widest">{a.alias}</h1>
        <Glyph kind={a.status} />
      </div>
      <div className="grid grid-cols-2 gap-4">
        <Detail label="EMAIL" value={a.email} />
        <Detail label="LATENCY" value={`${a.latency}ms`} />
        <Detail label="LAST LOGIN" value="13 Aug 2026" />
        <Detail label="SESSION" value="VALID" />
      </div>
      <div className="card p-4 mt-4 space-y-3">
        <div><div className="font-mono text-tiny text-text-secondary mb-1">5H · RESET {a.fiveH.resetAt}</div><Bar pct={pct(a.fiveH.used, a.fiveH.total)} /></div>
        <div><div className="font-mono text-tiny text-text-secondary mb-1">WEEK · RESET {a.weekly.resetAt}</div><Bar pct={pct(a.weekly.used, a.weekly.total)} /></div>
        <div><div className="font-mono text-tiny text-text-secondary mb-1">MONTH · RESET {a.monthly.resetAt}</div><Bar pct={pct(a.monthly.used, a.monthly.total)} /></div>
      </div>
    </div>
  )
}

function Detail({ label, value }: { label: string; value: string }) {
  return (
    <div className="card p-3">
      <div className="font-mono text-tiny uppercase tracking-wider text-text-muted">{label}</div>
      <div className="font-mono text-mono text-text-primary mt-0.5">{value}</div>
    </div>
  )
}
