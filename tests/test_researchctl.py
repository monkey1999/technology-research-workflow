from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "cli" / "researchctl.py"


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
        encoding="utf-8",
    )


def valid_source() -> dict:
    return {
        "source_id": "S-PAPER-1",
        "source_class": "journal_paper",
        "title": "Representative peer-reviewed experiment",
        "authors": ["A. Researcher"],
        "year": 2025,
        "doi": "10.1000/example",
        "canonical_url": "https://doi.org/10.1000/example",
        "authority": "primary",
        "verification_level": "full_text_verified",
        "locator": "p. 4, Fig. 2",
        "extracted_evidence": "The reported experiment states a bounded quantitative result.",
        "accessed_at": "2026-08-16T00:00:00Z",
        "content_hash": "sha256:example",
    }


def valid_claim() -> dict:
    return {
        "claim_id": "C-1",
        "claim": "The route has experimental support under the reported laboratory conditions.",
        "importance": "decision_critical",
        "claim_type": "experimental_result",
        "support_type": "direct",
        "evidence_ids": ["S-PAPER-1"],
        "counter_evidence_ids": [],
        "counter_evidence_note": "No directly contradictory study was found in the defined search window.",
        "conditions": "Laboratory setup described by the source.",
        "scope_limit": "Does not establish production readiness.",
        "confidence": "medium",
    }


def valid_report() -> str:
    sections = [
        ("摘要与核心判断", "本报告在限定实验条件下形成判断，并区分实验可行性和量产成熟度。"),
        ("技术问题与作用机制", "该路线通过可解释的物理机制把被测变化转换为可读信号，系统边界包括传感、解调与标定。"),
        ("技术路线与关键差异", "不同路线的差异来自测量位置、敏感机理和解调复杂度，因此不能只比较单一峰值指标。"),
        ("实验证据、性能与适用边界", "代表性实验给出了受条件约束的量化结果，但其样本、环境和时间尺度不足以证明量产可靠性。"),
        ("工程化、产业格局与应用选择", "工程选择还取决于封装、温漂、校准、成本与现有系统集成，实验优势只有在这些约束下才有产品意义。"),
        ("结论与未来路线", "下一步应使用预先定义的对照实验验证漂移和重复性；若结果不满足门限，应重新比较替代路线。"),
    ]
    body = "\n\n".join(f"## {heading}\n\n{text} [代表性同行评议实验](https://doi.org/10.1000/example)" for heading, text in sections)
    return f"# 合格技术调研报告\n\n{body}\n\n## 参考文献\n\n- [Representative peer-reviewed experiment](https://doi.org/10.1000/example)\n"


class ResearchCtlTests(unittest.TestCase):
    def make_run(self, root: Path) -> Path:
        run = root / "run"
        (run / "validation").mkdir(parents=True)
        (run / "request.yaml").write_text(
            "scope:\n  exclude: [patents]\nquality:\n  require_counter_evidence: true\n",
            encoding="utf-8",
        )
        write_jsonl(run / "sources.jsonl", [valid_source()])
        write_jsonl(run / "claims.jsonl", [valid_claim()])
        (run / "REPORT.md").write_text(valid_report(), encoding="utf-8")
        (run / "validation" / "report-review.json").write_text(
            json.dumps(
                {
                    "independent": True,
                    "status": "pass",
                    "release_recommendation": "ready",
                    "findings": [],
                }
            ),
            encoding="utf-8",
        )
        return run

    def verify(self, run: Path, stage: str = "release") -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        environment["PYTHONIOENCODING"] = "utf-8"
        environment["PYTHONUTF8"] = "1"
        return subprocess.run(
            [sys.executable, str(CLI), "verify", "--run", str(run), "--stage", stage, "--no-write"],
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
            env=environment,
        )

    def test_release_passes_for_reader_report(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.make_run(Path(temporary))
            result = self.verify(run)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "pass")
            self.assertEqual(payload["release_state"], "ready")

    def test_evidence_gate_rejects_legacy_and_patent_material(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.make_run(Path(temporary))
            write_jsonl(
                run / "sources.jsonl",
                [
                    {
                        "source_id": "S-PATENT-1",
                        "source_type": "patent",
                        "title": "Example patent",
                        "url": "https://example.com/patent",
                        "verification_status": "verified",
                    }
                ],
            )
            result = self.verify(run, "evidence")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("legacy source_type is not release-safe", result.stdout)
            self.assertIn("excluded patent material is present", result.stdout)

    def test_release_rejects_audit_report_and_missing_independent_review(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.make_run(Path(temporary))
            (run / "REPORT.md").write_text(
                valid_report() + "\n## 证据附录\n\n这是不应出现在读者正文中的后台检查表。\n",
                encoding="utf-8",
            )
            (run / "validation" / "report-review.json").unlink()
            result = self.verify(run)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("backstage audit section appears in reader report", result.stdout)
            self.assertIn("missing independent review", result.stdout)

    def test_renderer_embeds_images_and_renders_reader_features(self) -> None:
        spec = importlib.util.spec_from_file_location("researchctl", CLI)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary)
            (run / "figure.svg").write_text(
                '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="10"></svg>',
                encoding="utf-8",
            )
            markdown = (
                "# 报告\n\n## 摘要与核心判断\n\n"
                "**关键判断**与`边界`见 https://example.com/source\n\n"
                "| 路线 | 结论 |\n| --- | --- |\n| A | 有条件成立 |\n\n"
                "![证据图](figure.svg)\n"
            )
            document, issues = module.markdown_to_html(markdown, "报告", run)
            self.assertEqual(issues, [])
            self.assertIn("<strong>关键判断</strong>", document)
            self.assertIn("<code>边界</code>", document)
            self.assertIn('<a href="https://example.com/source">', document)
            self.assertIn('<nav class="toc"', document)
            self.assertIn("<table>", document)
            self.assertIn("data:image/svg+xml;base64,", document)
            self.assertNotIn("<p><figure", document)

    def test_render_and_package_cli(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.make_run(Path(temporary))
            environment = os.environ.copy()
            environment["PYTHONDONTWRITEBYTECODE"] = "1"
            environment["PYTHONIOENCODING"] = "utf-8"
            render = subprocess.run(
                [sys.executable, str(CLI), "render", "--run", str(run)],
                text=True,
                encoding="utf-8",
                capture_output=True,
                check=False,
                env=environment,
            )
            self.assertEqual(render.returncode, 0, render.stdout + render.stderr)
            package = subprocess.run(
                [sys.executable, str(CLI), "package", "--run", str(run)],
                text=True,
                encoding="utf-8",
                capture_output=True,
                check=False,
                env=environment,
            )
            self.assertEqual(package.returncode, 0, package.stdout + package.stderr)
            self.assertTrue((run / "REPORT.html").is_file())
            self.assertTrue((run / "REPORT-package.zip").is_file())
            manifest = json.loads((run / "package-manifest.json").read_text(encoding="utf-8"))
            self.assertIn("REPORT.html", {item["path"] for item in manifest["files"]})


if __name__ == "__main__":
    unittest.main()
