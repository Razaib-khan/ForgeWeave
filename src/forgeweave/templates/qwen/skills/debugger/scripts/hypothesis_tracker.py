"""Track debugging hypotheses and narrow down root cause."""
import argparse
import json
from datetime import datetime
from pathlib import Path


def create_session(symptom: str) -> dict:
    return {
        "symptom": symptom,
        "created": datetime.now().isoformat(),
        "hypotheses": [],
        "root_cause": None,
        "fix": None,
        "status": "active",
    }


def add_hypothesis(session: dict, description: str, test: str) -> dict:
    h = {
        "id": len(session["hypotheses"]) + 1,
        "description": description,
        "test": test,
        "result": None,
        "eliminated": False,
    }
    session["hypotheses"].append(h)
    return session


def eliminate_hypothesis(session: dict, h_id: int) -> dict:
    for h in session["hypotheses"]:
        if h["id"] == h_id:
            h["eliminated"] = True
            h["result"] = "eliminated"
    return session


def main():
    parser = argparse.ArgumentParser(description="Debugging hypothesis tracker")
    parser.add_argument("symptom", nargs="?", help="The bug symptom")
    parser.add_argument("--session", type=Path, help="Existing session file to continue")
    parser.add_argument("--add-hypothesis", nargs=2, metavar=("DESC", "TEST"), help="Add hypothesis")
    parser.add_argument("--eliminate", type=int, metavar="ID", help="Eliminate hypothesis by ID")
    parser.add_argument("--save", type=Path, default=Path("debug-session.json"), help="Session file")
    args = parser.parse_args()

    if args.session and args.session.exists():
        session = json.loads(args.session.read_text())
    elif args.symptom:
        session = create_session(args.symptom)
    else:
        parser.print_help()
        return

    if args.add_hypothesis:
        session = add_hypothesis(session, args.add_hypothesis[0], args.add_hypothesis[1])

    if args.eliminate:
        session = eliminate_hypothesis(session, args.eliminate)

    args.save.write_text(json.dumps(session, indent=2))
    print(f"Session saved to {args.save}")

    remaining = [h for h in session["hypotheses"] if not h["eliminated"]]
    if remaining:
        print(f"\nRemaining hypotheses ({len(remaining)}):")
        for h in remaining:
            print(f"  [{h['id']}] {h['description']}")
            print(f"       Test: {h['test']}")
    else:
        print("\nAll hypotheses eliminated. Need new hypotheses.")


if __name__ == "__main__":
    main()
