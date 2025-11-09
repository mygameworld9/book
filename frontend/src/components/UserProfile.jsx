import './UserProfile.css'

function UserProfile({ profile }) {
  const { genre, style, mood, previous_books, reading_goal } = profile

  return (
    <div className="user-profile">
      <h3>👤 您的阅读画像</h3>
      <div className="profile-tags">
        <span className="profile-tag tag-genre">
          <span className="tag-icon">📚</span>
          <span className="tag-label">类型</span>
          <span className="tag-value">{genre}</span>
        </span>

        <span className="profile-tag tag-style">
          <span className="tag-icon">✨</span>
          <span className="tag-label">风格</span>
          <span className="tag-value">{style}</span>
        </span>

        <span className="profile-tag tag-mood">
          <span className="tag-icon">💭</span>
          <span className="tag-label">心情</span>
          <span className="tag-value">{mood}</span>
        </span>

        <span className="profile-tag tag-goal">
          <span className="tag-icon">🎯</span>
          <span className="tag-label">目标</span>
          <span className="tag-value">{reading_goal}</span>
        </span>
      </div>

      {previous_books && previous_books.length > 0 && (
        <div className="previous-books">
          <span className="books-label">📖 已读书籍：</span>
          <span className="books-list">{previous_books.join(', ')}</span>
        </div>
      )}
    </div>
  )
}

export default UserProfile
