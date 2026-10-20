'use client'

import { AnimatePresence, motion, useReducedMotion } from 'framer-motion'
import { useEffect, useMemo, useState } from 'react'

const steps = [
  'SYSTEM INITIALIZATION',
  '[ OK ] Hardware interface initialized',
  '[ OK ] Runtime environment loaded',
  '[ OK ] Network stack initialized',
  'SECURITY CHECK',
  '[ OK ] Firewall module active',
  '[ OK ] Encryption module active',
  '[ OK ] Threat detection active',
  '[ OK ] Session integrity verified',
  'SATYAMOS BOOT',
  '[ OK ] Portfolio kernel loaded',
  '[ OK ] Terminal interface ready',
  '[ OK ] Visual systems online',
  'WELCOME',
]

const checks = ['Environment verified', 'Portfolio integrity verified', 'Secure session established']

function shouldReplay() {
  if (typeof window === 'undefined') return false
  return new URLSearchParams(window.location.search).get('boot') === 'true'
}

export function BootSequence() {
  const reduceMotion = useReducedMotion()
  const [visible, setVisible] = useState(false)
  const [step, setStep] = useState(steps.length)
  const [complete, setComplete] = useState(false)

  const interval = useMemo(() => (reduceMotion ? 25 : 105), [reduceMotion])

  useEffect(() => {
    const replay = shouldReplay()
    if (!replay && sessionStorage.getItem('satyam-boot-seen') === 'true') return
    setVisible(true)
    setStep(reduceMotion ? steps.length : 0)
  }, [reduceMotion])

  useEffect(() => {
    if (!visible || step >= steps.length) return
    const timer = window.setTimeout(() => setStep((current) => current + 1), interval)
    return () => window.clearTimeout(timer)
  }, [interval, step, visible])

  useEffect(() => {
    if (!visible || step < steps.length) return
    const timer = window.setTimeout(() => {
      setComplete(true)
      sessionStorage.setItem('satyam-boot-seen', 'true')
    }, reduceMotion ? 80 : 800)
    return () => window.clearTimeout(timer)
  }, [reduceMotion, step, visible])

  const skip = () => {
    sessionStorage.setItem('satyam-boot-seen', 'true')
    setComplete(true)
  }

  useEffect(() => {
    if (!visible) return
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape' || event.key === 'Enter') skip()
    }
    window.addEventListener('keydown', onKeyDown)
    return () => window.removeEventListener('keydown', onKeyDown)
  })

  return (
    <AnimatePresence>
      {visible && !complete && (
        <motion.div className="boot-overlay" initial={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: reduceMotion ? 0.1 : 0.65 }} role="dialog" aria-label="SATYAM OS secure boot">
          <video className="boot-video" autoPlay muted loop playsInline aria-hidden="true">
            <source src="/81188-576082864_medium.mp4" type="video/mp4" />
          </video>
          <div className="boot-video-tint" aria-hidden="true" />
          <div className="boot-grid" aria-hidden="true" /><div className="boot-particles" aria-hidden="true"><i /><i /><i /><i /><i /></div>
          <div className="boot-terminal">
            <div className="boot-brand"><strong>SATYAM OS</strong><span>SECURE BOOT v1.0.0</span></div>
            <div className="boot-log" aria-live="polite">
              {steps.slice(0, step).map((line, index) => (
                <motion.div key={`${line}-${index}`} className={line.startsWith('[ OK ]') ? 'boot-line ok' : 'boot-line'} initial={reduceMotion ? false : { opacity: 0, x: -8 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.2 }}>{line}</motion.div>
              ))}
              {step >= steps.length && <div className="boot-security"><div>BOOT VALIDATION</div>{checks.map((check) => <div key={check} className="boot-line ok">[✓] {check}</div>)}</div>}
            </div>
            <div className="boot-footer">
              <div className="boot-progress-label"><span>{step >= steps.length ? 'SYSTEM READY' : 'BOOTING SYSTEM'}</span><span>{Math.round((Math.min(step, steps.length) / steps.length) * 100)}%</span></div>
              <div className="boot-progress"><span style={{ width: `${(Math.min(step, steps.length) / steps.length) * 100}%` }} /></div>
              {step >= steps.length && <div className="boot-ready">SECURITY STATUS: SECURE</div>}
            </div>
          </div>
          <button className="boot-skip" onClick={skip}>SKIP BOOT <span>→</span></button>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
