import { useState } from 'react'
import ChatInterface from './components/ChatInterface'
import RecommendationCards from './components/RecommendationCards'
import './App.css'

function App() {
  const [recommendations, setRecommendations] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleRecommendation = (data) => {
    setRecommendations(data)
    setError(null)
  }

  const handleError = (err) => {
    setError(err)
    setRecommendations(null)
  }

  const handleLoading = (isLoading) => {
    setLoading(isLoading)
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>📚 AI图书推荐系统</h1>
        <p className="subtitle">基于多Agent协作的智能推荐</p>
      </header>

      <main className="app-main">
        <ChatInterface
          onRecommendation={handleRecommendation}
          onError={handleError}
          onLoading={handleLoading}
        />

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>AI正在为您精心挑选书籍...</p>
          </div>
        )}

        {error && (
          <div className="error">
            <h3>⚠️ 出错了</h3>
            <p>{error}</p>
          </div>
        )}

        {recommendations && !loading && (
          <RecommendationCards recommendations={recommendations} />
        )}
      </main>

      <footer className="app-footer">
        <p>
          🤖 Powered by LangChain Multi-Agent System |{' '}
          <a
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noopener noreferrer"
          >
            API文档
          </a>
        </p>
      </footer>
    </div>
  )
}

export default App
