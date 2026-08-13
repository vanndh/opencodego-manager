import { APP_NAME, APP_VERSION, APP_AUTHOR } from '@/config/app'

export default function About() {
  return (
    <div className="p-6 max-w-md">
      <pre className="font-mono text-accent mb-4">{String.raw`
   ┌─────┐
───┤  >_ ├──
   └─────┘`}</pre>
      <div className="card p-4 space-y-2 font-mono text-mono">
        <div className="text-text-primary">{APP_NAME}</div>
        <div className="text-text-secondary">OpenCode GO Account Manager</div>
        <div className="text-text-muted text-tiny">Version {APP_VERSION}</div>
        <div className="text-text-secondary">Author: {APP_AUTHOR}</div>
      </div>
    </div>
  )
}
