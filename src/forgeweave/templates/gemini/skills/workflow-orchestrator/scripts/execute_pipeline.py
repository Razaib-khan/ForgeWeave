"""Execute a multi-step pipeline from a pipeline definition."""

import argparse
import json
import sys
from pathlib import Path


def validate_pipeline(pipeline: dict) -> list[str]:
    errors = []
    steps = pipeline.get("steps", [])
    if not steps:
        errors.append("Pipeline has no steps")
    for i, step in enumerate(steps):
        if not step.get("action"):
            errors.append(f"Step {i}: missing 'action'")
        if step.get("type") not in ("skill", "script", "agent", "command"):
            errors.append(f"Step {i}: invalid type '{step.get('type')}'")
    return errors


def execute_step(step: dict, context: dict) -> dict:
    step_type = step.get("type")
    action = step.get("action")

    result = {"step": step.get("name", action), "status": "pending", "output": None}

    if step_type == "script":
        import subprocess

        try:
            r = subprocess.run(action, shell=True, capture_output=True, text=True)
            result["output"] = r.stdout
            result["status"] = "success" if r.returncode == 0 else "failed"
        except Exception as e:
            result["output"] = str(e)
            result["status"] = "failed"

    elif step_type == "skill":
        result["output"] = f"Would invoke skill: {action}"
        result["status"] = "delegated"

    elif step_type == "command":
        result["output"] = f"Would run command: {action}"
        result["status"] = "delegated"

    else:
        result["output"] = f"Unknown step type: {step_type}"
        result["status"] = "failed"

    return result


def main():
    parser = argparse.ArgumentParser(description="Execute a pipeline")
    parser.add_argument("--pipeline", type=Path, required=True, help="Pipeline JSON definition")
    parser.add_argument("--validate-only", action="store_true", help="Only validate the pipeline")
    args = parser.parse_args()

    pipeline = json.loads(args.pipeline.read_text())

    errors = validate_pipeline(pipeline)
    if errors:
        print("Pipeline validation errors:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    if args.validate_only:
        print("Pipeline is valid")
        return

    context = {"pipeline": pipeline, "results": []}
    for step in pipeline.get("steps", []):
        result = execute_step(step, context)
        context["results"].append(result)
        icon = (
            "✓"
            if result["status"] == "success"
            else "→"
            if result["status"] == "delegated"
            else "✗"
        )
        print(f"  [{icon}] {result['step']}: {result['status']}")
        if result["output"]:
            print(f"          {str(result['output'])[:200]}")

    all_ok = all(r["status"] in ("success", "delegated") for r in context["results"])
    print(f"\nPipeline {'completed' if all_ok else 'failed'}")
    if not all_ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
