'use client'

import { useEffect, useState } from 'react'
import { api } from '@/lib/api'

const metrics = [
  { label: 'CPU', bar: '███████░░░', value: '72%' },
  { label: 'MEMORY', bar: '█████░░░░░', value: '48%' },
  { label: 'NETWORK', bar: '█████████░', value: '91%' },
  { label: 'SECURITY', bar: '██████████', value: '100%' },
]

export function SystemStatus() {
  const [apiStatus, setApiStatus] = useState<'ONLINE' | 'OFFLINE'>('OFFLINE')

  useEffect(() => {
    let mounted = true
    api.health()
      .then(() => { if (mounted) setApiStatus('ONLINE') })
      .catch(() => { if (mounted) setApiStatus('OFFLINE') })
    return () => { mounted = false }
  }, [])

  return (
    <aside className="system-status" aria-label="System status">
      <div className="system-status-heading">
        <span>SYSTEM STATUS / {apiStatus}</span>
        <i aria-hidden="true" />
      </div>
      <div className="system-metrics">
        {metrics.map((metric) => (
          <div className="system-metric" key={metric.label}>
            <div className="system-metric-label"><span>{metric.label}</span><span>{metric.value}</span></div>
            <div className="system-bar" aria-label={`${metric.label} ${metric.value}`} role="img">{metric.bar}</div>
          </div>
        ))}
      </div>
      <div className="system-meta">
        <div><span>STATUS</span><strong><b aria-hidden="true">●</b> ONLINE</strong></div>
        <div><span>MODE</span><strong>FOCUSED</strong></div>
      </div>
    </aside>
  )
}

export default SystemStatus
