import { useEffect, useState } from 'react';

interface Quality {
  judged: number;
  hallucination_rate: number;
  avg_correct: number;
  quality_score: number;
}

export function QualityPanel({ assistantId }: { assistantId: string }) {
  const [q, setQ] = useState<Quality | null>(null);

  useEffect(() => {
    // Poll the rolled-up snapshot; the live stream feeds the raw list it reads.
    const tick = () =>
      fetch(`/assistants/${assistantId}/quality`).then((r) => r.json()).then(setQ);
    tick();
    const id = setInterval(tick, 5000);
    return () => clearInterval(id);
  }, [assistantId]);

  if (!q || q.judged === 0) return <p>No quality samples yet.</p>;
  const danger = q.hallucination_rate > 0.1;
  return (
    <div style={{ borderLeft: danger ? '4px solid red' : '4px solid green' }}>
      <h3>Quality · {assistantId}</h3>
      <p>Score: {q.quality_score} (over {q.judged} judged)</p>
      <p>Hallucination: {(q.hallucination_rate * 100).toFixed(1)}%</p>
      <p>Avg correctness: {q.avg_correct}</p>
    </div>
  );
}
