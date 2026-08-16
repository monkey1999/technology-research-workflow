#!/usr/bin/env python3
"""Render a traceable SVG chart from the workflow data-points ledger."""

from __future__ import annotations

import argparse
import csv
import html
import json
from pathlib import Path


COLORS = ["#1f5a94", "#c05a28", "#2f7d5b", "#7a5195", "#b08b24"]


def load_points(path: Path, figure_id: str) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        rows = [dict(row) for row in csv.DictReader(stream)]
    points = [row for row in rows if row.get("figure_id", "").strip() == figure_id]
    if not points:
        raise SystemExit(f"no data points found for {figure_id}")
    required = {"series", "source_id", "metric", "value", "unit", "condition", "locator", "uncertainty"}
    for index, point in enumerate(points, start=1):
        missing = sorted(key for key in required if not point.get(key, "").strip())
        if missing:
            raise SystemExit(f"row {index} has empty required values: {missing}")
        try:
            point["_numeric"] = float(point["value"])
        except ValueError as exc:
            raise SystemExit(f"row {index} value is not numeric: {point['value']}") from exc
    return points


def render(points: list[dict[str, str]], title: str, chart: str) -> str:
    width, height = 1080, 680
    left, right, top, bottom = 115, 50, 105, 165
    plot_width, plot_height = width - left - right, height - top - bottom
    values = [float(point["_numeric"]) for point in points]
    minimum = min(0.0, min(values))
    maximum = max(values)
    if maximum == minimum:
        maximum = minimum + 1.0
    span = maximum - minimum
    maximum += span * 0.12
    minimum -= span * 0.08 if minimum < 0 else 0
    span = maximum - minimum
    unit = points[0]["unit"]
    metric = points[0]["metric"]

    def y(value: float) -> float:
        return top + (maximum - value) / span * plot_height

    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">',
        f"<title>{html.escape(title)}</title>",
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<style>text{font-family:"Noto Sans CJK SC","Microsoft YaHei",Arial,sans-serif;fill:#17212b}'
        '.grid{stroke:#dce3e9;stroke-width:1}.axis{stroke:#52616f;stroke-width:1.5}'
        '.label{font-size:16px}.small{font-size:13px;fill:#4d5b66}.title{font-size:25px;font-weight:700}</style>',
        f'<text x="{left}" y="48" class="title">{html.escape(title)}</text>',
        f'<text x="{left}" y="76" class="small">指标：{html.escape(metric)}；单位：{html.escape(unit)}。仅比较数据表中记录的条件。</text>',
    ]
    for tick in range(6):
        value = minimum + span * tick / 5
        y_pos = y(value)
        elements.append(f'<line x1="{left}" y1="{y_pos:.1f}" x2="{left + plot_width}" y2="{y_pos:.1f}" class="grid"/>')
        elements.append(f'<text x="{left - 12}" y="{y_pos + 5:.1f}" text-anchor="end" class="small">{value:.3g}</text>')
    zero_y = y(0.0) if minimum <= 0 <= maximum else top + plot_height
    elements.extend([
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_height}" class="axis"/>',
        f'<line x1="{left}" y1="{zero_y:.1f}" x2="{left + plot_width}" y2="{zero_y:.1f}" class="axis"/>',
    ])
    step = plot_width / len(points)
    coordinates: list[tuple[float, float]] = []
    for index, point in enumerate(points):
        x = left + step * (index + 0.5)
        value = float(point["_numeric"])
        y_pos = y(value)
        color = COLORS[index % len(COLORS)]
        if chart == "bar":
            bar_width = min(92, step * 0.62)
            bar_y = min(y_pos, zero_y)
            bar_height = max(2, abs(zero_y - y_pos))
            elements.append(f'<rect x="{x - bar_width / 2:.1f}" y="{bar_y:.1f}" width="{bar_width:.1f}" height="{bar_height:.1f}" fill="{color}" rx="3"/>')
        coordinates.append((x, y_pos))
        elements.append(f'<circle cx="{x:.1f}" cy="{y_pos:.1f}" r="5" fill="{color}"/>')
        elements.append(f'<text x="{x:.1f}" y="{y_pos - 12:.1f}" text-anchor="middle" class="label">{value:g}</text>')
        label = html.escape(point["series"])
        source = html.escape(point["source_id"])
        elements.append(f'<text x="{x:.1f}" y="{top + plot_height + 32}" text-anchor="middle" class="label">{label}</text>')
        elements.append(f'<text x="{x:.1f}" y="{top + plot_height + 54}" text-anchor="middle" class="small">{source}</text>')
    if chart == "line" and len(coordinates) > 1:
        path = " ".join(("M" if index == 0 else "L") + f" {x:.1f} {y_pos:.1f}" for index, (x, y_pos) in enumerate(coordinates))
        elements.insert(-4 * len(points), f'<path d="{path}" fill="none" stroke="#1f5a94" stroke-width="3"/>')
    elements.append(
        f'<text x="{left}" y="{height - 40}" class="small">来源与条件详见 data-points.csv；图中数值不消除试验对象、布置和协议差异。</text>'
    )
    elements.append("</svg>")
    return "\n".join(elements) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--figure-id", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--chart", choices=("bar", "line"), default="bar")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    data_path = Path(args.data).resolve()
    output = Path(args.out).resolve()
    points = load_points(data_path, args.figure_id)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(points, args.title, args.chart), encoding="utf-8")
    result = {"ok": True, "figure_id": args.figure_id, "points": len(points), "output": str(output)}
    print(json.dumps(result, ensure_ascii=False) if args.json else output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
