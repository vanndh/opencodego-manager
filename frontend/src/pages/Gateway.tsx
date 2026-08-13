import { Pill } from '@/components/Pill'

export default function Gateway() {
  return (
    <div className="p-6 max-w-3xl">
      <h1 className="font-mono text-h1 uppercase tracking-widest mb-4">GATEWAY</h1>
      <div className="card p-4 space-y-3">
        <div className="flex items-center justify-between">
          <span className="font-mono text-mono text-text-secondary">STATUS</span>
          <Pill kind="active">● RUNNING</Pill>
        </div>
        <div className="flex items-center justify-between">
          <span className="font-mono text-mono text-text-secondary">ENDPOINT</span>
          <span className="font-mono text-mono">http://127.0.0.1:3456</span>
        </div>
        <div className="flex items-center justify-between">
          <span className="font-mono text-mono text-text-secondary">LOCAL API KEY</span>
          <span className="font-mono text-mono">••••••••••••••••</span>
        </div>
        <div className="flex items-center justify-between">
          <span className="font-mono text-mono text-text-secondary">STRATEGY</span>
          <span className="font-mono text-mono">MOST AVAILABLE</span>
        </div>
        <div className="grid grid-cols-3 gap-2 pt-2 border-t border-border-muted">
          <Stat l="REQUESTS" v="1,248" />
          <Stat l="SUCCESS" v="1,223" />
          <Stat l="ERRORS" v="25" />
        </div>
        <div className="flex gap-2 pt-2">
          <button className="pill pill-muted">STOP</button>
          <button className="pill pill-active">RESTART</button>
          <button className="pill pill-muted">COPY ENDPOINT</button>
          <button className="pill pill-muted">COPY API KEY</button>
        </div>
      </div>
    </div>
  )
}

function Stat({ l, v }: { l: string; v: string }) {
  return (
    <div>
      <div className="font-mono text-h2 text-text-primary">{v}</div>
      <div className="font-mono text-tiny text-text-muted uppercase">{l}</div>
    </div>
  )
}
