import { useMemo, useState } from 'react'
import { THEME_CONFIG } from '../constants/themes'
import './ChatInterface.css'

function ChatInterface({ theme, messages, loading, onSend, onReset }) {
  const [input, setInput] = useState('')
  const themeInfo = THEME_CONFIG[theme]
  const examples = useMemo(() => themeInfo.examples ?? [], [themeInfo])

  const handleSubmit = async (event) => {
    event.preventDefault()
    if (!input.trim()) return
    await onSend(input.trim())
    setInput('')
  }

  const handleExample = (text) => {
    setInput(text)
  }

  return (
    <div className="chat-interface">
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <h2>{themeInfo.icon} 欢迎体验{themeInfo.label}推荐</h2>
            <p>{themeInfo.description}</p>
            {examples.length > 0 && (
              <div className="example-prompts">
                <p className="example-label">试试这些提示：</p>
                <div className="example-list">
                  {examples.map((example) => (
                    <button
                      key={example}
                      className="example-btn"
                      type="button"
                      onClick={() => handleExample(example)}
                    >
                      {example}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="message-list">
            {messages.map((msg, index) => (
              <div key={index} className={`message message-${msg.role}`}>
                <div className="message-icon">
                  {msg.role === 'user' ? '👤' : themeInfo.icon}
                </div>
                <div className="message-content">
                  <div className="message-header">
                    {msg.role === 'user' ? '你' : '智能助手'}
                  </div>
                  <div className="message-text">{msg.content}</div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <form className="chat-input-form" onSubmit={handleSubmit}>
        <div className="input-wrapper">
          <textarea
            className="chat-input"
            placeholder={themeInfo.placeholder}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault()
                handleSubmit(e)
              }
            }}
            rows="3"
          />
        </div>
        <div className="input-actions">
          {messages.length > 0 && (
            <button
              type="button"
              className="btn-reset"
              onClick={() => {
                setInput('')
                onReset()
              }}
            >
              🔄 重新开始
            </button>
          )}
          <button
            type="submit"
            className="btn-send"
            disabled={!input.trim() || loading}
          >
            {loading ? '生成中...' : '📤 发送'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default ChatInterface
