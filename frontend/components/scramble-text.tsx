'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'

interface ScrambleTextProps {
  text: string
  className?: string
  delay?: number
}

const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#$%^&*()_+=-{}[]<>?'

export function ScrambleText({ text, className = '', delay = 0 }: ScrambleTextProps) {
  const [displayText, setDisplayText] = useState('')
  const [isComplete, setIsComplete] = useState(false)

  useEffect(() => {
    const timeout = setTimeout(() => {
      let iteration = 0
      const interval = setInterval(() => {
        setDisplayText(
          text.split('')
            .map((char, index) => {
              if (index < iteration) {
                return text[index]
              }
              return chars[Math.floor(Math.random() * chars.length)]
            })
            .join('')
        )

        if (iteration >= text.length) {
          clearInterval(interval)
          setIsComplete(true)
        }

        iteration += 1 / 3
      }, 30)

      return () => clearInterval(interval)
    }, delay)

    return () => clearTimeout(timeout)
  }, [text, delay])

  return (
    <motion.span
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className={className}
    >
      {displayText || text}
    </motion.span>
  )
}
