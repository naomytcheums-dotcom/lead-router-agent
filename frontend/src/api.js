export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8070'

async function handle(res) {
  if (!res.ok) {
    let message = 'Something went wrong.'
    try {
      const data = await res.json()
      message = data.detail || message
    } catch {
      // ignore
    }
    throw new Error(message)
  }
  return res.json()
}

export function connectGoogleUrl() {
  return `${API_URL}/api/google/connect`
}

export async function getGoogleStatus() {
  const res = await fetch(`${API_URL}/api/google/status`)
  return handle(res)
}

export async function getCompanyProfile() {
  const res = await fetch(`${API_URL}/api/company-profile`)
  return handle(res)
}

export async function saveCompanyProfile(profile) {
  const res = await fetch(`${API_URL}/api/company-profile`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(profile),
  })
  return handle(res)
}

export async function listTeam() {
  const res = await fetch(`${API_URL}/api/team`)
  return handle(res)
}

export async function addTeamMember(member) {
  const res = await fetch(`${API_URL}/api/team`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(member),
  })
  return handle(res)
}

export async function removeTeamMember(id) {
  const res = await fetch(`${API_URL}/api/team/${id}`, { method: 'DELETE' })
  return handle(res)
}

export async function listLeads() {
  const res = await fetch(`${API_URL}/api/leads`)
  return handle(res)
}

export async function submitLead(lead) {
  const res = await fetch(`${API_URL}/api/leads`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(lead),
  })
  return handle(res)
}

export async function sendLeadNotification(id) {
  const res = await fetch(`${API_URL}/api/leads/${id}/send`, { method: 'POST' })
  return handle(res)
}
