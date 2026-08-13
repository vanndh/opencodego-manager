/**
 * Mock store — PHASE 3 (прототип на mock data).
 * Реальные данные придут через WS/REST в PHASE 4+.
 */

export type AccountStatus =
  | 'online' | 'offline' | 'limited' | 'error' | 'disabled' | 'logging_in' | 'reauth'

export interface Account {
  id: string
  alias: string
  email: string
  status: AccountStatus
  group: string
  favorite: boolean
  paused: boolean
  useInGateway: boolean
  gatewayPriority: number
  fiveH: { used: number; total: number; resetAt: string }
  weekly: { used: number; total: number; resetAt: string }
  monthly: { used: number; total: number; resetAt: string }
  bonus: { available: boolean; pct: number }
  apiReady: boolean
  latency: number
  lastUpdate: string
}

export const mockAccounts: Account[] = [
  {
    id: 'a1', alias: 'MAIN-01', email: 'user01********@gmail.com', status: 'online',
    group: 'MAIN', favorite: true, paused: false, useInGateway: true, gatewayPriority: 1,
    fiveH: { used: 9.7, total: 12, resetAt: '01:42:17' },
    weekly: { used: 18.6, total: 30, resetAt: '4d 11h' },
    monthly: { used: 55.8, total: 60, resetAt: '18d 02h' },
    bonus: { available: true, pct: 25 }, apiReady: true, latency: 182, lastUpdate: '11:24:12',
  },
  {
    id: 'a2', alias: 'MAIN-02', email: 'user02********@gmail.com', status: 'online',
    group: 'MAIN', favorite: false, paused: false, useInGateway: true, gatewayPriority: 2,
    fiveH: { used: 7.2, total: 12, resetAt: '03:11:44' },
    weekly: { used: 12.0, total: 30, resetAt: '5d 02h' },
    monthly: { used: 30.0, total: 60, resetAt: '20d 10h' },
    bonus: { available: false, pct: 0 }, apiReady: true, latency: 210, lastUpdate: '11:24:10',
  },
  {
    id: 'a3', alias: 'ALT-01', email: 'alt01********@gmail.com', status: 'limited',
    group: 'BACKUP', favorite: false, paused: false, useInGateway: true, gatewayPriority: 3,
    fiveH: { used: 11.5, total: 12, resetAt: '00:18:02' },
    weekly: { used: 28.9, total: 30, resetAt: '1d 03h' },
    monthly: { used: 58.2, total: 60, resetAt: '6d 12h' },
    bonus: { available: true, pct: 25 }, apiReady: true, latency: 265, lastUpdate: '11:23:58',
  },
  {
    id: 'a4', alias: 'BACKUP-01', email: 'backup********@gmail.com', status: 'error',
    group: 'BACKUP', favorite: false, paused: true, useInGateway: false, gatewayPriority: 4,
    fiveH: { used: 0, total: 12, resetAt: '—' },
    weekly: { used: 0, total: 30, resetAt: '—' },
    monthly: { used: 0, total: 60, resetAt: '—' },
    bonus: { available: false, pct: 0 }, apiReady: false, latency: 0, lastUpdate: '10:52:31',
  },
  {
    id: 'a5', alias: 'TEST-01', email: 'test01********@gmail.com', status: 'disabled',
    group: 'TEST', favorite: false, paused: true, useInGateway: false, gatewayPriority: 5,
    fiveH: { used: 3.0, total: 12, resetAt: '02:20:00' },
    weekly: { used: 5.0, total: 30, resetAt: '6d 00h' },
    monthly: { used: 10.0, total: 60, resetAt: '25d 00h' },
    bonus: { available: false, pct: 0 }, apiReady: false, latency: 0, lastUpdate: '09:00:00',
  },
]

export function pct(used: number, total: number): number {
  return total > 0 ? Math.round((used / total) * 100) : 0
}
