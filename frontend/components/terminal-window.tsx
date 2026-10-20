'use client'

import { useEffect, useRef, useState } from 'react'

type TerminalLine = { prompt?: string; text: string; tone?: 'accent' | 'muted' | 'info'; cwd?: string }

const commandOutput: Record<string, string[]> = {
  help: ['Available commands:', '  about      operator profile', '  skills     technical capabilities', '  projects   selected work', '  contact    secure channels', '  ls / dir   list workspace files', '  cat file   read a workspace file', '  cd <dir>   change directory', '  pwd        print working directory', '  whoami     show current user', '  date       show system date', '  clear/cls  clear session', '  history    command history', '  ver        Windows version alias', '  uname -a   system information'],
  about: ['SATYAM PRAJAPATI', 'Cybersecurity Engineer / Backend Developer', 'Building secure systems, APIs and resilient infrastructure.'],
  skills: ['CORE CAPABILITIES', 'Python · FastAPI · React · TypeScript', 'PostgreSQL · Linux · Nmap · Burp Suite', 'OWASP · API Security · Networking'],
  projects: ['SELECTED WORK', 'cyber fraud detection system', 'healthcare automation system', 'network security lab'],
  contact: ['SECURE CHANNELS', 'email    your.email@example.com', 'github   github.com/yourusername', 'linkedin linkedin.com/in/yourusername'],
  pwd: ['/home/satyam/portfolio'],
  whoami: ['satyam'],
  hostname: ['satyam-portfolio'],
  date: [new Date().toString()],
  ver: ['Microsoft Windows [Version 11.0.26100.1]', 'Portfolio Terminal Compatibility Layer'],
  'uname -a': ['Linux satyam-portfolio 6.8.0-portfolio x86_64 GNU/Linux'],
  ipconfig: ['Windows IP Configuration', '', 'Ethernet adapter SecureLink:', '   IPv4 Address . . . . . . . . . : 192.168.1.42', '   Default Gateway . . . . . . . : 192.168.1.1'],
  ifconfig: ['eth0: flags=4163<UP,BROADCAST,RUNNING>  mtu 1500', '    inet 192.168.1.42  netmask 255.255.255.0', '    status: secure / monitored'],
  'cat readme.md': ['# SATYAM PRAJAPATI', '', 'Security-minded engineer building reliable backend systems.', 'Use `help` to explore this portfolio.'],
  'cat about.txt': ['Operator profile: cybersecurity engineer and backend developer.', 'Mission: build secure, useful, resilient software.'],
  neofetch: ['       .--.       satyam@portfolio', '      |o_o |      ----------------', '      |:_/ |      OS: SATYAM OS', '     //   \\      Shell: portfolio-sh', '    (|     |)     Uptime: always learning', '   /\\_   _/\\     Security: enabled'],
}

const filesByDirectory: Record<string, string[]> = {
  '~': ['about.txt', 'contact.txt', 'projects/', 'skills/', 'resume.pdf', 'README.md'],
  '~/projects': ['fraud-detection.md', 'healthcare-automation.md', 'network-security-lab.md'],
  '~/skills': ['full-stack-skill/', 'cybersecurity-tools/'],
  '~/skills/full-stack-skill': ['HTML', 'CSS', 'JavaScript', 'TypeScript', 'React', 'Next.js', 'Node.js', 'Express.js', 'Python', 'FastAPI', 'SQL', 'PostgreSQL', 'REST API', 'Git'],
  '~/skills/cybersecurity-tools': ['Linux', 'Nmap', 'Burp Suite', 'OWASP', 'Web Security', 'Network Security', 'TCP/IP', 'DNS', 'HTTP/HTTPS', 'Wireshark', 'Metasploit', 'Vulnerability Assessment', 'API Security', 'CCNA Fundamentals'],
}

