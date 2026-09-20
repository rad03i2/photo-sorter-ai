from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core import SorterError, analyze, apply_plan, build_plan, cluster, discover, plan_as_json


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="photo-sorter", description="Local, privacy-first photo organizer")
    p.add_argument("source", type=Path)
    p.add_argument("destination", type=Path)
    p.add_argument("--mode", choices=["date", "orientation"], default="date")
    p.add_argument("--no-recursive", action="store_true")
    p.add_argument("--include-hidden", action="store_true")
    p.add_argument("--similar", action="store_true", help="print perceptual-similarity groups")
    p.add_argument("--threshold", type=int, default=8)
    p.add_argument("--json", action="store_true", help="print machine-readable preview")
    p.add_argument("--apply", action="store_true", help="execute the previewed copy plan")
    p.add_argument("--move", action="store_true", help="move instead of copy; requires --apply")
    p.add_argument("--manifest", type=Path, default=Path("photo-sorter-manifest.json"))
    p.add_argument("--version", action="version", version="photo-sorter-ai 1.0.0 — Radwan Abdulhadi Ahmed / @rad03i2")
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.move and not args.apply:
        print("error: --move requires --apply", file=sys.stderr)
        return 2
    try:
        paths = discover(args.source, not args.no_recursive, args.include_hidden)
        photos = [analyze(path) for path in paths]
        if args.similar:
            groups = [[p.path for p in g] for g in cluster(photos, args.threshold) if len(g) > 1]
            print(json.dumps(groups, indent=2, ensure_ascii=False))
            return 0
        plan = build_plan(photos, args.destination, args.mode)
        if args.json:
            print(plan_as_json(plan))
        else:
            print(f"Found {len(photos)} photo(s). Planned {len(plan)} operation(s).")
            for item in plan:
                print(f"{item.source} -> {item.destination}")
            if not args.apply:
                print("Preview only. Re-run with --apply to copy files.")
        if args.apply:
            apply_plan(plan, args.manifest, args.move)
            print(f"Completed. Manifest: {args.manifest}")
        return 0
    except (SorterError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
