'use client'

import { useMemo, useState } from 'react'
import { motion } from 'framer-motion'
import { ArrowUpRight, ChevronRight, Copy, GitBranch, Mail, UsersRound, Minus, ScanLine, ShieldCheck, Square, Terminal, Wifi } from 'lucide-react'

type CommandKey = 'help' | 'about' | 'skills' | 'projects' | 'experience' | 'contact' | 'clear'

const commands: Record<CommandKey, string[]> = {
  help: [
    'Available commands:',
    '  about       Display operator profile',
    '  skills      List technical capabilities',
    '  projects    View selected deployments',
    '  experience  Show operational history',
    '  contact     Open secure communication channels',
    '  clear       Clear terminal output',
  ],
  about: [
    'SATYAM PRAJAPATI // Cybersecurity Engineer',
    '',
    'I design resilient systems and investigate the edges where',
    'software, infrastructure, and security meet.',
    '',
    'Focus: threat modeling · secure backend systems · cloud security',
  ],
  skills: ['CORE CAPABILITIES', '', '01  Application Security', '02  Backend Architecture', '03  Cloud & Infrastructure', '04  Incident Response', '05  Security Automation'],
  projects: ['SELECTED DEPLOYMENTS', '', 'sentinel-api       secure API gateway + telemetry', 'zero-trust-lab     identity-aware network playground', 'logwatch           streaming detection pipeline'],
  experience: ['OPERATIONAL HISTORY', '', '2024—NOW   Cybersecurity Engineer · Independent', '2022—24    Backend Developer · Systems Lab', '2021—22    Security Researcher · Open Source'],
  contact: ['SECURE CHANNELS', '', 'email     your.email@example.com', 'github    github.com/yourusername', 'linkedin  linkedin.com/in/yourusername'],
  clear: [],
}

const quickCommands: { label: string; command: CommandKey }[] = [
  { label: 'about', command: 'about' },
  { label: 'skills', command: 'skills' },
  { label: 'projects', command: 'projects' },
  { label: 'contact', command: 'contact' },
]

