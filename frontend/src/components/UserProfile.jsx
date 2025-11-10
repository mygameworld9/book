import './UserProfile.css'

function formatValue(value) {
  if (Array.isArray(value)) {
    return value.join('、')
  }
  if (value && typeof value === 'object') {
    return Object.entries(value)
      .map(([key, val]) => `${key}:${val}`)
      .join(' | ')
  }
  return value
}

function UserProfile({ profile }) {
  if (!profile) return null
  const entries = Object.entries(profile.attributes || {})

  return (
    <div className="user-profile">
      <h3>👤 用户画像</h3>
      {profile.summary && (
        <p className="profile-summary">{profile.summary}</p>
      )}

      {entries.length > 0 && (
        <div className="profile-tags">
          {entries.map(([key, value]) => (
            <span key={key} className="profile-tag">
              <span className="tag-label">{key}</span>
              <span className="tag-value">{formatValue(value)}</span>
            </span>
          ))}
        </div>
      )}
    </div>
  )
}

export default UserProfile
