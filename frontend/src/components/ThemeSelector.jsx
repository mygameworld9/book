import { THEME_CONFIG, THEME_ORDER } from '../constants/themes'
import './ThemeSelector.css'

function ThemeSelector({ currentTheme, onSelect }) {
  return (
    <nav className="theme-selector">
      {THEME_ORDER.map((theme) => {
        const info = THEME_CONFIG[theme]
        const active = currentTheme === theme
        return (
          <button
            key={theme}
            type="button"
            className={`theme-pill ${active ? 'active' : ''}`}
            onClick={() => onSelect(theme)}
            aria-pressed={active}
          >
            <span className="theme-icon">{info.icon}</span>
            <span className="theme-label">{info.label}</span>
          </button>
        )
      })}
    </nav>
  )
}

export default ThemeSelector
