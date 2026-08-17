from __future__ import annotations

import hashlib
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
CHART = ROOT / "skill" / "technology-research" / "scripts" / "render_evidence_chart.py"
REPORT_QUALITY = ROOT / "skill" / "technology-research" / "scripts" / "report_quality.py"
AUDIT_HEAVY = ROOT / "skill" / "technology-research" / "evals" / "files" / "audit-heavy.md"


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.write_text("".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records), encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def valid_source(source_id: str = "S-PAPER-1", content_hash: str = "sha256:paper-1") -> dict:
    return {
        "source_id": source_id,
        "source_class": "journal_paper",
        "title": f"Representative peer-reviewed experiment {source_id}",
        "authors": ["A. Researcher"],
        "year": 2025,
        "doi": "10.1000/example",
        "canonical_url": f"https://doi.org/10.1000/{source_id.lower()}",
        "authority": "primary",
        "verification_level": "full_text_verified",
        "locator": "p. 4, Fig. 2",
        "extracted_evidence": "The experiment reports a bounded quantitative result.",
        "accessed_at": "2026-08-17T00:00:00Z",
        "content_hash": content_hash,
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


def valid_report(with_visual: bool = False, body_link: bool = True) -> str:
    citation = " [代表性实验](https://doi.org/10.1000/s-paper-1)" if body_link else ""
    sections = [
        ("摘要与核心判断", "限定实验条件支持可行性，但还不能证明量产成熟度。"),
        ("技术问题与作用机制", "可解释的物理机制把被测变化转换为信号，系统边界包括传感、解调与标定。"),
        ("技术路线与关键差异", "路线差异来自测量位置、敏感机理和解调复杂度，不能只比较峰值指标。"),
        ("实验证据、性能与适用边界", "实验给出受条件约束的量化结果，样本、环境和时间尺度仍限制外推。"),
        ("工程化、产业格局与应用选择", "工程选择取决于封装、温漂、校准、成本和系统集成。"),
        ("结论与未来路线", "下一步应以预定义对照实验验证漂移和重复性，并设置路线退出条件。"),
    ]
    body = "\n\n".join(f"## {heading}\n\n{text}{citation}" for heading, text in sections)
    visual = ""
    if with_visual:
        visual = (
            "\n\n| 路线 | 对象 | 条件 | 结果 | 边界 |\n| --- | --- | --- | --- | --- |\n"
            "| 路线A | 样件 | 实验室 | 有条件成立 | 尚无长期数据 |\n\n"
            "![机制与证据边界](figures/FIG-01.svg)\n"
        )
    return f"# 合格技术调研报告\n\n{body}{visual}\n\n## 参考文献\n\n- [Representative experiment](https://doi.org/10.1000/s-paper-1)\n"


class ResearchCtlTests(unittest.TestCase):
    def environment(self) -> dict[str, str]:
        environment = os.environ.copy()
        environment.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"})
        return environment

    def invoke(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CLI), *arguments],
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
            env=self.environment(),
        )

    def verify(self, run: Path, stage: str = "release") -> subprocess.CompletedProcess[str]:
        return self.invoke("verify", "--run", str(run), "--stage", stage, "--no-write")

    def make_run(self, root: Path, doctoral: bool = False) -> Path:
        run = root / "run"
        (run / "validation").mkdir(parents=True)
        (run / "figures").mkdir()
        quality = ""
        if doctoral:
            quality = (
                "workflow_version: '0.4'\nreport:\n  report_type: technical-survey\n  quality_profile: doctoral\nquality:\n"
                "  require_counter_evidence: true\n  maximum_reader_headings: 20\n"
                "  maximum_process_headings: 0\n  maximum_process_meta_mentions: 0\n"
                "  minimum_body_citations: 1\n  minimum_figures: 1\n  minimum_tables: 1\n"
                "  minimum_synthesis_figures: 1\n  minimum_quantitative_figures: 1\n"
                "  minimum_multi_source_figures: 0\n"
                "  minimum_experiment_rows: 1\n  minimum_data_points: 1\n"
                "  minimum_full_text_academic_sources: 1\n  minimum_primary_research_sources: 1\n"
                "  require_report_type_fit: true\n  require_companion_outputs: true\n"
            )
        else:
            quality = "quality:\n  require_counter_evidence: true\n"
        (run / "request.yaml").write_text("scope:\n  exclude: [patents]\n" + quality, encoding="utf-8")
        write_jsonl(run / "sources.jsonl", [valid_source()])
        write_jsonl(run / "claims.jsonl", [valid_claim()])
        (run / "REPORT.md").write_text(valid_report(with_visual=doctoral), encoding="utf-8")
        if doctoral:
            (run / "EXECUTIVE_BRIEF.md").write_text(
                "# 技术负责人摘要\n\n核心判断在限定实验条件下成立，仍需验证长期稳定性。\n",
                encoding="utf-8",
            )
            (run / "EVIDENCE_ATLAS.md").write_text(
                "# 研发证据图谱\n\n代表性实验记录对象、装置、条件、结果、不确定性与边界。\n",
                encoding="utf-8",
            )
            (run / "experiment-matrix.csv").write_text(
                "study_id,source_id,route,cell_format,chemistry,sensor_placement,sample_size,test_conditions,reference_measurement,metric,result,uncertainty,replication,limitations\n"
                "ST-1,S-PAPER-1,A,pouch,NMC,surface,3,25 C chamber,thermocouple,error,0.2 C,reported SD,three cells,no cycling data\n",
                encoding="utf-8",
            )
            (run / "data-points.csv").write_text(
                "figure_id,series,source_id,metric,value,unit,condition,locator,uncertainty\n"
                "FIG-01,A,S-PAPER-1,error,0.2,C,25 C,p. 4 Fig. 2,reported SD\n",
                encoding="utf-8",
            )
            (run / "visual-plan.json").write_text(
                json.dumps({"items": [
                    {"figure_id": "FIG-01", "role": "mechanism", "kind": "schematic", "purpose": "mechanism", "status": "complete", "source_ids": ["S-PAPER-1"]},
                    {"figure_id": "FIG-02", "role": "quantitative_comparison", "kind": "chart", "purpose": "comparison", "status": "complete", "source_ids": ["S-PAPER-1"]},
                    {"figure_id": "FIG-03", "role": "route_or_maturity", "kind": "map", "purpose": "route", "status": "complete", "source_ids": ["S-PAPER-1"]},
                ]}, ensure_ascii=False),
                encoding="utf-8",
            )
            plan = json.loads((run / "visual-plan.json").read_text(encoding="utf-8"))
            for item in plan["items"]:
                item.update({
                    "reader_question": "What should the reader understand?",
                    "intended_insight": "A bounded technical relationship.",
                    "presentation": "data_reconstruction" if item["role"] == "quantitative_comparison" else "synthesis",
                    "destination": "main",
                })
            (run / "visual-plan.json").write_text(json.dumps(plan), encoding="utf-8")
            (run / "figures" / "FIG-01.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" width="40" height="20"></svg>', encoding="utf-8")
            write_jsonl(run / "figures" / "figure-register.jsonl", [{
                "figure_id": "FIG-01", "path": "figures/FIG-01.svg", "kind": "schematic",
                "caption": "Mechanism and evidence boundary", "source_ids": ["S-PAPER-1"],
                "data_file": "data-points.csv", "license": "author-generated",
                "provenance": "derived from cited source", "generated_by": "test",
                "role": "quantitative_comparison", "presentation": "data_reconstruction",
                "reader_question": "How does the bounded result compare?",
                "information_gain": "Shows the quantitative result directly.", "destination": "main",
            }])
        self.assertEqual(self.invoke("render", "--run", str(run)).returncode, 0)
        recommendation = "candidate_for_human_acceptance" if doctoral else "ready"
        (run / "validation" / "report-review.md").write_text("# Findings\n\nNo blocker, major, or minor findings.\n", encoding="utf-8")
        if doctoral:
            review = {
                "review_version": "0.4", "independent": True,
                "reviewers": {
                    "technical": {"agent": "test-technical", "session_id": "technical-session", "fresh_context": True},
                    "reader_editor": {"agent": "test-reader", "session_id": "reader-session", "fresh_context": True},
                },
                "artifacts": {"report_sha256": sha256(run / "REPORT.md"), "html_sha256": sha256(run / "REPORT.html")},
                "scientific_review": {"status": "pass"}, "synthesis_review": {"status": "pass"},
                "narrative_review": {"status": "pass"},
                "visual_review": {"status": "pass", "viewports": ["1440x1000", "1024x768", "print"], "figures_reviewed": 1, "tables_reviewed": 1, "synthesis_figures_reviewed": 1, "quantitative_figures_reviewed": 1},
                "report_type_review": {"status": "pass", "report_type": "technical-survey", "primary_report_fit": True, "audit_material_backstage": True},
                "reader_experience_review": {"status": "pass", "continuous_reading_pass": True, "five_minute_orientation_pass": True},
                "status": "pass", "release_recommendation": recommendation, "findings": [],
            }
            (run / "validation" / "reader-review.md").write_text(
                "# Findings\n\nNo blocker, major, or minor findings.\n", encoding="utf-8"
            )
        else:
            review = {
                "review_version": "0.3", "independent": True,
                "reviewer": {"agent": "test-reviewer", "session_id": "review-session-1", "fresh_context": True},
                "artifacts": {"report_sha256": sha256(run / "REPORT.md"), "html_sha256": sha256(run / "REPORT.html")},
                "scientific_review": {"status": "pass"}, "narrative_review": {"status": "pass"},
                "visual_review": {"status": "pass", "viewports": ["1440x1000", "1024x768", "print"], "figures_reviewed": 0, "tables_reviewed": 0},
                "status": "pass", "release_recommendation": recommendation, "findings": [],
            }
        (run / "validation" / "report-review.json").write_text(
            json.dumps(review, ensure_ascii=False), encoding="utf-8"
        )
        return run

    def refresh_review_hashes(self, run: Path) -> None:
        self.assertEqual(self.invoke("render", "--run", str(run)).returncode, 0)
        review_path = run / "validation" / "report-review.json"
        review = json.loads(review_path.read_text(encoding="utf-8"))
        review["artifacts"] = {"report_sha256": sha256(run / "REPORT.md"), "html_sha256": sha256(run / "REPORT.html")}
        review_path.write_text(json.dumps(review), encoding="utf-8")

    def test_standard_release_passes_with_hash_bound_review(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result = self.verify(self.make_run(Path(temporary)))
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertEqual(json.loads(result.stdout)["release_state"], "ready")

    def test_doctoral_release_passes_and_remains_human_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result = self.verify(self.make_run(Path(temporary), doctoral=True))
            self.assertEqual(result.returncode, 0, result.stdout)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["release_state"], "candidate_for_human_acceptance")
            self.assertEqual(payload["report_metrics"]["figures"], 1)

    def test_bibliography_links_do_not_count_as_body_citations(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.make_run(Path(temporary), doctoral=True)
            (run / "REPORT.md").write_text(valid_report(with_visual=True, body_link=False), encoding="utf-8")
            self.refresh_review_hashes(run)
            result = self.verify(run)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("bibliography links do not count", result.stdout)
            self.assertIn("has no supporting source link in the report body", result.stdout)

    def test_doctoral_text_wall_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.make_run(Path(temporary), doctoral=True)
            (run / "REPORT.md").write_text(valid_report(with_visual=False), encoding="utf-8")
            self.refresh_review_hashes(run)
            result = self.verify(run)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("evidence-bearing figures; found 0", result.stdout)
            self.assertIn("analytical tables; found 0", result.stdout)

    def test_v04_rejects_audit_heavy_primary_report_even_when_quantity_floors_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.make_run(Path(temporary), doctoral=True)
            report = (run / "REPORT.md").read_text(encoding="utf-8")
            report = report.replace(
                "## 结论与未来路线",
                "## 证据如何从实验收敛为本章判断\n\n本节解释证据门与裁决闭环。\n\n## 结论与未来路线",
            )
            (run / "REPORT.md").write_text(report, encoding="utf-8")
            self.refresh_review_hashes(run)
            result = self.verify(run)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("process or adjudication headings", result.stdout)
            self.assertIn("audit/process meta mentions", result.stdout)

    def test_v04_body_length_is_diagnostic_not_a_release_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.make_run(Path(temporary), doctoral=True)
            report = (run / "REPORT.md").read_text(encoding="utf-8")
            report = report.replace("## 参考文献", ("补充技术解释。" * 8000) + "\n\n## 参考文献")
            (run / "REPORT.md").write_text(report, encoding="utf-8")
            self.refresh_review_hashes(run)
            result = self.verify(run)
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertGreater(json.loads(result.stdout)["report_metrics"]["body_characters"], 45000)

    def test_v04_source_figure_ratio_is_diagnostic_not_a_release_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.make_run(Path(temporary), doctoral=True)
            request = (run / "request.yaml").read_text(encoding="utf-8")
            (run / "request.yaml").write_text(
                request.replace("minimum_synthesis_figures: 1", "minimum_synthesis_figures: 0"),
                encoding="utf-8",
            )
            register = [json.loads(line) for line in (run / "figures" / "figure-register.jsonl").read_text(encoding="utf-8").splitlines()]
            register[0]["presentation"] = "source_figure"
            write_jsonl(run / "figures" / "figure-register.jsonl", register)
            result = self.verify(run)
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertEqual(json.loads(result.stdout)["report_metrics"]["source_figure_ratio"], 1.0)

    def test_v04_does_not_count_repeated_image_placements_as_new_figures(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.make_run(Path(temporary), doctoral=True)
            request = (run / "request.yaml").read_text(encoding="utf-8")
            request = request.replace("minimum_figures: 1", "minimum_figures: 2")
            request = request.replace("minimum_synthesis_figures: 1", "minimum_synthesis_figures: 2")
            (run / "request.yaml").write_text(request, encoding="utf-8")
            report = (run / "REPORT.md").read_text(encoding="utf-8")
            report = report.replace(
                "## 参考文献",
                "![重复放置不构成新图](figures/FIG-01.svg)\n\n## 参考文献",
            )
            (run / "REPORT.md").write_text(report, encoding="utf-8")
            self.refresh_review_hashes(run)
            result = self.verify(run)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(json.loads(result.stdout)["report_metrics"]["figures"], 1)
            self.assertIn("repeats the same image reference", result.stdout)

    def test_v04_requires_distinct_technical_and_reader_review_contexts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.make_run(Path(temporary), doctoral=True)
            review_path = run / "validation" / "report-review.json"
            review = json.loads(review_path.read_text(encoding="utf-8"))
            review["reviewers"]["reader_editor"]["session_id"] = review["reviewers"]["technical"]["session_id"]
            review_path.write_text(json.dumps(review), encoding="utf-8")
            result = self.verify(run)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("must use distinct fresh contexts", result.stdout)

    def test_evidence_gate_rejects_missing_matrices_and_duplicate_documents(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.make_run(Path(temporary), doctoral=True)
            (run / "experiment-matrix.csv").unlink()
            write_jsonl(run / "sources.jsonl", [valid_source(), valid_source("S-PAPER-2", "sha256:paper-1")])
            result = self.verify(run, "evidence")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("content_hash duplicates", result.stdout)
            self.assertIn("missing artifact: experiment-matrix.csv", result.stdout)

    def test_release_rejects_stale_review_and_omitted_finding(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.make_run(Path(temporary), doctoral=True)
            (run / "validation" / "report-review.md").write_text("# Findings\n\n## MAJ-1 Missing boundary\n", encoding="utf-8")
            (run / "REPORT.md").write_text((run / "REPORT.md").read_text(encoding="utf-8") + "\nChanged after review.\n", encoding="utf-8")
            result = self.verify(run)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("review is stale", result.stdout)
            self.assertIn("review JSON omits findings", result.stdout)

    def test_renderer_embeds_images_and_package_contains_html(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.make_run(Path(temporary), doctoral=True)
            html_text = (run / "REPORT.html").read_text(encoding="utf-8")
            self.assertIn("data:image/svg+xml;base64,", html_text)
            package = self.invoke("package", "--run", str(run))
            self.assertEqual(package.returncode, 0, package.stdout)
            manifest = json.loads((run / "package-manifest.json").read_text(encoding="utf-8"))
            self.assertIn("REPORT.html", {item["path"] for item in manifest["files"]})

    def test_package_refuses_a_failed_or_stale_release(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run = self.make_run(Path(temporary), doctoral=True)
            (run / "REPORT.md").write_text((run / "REPORT.md").read_text(encoding="utf-8") + "\nPost-review edit.\n", encoding="utf-8")
            package = self.invoke("package", "--run", str(run))
            self.assertNotEqual(package.returncode, 0)
            self.assertIn("package: refused because release verification failed", package.stdout)
            self.assertFalse((run / "REPORT-package.zip").exists())

    def test_chart_script_renders_traceable_svg(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            data = root / "data.csv"
            output = root / "figure.svg"
            data.write_text(
                "figure_id,series,source_id,metric,value,unit,condition,locator,uncertainty\n"
                "FIG-9,A,S-1,error,0.2,C,25 C,p. 4,SD\nFIG-9,B,S-2,error,0.4,C,25 C,p. 5,SD\n",
                encoding="utf-8",
            )
            result = subprocess.run([sys.executable, str(CHART), "--data", str(data), "--figure-id", "FIG-9", "--out", str(output), "--title", "Bounded comparison", "--json"], text=True, encoding="utf-8", capture_output=True, env=self.environment())
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout)["points"], 2)
            self.assertIn("data-points.csv", output.read_text(encoding="utf-8"))

    def test_reader_fit_evaluator_rejects_audit_heavy_fixture(self) -> None:
        result = subprocess.run(
            [
                sys.executable, str(REPORT_QUALITY), "--report", str(AUDIT_HEAVY),
                "--min-body-characters", "100", "--min-body-citations", "1",
                "--min-figures", "1", "--min-tables", "1",
                "--max-process-headings", "0", "--max-process-meta-mentions", "0", "--json",
            ],
            text=True,
            encoding="utf-8",
            capture_output=True,
            env=self.environment(),
        )
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertGreaterEqual(payload["metrics"]["process_headings"], 1)
        self.assertGreaterEqual(payload["metrics"]["process_meta_mentions"], 1)

    def test_init_creates_doctoral_research_scaffolding(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            config = root / "request.yaml"
            config.write_text("topic: test\n", encoding="utf-8")
            run = root / "new-run"
            result = self.invoke("init", "--config", str(config), "--out", str(run))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for relative in ("EXECUTIVE_BRIEF.md", "EVIDENCE_ATLAS.md", "experiment-matrix.csv", "data-points.csv", "visual-plan.json", "figures/figure-register.jsonl"):
                self.assertTrue((run / relative).is_file(), relative)
            manifest = json.loads((run / "run-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["workflow_version"], "0.4.1")


if __name__ == "__main__":
    unittest.main()
