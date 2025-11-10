import { useCallback, useEffect, useState } from 'react'
import { THEME_ORDER } from '../constants/themes'

const DEFAULT_THEME = THEME_ORDER[0]

function normalizePath(pathname) {
  if (!pathname) return DEFAULT_THEME
  const clean = pathname.replace(/^\/+/, '').split('/')[0]
  return clean || DEFAULT_THEME
}

function clampTheme(theme) {
  return THEME_ORDER.includes(theme) ? theme : DEFAULT_THEME
}

export default function useThemeRouting() {
  const [theme, setTheme] = useState(() =>
    clampTheme(normalizePath(window.location.pathname))
  )

  useEffect(() => {
    const currentPath = normalizePath(window.location.pathname)
    if (currentPath !== theme) {
      window.history.replaceState({ theme }, '', `/${theme}`)
    }
  }, [theme])

  useEffect(() => {
    const handlePopState = (event) => {
      const nextTheme = clampTheme(
        event.state?.theme || normalizePath(window.location.pathname)
      )
      setTheme(nextTheme)
    }

    window.addEventListener('popstate', handlePopState)
    return () => window.removeEventListener('popstate', handlePopState)
  }, [])

  const navigate = useCallback(
    (nextTheme) => {
      const safeTheme = clampTheme(nextTheme)
      if (safeTheme === theme) return
      window.history.pushState({ theme: safeTheme }, '', `/${safeTheme}`)
      setTheme(safeTheme)
    },
    [theme]
  )

  return { theme, navigate }
}
