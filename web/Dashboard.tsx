import { useEffect, useState } from 'react';

interface Trace {
  assistant_id: string;
  latency_ms: number;
  cost_usd: number;
  truncated: boolean;
}

export function Dashboard() {
  const [recent, setRecent] = useState<Trace[]>([]);

  useEffect(() => {
    // EventSource is the browser's built-in SSE client — auto-reconnects.
    const es = new EventSource('/metrics/stream');
    es.onmessage = (e) => {
      const trace: Trace = JSON.parse(e.data);
      setRecent((prev) => [trace, ...prev].slice(0, 50));
    };
    return () => es.close();
  }, []);

  const avgLatency =
    recent.reduce((a, t) => a + t.latency_ms, 0) / (recent.length || 1);

  return (
    <div>
      <h2>Live assistant metrics</h2>
      <p>Avg latency (last {recent.length}): {avgLatency.toFixed(0)} ms</p>
      <ul>
        {recent.map((t, i) => (
          <li key={i}>
            {t.assistant_id}: {t.latency_ms.toFixed(0)}ms · ${t.cost_usd.toFixed(4)}
            {t.truncated ? ' truncated' : ''}
          </li>
        ))}
      </ul>
    </div>
  );
}
