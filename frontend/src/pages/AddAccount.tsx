import { useState, type ReactNode } from 'react'
import { useNavigate } from 'react-router-dom'

export default function AddAccount() {
  const nav = useNavigate()
  const [step, setStep] = useState<'form' | 'saving'>('form')
  const [form, setForm] = useState({ alias: '', email: '', password: '', totp: '', recovery: '' })

  if (step === 'saving') {
    return (
      <div className="p-6 max-w-md font-mono text-mono space-y-1">
        <div>Saving credentials_</div>
        <div className="text-text-secondary">Authenticating…</div>
        <div className="text-text-secondary">2FA detected · TOTP generated</div>
        <div className="text-text-secondary">Session saved · Fetching limits…</div>
        <div className="text-accent">● READY</div>
        <button className="pill pill-active mt-4" onClick={() => nav('/accounts')}>VIEW ACCOUNTS</button>
      </div>
    )
  }

  return (
    <div className="p-6 max-w-md">
      <h1 className="font-mono text-h1 uppercase tracking-widest mb-4">+ ADD ACCOUNT</h1>
      <div className="card p-4 space-y-3">
        <Field label="ALIAS">
          <input className="input" value={form.alias} onChange={(e) => setForm({ ...form, alias: e.target.value })} placeholder="MAIN-01" />
        </Field>
        <Field label="EMAIL">
          <input className="input" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} placeholder="user@gmail.com" />
        </Field>
        <Field label="PASSWORD">
          <input className="input" type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} placeholder="••••••••" />
        </Field>
        <Field label="TOTP SECRET">
          <input className="input" value={form.totp} onChange={(e) => setForm({ ...form, totp: e.target.value })} placeholder="JBSWY3DP…" />
        </Field>
        <Field label="RECOVERY CODES">
          <textarea className="input font-mono" rows={4} value={form.recovery}
            onChange={(e) => setForm({ ...form, recovery: e.target.value })}
            placeholder={'code1\ncode2\ncode3\ncode4'} />
        </Field>
        <div className="flex gap-2 pt-2">
          <button className="pill pill-muted" onClick={() => nav(-1)}>CANCEL</button>
          <button className="pill pill-active" onClick={() => setStep('saving')}>ADD ACCOUNT</button>
        </div>
      </div>
    </div>
  )
}

function Field({ label, children }: { label: string; children: ReactNode }) {
  return (
    <label className="block">
      <div className="font-mono text-tiny uppercase tracking-wider text-text-secondary mb-1">{label}</div>
      {children}
    </label>
  )
}
