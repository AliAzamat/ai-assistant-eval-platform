# Platform on-call runbook

## Health
- Liveness: `GET /health` is 200; Postgres and Redis reachable.
- Watch p95 latency in the dashboard — alert if it crosses your SLO.
- Watch `total_cost_usd` per assistant — alert on a sudden spend spike.
- Watch the quality panel's `hallucination_rate` and `quality_score`.

## Common incidents
- **Dashboard frozen**: the SSE connection dropped at the ALB — confirm idle
  timeouts are long and the target is healthy; EventSource will auto-reconnect.
- **Cost spike**: a prompt change blew up output tokens, or traffic shifted to
  `gpt-4o` — check per-assistant cost and recent promotions.
- **Quality drop**: the quality panel's hallucination_rate climbed — re-run the
  eval suite against the active version; if it regressed, `activate(...)` the prior.
- **Agent amnesia**: ElastiCache eviction or a flush wiped checkpoints — check
  Redis memory policy (agent state must not be evicted).
- **No quality samples**: scoring is sampled at 10% — low traffic means few
  judged answers; raise `SAMPLE_RATE` temporarily to investigate.
