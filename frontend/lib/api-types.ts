export type ApiHealth = {
  status: string
  environment: string
  version: string
}

export type Profile = {
  name: string
  headline: string
  secondary_title: string | null
  bio: string
  location: string | null
  email: string | null
  github_url: string | null
  linkedin_url: string | null
  resume_url: string | null
}

export type SkillGroup = {
  category: string
  skills: string[]
}

export type Project = {
  id: string
  title: string
  slug: string
  short_description: string
  description: string
  category: string
  technologies: string[]
  features: string[]
  github_url: string | null
  live_url: string | null
  image_url: string | null
  featured: boolean
  created_at: string
  updated_at: string
}

export type Experience = {
  company: string
  position: string
  location: string | null
  start_date: string
  end_date: string | null
  description: string
  technologies: string[]
  achievements: string[]
}

export type Education = {
  degree: string
  field: string
  institution: string
  location: string | null
  start_date: string | null
  end_date: string | null
  description: string | null
}

export type Certification = {
  name: string
  issuer: string
  issue_date: string | null
  credential_url: string | null
  description: string | null
}

export type SecurityCategory = {
  category: string
  description: string
  focus_areas: string[]
}

export type SecurityTool = {
  name: string
  description: string
  category: string | null
}

export type SecurityOverview = {
  categories: SecurityCategory[]
  tools: SecurityTool[]
}

export type ContactMessageInput = {
  name: string
  email: string
  message: string
}

export type ContactMessageResponse = {
  success: boolean
  message: string
}

export type ApiError = {
  detail?: string
  error?: {
    code?: string
    message?: string
  }
}

export type ApiRequestOptions = Omit<RequestInit, 'body'> & {
  body?: unknown
}
