import { Link } from 'react-router-dom'
import { mockAccounts } from '@/store/mock'

export default function Accounts() {
  return (
    <div className="p-6 max-w-5xl">
      <h1 className="font-mono text-h1 uppercase tracking-widest mb-4">ACCOUNTS</h1>
      <Link to="/accounts/add" className="pill pill-active mb-4 inline-block">+ ADD ACCOUNT</Link>
      <div className="space-y-2 mt-4">
        {mockAccounts.map((a) => (
          <Link key={a.id} to={`/accounts/${a.id}`}
            className="card p-3 flex items-center justify-between hover:border-text-muted">
            <span className="font-mono">{a.alias}</span>
            <span className="font-mono text-tiny text-text-secondary">{a.email}</span>
            <span className="font-mono text-tiny text-text-muted">{a.status.toUpperCase()}</span>
          </Link>
        ))}
      </div>
    </div>
  )
}
