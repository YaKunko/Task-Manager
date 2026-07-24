const BASE_URL = '/api/v1'

function buildQuery(params = {}) {
  const query = new URLSearchParams()
  for (const [key, value] of Object.entries(params)) {
    if (value !== null && value !== undefined && value !== '') {
      query.set(key, value)
    }
  }
  const encoded = query.toString()
  return encoded ? `?${encoded}` : ''
}

function extractErrorMessage(payload, status) {
  if (!payload || payload.detail === undefined) return `Request failed (${status})`
  if (typeof payload.detail === 'string') return payload.detail
  if (Array.isArray(payload.detail)) {
    return payload.detail
      .map((error) => {
        const field = error.loc?.slice(1).join('.') || 'request'
        return `${field}: ${error.msg}`
      })
      .join('; ')
  }
  return `Request failed (${status})`
}

async function request(path, options = {}) {
  let response
  try {
    response = await fetch(`${BASE_URL}${path}`, {
      headers: { 'Content-Type': 'application/json' },
      ...options,
    })
  } catch {
    throw new Error('Network error — is the server running?')
  }
  if (!response.ok) {
    const payload = await response.json().catch(() => null)
    throw new Error(extractErrorMessage(payload, response.status))
  }
  if (response.status === 204) return null
  return response.json()
}

export const tasksApi = {
  list: (params) => request(`/tasks${buildQuery(params)}`),
  get: (id) => request(`/tasks/${id}`),
  create: (data) => request('/tasks', { method: 'POST', body: JSON.stringify(data) }),
  update: (id, data) => request(`/tasks/${id}`, { method: 'PATCH', body: JSON.stringify(data) }),
  remove: (id) => request(`/tasks/${id}`, { method: 'DELETE' }),
}
