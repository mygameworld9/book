import ThemeSelector from './components/ThemeSelector'
import ThemePage from './pages/ThemePage'
import useThemeRouting from './hooks/useThemeRouting'
import { THEME_CONFIG } from './constants/themes'
import './App.css'

function App() {
  const { theme, navigate } = useThemeRouting()
  const themeInfo = THEME_CONFIG[theme]

  return (
    <div className={`app theme-${theme}`}>
      <header className="app-header">
        <div>
          <p className="eyebrow">LangChain Multi-Agent Playground</p>
          <h1>
            🌌 多主题智能推荐 <span>{themeInfo.label}</span>
          </h1>
          <p className="subtitle">
            四大主题共享一套Agent框架，随时切换书籍、游戏、电影与动漫灵感。
          </p>
        </div>
        <ThemeSelector currentTheme={theme} onSelect={navigate} />
      </header>

      <ThemePage theme={theme} />

      <footer className="app-footer">
        <p>
          🤖 Powered by FastAPI · LangChain · React |{' '}
          <a
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noopener noreferrer"
          >
            查看API文档
          </a>
        </p>
      </footer>
    </div>
  )
}

export default App
