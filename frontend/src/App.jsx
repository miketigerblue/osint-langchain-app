
import React, { useEffect, useState } from 'react';
import ThreatCard from './components/ThreatCard';
import { fetchThreats } from './services/api';

function App() {
  const [threats, setThreats] = useState([]);
  const [sortCriteria, setSortCriteria] = useState('severity');

  const severityOrder = { Critical: 4, High: 3, Medium: 2, Low: 1, Unknown: 0 };
  const confidenceOrder = { High: 3, Medium: 2, Low: 1, Unknown: 0 };

  useEffect(() => {
    fetchThreats().then(data => setThreats(data));
  }, []);

  const sortedThreats = [...threats].sort((a, b) => {
    if (sortCriteria === 'confidence') {
      return confidenceOrder[b.analysis.confidence] - confidenceOrder[a.analysis.confidence];
    }
    return severityOrder[b.analysis.severity_level] - severityOrder[a.analysis.severity_level];
  });

  // return <h1 style={{padding: 40}}>👋 If you can read this, React is alive</h1>;

  return (
    <div className="min-h-screen bg-gradient-to-r from-gray-50 to-gray-100 py-10 px-4 md:px-12">
      <header className="text-center mb-10">
        <h1 className="text-4xl font-bold text-gray-900">🌐 Public Cyber Threat Dashboard</h1>
      </header>

      <div className="flex justify-center mb-6">
        <select
          className="p-2 border rounded-lg shadow-sm"
          onChange={(e) => setSortCriteria(e.target.value)}
          value={sortCriteria}
        >
          <option value="severity">Sort by Severity</option>
          <option value="confidence">Sort by Confidence</option>
        </select>
      </div>

      <main className="max-w-5xl mx-auto">
        {sortedThreats.map((threat) => (
          <ThreatCard key={threat.id} threat={threat} />
        ))}
      </main>
    </div>
  );
}

export default App;