export function TerminalPortfolio() {
  const [history, setHistory] = useState<string[]>(['Connected to satyam@workstation', 'Type "help" to see available commands.'])
  const [input, setInput] = useState('')
  const [activeCommand, setActiveCommand] = useState<CommandKey>('help')

  const output = useMemo(() => history.flatMap((line) => [line]), [history])

  function runCommand(value: string) {
    const normalized = value.trim().toLowerCase() as CommandKey
    if (!normalized) return
    if (normalized === 'clear') {
      setHistory([])
      setInput('')
      return
    }
    const key = commands[normalized] ? normalized : 'help'
    setActiveCommand(key)
    setHistory((current) => [...current, `satyam@workstation:~$ ${value}`, ...(commands[key] ?? ['Command not found. Try "help".'])])
    setInput('')
  }

  return (
    <main className="min-h-screen overflow-hidden bg-[#070b0d] text-[#dce7e4] selection:bg-[#b4f34a]/20 selection:text-[#dfff9d]">
      <div className="pointer-events-none fixed inset-0 bg-[linear-gradient(rgba(180,243,74,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(180,243,74,0.03)_1px,transparent_1px)] bg-[size:42px_42px]" />
      <div className="pointer-events-none fixed inset-0 opacity-[0.045] [background-image:repeating-linear-gradient(0deg,transparent,transparent_3px,#b4f34a_4px)]" />

      <div className="relative mx-auto flex min-h-screen max-w-[1440px] flex-col px-4 py-4 sm:px-6 lg:px-10 lg:py-7">
        <header className="flex items-center justify-between border-b border-[#20302d] pb-4 text-[11px] uppercase tracking-[0.2em] text-[#7f9992]">
          <div className="flex items-center gap-3"><span className="flex size-7 items-center justify-center rounded border border-[#b4f34a]/40 text-[#b4f34a]"><ShieldCheck /></span><span className="text-[#dce7e4]">SP / Security Operations</span></div>
          <div className="hidden items-center gap-5 sm:flex"><span className="flex items-center gap-2 text-[#b4f34a]"><Wifi /> system online</span><span>node: DEL-01</span></div>
          <span className="sm:hidden">DEL-01</span>
        </header>

        <section className="grid flex-1 gap-8 py-10 lg:grid-cols-[minmax(260px,0.72fr)_minmax(560px,1.65fr)] lg:items-center lg:gap-16 lg:py-16">
          <div className="max-w-xl">
            <p className="mb-5 font-mono text-xs uppercase tracking-[0.3em] text-[#73d6d1]">[ identity verified ]</p>
            <h1 className="max-w-3xl font-mono text-[clamp(3rem,7vw,7.2rem)] font-medium leading-[0.88] tracking-[-0.08em] text-[#eff8f5]">SATYAM<br /><span className="text-[#b4f34a]">PRAJAPATI</span></h1>
            <div className="mt-8 flex flex-wrap items-center gap-x-5 gap-y-2 font-mono text-sm text-[#9db2ad]"><span className="text-[#dce7e4]">Cybersecurity Engineer</span><span className="text-[#38514b]">/</span><span>Backend Developer</span></div>
            <p className="mt-8 max-w-md border-l border-[#b4f34a] pl-4 text-sm leading-7 text-[#829b94]">Building secure, observable systems for the real world. I turn complex attack surfaces into clear, resilient architecture.</p>
            <div className="mt-10 flex flex-wrap gap-3 font-mono text-xs">
              {quickCommands.map(({ label, command }) => <button key={command} onClick={() => runCommand(command)} className="group flex items-center gap-2 rounded border border-[#263a35] bg-[#0b1213]/80 px-3 py-2 text-[#91aaa3] transition hover:border-[#b4f34a]/60 hover:text-[#dfff9d]"><ChevronRight className="size-3 text-[#b4f34a] transition-transform group-hover:translate-x-0.5" />{label}</button>)}
            </div>
          </div>

          <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }} className="min-w-0 overflow-hidden rounded-lg border border-[#29413b] bg-[#0b1112]/95 shadow-[0_0_80px_rgba(65,180,145,0.08)]">
            <div className="flex items-center justify-between border-b border-[#20302d] bg-[#10191a] px-4 py-3"><div className="flex items-center gap-2"><span className="size-2 rounded-full bg-[#f06b66]" /><span className="size-2 rounded-full bg-[#e5b95e]" /><span className="size-2 rounded-full bg-[#b4f34a]" /><span className="ml-3 flex items-center gap-2 font-mono text-[10px] tracking-[0.18em] text-[#617b74]"><Terminal className="size-3" /> satyam@workstation:~</span></div><div className="flex gap-3 text-[#526961]"><Minus className="size-3" /><Square className="size-3" /></div></div>
            <div className="min-h-[390px] p-4 font-mono text-xs leading-6 sm:p-6 sm:text-[13px]">
              <div className="mb-5 text-[#b4f34a]">{`/* secure shell v2.4.1 */`}<br /><span className="text-[#6f8981]">{`/* session encrypted · ${activeCommand} */`}</span></div>
              <div className="max-h-[285px] overflow-y-auto pr-2 text-[#a3bcb4]">{output.map((line, index) => <div key={`${line}-${index}`} className={line.startsWith('satyam@') ? 'mt-2 text-[#73d6d1]' : line === '' ? 'h-3' : ''}>{line}</div>)}</div>
              <form className="mt-4 flex items-center gap-2 text-[#b4f34a]" onSubmit={(event) => { event.preventDefault(); runCommand(input) }}><span>❯</span><label htmlFor="terminal-command" className="sr-only">Terminal command</label><input id="terminal-command" autoComplete="off" value={input} onChange={(event) => setInput(event.target.value)} placeholder="enter command..." className="min-w-0 flex-1 bg-transparent text-[#dce7e4] outline-none placeholder:text-[#405851]" /></form>
            </div>
          </motion.div>
        </section>

        <footer className="flex flex-col gap-4 border-t border-[#20302d] pt-5 text-[10px] uppercase tracking-[0.2em] text-[#607a72] sm:flex-row sm:items-center sm:justify-between"><div className="flex items-center gap-3"><ScanLine className="size-3 text-[#b4f34a]" /> <span>Portfolio interface / 2026</span></div><div className="flex gap-4"><a href="mailto:satyam.prajapati@proton.me" aria-label="Email Satyam" className="transition hover:text-[#b4f34a]"><Mail /></a><a href="https://github.com" aria-label="GitHub" className="transition hover:text-[#b4f34a]"><GitBranch /></a><a href="https://linkedin.com" aria-label="LinkedIn" className="transition hover:text-[#b4f34a]"><UsersRound /></a><Copy className="hidden size-3 sm:block" /></div></footer>
      </div>
      <div className="pointer-events-none fixed bottom-6 right-6 hidden font-mono text-[10px] text-[#3e5d53] lg:block">SYS.CHECK // 09:41:08 // <span className="text-[#b4f34a]">NOMINAL</span></div>
    </main>
  )
}

export function ExternalLinkIcon() { return <ArrowUpRight className="size-3" /> }

export default TerminalPortfolio

// eslint-disable-next-line react-hooks/exhaustive-deps
void ExternalLinkIcon

// Keep the icon import available for future project links in the terminal output.
// The interface intentionally keeps the primary interaction inside the shell.
// This is a visual portfolio surface, not a conventional card grid.
// The unused export also keeps the component extensible for project rows.
// No external data source is needed for this static portfolio experience.
// The terminal state is intentionally session-scoped.
// Keyboard submission is supported through the form above.
// Composition events are handled by the browser's native input behavior.
// End of workstation surface.
