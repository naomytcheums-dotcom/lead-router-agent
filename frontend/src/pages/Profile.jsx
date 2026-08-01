import { useEffect, useState } from 'react'
import { getCompanyProfile, saveCompanyProfile } from '../api'

function Profile() {
  const [companyName, setCompanyName] = useState('')
  const [productsAndServices, setProductsAndServices] = useState('')
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState(null)
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    getCompanyProfile()
      .then((profile) => {
        if (profile) {
          setCompanyName(profile.company_name || '')
          setProductsAndServices(profile.products_and_services || '')
        }
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  async function handleSubmit(e) {
    e.preventDefault()
    setSaving(true)
    setError(null)
    setSaved(false)
    try {
      await saveCompanyProfile({ company_name: companyName, products_and_services: productsAndServices })
      setSaved(true)
    } catch (err) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  if (loading) return null

  return (
    <div>
      <div className="page-header">
        <h1>Company profile</h1>
        <p>The AI reads this to decide whether an inquiry is actually relevant, and to match it with the right product or service.</p>
      </div>

      <div className="panel">
        {error && <div className="form-error">{error}</div>}
        {saved && <div className="form-success">Saved.</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-field">
            <label>Company name</label>
            <input value={companyName} onChange={(e) => setCompanyName(e.target.value)} placeholder="e.g. Northwind Studio" required />
          </div>

          <div className="form-field">
            <label>Products & services</label>
            <textarea
              value={productsAndServices}
              onChange={(e) => setProductsAndServices(e.target.value)}
              placeholder="Describe what your company sells or offers, in enough detail for the AI to tell a real inquiry from an unrelated one — e.g. workflow automation consulting, custom software development, and ongoing support contracts for mid-size businesses."
              required
              style={{ minHeight: 140 }}
            />
          </div>

          <button className="btn-primary" type="submit" disabled={saving}>
            {saving ? 'Saving…' : 'Save'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default Profile
