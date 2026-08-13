const EVENTS = [
  { t: '11:41:02', a: 'MAIN-01', m: 'Limits updated', c: 'LIMITS' },
  { t: '11:41:08', a: 'MAIN-04', m: 'Session expired', c: 'AUTH' },
  { t: '11:41:09', a: 'MAIN-04', m: 'Reauthentication started', c: 'AUTH' },
  { t: '11:41:14', a: 'MAIN-04', m: 'Authentication successful', c: 'AUTH' },
  { t: '11:42:07', a: 'ALT-02', m: 'Bonus detected', c: 'BONUSES' },
  { t: '11:42:11', a: 'ALT-02', m: 'Bonus activated', c: 'BONUSES' },
  { t: '11:43:51', a: 'MAIN-03', m: 'Weekly limit updated', c: 'LIMITS' },
  { t: '11:43:52', a: 'Gateway', m: 'MAIN-03 → MAIN-05', c: 'GATEWAY' },
]

export default function Activity() {
  return (
    <div className="p-6 max-w-3xl">
      <h1 className="font-mono text-h1 uppercase tracking-widest mb-4">ACTIVITY</h1>
      <div className="card p-2 font-mono text-mono">
        {EVENTS.map((e, i) => (
          <div key={i} className="flex gap-3 px-2 py-1.5 border-b border-border-muted last:border-0">
            <span className="text-text-muted">{e.t}</span>
            <span className="w-20 text-text-secondary">{e.a}</span>
            <span className="text-text-primary">{e.m}</span>
            <span className="ml-auto text-tiny text-text-muted">{e.c}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
