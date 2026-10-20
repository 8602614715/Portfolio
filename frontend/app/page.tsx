'use client'

import { useEffect, useState } from 'react'
import { ArrowDownRight, Code2, Download, ExternalLink, GitBranch, Mail, Moon, Send, ShieldCheck, Sun, Terminal, UsersRound } from 'lucide-react'
import { BootSequence } from '@/components/boot-sequence'
import { SystemStatus } from '@/components/system-status'
import { TerminalWindow } from '@/components/terminal-window'
import { PortfolioFooter } from '@/components/portfolio-footer'
import { api, ApiClientError } from '@/lib/api'
import type { Certification, Education, Experience, Profile, Project, SecurityOverview, SkillGroup } from '@/lib/api-types'

// Replace the sample values below with your real stack, projects, experience, and contact details.
const technologies = ['FastAPI', 'React', 'PostgreSQL', 'Linux', 'Nmap', 'Burp Suite']
const tools = ['Nmap', 'Burp Suite', 'Wireshark', 'Hydra', 'Hashcat', 'VirusTotal']
const skillGroups = [
  { label: 'PROGRAMMING', code: '01', items: ['Python', 'JavaScript', 'TypeScript', 'SQL'] },
  { label: 'BACKEND', code: '02', items: ['FastAPI', 'REST APIs', 'SQLAlchemy', 'PostgreSQL', 'JWT'] },
  { label: 'FRONTEND', code: '03', items: ['React', 'Tailwind CSS'] },
  { label: 'CYBERSECURITY', code: '04', items: ['Linux', 'Nmap', 'Burp Suite', 'OWASP', 'VirusTotal API', 'Web Security'] },
  { label: 'NETWORKING', code: '05', items: ['TCP/IP', 'DNS', 'HTTP/HTTPS', 'DHCP', 'NAT', 'CCNA Fundamentals'] },
]
const projects = [
  { title: 'CYBER FRAUD DETECTION SYSTEM', slug: 'fraud-detection', description: 'A security analysis platform for identifying potentially malicious files, URLs, domains, IP addresses and email indicators.', tech: ['FastAPI', 'React', 'PostgreSQL', 'VirusTotal API'], features: ['File scanning', 'URL scanning', 'Domain scanning', 'IP scanning'], metric: '04 SCAN VECTORS', command: 'scan --target suspicious.url', primary: true },
  { title: 'HEALTHCARE AUTOMATION SYSTEM', slug: 'healthcare-automation', description: 'Workflow automation patterns for safer, faster operational systems in healthcare environments.', tech: ['Python', 'APIs', 'PostgreSQL'], features: ['Process automation', 'Data workflows'], metric: '02 CORE FLOWS', command: 'automate --workflow intake', primary: false },
  { title: 'NETWORK SECURITY LAB', slug: 'network-security-lab', description: 'A practical lab for testing network visibility, reconnaissance and defensive controls.', tech: ['Linux', 'Nmap', 'Wireshark'], features: ['Reconnaissance', 'Security testing'], metric: '03 LAB MODULES', command: 'nmap --profile defensive', primary: false },
]
const experiences = [
  { role: 'CYBERSECURITY & BACKEND ENGINEER', org: 'Independent / Project Work', duration: '2023 — PRESENT', description: 'Designing secure APIs and security-focused applications with an emphasis on clear threat surfaces and resilient infrastructure.', tech: 'FastAPI · React · PostgreSQL · Linux', achievement: 'Built full-stack security analysis workflows.' },
  { role: 'INFORMATION TECHNOLOGY ENGINEER', org: 'SGSITS INDORE', duration: '2021 — 2025', description: 'Developed a broad foundation across programming, networks, operating systems and application security.', tech: 'Python · Networking · SQL · Web security', achievement: 'Combined engineering fundamentals with hands-on security labs.' },
]
const certifications = [
  { name: 'THE COMPLETE ETHICAL HACKING COURSE', issuer: 'Udemy', date: '2024', link: '#' },
  { name: 'NETWORK SECURITY FUNDAMENTALS', issuer: 'Independent Study', date: '2024', link: '#' },
]

