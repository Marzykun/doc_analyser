function titleCase(value) {
  return value.charAt(0).toUpperCase() + value.slice(1)
}

export default function ResultsDisplay({ data }) {
  if (!data) return null

  const clauseTypes = ['termination', 'payment', 'liability']
  const entities = Array.isArray(data.entities) ? data.entities : []
  const risks = Array.isArray(data.risks) ? data.risks : []
  const ai = data.ai_analysis || {}

  return (
    <div className="results-container">
      <div className="results-grid">
        <section className="result-section">
          <h3>Detected Clauses</h3>
          {clauseTypes.map((type) => (
            <div key={type} style={{ marginBottom: '14px' }}>
              <h4>{titleCase(type)}</h4>
              {data.clauses?.[type]?.length ? (
                <ul className="clause-list">
                  {data.clauses[type].map((item, idx) => (
                    <li key={`${type}-${idx}`} className="clause-item">
                      <p className="clause-text">{item.sentence}</p>
                      <span className="confidence">
                        Keywords: {(item.matched_keywords || []).join(', ')}
                      </span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="confidence">No {type} clause detected</p>
              )}
            </div>
          ))}
        </section>

        <section className="result-section">
          <h3>Extracted Entities</h3>
          {entities.length ? (
            <ul className="clause-list">
              {entities.map((entity, idx) => (
                <li key={idx} className="clause-item">
                  <span className="clause-type">{entity.label}</span>
                  <p className="clause-text">{entity.text}</p>
                </li>
              ))}
            </ul>
          ) : (
            <p className="confidence">No entities extracted</p>
          )}
        </section>
      </div>

      <section className="result-section" style={{ marginBottom: '20px' }}>
        <h3>Detected Risks</h3>
        {risks.length ? (
          <ul>
            {risks.map((risk, idx) => (
              <li key={idx}>{risk}</li>
            ))}
          </ul>
        ) : (
          <p className="confidence">No rule-based risks detected</p>
        )}
      </section>

      <section className="result-section">
        <h3>Gemini Analysis</h3>
        {ai.error ? (
          <p className="error">{ai.details || ai.error}</p>
        ) : (
          <>
            {ai.summary && <p style={{ marginBottom: '12px' }}>{ai.summary}</p>}

            <h4>AI Risks</h4>
            {Array.isArray(ai.risks) && ai.risks.length ? (
              <ul>
                {ai.risks.map((risk, idx) => (
                  <li key={idx}>{risk}</li>
                ))}
              </ul>
            ) : (
              <p className="confidence">No AI risks returned</p>
            )}

            <h4 style={{ marginTop: '12px' }}>Clause Explanations</h4>
            {Array.isArray(ai.clauses_explained) && ai.clauses_explained.length ? (
              <ul className="clause-list">
                {ai.clauses_explained.map((item, idx) => (
                  <li key={idx} className="clause-item">
                    <span className="clause-type">{item.clause}</span>
                    <p className="clause-text">{item.explanation}</p>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="confidence">No clause explanation returned</p>
            )}
          </>
        )}
      </section>
    </div>
  )
}
