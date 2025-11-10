import RecommendationCard from './RecommendationCard'
import UserProfile from './UserProfile'
import { THEME_CONFIG } from '../constants/themes'
import './RecommendationCards.css'

function RecommendationCards({ data }) {
  const { user_profile, recommendations, message, theme } = data
  const themeLabel = THEME_CONFIG[theme]?.label ?? '内容'

  return (
    <section className="recommendations-container">
      <div className="recommendations-header">
        <h2>✨ 为你定制的{themeLabel}推荐</h2>
        <UserProfile profile={user_profile} />
      </div>

      <div className="cards-grid">
        {recommendations.map((item, index) => (
          <RecommendationCard
            key={item.title}
            item={item}
            rank={index + 1}
            theme={theme}
          />
        ))}
      </div>

      <div className="recommendations-message">
        <p>{message}</p>
      </div>
    </section>
  )
}

export default RecommendationCards
