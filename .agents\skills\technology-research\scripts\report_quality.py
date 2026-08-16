#!/usr/bin/env python3
"""Compute reader-body report metrics for deterministic skill evaluation."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)(?:\s+\"([^\"]*)\")?\)")
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"([^\"]*)\")?\)")


def is_separator(line: str) -> bool:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def metrics(text: str) -> dict[str, int]:
    body = text.split("## 参考文献", 1)[0]
    body = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    lines = body.splitlines()
    return {
        "body_characters": len(re.sub(r"\s+", "", body)),
        "body_citations": len(LINK_RE.findall(body)),
        "figures": len(IMAGE_RE.findall(body)),
        "tables": sum(1 for index in range(1, len(lines)) if "|" in lines[index - 1] and is_separator(lines[index])),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True)
    parser.add_argument("--min-body-characters", type=int, default=18000)
    parser.add_argument("--min-body-citations", type=int, default=20)
    parser.add_argument("--min-figures", type=int, default=3)
    parser.add_argument("--min-tables", type=int, default=3)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    measured = metrics(Path(args.report).read_text(encoding="utf-8"))
    required = {
        "body_characters": args.min_body_characters,
        "body_citations": args.min_body_citations,
        "figures": args.min_figures,
        "tables": args.min_tables,
    }
    failures = [key for key, minimum in required.items() if measured[key] < minimum]
    result = {"ok": not failures, "metrics": measured, "required": required, "failures": failures}
    print(json.dumps(result, ensure_ascii=False) if args.json else result)
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
