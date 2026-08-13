import { mockAccounts } from '@/store/mock'
import { Pill } from '@/components/Pill'

export default function Bonuses() {
  const withBonus = mockAccounts.filter((a) => a.bonus.available)
  return (
    <div className="p-6 max-w-3xl">
      <h1 className="font-mono text-h1 uppercase tracking-widest mb-4">BONUSES</h1>
      {withBonus.length === 0 ? (
        <div className="card p-6 text-center font-mono text-mono text-text-secondary">
          NO BONUSES AVAILABLE
        </div>
      ) : (
        <div className="space-y-3">
          {withBonus.map((a) => (
            <div key={a.id} className="card p-4 flex items-center justify-between">
              <div>
                <div className="font-mono">{a.alias}</div>
                <div className="font-mono text-tiny text-text-secondary">+{a.bonus.pct}% WEEKLY · DETECTED 11:42:07</div>
              </div>
              <div className="flex items-center gap-2">
                <Pill kind="amber">AUTO OFF</Pill>
                <button className="pill pill-active">ACTIVATE</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