const fallbackProfile: Profile = {
  name: 'Satyam Prajapati',
  headline: 'Cybersecurity Engineer',
  secondary_title: 'Backend Developer',
  bio: 'Building secure systems, APIs and impactful applications.',
  location: 'India',
  email: 'your.email@example.com',
  github_url: 'https://github.com/yourusername',
  linkedin_url: 'https://linkedin.com/in/yourusername',
  resume_url: null,
}

const categoryLabels: Record<string, string> = {
  programming: 'PROGRAMMING',
  backend: 'BACKEND',
  frontend: 'FRONTEND',
  cybersecurity: 'CYBERSECURITY',
  networking: 'NETWORKING',
  database: 'DATABASE',
  tools: 'TOOLS',
}

function formatDate(value: string | null) {
  if (!value) return 'PRESENT'
  return new Intl.DateTimeFormat('en', { month: 'short', year: 'numeric' }).format(new Date(value))
}

export default function Page() {
  const [isDark, setIsDark] = useState(true)
  const [sent, setSent] = useState(false)
  const [sending, setSending] = useState(false)
  const [contactError, setContactError] = useState('')
  const [profile, setProfile] = useState<Profile | null>(null)
  const [skillGroupsData, setSkillGroupsData] = useState<SkillGroup[] | null>(null)
  const [projectsData, setProjectsData] = useState<Project[] | null>(null)
  const [experiencesData, setExperiencesData] = useState<Experience[] | null>(null)
  const [educationData, setEducationData] = useState<Education[] | null>(null)
  const [certificationsData, setCertificationsData] = useState<Certification[] | null>(null)
  const [securityData, setSecurityData] = useState<SecurityOverview | null>(null)

  useEffect(() => {
    let mounted = true
    Promise.allSettled([
      api.profile(),
      api.skills(),
      api.projects(),
      api.experience(),
      api.education(),
      api.certifications(),
      api.security(),
    ]).then((results) => {
      if (!mounted) return
      const [profileResult, skillsResult, projectsResult, experienceResult, educationResult, certificationsResult, securityResult] = results
      if (profileResult.status === 'fulfilled') setProfile(profileResult.value)
      if (skillsResult.status === 'fulfilled') setSkillGroupsData(skillsResult.value)
      if (projectsResult.status === 'fulfilled') setProjectsData(projectsResult.value)
      if (experienceResult.status === 'fulfilled') setExperiencesData(experienceResult.value)
      if (educationResult.status === 'fulfilled') setEducationData(educationResult.value)
      if (certificationsResult.status === 'fulfilled') setCertificationsData(certificationsResult.value)
      if (securityResult.status === 'fulfilled') setSecurityData(securityResult.value)
    })

    return () => { mounted = false }
  }, [])

  const activeProfile = profile ?? fallbackProfile
  const visibleSkillGroups = skillGroupsData?.map((group, index) => ({
    label: categoryLabels[group.category] ?? group.category.toUpperCase(),
    code: String(index + 1).padStart(2, '0'),
    items: group.skills,
  })) ?? skillGroups
  const visibleProjects = projectsData?.map((project) => ({
    title: project.title.toUpperCase(),
    slug: project.slug,
    description: project.description,
    tech: project.technologies,
    features: project.features,
    metric: `${String(project.features.length).padStart(2, '0')} FEATURES`,
    command: `inspect --project ${project.slug}`,
    primary: project.featured,
    githubUrl: project.github_url,
    liveUrl: project.live_url,
  })) ?? projects.map((project) => ({ ...project, githubUrl: 'https://github.com', liveUrl: null }))
  const visibleExperiences = experiencesData?.map((experience) => ({
    role: experience.position.toUpperCase(),
    org: experience.company,
    duration: `${formatDate(experience.start_date)} — ${formatDate(experience.end_date)}`,
    description: experience.description,
    tech: experience.technologies.join(' · '),
    achievement: experience.achievements[0] ?? 'Delivered reliable engineering work.',
  })) ?? experiences
  const visibleTools = securityData?.tools.map((tool) => tool.name) ?? tools
  const visibleSecurityCategories = securityData?.categories.map((category) => category.category) ?? ['Web Security', 'Network Security', 'Linux', 'API Security', 'Reconnaissance', 'Security Testing']
  const visibleEducation = educationData?.[0]
  const visibleCertifications = certificationsData?.map((cert) => ({
    name: cert.name,
    issuer: cert.issuer,
    date: cert.issue_date ? formatDate(cert.issue_date) : 'DATE UNAVAILABLE',
    link: cert.credential_url ?? '#',
  })) ?? certifications

  async function handleContactSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setSending(true)
    setContactError('')
    const form = event.currentTarget
    const formData = new FormData(form)
    try {
      await api.sendContactMessage({
        name: String(formData.get('name') ?? ''),
        email: String(formData.get('email') ?? ''),
        message: String(formData.get('message') ?? ''),
      })
      setSent(true)
      form.reset()
    } catch (error) {
      setContactError(error instanceof ApiClientError ? error.detail : 'Unable to send the message. Please try again.')
    } finally {
      setSending(false)
    }
  }

  return (
    <>
      <BootSequence />
      <main className={isDark ? 'portfolio-shell' : 'portfolio-shell light-shell'}>
        <div className="ambient-background" aria-hidden="true"><div className="ambient-grid" /><div className="network-lines" /><div className="atmospheric-glow atmospheric-glow-cyan" /><div className="atmospheric-glow atmospheric-glow-lime" /><div className="ambient-particles" /><div className="ambient-scanlines" /><span className="hud-corner hud-corner-top">SYS.NEWS // 04.17.26</span><span className="hud-corner hud-corner-bottom">SECURE CHANNEL / 001</span><span className="coordinate coordinate-one">28.6139° N / 77.2090° E</span><span className="coordinate coordinate-two">NODE_07 :: 0x4F2A</span></div>
        <div className="portfolio-inner">
          <header className="site-header"><a className="wordmark" href="#home" aria-label={`${activeProfile.name} home`}>{activeProfile.name.split(' ')[0].toUpperCase()}<span className="text-accent-lime">.{activeProfile.name.split(' ').slice(1).join('.').toUpperCase()}</span></a><nav className="desktop-nav" aria-label="Primary navigation">{['HOME', 'ABOUT', 'PROJECTS', 'SECURITY', 'EXPERIENCE', 'CONTACT'].map((item) => <a key={item} href={`#${item.toLowerCase()}`} className={item === 'HOME' ? 'active' : ''}>{item}</a>)}</nav><div className="header-actions"><a href={activeProfile.github_url ?? '#'} target="_blank" rel="noreferrer" aria-label="GitHub"><Code2 /></a><a href={activeProfile.linkedin_url ?? '#'} target="_blank" rel="noreferrer" aria-label="LinkedIn"><UsersRound /></a><button className="theme-toggle" onClick={() => setIsDark((value) => !value)} aria-label="Toggle theme">{isDark ? <Sun /> : <Moon />}</button><span className="status-indicator"><i /> AVAILABLE</span></div></header>
          <section id="home" className="hero-section reveal-section"><div className="hero-copy"><p className="eyebrow"><span>// 001</span> DIGITAL DEFENSE / SYSTEMS ENGINEERING</p><div className="hero-identity"><img className="hero-portrait" src="/profile-photo.jpg" alt={`${activeProfile.name} profile`} /><h1 data-text={activeProfile.name.toUpperCase()}>{activeProfile.name.split(' ')[0].toUpperCase()}<br /><em>{activeProfile.name.split(' ').slice(1).join(' ').toUpperCase()}</em></h1></div><div className="hero-role"><span>{activeProfile.headline.toUpperCase()}</span><b>/</b><span>{(activeProfile.secondary_title ?? 'SECURE SYSTEMS').toUpperCase()}</span></div><p className="hero-description">{activeProfile.bio}</p><div className="hero-actions"><a href="#terminal" className="button button-primary"><Terminal /> ENTER TERMINAL <ArrowDownRight /></a><a href="#projects" className="button button-ghost">VIEW PROJECTS <ArrowDownRight /></a></div></div><div className="hero-terminal-stack"><TerminalWindow /><SystemStatus /></div></section>
          <section className="tech-strip reveal-section reveal-delay-1" aria-label="Technologies"><span className="strip-label">// CORE TOOLKIT</span><div className="tech-list">{technologies.map((tech, index) => <span key={tech}><b>0{index + 1}</b>{tech}</span>)}</div></section>
          <section id="about" className="content-section about-section reveal-section reveal-delay-1"><SectionHeading kicker="ABOUT / 002" title="$ about" index="[PROFILE_01]" /><div className="about-grid"><div className="about-intro"><p>Satyam Prajapati is an Information Technology engineer focused on cybersecurity, backend development, networking and secure application development.</p><p className="muted">I work at the intersection of offensive thinking and thoughtful engineering — turning complex security problems into calm, resilient products.</p></div><div className="about-details"><div><span>AREAS OF INTEREST</span><strong>Application security<br />API architecture<br />Automation & infrastructure</strong></div><div><span>CAREER FOCUS</span><strong>Secure systems<br />Resilient backend services<br />Practical defense</strong></div></div><div className="about-terminal" aria-label="Terminal profile information"><span className="terminal-prompt">satyam@portfolio:~$ whoami</span><b>security-minded engineer</b><span>mode: building / learning / hardening</span><span>location: india // status: online</span></div></div></section>
          <section id="skills" className="content-section skills-section reveal-section reveal-delay-2"><SectionHeading kicker="CAPABILITIES / 003" title="$ skills" index="[LOADOUT_05]" /><div className="skills-grid">{visibleSkillGroups.map((group, index) => <article className="skill-row" key={group.label}><div className="skill-row-index">0{index + 1}</div><div className="skill-row-main"><div className="skill-row-heading"><span>{group.code}</span><h3>{group.label}</h3><i aria-hidden="true">●</i></div><ul>{group.items.map((skill) => <li key={skill}><span aria-hidden="true">›</span>{skill}</li>)}</ul></div><div className="skill-row-signal" aria-hidden="true"><span /><span /><span /><span /></div></article>)}</div></section>
          <section id="projects" className="content-section projects-section reveal-section reveal-delay-2"><SectionHeading kicker="SELECTED WORK / 004" title="$ projects" index="[BUILD_LOG]" /><div className="projects-grid">{visibleProjects.map((project, index) => <article className={`project-card ${project.primary ? 'project-primary' : ''}`} key={project.title}><div className="project-card-top"><span className="project-number">{String(index + 1).padStart(2, '0')}</span><span className="project-state"><i /> {project.primary ? 'ACTIVE / FLAGSHIP' : 'ARCHIVED / LAB'}</span></div><div className="project-card-heading"><span className="project-kind">CASE FILE / {project.slug}</span><span className="project-metric">{project.metric}</span></div><h3>{project.title}</h3><p>{project.description}</p><div className="project-features">{project.features.map((feature) => <span key={feature}>+ {feature}</span>)}</div><div className="project-command"><span>$</span> {project.command}<b>_</b></div><div className="project-tech">{project.tech.map((item) => <span key={item}>{item}</span>)}</div><div className="project-actions"><a href={project.liveUrl ?? '#contact'} className="button button-primary">VIEW PROJECT <ExternalLink /></a><a href={project.githubUrl ?? '#'} target="_blank" rel="noreferrer" className="button button-ghost"><GitBranch /> GITHUB</a></div></article>)}</div></section>
          <section id="security" className="content-section security-section reveal-section reveal-delay-3"><SectionHeading kicker="DEFENSE PROFILE / 005" title="$ security" index="[THREAT_MODEL]" /><div className="security-layout"><div className="security-skills">{visibleSecurityCategories.map((skill, index) => <div className="security-skill" key={skill}><div><span>{skill}</span><small>CAPABILITY 0{index + 1}</small></div><div className="skill-meter" aria-label={`${skill} capability indicator`}><i style={{ width: `${62 + index * 5}%` }} /></div></div>)}</div><div className="tools-panel"><div className="tools-heading"><ShieldCheck /> TOOLKIT / VERIFIED IN PRACTICE</div><div className="tools-list">{visibleTools.map((tool) => <span key={tool}>{tool}</span>)}</div><p>Indicators show areas of working focus, not numeric scores.</p></div></div></section>
          <section id="experience" className="content-section experience-section reveal-section reveal-delay-3"><SectionHeading kicker="FIELD LOG / 006" title="$ experience" index="[TIMELINE]" /><div className="timeline">{visibleExperiences.map((experience) => <article className="timeline-item" key={experience.role}><div className="timeline-marker">●</div><div className="timeline-content"><div className="timeline-meta"><span>{experience.duration}</span><span>{experience.org}</span></div><h3>{experience.role}</h3><p>{experience.description}</p><span className="timeline-tech">{experience.tech}</span><strong>+ {experience.achievement}</strong></div></article>)}</div></section>
          <div className="info-grid"><section id="education" className="content-section education-section"><SectionHeading kicker="FOUNDATION / 007" title="$ education" index="[ORIGIN]" /><article className="education-card"><span className="card-code">01 / ACADEMIC RECORD</span><h3>{visibleEducation ? `${visibleEducation.degree} — ${visibleEducation.field}` : 'B.Tech — Information Technology'}</h3><p>{visibleEducation?.institution ?? 'SGSITS Indore'}</p><div className="education-tags"><span>{visibleEducation?.location ?? 'Networks'}</span><span>{visibleEducation?.start_date ? formatDate(visibleEducation.start_date) : 'Systems'}</span><span>{visibleEducation?.end_date ? formatDate(visibleEducation.end_date) : 'Application Security'}</span></div></article></section><section id="certs" className="content-section certs-section"><SectionHeading kicker="CREDENTIALS / 008" title="$ certs" index="[VALIDATED]" /><div className="cert-list">{visibleCertifications.map((cert) => <article className="cert-card" key={cert.name}><ShieldCheck /><div><h3>{cert.name}</h3><p>{cert.issuer} <span>/</span> {cert.date}</p></div><a href={cert.link} aria-label={`View ${cert.name} credential`}><ExternalLink /></a></article>)}</div></section></div>
          <section id="resume" className="resume-section"><div className="resume-terminal"><div className="resume-top"><Terminal /><span>RESUME.EXE</span><span>READY</span></div><div className="resume-output"><span className="terminal-prompt">satyam@portfolio:~$ resume</span><strong>Resume found.</strong><span>Last updated: 2026. Available for secure collaboration.</span></div><div className="resume-actions"><a className="button button-primary" href="/resume.pdf"><Download /> VIEW RESUME</a><a className="button button-ghost" href="/resume.pdf">DOWNLOAD PDF <ArrowDownRight /></a></div></div></section>
           <section id="contact" className="contact-section reveal-section reveal-delay-2"><div className="contact-copy"><p className="section-kicker">OPEN CHANNEL / 009</p><h2>Build something<br /><em>secure.</em></h2><div className="contact-links"><a href={activeProfile.email ? `mailto:${activeProfile.email}` : '#'}><Mail /> {activeProfile.email ?? 'Email unavailable'}</a><a href={activeProfile.github_url ?? '#'} target="_blank" rel="noreferrer"><GitBranch /> {activeProfile.github_url ?? 'GitHub unavailable'}</a><a href={activeProfile.linkedin_url ?? '#'} target="_blank" rel="noreferrer"><UsersRound /> {activeProfile.linkedin_url ?? 'LinkedIn unavailable'}</a></div></div><form className="contact-form" onSubmit={handleContactSubmit}><label>Name<input required name="name" placeholder="Your name" /></label><label>Email<input required type="email" name="email" placeholder="you@example.com" /></label><label>Message<textarea required name="message" rows={4} placeholder="Tell me about the system you are building..." /></label><button className="button button-primary" type="submit" disabled={sending}><Send /> {sending ? 'TRANSMITTING...' : sent ? 'MESSAGE SENT' : 'SEND MESSAGE'}</button>{sent && <p className="form-success" role="status">Message received. I&apos;ll get back to you soon.</p>}{contactError && <p className="form-error" role="alert">{contactError}</p>}</form></section>
          <PortfolioFooter />
        </div>
      </main>
    </>
  )
}

function SectionHeading({ kicker, title, index }: { kicker: string; title: string; index: string }) { return <div className="section-heading-row"><div><p className="section-kicker">{kicker}</p><h2>{title}</h2></div><span className="section-index">{index}</span></div> }
