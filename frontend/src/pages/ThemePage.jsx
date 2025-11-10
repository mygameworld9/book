import RecommendationCards from '../components/RecommendationCards'
import ChatInterface from '../components/ChatInterface'
import useRecommendation from '../hooks/useRecommendation'
import { THEME_CONFIG } from '../constants/themes'
import './ThemePage.css'

function ThemePage({ theme }) {
  const {
    messages,
    recommendations,
    loading,
    error,
    sendMessage,
    resetSession,
  } = useRecommendation(theme)

  const themeInfo = THEME_CONFIG[theme]

  return (
    <main className={`theme-page theme-${theme}`}>
      <div className="theme-preview">
        <div className="theme-icon">{themeInfo.icon}</div>
        <div>
          <h2>{themeInfo.label}多主题推荐</h2>
          <p>{themeInfo.description}</p>
        </div>
      </div>

      <ChatInterface
        theme={theme}
        messages={messages}
        loading={loading}
        onSend={sendMessage}
        onReset={resetSession}
      />

      {loading && (
        <div className="loading">
          <div className="spinner" />
          <p>AI正在根据您的画像挑选最佳{themeInfo.label}...</p>
        </div>
      )}

      {error && (
        <div className="error">
          <h3>⚠️ 出错了</h3>
          <p>{error}</p>
        </div>
      )}

      {recommendations && !loading && (
        <RecommendationCards data={recommendations} />
      )}
    </main>
  )
}

export default ThemePage
