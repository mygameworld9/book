import './RecommendationCard.css'

function RecommendationCard({ item, rank, theme }) {
  const { title, creator, metadata = {}, summary, reason } = item
  const metadataEntries = Object.entries(metadata)

  return (
    <article className={`recommendation-card theme-${theme}`}>
      <div className="card-rank">#{rank}</div>

      <header className="card-header">
        <div className="card-title-group">
          <h3>{title}</h3>
          <p className="card-creator">由 {creator}</p>
          {metadataEntries.length > 0 && (
            <div className="card-metadata">
              {metadataEntries.map(([key, value]) => (
                <span key={key} className="metadata-pill">
                  <span className="metadata-key">{key}</span>
                  <span className="metadata-value">{value}</span>
                </span>
              ))}
            </div>
          )}
        </div>
      </header>

      <section className="card-section">
        <h4>📖 精髓摘要</h4>
        <p>{summary}</p>
      </section>

      <section className="card-section">
        <h4>💡 推荐理由</h4>
        <p>{reason}</p>
      </section>
    </article>
  )
}

export default RecommendationCard
