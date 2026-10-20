import type {
  ApiError,
  ApiHealth,
  ApiRequestOptions,
  Certification,
  ContactMessageInput,
  ContactMessageResponse,
  Education,
  Experience,
  Profile,
  Project,
  SecurityOverview,
  SkillGroup,
} from './api-types'

const API_BASE_URL = (process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000/api/v1').replace(/\/$/, '')

export class ApiClientError extends Error {
  status: number
  detail: string

  constructor(status: number, detail: string) {
    super(detail)
    this.name = 'ApiClientError'
    this.status = status
    this.detail = detail
  }
}

async function request<T>(path: string, options: ApiRequestOptions = {}): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      Accept: 'application/json',
      ...(options.body !== undefined ? { 'Content-Type': 'application/json' } : {}),
      ...options.headers,
    },
    body: options.body === undefined ? undefined : JSON.stringify(options.body),
  })

  if (!response.ok) {
    let error: ApiError | undefined
    try {
      error = (await response.json()) as ApiError
    } catch {
      // Keep a useful fallback when FastAPI returns a non-JSON error response.
    }
    throw new ApiClientError(
      response.status,
      error?.error?.message ?? error?.detail ?? `Request failed with status ${response.status}`,
    )
  }

  if (response.status === 204) return undefined as T
  return (await response.json()) as T
}

export const api = {
  health: () => request<ApiHealth>('/health'),
  profile: () => request<Profile>('/profile'),
  skills: () => request<SkillGroup[]>('/skills'),
  projects: () => request<Project[]>('/projects'),
  experience: () => request<Experience[]>('/experience'),
  education: () => request<Education[]>('/education'),
  certifications: () => request<Certification[]>('/certifications'),
  security: () => request<SecurityOverview>('/security'),
  sendContactMessage: (input: ContactMessageInput) =>
    request<ContactMessageResponse>('/contact', {
      method: 'POST',
      body: input,
    }),
}

export { API_BASE_URL }
