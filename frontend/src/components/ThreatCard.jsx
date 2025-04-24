import React from 'react';

const severityStyles = {
  Critical: 'bg-red-100 border-red-500',
  High: 'bg-orange-100 border-orange-500',
  Medium: 'bg-yellow-100 border-yellow-500',
  Low: 'bg-green-100 border-green-500',
  Unknown: 'bg-gray-100 border-gray-500',
};

const ThreatCard = ({ threat }) => {
  const { title, timestamp, analysis } = threat;
  const severityClass = severityStyles[analysis.severity_level] || severityStyles['Unknown'];

  return (
    <div className={`border-l-4 p-4 rounded shadow-md mb-4 ${severityClass}`}>
      <h2 className="text-xl font-semibold text-gray-800">{title}</h2>
      <p className="text-gray-600 text-sm"><strong>Timestamp:</strong> {new Date(timestamp).toLocaleString()}</p>
      
      <div className="mt-2 text-sm text-gray-700 grid grid-cols-1 md:grid-cols-2 gap-2">
        <p><strong>Severity:</strong> {analysis.severity_level}</p>
        <p><strong>Confidence:</strong> {analysis.confidence}</p>
        <p><strong>Summary Impact:</strong> {analysis.summary_impact}</p>
        <p><strong>Historical Context:</strong> {analysis.historical_context}</p>
        <p><strong>Relevance:</strong> {analysis.relevance}</p>
        <p><strong>Potential Actors:</strong> {analysis.potential_threat_actors.join(", ")}</p>
        <p><strong>Recommended Actions:</strong> {analysis.recommended_actions.join(", ")}</p>
        <p><strong>Key IOCs:</strong> {analysis.key_IOCs.join(", ")}</p>
        <p><strong>Affected Sectors:</strong> {analysis.affected_systems_sectors.join(", ")}</p>
        <p><strong>Mitigation Strategies:</strong> {analysis.mitigation_strategies.join(", ")}</p>
        <p><strong>CVE References:</strong> {analysis.cve_references.join(", ")}</p>
        <p><strong>Additional Notes:</strong> {analysis.additional_notes}</p>
      </div>

      <div className="mt-2">
        <a href={analysis.source_url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
          Source: {analysis.source_name}
        </a>
      </div>
    </div>
  );
};

export default ThreatCard;