export function TerminalWindow() {
  const [history, setHistory] = useState<TerminalLine[]>([])
  const [input, setInput] = useState('')
  const [cwd, setCwd] = useState('~')
  const [commandHistory, setCommandHistory] = useState<string[]>([])
  const [historyIndex, setHistoryIndex] = useState(-1)
  const inputRef = useRef<HTMLInputElement>(null)
  const outputRef = useRef<HTMLDivElement>(null)
  const followOutputRef = useRef(true)
  const cwdRef = useRef('~')
  const resumeWindowRef = useRef<Window | null>(null)

  useEffect(() => {
    const output = outputRef.current
    if (output && followOutputRef.current) output.scrollTop = output.scrollHeight
  }, [history])

  function handleOutputScroll(event: React.UIEvent<HTMLDivElement>) {
    const output = event.currentTarget
    followOutputRef.current = output.scrollHeight - output.scrollTop - output.clientHeight < 8
  }

  function changeDirectory(nextDirectory: string) {
    cwdRef.current = nextDirectory
    setCwd(nextDirectory)
  }

  function runCommand(value: string) {
    const raw = value.trim()
    const command = raw.toLowerCase()
    if (!raw) return
    const commandCwd = cwdRef.current
    setCommandHistory((current) => [...current, raw])
    setHistoryIndex(-1)
    if (command === 'clear' || command === 'cls') {
      setHistory([])
      setInput('')
      return
    }
    if (command === 'pwd') {
      const activeDirectory = commandCwd
      const path = activeDirectory === '~' ? '/home/satyam/portfolio' : `/home/satyam/portfolio/${activeDirectory.slice(2)}`
      setHistory((current) => [...current, { prompt: raw, text: '', cwd: commandCwd }, { text: path, tone: 'accent' }])
      setInput('')
      return
    }
    if (command === 'ls' || command === 'ls -la' || command === 'dir') {
      const directoryFiles = filesByDirectory[commandCwd] ?? []
      setHistory((current) => [...current, { prompt: raw, text: '', cwd: commandCwd }, ...directoryFiles.map((text) => ({ text, tone: 'info' as const }))])
      setInput('')
      return
    }
    if (command === 'open resume.pdf' || command === 'start resume.pdf' || command === 'resume') {
      resumeWindowRef.current = window.open('/resume.pdf', '_blank', 'noopener,noreferrer')
      setHistory((current) => [...current, { prompt: raw, text: '', cwd: commandCwd }, { text: 'Opening resume.pdf...', tone: 'accent' }])
      setInput('')
      return
    }
    if (command === 'cat resume.pdf') {
      setHistory((current) => [...current, { prompt: raw, text: '', cwd: commandCwd }, { text: 'resume.pdf is a binary document. Use "open resume.pdf" to view it.', tone: 'muted' }])
      setInput('')
      return
    }
    if (command === 'cd' || command === 'cd ~' || command === 'cd /home/satyam/portfolio') {
      setHistory((current) => [...current, { prompt: raw, text: '', cwd: commandCwd }])
      changeDirectory('~')
      setInput('')
      return
    }
    if (command === 'cd ..') {
      const parentDirectory = commandCwd.includes('/') ? commandCwd.slice(0, commandCwd.lastIndexOf('/')) || '~' : '~'
      setHistory((current) => [...current, { prompt: raw, text: '', cwd: commandCwd }])
      changeDirectory(parentDirectory)
      setInput('')
      return
    }
    if (command.startsWith('cd ')) {
      const target = raw.slice(3).trim()
      const directoryTargets: Record<string, string> = {
        projects: '~/projects',
        skills: '~/skills',
        'full-stack-skill': '~/skills/full-stack-skill',
        'cybersecurity-tools': '~/skills/cybersecurity-tools',
        'about.txt': '~/about',
      }
      const nextDirectory = directoryTargets[target]
      if (nextDirectory && (nextDirectory.startsWith(`${commandCwd}/`) || target === 'projects' || target === 'skills' || target === 'about.txt')) {
        setHistory((current) => [...current, { prompt: raw, text: '', cwd: commandCwd }])
        changeDirectory(nextDirectory)
      } else setHistory((current) => [...current, { prompt: raw, text: `bash: cd: ${target}: No such file or directory`, tone: 'muted', cwd: commandCwd }])
      setInput('')
      return
    }
    if (command.startsWith('echo ')) {
      setHistory((current) => [...current, { prompt: raw, text: raw.slice(5), cwd: commandCwd }])
      setInput('')
      return
    }
    const output = commandOutput[command] ?? (command.startsWith('cat ') ? [`cat: ${raw.slice(4)}: No such file or directory`] : [`${command}: command not found`, 'Type "help" for available commands.'])
    setHistory((current) => [...current, { prompt: raw, text: '', cwd: commandCwd }, ...output.map((text) => ({ text, tone: text.includes('not found') || text.includes('No such') ? 'muted' as const : undefined }))])
    setInput('')
  }

  function handleKeyDown(event: React.KeyboardEvent<HTMLInputElement>) {
    if (event.ctrlKey && event.key.toLowerCase() === 'c') {
      event.preventDefault()
      if (resumeWindowRef.current && !resumeWindowRef.current.closed) resumeWindowRef.current.close()
      resumeWindowRef.current = null
      if (input) {
        setHistory((current) => [...current, { prompt: input, text: '', cwd: cwdRef.current }, { text: '^C', tone: 'muted' }])
      } else {
        setHistory((current) => [...current, { text: '^C', tone: 'muted' }])
      }
      setInput('')
      setHistoryIndex(-1)
      return
    }
    if (event.key === 'ArrowUp') {
      event.preventDefault()
      const next = Math.max(0, commandHistory.length - 1 - Math.max(historyIndex, 0))
      setHistoryIndex(commandHistory.length - 1 - next)
      setInput(commandHistory[next] ?? '')
    }
    if (event.key === 'ArrowDown') {
      event.preventDefault()
      const next = historyIndex + 1
      if (next >= commandHistory.length) { setHistoryIndex(-1); setInput('') } else setInput(commandHistory[next])
    }
  }

  const prompt = `satyam@portfolio:${cwd}$`
    const lines = history


  return (
    <div className="terminal-window" id="terminal" aria-label="Interactive portfolio terminal" onClick={() => inputRef.current?.focus()}>
      <div className="terminal-header">
        <div className="terminal-controls" aria-hidden="true"><i /><i /><i /></div>
        <span>satyam@portfolio:{cwd}</span>
        <span className="terminal-header-status">LIVE SESSION · UTF-8</span>
      </div>
      <div className="terminal-body" aria-live="polite">
        <div ref={outputRef} className="terminal-output" onScroll={handleOutputScroll}>
          {lines.map((line, index) => (
            <div className={`terminal-line ${line.prompt ? 'terminal-prompt' : ''} ${line.tone === 'accent' ? 'terminal-accent' : ''} ${line.tone === 'muted' ? 'terminal-muted' : ''}`} key={`${line.prompt ?? line.text}-${index}`}>
              {line.prompt && <><span className="terminal-user">satyam@portfolio:{line.cwd ?? cwd}$</span><span>{line.prompt}</span></>}
              {!line.prompt && <span>{line.text}</span>}
            </div>
          ))}
        </div>
        <form className="terminal-input-row" onSubmit={(event) => { event.preventDefault(); runCommand(input) }}>
          <span className="terminal-user" aria-hidden="true">{prompt}</span>
          <label className="sr-only" htmlFor="terminal-command">Terminal command</label>
          <input ref={inputRef} id="terminal-command" value={input} onChange={(event) => setInput(event.target.value)} onKeyDown={handleKeyDown} autoComplete="off" spellCheck={false} placeholder="type a command..." autoFocus />
          <span className="terminal-cursor" aria-hidden="true">_</span>
        </form>
      </div>
      <div className="terminal-scanlines" aria-hidden="true" />
    </div>
  )
}

export default TerminalWindow
