export default function ClauseHighlight({ clause }) {
  return (
    <li className="clause-item">
      <span className={`clause-type ${clause.type.toLowerCase()}`}>
        {clause.type}
      </span>
      <p className="clause-text">{clause.text}</p>
      <span className="confidence">
        Confidence: {(clause.confidence * 100).toFixed(0)}%
      </span>
    </li>
  )
}
