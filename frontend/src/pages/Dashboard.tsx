import { useState } from 'react'
import { Link } from 'react-router-dom'
import { mockAccounts, pct, type Account } from '@/store/mock'
import { Glyph } from '@/components/Glyph'
import { Bar } from '@/components/Bar'
import { Pill } from '@/components/Pill'

export default function Dashboard() {
  const [mode, setMode] = useState<'cards' | 'compact'>('cards')
  const accounts = mockAccounts

  const online = accounts.filter((a) => a.status === 'online').length
  const limited = accounts.filter((a) => a.status === 'limited').length
  const errored = accounts.filter((a) => a.status === 'error').length

  const agg = (key: 'fiveH' | 'weekly' | 'monthly') => {
    const used = accounts.reduce((s, a) => s + a[key].used, 0)
    const total = accounts.reduce((s, a) => s + a[key].total, 0)
    return { used, total, pct: pct(used, total) }
  }
  const fiveH = agg('fiveH')
  const weekly = agg('weekly')
  const monthly = agg('monthly')

  return (
    <div className="p-6 max-w-6xl">
      {/* Header */}
      <header className="flex items-baseline justify-between mb-6">
        <div>
          <h1 className="font-mono text-h1 uppercase tracking-widest text-text-primary">
            OPENCODE GO MANAGER
          </h1>
          <div className="mt-1 text-text-secondary font-mono text-mono">
            {accounts.length} ACCOUNTS · {online} ONLINE · {limited} LIMITED · {errored} ERROR
          </div>
        </div>
        <div className="flex items-center gap-2 font-mono text-mono">
          <Glyph kind="online" />
          <span className="text-text-secondary">Gateway</span>
          <Pill kind="active">RUNNING</Pill>
        </div>
      </header>

      {/* Aggregate limits */}
      <section className="card p-4 mb-6 grid grid-cols-1 md:grid-cols-3 gap-4">
        <LimitBlock label="5 HOURS" pct={fiveH.pct} reset="01:42:17" />
        <LimitBlock label="WEEK" pct={weekly.pct} reset="4d 11h" />
        <LimitBlock label="MONTH" pct={monthly.pct} reset="18d 02h" />
      </section>

      {/* Stats row */}
      <section className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
        <Stat label="BONUSES AVAILABLE" value="3" />
        <Stat label="ACTIVE API ACCOUNTS" value="11" />
        <Stat label="GATEWAY REQUESTS" value="1,284" />
        <Stat label="ERRORS" value="12" />
      </section>

      {/* Toolbar */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex gap-2">
          <button
            onClick={() => setMode('cards')}
            className={`pill ${mode === 'cards' ? 'pill-active' : 'pill-muted'}`}
          >
            CARDS
          </button>
          <button
            onClick={() => setMode('compact')}
            className={`pill ${mode === 'compact' ? 'pill-active' : 'pill-muted'}`}
          >
            COMPACT
          </button>
        </div>
        <Link to="/accounts/add" className="pill pill-active">+ ADD ACCOUNT</Link>
      </div>

      {/* Accounts */}
      {mode === 'cards' ? <Cards accounts={accounts} /> : <Compact accounts={accounts} />}

      {/* Footer */}
      <footer className="mt-6 font-mono text-tiny text-text-muted flex items-center gap-3">
        <span className="animate-pulse">▸ refreshing_</span>
        <span>last sync 11:24:12</span>
        <span className="text-text-muted">[R] refresh  [/] search</span>
      </footer>
    </div>
  )
}

function LimitBlock({ label, pct: p, reset }: { label: string; pct: number; reset: string }) {
  return (
    <div>
      <div className="flex items-baseline justify-between mb-1">
        <span className="font-mono text-h2 uppercase tracking-wider text-text-secondary">{label}</span>
        <span className="font-mono text-tiny text-text-muted">RESET {reset}</span>
      </div>
      <Bar pct={p} />
    </div>
  )
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="card p-3">
      <div className="font-mono text-h2 text-text-primary">{value}</div>
      <div className="text-tiny text-text-secondary uppercase tracking-wider mt-0.5">{label}</div>
    </div>
  )
}

