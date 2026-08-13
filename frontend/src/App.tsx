import { Routes, Route } from 'react-router-dom'
import { Layout } from '@/app/Layout'
import Dashboard from '@/pages/Dashboard'
import Accounts from '@/pages/Accounts'
import AddAccount from '@/pages/AddAccount'
import AccountDetails from '@/pages/AccountDetails'
import Bonuses from '@/pages/Bonuses'
import Api from '@/pages/Api'
import Gateway from '@/pages/Gateway'
import Activity from '@/pages/Activity'
import Settings from '@/pages/Settings'
import About from '@/pages/About'

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="accounts" element={<Accounts />} />
        <Route path="accounts/add" element={<AddAccount />} />
        <Route path="accounts/:id" element={<AccountDetails />} />
        <Route path="bonuses" element={<Bonuses />} />
        <Route path="api" element={<Api />} />
        <Route path="gateway" element={<Gateway />} />
        <Route path="activity" element={<Activity />} />
        <Route path="settings" element={<Settings />} />
        <Route path="about" element={<About />} />
      </Route>
    </Routes>
  )
}