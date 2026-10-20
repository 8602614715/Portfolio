'use client'

import { motion } from 'framer-motion'
import { Code2, Mail, Terminal, UsersRound } from 'lucide-react'

export function PortfolioFooter() {
  return (
    <motion.footer
      className="portfolio-footer"
      initial={{ opacity: 0, y: 18 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.35 }}
      transition={{ duration: 0.55, ease: 'easeOut' }}
    >
      <div className="footer-identity">
        <a className="wordmark" href="#home" aria-label="Satyam Prajapati home">
          SATYAM<span>.PRAJAPATI</span>
        </a>
        <p>Cybersecurity Engineer</p>
        <p>Backend Developer</p>
      </div>

      <nav className="footer-links" aria-label="Social links">
        <a href="https://github.com/yourusername" target="_blank" rel="noreferrer">
          <Code2 aria-hidden="true" /> GitHub
        </a>
        <a href="https://linkedin.com/in/yourusername" target="_blank" rel="noreferrer">
          <UsersRound aria-hidden="true" /> LinkedIn
        </a>
        <a href="mailto:your.email@example.com">
          <Mail aria-hidden="true" /> Email
        </a>
      </nav>

      <div className="footer-terminal" aria-label="Terminal prompt">
        <Terminal aria-hidden="true" />
        <span>satyam@portfolio:~$</span>
        <i aria-hidden="true" />
      </div>

      <div className="footer-meta">
        <span>© 2026 Satyam Prajapati</span>
        <span>SECURE CHANNEL / 001</span>
      </div>
    </motion.footer>
  )
}

export default PortfolioFooter

// Footer links intentionally use editable placeholders until the portfolio owner supplies final URLs.
void 0