function Cards({ accounts }: { accounts: Account[] }) {
  return (
    <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
      {accounts.map((a) => (
        <Link key={a.id} to={`/accounts/${a.id}`} className="card p-4 hover:border-text-muted transition-colors">
          <div className="flex items-center justify-between mb-2">
            <span className="font-mono text-h2 text-text-primary">{a.alias}</span>
            <Glyph kind={a.status} />
          </div>
          <div className="font-mono text-tiny text-text-secondary mb-3">{a.email}</div>
          <div className="grid grid-cols-1 gap-1.5 mb-2">
            <Row label="5H" pct={pct(a.fiveH.used, a.fiveH.total)} reset={a.fiveH.resetAt} />
            <Row label="WEEK" pct={pct(a.weekly.used, a.weekly.total)} reset={a.weekly.resetAt} />
            <Row label="MONTH" pct={pct(a.monthly.used, a.monthly.total)} reset={a.monthly.resetAt} />
          </div>
          <div className="flex items-center justify-between pt-2 border-t border-border-muted">
            <div className="flex items-center gap-2">
              {a.bonus.available && <Pill kind="amber">BONUS +{a.bonus.pct}%</Pill>}
              {a.apiReady && <Pill kind="active">API READY</Pill>}
            </div>
            <span className="font-mono text-tiny text-text-muted">LAT {a.latency}ms</span>
          </div>
        </Link>
      ))}
    </div>
  )
}

function Row({ label, pct: p, reset }: { label: string; pct: number; reset: string }) {
  return (
    <div className="flex items-center gap-2">
      <span className="w-12 font-mono text-tiny text-text-secondary">{label}</span>
      <Bar pct={p} />
      <span className="ml-auto font-mono text-tiny text-text-muted">R {reset}</span>
    </div>
  )
}

function Compact({ accounts }: { accounts: Account[] }) {
  return (
    <div className="card overflow-x-auto">
      <table className="w-full text-left">
        <thead>
          <tr className="border-b border-border text-tiny font-mono uppercase tracking-wider text-text-muted">
            <th className="px-3 py-2">Status</th>
            <th className="px-3 py-2">Alias</th>
            <th className="px-3 py-2">Account</th>
            <th className="px-3 py-2">5H</th>
            <th className="px-3 py-2">Week</th>
            <th className="px-3 py-2">Month</th>
            <th className="px-3 py-2">Bonus</th>
            <th className="px-3 py-2">API</th>
            <th className="px-3 py-2">Lat</th>
            <th className="px-3 py-2">Updated</th>
          </tr>
        </thead>
        <tbody>
          {accounts.map((a) => (
            <tr key={a.id} className="border-b border-border-muted hover:bg-surface-2">
              <td className="px-3 py-2"><Glyph kind={a.status} /></td>
              <td className="px-3 py-2 font-mono text-text-primary">{a.alias}</td>
              <td className="px-3 py-2 font-mono text-tiny text-text-secondary">{a.email}</td>
              <td className="px-3 py-2 font-mono text-mono text-text-secondary">{pct(a.fiveH.used, a.fiveH.total)}%</td>
              <td className="px-3 py-2 font-mono text-mono text-text-secondary">{pct(a.weekly.used, a.weekly.total)}%</td>
              <td className="px-3 py-2 font-mono text-mono text-text-secondary">{pct(a.monthly.used, a.monthly.total)}%</td>
              <td className="px-3 py-2">{a.bonus.available ? <Pill kind="amber">+{a.bonus.pct}%</Pill> : <span className="text-text-muted font-mono">—</span>}</td>
              <td className="px-3 py-2 font-mono text-tiny">{a.apiReady ? <span className="text-accent">●</span> : <span className="text-text-muted">○</span>}</td>
              <td className="px-3 py-2 font-mono text-tiny text-text-secondary">{a.latency}ms</td>
              <td className="px-3 py-2 font-mono text-tiny text-text-muted">{a.lastUpdate}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
