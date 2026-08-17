#!/usr/bin/env python3
"""Compute reader-body report metrics for deterministic skill evaluation."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)(?:\s+\"([^\"]*)\")?\)")
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"([^\"]*)\")?\)")
PROCESS_META_RE = re.compile(
    r"如何从论文进入正文|证据如何(?:从.{0,20})?(?:收敛|进入|推导)|"
    r"如何由.{0,20}(?:得到|推导)|裁决闭环|证据门|门禁|判定纪律|"
    r"阈值如何.{0,12}冻结|审查结论|机械验证|受保护基线|"
    r"检索日志|论断与证据映射|证据簇(?:台账|映射)|artifact hash|SHA-?256",
    re.IGNORECASE,
)


def is_separator(line: str) -> bool:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def metrics(text: str) -> dict[str, int]:
    body = text.split("## 参考文献", 1)[0]
    body = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    lines = body.splitlines()
    headings = re.findall(r"(?m)^#{2,4}\s+(.+?)\s*$", body)
    figure_paths = [match[1].replace("\\", "/") for match in IMAGE_RE.findall(body)]
    return {
        "body_characters": len(re.sub(r"\s+", "", body)),
        "body_citations": len(LINK_RE.findall(body)),
        "figures": len(dict.fromkeys(figure_paths)),
        "tables": sum(1 for index in range(1, len(lines)) if "|" in lines[index - 1] and is_separator(lines[index])),
        "reader_headings": len(headings),
        "process_headings": sum(1 for heading in headings if PROCESS_META_RE.search(heading)),
        "process_meta_mentions": len(PROCESS_META_RE.findall(body)),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True)
    parser.add_argument("--min-body-characters", type=int)
    parser.add_argument("--min-body-citations", type=int, default=20)
    parser.add_argument("--min-figures", type=int, default=3)
    parser.add_argument("--min-tables", type=int, default=3)
    parser.add_argument("--max-body-characters", type=int)
    parser.add_argument("--max-reader-headings", type=int)
    parser.add_argument("--max-process-headings", type=int)
    parser.add_argument("--max-process-meta-mentions", type=int)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    measured = metrics(Path(args.report).read_text(encoding="utf-8"))
    required = {
        "body_citations": args.min_body_citations,
        "figures": args.min_figures,
        "tables": args.min_tables,
    }
    failures = [key for key, minimum in required.items() if measured[key] < minimum]
    maxima = {
        "reader_headings": args.max_reader_headings,
        "process_headings": args.max_process_headings,
        "process_meta_mentions": args.max_process_meta_mentions,
    }
    failures.extend(
        f"{key}_above_maximum"
        for key, maximum in maxima.items()
        if maximum is not None and measured[key] > maximum
    )
    length_diagnostics = []
    if args.min_body_characters is not None and measured["body_characters"] < args.min_body_characters:
        length_diagnostics.append("body_characters_below_diagnostic_range")
    if args.max_body_characters is not None and measured["body_characters"] > args.max_body_characters:
        length_diagnostics.append("body_characters_above_diagnostic_range")
    result = {
        "ok": not failures,
        "metrics": measured,
        "required": required,
        "maxima": maxima,
        "length_diagnostics": {
            "minimum": args.min_body_characters,
            "maximum": args.max_body_characters,
            "signals": length_diagnostics,
            "release_gate": False,
        },
        "failures": failures,
    }
    print(json.dumps(result, ensure_ascii=False) if args.json else result)
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
