import { Outlet } from 'react-router-dom'
import { APP_NAME, APP_VERSION, APP_AUTHOR } from '@/config/app'
import { SidebarNav } from './SidebarNav'

export function Layout() {
  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <aside className="w-56 shrink-0 border-r border-border bg-surface flex flex-col">
        <div className="px-3 py-4 border-b border-border-muted">
          <div className="font-mono text-h1 tracking-tight text-text-primary">
            &gt;_
          </div>
          <div className="text-tiny text-text-secondary mt-0.5 uppercase tracking-wider">{APP_NAME}</div>
        </div>
        <SidebarNav />
        <div className="mt-auto px-3 py-3 border-t border-border-muted text-tiny text-text-muted">
          v{APP_VERSION} · {APP_AUTHOR}
        </div>
      </aside>
      {/* Main */}
      <main className="flex-1 overflow-auto bg-bg">
        <Outlet />
      </main>
    </div>
  )
}