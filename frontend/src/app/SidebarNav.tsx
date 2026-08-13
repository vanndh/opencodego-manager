import { NavLink } from 'react-router-dom'

const NAV = [
  { to: '/', label: 'Dashboard', glyph: '>' },
  { to: '/accounts', label: 'Accounts', glyph: ' ' },
  { to: '/bonuses', label: 'Bonuses', glyph: ' ' },
  { to: '/api', label: 'API', glyph: ' ' },
  { to: '/gateway', label: 'Gateway', glyph: ' ' },
  { to: '/activity', label: 'Activity', glyph: ' ' },
  { to: '/settings', label: 'Settings', glyph: ' ' },
  { to: '/about', label: 'About', glyph: ' ' },
]

export function SidebarNav() {
  return (
    <nav className="flex-1 py-2 px-2 space-y-0.5">
      {NAV.map((item) => (
        <NavLink
          key={item.to}
          to={item.to}
          end={item.to === '/'}
          className={({ isActive }) =>
            `nav-item ${isActive ? 'nav-item-active' : ''}`
          }
        >
          <span className="w-3 text-accent font-mono">{item.glyph}</span>
          <span className="font-medium">{item.label}</span>
        </NavLink>
      ))}
    </nav>
  )
}