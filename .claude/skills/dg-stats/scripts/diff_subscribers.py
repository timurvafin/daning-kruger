#!/usr/bin/env python3
"""Compare two subscriber snapshots and output diff as JSON."""

import json
import sys


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} prev.json curr.json", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1]) as f:
        prev = json.load(f)
    with open(sys.argv[2]) as f:
        curr = json.load(f)

    prev_ids = {p["id"] for p in prev["participants"]}
    curr_ids = {p["id"] for p in curr["participants"]}

    curr_by_id = {p["id"]: p for p in curr["participants"]}
    prev_by_id = {p["id"]: p for p in prev["participants"]}

    new = [curr_by_id[uid] for uid in sorted(curr_ids - prev_ids)]
    left = [prev_by_id[uid] for uid in sorted(prev_ids - curr_ids)]

    result = {
        "prev_date": prev["date"],
        "curr_date": curr["date"],
        "total_before": prev["total"],
        "total_after": curr["total"],
        "new": new,
        "left": left,
    }
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
