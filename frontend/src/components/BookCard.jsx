import './BookCard.css'

function BookCard({ book, rank }) {
  const { title, author, isbn, summary, recommendation_reason } = book

  return (
    <div className="book-card">
      <div className="book-rank">#{rank}</div>

      <div className="book-header">
        <div className="book-icon">📚</div>
        <div className="book-title-section">
          <h3 className="book-title">{title}</h3>
          <p className="book-author">作者：{author}</p>
          {isbn && <p className="book-isbn">ISBN: {isbn}</p>}
        </div>
      </div>

      <div className="book-content">
        <div className="book-section">
          <h4 className="section-title">📖 内容简介</h4>
          <p className="book-summary">{summary}</p>
        </div>

        <div className="book-section">
          <h4 className="section-title">💡 推荐理由</h4>
          <p className="book-reason">{recommendation_reason}</p>
        </div>
      </div>

      <div className="book-footer">
        <button className="btn-primary">我想读这本</button>
        <button className="btn-secondary">了解更多</button>
      </div>
    </div>
  )
}

export default BookCard
