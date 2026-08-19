from app.evals.report import evaluate_version, regressed, Report
from app.db.prompts import activate
from sqlalchemy.orm import Session


async def promote(db: Session, assistant_id: str, version: int,
                  prompt: str, baseline: Report) -> bool:
    """The gate: a candidate version may go live ONLY if it doesn't regress."""
    candidate = await evaluate_version(f"v{version}", prompt)
    if regressed(baseline, candidate):
        print(f"BLOCKED v{version}: correct={candidate.avg_correct:.2f} "
              f"halluc={candidate.hallucination_rate:.2f} (baseline not beaten)")
        return False
    activate(db, assistant_id, version)
    print(f"PROMOTED v{version} to active")
    return True
