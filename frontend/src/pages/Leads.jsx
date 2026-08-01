import { useEffect, useState } from 'react'
import { connectGoogleUrl, getGoogleStatus, listLeads, sendLeadNotification, submitLead } from '../api'

function Leads() {
  const [status, setStatus] = useState(null)
  const [leads, setLeads] = useState([])
  const [leadName, setLeadName] = useState('')
  const [companyName, setCompanyName] = useState('')
  const [notes, setNotes] = useState('')
  const [city, setCity] = useState('')
  const [country, setCountry] = useState('')
  const [mobile, setMobile] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [sendingId, setSendingId] = useState(null)
  const [error, setError] = useState(null)
  const [showSetupInfo, setShowSetupInfo] = useState(false)

  useEffect(() => {
    refresh()
  }, [])

  async function refresh() {
    try {
      const current = await getGoogleStatus()
      setStatus(current)
      if (current.connected) {
        setLeads(await listLeads())
      }
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setSubmitting(true)
    setError(null)
    try {
      await submitLead({ lead_name: leadName, company_name: companyName, notes, city, country, mobile })
      setLeadName('')
      setCompanyName('')
      setNotes('')
      setCity('')
      setCountry('')
      setMobile('')
      setLeads(await listLeads())
    } catch (err) {
      setError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  async function handleSend(id) {
    setSendingId(id)
    setError(null)
    try {
      await sendLeadNotification(id)
      setLeads(await listLeads())
    } catch (err) {
      setError(err.message)
    } finally {
      setSendingId(null)
    }
  }

  function handleConnectClick(e) {
    if (!status.oauth_configured) {
      e.preventDefault()
      setShowSetupInfo(true)
    }
  }

  if (!status) return null

  if (!status.connected) {
    return (
      <div>
        <div className="page-header">
          <h1>Lead Router Agent</h1>
          <p>Connect Google so the agent can notify your team by email once a lead has been analyzed.</p>
        </div>
        <div className="panel connect-panel">
          <h2>Connect your Google account</h2>
          <p>You'll be asked for permission to send email on your behalf — nothing else.</p>
          <a className="btn-primary" href={connectGoogleUrl()} onClick={handleConnectClick}>
            Connect Google
          </a>

          {showSetupInfo && (
            <div className="form-error" style={{ textAlign: 'left', marginTop: 20 }}>
              This public demo doesn't have Google OAuth credentials configured, so no email is ever sent from
              here. To run it yourself: grab the code from{' '}
              <a href="https://github.com/naomytcheums-dotcom/lead-router-agent" target="_blank" rel="noreferrer">
                GitHub
              </a>
              , create a free Google Cloud project, enable the Gmail API, generate an OAuth Client ID, and add it
              to your own <code>backend/.env</code> — full steps are in the README.
            </div>
          )}
        </div>
      </div>
    )
  }

  return (
    <div>
      <div className="page-header">
        <h1>New lead</h1>
        <p>Submit an inquiry and the AI will decide if it's relevant, pick who should handle it, and draft a notification.</p>
      </div>

      <div className="panel">
        {error && <div className="form-error">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-row">
            <div className="form-field">
              <label>Lead name</label>
              <input value={leadName} onChange={(e) => setLeadName(e.target.value)} placeholder="e.g. Amjid Ali" required />
            </div>
            <div className="form-field">
              <label>
                Company <span className="hint">optional</span>
              </label>
              <input value={companyName} onChange={(e) => setCompanyName(e.target.value)} placeholder="e.g. Syncbricks LLC" />
            </div>
          </div>

          <div className="form-field">
            <label>Notes / inquiry</label>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Paste the inquiry text — what they're asking about, in their own words."
              required
            />
          </div>

          <div className="form-row">
            <div className="form-field">
              <label>
                City <span className="hint">optional</span>
              </label>
              <input value={city} onChange={(e) => setCity(e.target.value)} />
            </div>
            <div className="form-field">
              <label>
                Country <span className="hint">optional</span>
              </label>
              <input value={country} onChange={(e) => setCountry(e.target.value)} />
            </div>
          </div>

          <div className="form-field">
            <label>
              Mobile <span className="hint">optional</span>
            </label>
            <input value={mobile} onChange={(e) => setMobile(e.target.value)} />
          </div>

          <button className="btn-primary" type="submit" disabled={submitting}>
            {submitting ? 'Analyzing…' : 'Analyze lead'}
          </button>
        </form>
      </div>

      <hr className="section-divider" />

      {leads.length === 0 && <div className="empty-state">No leads yet — submit one above.</div>}

      <div className="leads-list">
        {leads.map((lead) => (
          <div className="lead-row" key={lead.id}>
            <div className="lead-row-top">
              <div>
                <div className="lead-name">
                  {lead.lead_name}
                  {lead.company_name ? ` — ${lead.company_name}` : ''}
                </div>
                <div className="lead-meta">
                  {[lead.city, lead.country].filter(Boolean).join(', ')}
                  {lead.mobile ? ` — ${lead.mobile}` : ''}
                </div>
              </div>
              <span className={`tag ${lead.is_valid ? (lead.status === 'sent' ? 'tag-sent' : lead.status === 'failed' ? 'tag-failed' : 'tag-valid') : 'tag-invalid'}`}>
                {!lead.is_valid ? 'Invalid' : lead.status === 'sent' ? 'Notified' : lead.status === 'failed' ? 'Failed' : 'Ready to notify'}
              </span>
            </div>

            <p className="lead-notes">{lead.notes}</p>

            {!lead.is_valid && lead.invalid_reason && <p className="lead-notes">Why: {lead.invalid_reason}</p>}
            {lead.error_message && <div className="form-error">{lead.error_message}</div>}

            {lead.is_valid && lead.email_body && (
              <div className="email-preview">
                <div className="email-preview-label">Notification draft</div>
                <div className="email-preview-to">To: {lead.recipient_emails}</div>
                <strong>{lead.email_subject}</strong>
                {'\n\n'}
                {lead.email_body}
              </div>
            )}

            {lead.is_valid && lead.status !== 'sent' && (
              <div className="lead-actions">
                <button className="btn-secondary" onClick={() => handleSend(lead.id)} disabled={sendingId === lead.id}>
                  {sendingId === lead.id ? 'Sending…' : 'Send notification'}
                </button>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default Leads
