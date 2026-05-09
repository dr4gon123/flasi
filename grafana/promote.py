#!/usr/bin/env python3
"""Promote Grafana dashboards from dev to prod.

Usage:
  python3 grafana/promote.py --file grafana/dev/FortiGate/traffic-fortios.json
  python3 grafana/promote.py --vendor FortiGate
  python3 grafana/promote.py --vendor "Palo Alto"
"""
import argparse
import glob
import hashlib
import json
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEV_BASE = os.path.join(REPO_ROOT, "grafana", "dev")
PROD_BASE = os.path.join(REPO_ROOT, "grafana", "prod")


def _prod_uid(dev_uid: str) -> str:
    h = hashlib.sha256(f"{dev_uid}:prod".encode()).hexdigest()
    return h[:len(dev_uid)]


def promote_file(src: str) -> str:
    src = os.path.abspath(src)
    if not src.startswith(DEV_BASE + os.sep):
        print(f"error: {src} is not under grafana/dev/", file=sys.stderr)
        sys.exit(1)

    rel = os.path.relpath(src, DEV_BASE)
    dest = os.path.join(PROD_BASE, rel)
    os.makedirs(os.path.dirname(dest), exist_ok=True)

    with open(src) as f:
        d = json.load(f)

    d["metadata"]["name"] = _prod_uid(d["metadata"]["name"])

    if os.path.basename(src) != "_folder.json":
        spec = d.get("spec", {})
        spec["tags"] = ["prod" if t == "dev" else t for t in spec.get("tags", [])]
        for link in spec.get("links", []):
            if "tags" in link:
                link["tags"] = ["prod" if t == "dev" else t for t in link["tags"]]

    with open(dest, "w") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write("\n")

    return dest


def warn_unpromoted(vendor_dir: str, promoted: set[str]) -> None:
    siblings = {
        f for f in glob.glob(os.path.join(vendor_dir, "*.json"))
        if os.path.basename(f) != "_folder.json"  # _folder.json is not a dashboard
    }
    unpromoted = siblings - promoted
    if unpromoted:
        names = sorted(os.path.basename(p) for p in unpromoted)
        print(
            f"\nwarning: {len(names)} sibling(s) not yet promoted "
            f"(nav link dropdowns may be incomplete):"
        )
        for n in names:
            print(f"  {n}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Promote dashboards from dev to prod")
    parser.add_argument("--file", help="Single dashboard path under grafana/dev/")
    parser.add_argument("--vendor", help="Vendor folder name (promotes all dashboards)")
    args = parser.parse_args()

    if not args.file and not args.vendor:
        parser.print_help()
        sys.exit(1)

    sources: list[str] = []

    if args.vendor:
        vendor_dir = os.path.join(DEV_BASE, args.vendor)
        if not os.path.isdir(vendor_dir):
            print(f"error: vendor directory not found: {vendor_dir}", file=sys.stderr)
            sys.exit(1)
        sources = sorted(glob.glob(os.path.join(vendor_dir, "*.json")))

    if args.file:
        sources.append(os.path.join(REPO_ROOT, args.file) if not os.path.isabs(args.file) else args.file)

    promoted: set[str] = set()
    for src in sources:
        dest = promote_file(src)
        print(f"{os.path.relpath(src, REPO_ROOT)}  →  {os.path.relpath(dest, REPO_ROOT)}")
        promoted.add(src)

    if args.file and not args.vendor:
        vendor_dir = os.path.dirname(os.path.abspath(args.file if os.path.isabs(args.file)
                                                       else os.path.join(REPO_ROOT, args.file)))
        warn_unpromoted(vendor_dir, promoted)


if __name__ == "__main__":
    main()
