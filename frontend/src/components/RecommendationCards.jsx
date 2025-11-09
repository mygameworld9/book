import BookCard from './BookCard'
import UserProfile from './UserProfile'
import './RecommendationCards.css'

function RecommendationCards({ recommendations }) {
  const { user_profile, recommended_books, message } = recommendations

  return (
    <div className="recommendations-container">
      <div className="recommendations-header">
        <h2>📖 为您精选的推荐</h2>
        <UserProfile profile={user_profile} />
      </div>

      <div className="books-grid">
        {recommended_books.map((book, index) => (
          <BookCard key={index} book={book} rank={index + 1} />
        ))}
      </div>

      <div className="recommendations-message">
        <p>{message}</p>
      </div>
    </div>
  )
}

export default RecommendationCards
