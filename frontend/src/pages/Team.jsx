import { useEffect, useState } from 'react'
import { addTeamMember, listTeam, removeTeamMember } from '../api'

function Team() {
  const [members, setMembers] = useState([])
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [responsibility, setResponsibility] = useState('')
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    refresh()
  }, [])

  function refresh() {
    listTeam()
      .then(setMembers)
      .catch((err) => setError(err.message))
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setSaving(true)
    setError(null)
    try {
      await addTeamMember({ name, email, responsibility })
      setName('')
      setEmail('')
      setResponsibility('')
      refresh()
    } catch (err) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  async function handleRemove(id) {
    try {
      await removeTeamMember(id)
      refresh()
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div>
      <div className="page-header">
        <h1>Team directory</h1>
        <p>Who's responsible for what — the AI matches each lead against these descriptions to pick who to notify.</p>
      </div>

      <div className="panel">
        {error && <div className="form-error">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-row">
            <div className="form-field">
              <label>Name</label>
              <input value={name} onChange={(e) => setName(e.target.value)} placeholder="e.g. Alex Rivera" required />
            </div>
            <div className="form-field">
              <label>Email</label>
              <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="alex@company.com" required />
            </div>
          </div>

          <div className="form-field">
            <label>Responsible for</label>
            <input
              value={responsibility}
              onChange={(e) => setResponsibility(e.target.value)}
              placeholder="e.g. workflow automation projects and integrations"
              required
            />
          </div>

          <button className="btn-primary" type="submit" disabled={saving}>
            {saving ? 'Adding…' : 'Add to directory'}
          </button>
        </form>
      </div>

      <hr className="section-divider" />

      {members.length === 0 && <div className="empty-state">No team members yet — add one above.</div>}

      <div className="team-list">
        {members.map((member) => (
          <div className="team-row" key={member.id}>
            <div>
              <div className="team-row-name">
                {member.name} <span className="team-row-email">— {member.email}</span>
              </div>
              <div className="team-row-responsibility">{member.responsibility}</div>
            </div>
            <button className="btn-text" onClick={() => handleRemove(member.id)}>
              Remove
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Team
