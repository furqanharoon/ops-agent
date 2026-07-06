import json
import uuid
from fastapi import APIRouter, BackgroundTasks, HTTPException
from agent.runtime import run_agent_execution_debug
from agent.services.facts_extractor import build_investigation_facts
from agent.services.analyzer import analyze_incident
from agent.services.report_generator import generate_report
from agent.services.approval import requires_human_approval
from evals.scoring import compare_facts

router = APIRouter()

# In-memory store: job_id -> {"status": "running"|"done"|"error", "result": ...}
_jobs: dict[str, dict] = {}


async def _run_evals_job(job_id: str):
    try:
        with open("evals/investigations.json") as f:
            test_cases = json.load(f)

        results = []
        total = len(test_cases)
        passed_count = 0

        for test_case in test_cases:
            response = await run_agent_execution_debug(test_case["query"])
            test_passed = False
            comparison = {}

            if response:
                facts = build_investigation_facts(
                    response["incident"],
                    response["duration"],
                    response["timeline"]
                )

                if facts.case_id:
                    analyzer = analyze_incident(facts)
                    if not requires_human_approval(analyzer):
                        generate_report(facts, analyzer)

                comparison = compare_facts(test_case.get("expected"), facts)
                test_passed = all(r["passed"] for r in comparison.values())
                if test_passed:
                    passed_count += 1

            results.append({
                "id": test_case["id"],
                "name": test_case["name"],
                "query": test_case["query"],
                "passed": test_passed,
                "comparison": comparison
            })

        pass_rate = round((passed_count / total) * 100, 1) if total > 0 else 0

        _jobs[job_id] = {
            "status": "done",
            "result": {
                "total": total,
                "passed": passed_count,
                "pass_rate": pass_rate,
                "results": results
            }
        }
    except Exception as e:
        _jobs[job_id] = {"status": "error", "result": str(e)}


@router.post("/evals/run")
async def run_evals(background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    _jobs[job_id] = {"status": "running", "result": None}
    background_tasks.add_task(_run_evals_job, job_id)
    return {"job_id": job_id}


@router.get("/evals/result/{job_id}")
async def get_eval_result(job_id: str):
    job = _jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
