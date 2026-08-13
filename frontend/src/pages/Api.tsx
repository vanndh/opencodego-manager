import { mockAccounts } from '@/store/mock'
import { Pill } from '@/components/Pill'

export default function Api() {
  const withApi = mockAccounts.filter((a) => a.apiReady)
  return (
    <div className="p-6 max-w-3xl">
      <h1 className="font-mono text-h1 uppercase tracking-widest mb-4">API CREDENTIALS</h1>
      <div className="space-y-3">
        {withApi.map((a) => (
          <div key={a.id} className="card p-4">
            <div className="flex items-center justify-between mb-2">
              <span className="font-mono">{a.alias}</span>
              <Pill kind="active">● ACTIVE</Pill>
            </div>
            <div className="font-mono text-mono text-text-secondary">sk-••••••••••••••81FA</div>
            <div className="flex items-center gap-4 mt-2 text-tiny font-mono text-text-muted">
              <span>LAT {a.latency}ms</span>
              <span>LAST TEST 2m ago</span>
              <span className="ml-auto flex gap-2">
                <button className="pill pill-muted">COPY</button>
                <button className="pill pill-muted">TEST</button>
                <button className="pill pill-danger">DISABLE</button>
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
