const SECTIONS = ['GENERAL', 'INTERFACE', 'ACCOUNTS', 'AUTHENTICATION', 'LIMITS', 'BONUSES', 'GATEWAY', 'SECURITY', 'ADVANCED']

export default function Settings() {
  return (
    <div className="p-6 max-w-3xl">
      <h1 className="font-mono text-h1 uppercase tracking-widest mb-4">SETTINGS</h1>
      <div className="grid grid-cols-2 gap-2">
        {SECTIONS.map((s) => (
          <div key={s} className="card p-3 font-mono text-mono text-text-secondary hover:text-text-primary cursor-pointer">
            {s}
          </div>
        ))}
      </div>
    </div>
  )
}
