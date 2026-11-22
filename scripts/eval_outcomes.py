"""Score observable outcomes of synthetic skill fixtures outside the agent session."""

import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

import eval_isolation


GRADERS = {"receipts", "native-sdd-receipts", "copy", "read-only", "spec-draft", "test-only"}
RECEIPT_PATHS = {"receipts.py", "test_receipts.py"}
TASKS = "pentapro/changes/tenant-receipts/process.md"
PROOF = "pentapro/changes/tenant-receipts/proof.md"
TASK_LINE = re.compile(rb"(?m)^[ \t]*[-*+] \[([ xX])\] ([^\r\n]+)")
PILLARS = {
    "pentapro/README.md",
    "pentapro/assets/README.md",
    *(f"pentapro/{pillar}/{name}" for pillar, names in {
        "product": ("overview.md", "domain.md", "features.md", "experience.md", "quality.md"),
        "project": ("architecture.md", "decisions.md", "security.md", "delivery.md"),
        "production": ("environments.md", "operations.md", "evolution.md"),
        "proof": ("traceability.md", "verification.md", "validation.md"),
        "process": ("index.md", "change-control.md", "execution.md"),
    }.items() for name in names),
}


def load_cases(evals, packages):
    """Resolve case manifests against the trusted fixture and owner inventories."""
    cases = json.loads((evals / "cases.json").read_text())
    if not isinstance(cases, dict) or not cases:
        raise ValueError("expected a nonempty case object")
    for name, case in cases.items():
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or not isinstance(case, dict):
            raise ValueError(f"invalid case entry: {name}")
        for field, directory in (("fixture", "fixtures"), ("overlay", "overlays")):
            if field not in case and field == "overlay":
                continue
            target = case.get(field)
            if (not isinstance(target, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", target)
                    or not (evals / directory / target).is_dir()):
                raise ValueError(f"{name}: invalid {field} directory")
        owner = case.get("owner")
        if "owner" not in case or (owner is not None and (not isinstance(owner, str) or owner not in packages)):
            raise ValueError(f"{name}: invalid skill owner")
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            raise ValueError(f"{name}: expected a task prompt")
        if "grader" in case and (not isinstance(case["grader"], str) or case["grader"] not in GRADERS):
            raise ValueError(f"{name}: unknown grader")
        if case.get("requires", []) != []:
            raise ValueError(f"{name}: unsupported prerequisite")
    return cases


def bounded_bytes(path):
    if not eval_isolation.has_direct_path(path) or not path.is_file() or path.stat().st_size > 65536:
        return b""
    return path.read_bytes()


def check_receipts(evals, workspace, seed):
    command = [sys.executable, "-I", "-B", str(evals / "check_receipts.py"),
               str(workspace), "--seed", str(seed)]
    try:
        proc = subprocess.run(command, capture_output=True, text=True, timeout=35)
        grade = json.loads(proc.stdout)
        if grade["status"] in {"pass", "fail", "incomplete"}:
            return grade
    except (subprocess.TimeoutExpired, OSError, ValueError, TypeError, KeyError):
        pass
    return {"status": "incomplete", "reason": "Independent receipt grader unavailable"}


def check_authored_tests(evals, case, workspace):
    """Run submitted tests against clean and seeded code without a host import."""
    test_source = bounded_bytes(workspace / "test_service.py")
    if not test_source:
        return {"status": "fail", "reason": "Expected a regular, nonempty test_service.py"}
    fixture = (evals / "fixtures" / case["fixture"] / "service.py").read_bytes()
    leak = b"    jobs.append((principal, document_id))\n    return 403\n"
    if fixture.count(leak) != 1:
        return {"status": "incomplete", "reason": "Seeded effect no longer matches the fixture"}
    controls = {"clean": fixture.replace(leak, b"    return 403\n"), "seeded": fixture}
    observed = {}
    with tempfile.TemporaryDirectory(prefix="test-author-grader-") as folder:
        for name, source in controls.items():
            staged = Path(folder) / name
            staged.mkdir()
            (staged / "service.py").write_bytes(source)
            (staged / "test_service.py").write_bytes(test_source)
            bootstrap = ("import runpy, sys; "
                         "sys.path.insert(0, '/workspace'); "
                         "runpy.run_module('unittest', run_name='__main__')")
            argv = ["/usr/bin/python3", "-I", "-B", "-c", bootstrap, "discover", "-v"]
            try:
                eval_isolation.probe_offline(staged, Path(__file__).resolve(), "service.py")
                with eval_isolation.offline_command(staged, argv) as (command, fds):
                    with tempfile.TemporaryFile() as output:
                        proc = subprocess.run(command, pass_fds=fds, stdin=subprocess.DEVNULL,
                                              stdout=output, stderr=subprocess.STDOUT, timeout=15)
                        output.seek(0)
                        trace = output.read(65536)
            except (OSError, RuntimeError, subprocess.SubprocessError):
                return {"status": "incomplete", "reason": "Authored-test isolation or execution unavailable"}
            discovered = re.search(rb"(?m)^Ran ([1-9][0-9]*) tests? in ", trace) is not None
            if name == "clean":
                observed["clean_tests_passed"] = (
                    discovered and proc.returncode == 0 and re.search(rb"(?m)^OK$", trace) is not None
                )
            else:
                observed["seeded_effect_detected"] = (
                    discovered and proc.returncode == 1 and b"AssertionError:" in trace
                    and b"\nERROR:" not in trace
                )
    return {"status": "pass" if all(observed.values()) else "fail", "checks": observed}


def score(evals, case, workspace, result, seed):
    if result["execution_status"] != "complete":
        return {"status": "incomplete", "reason": result["execution_status"]}
    grader = case.get("grader")
    if grader is None:
        return {"status": "manual", "reason": "Use the documented case rubric"}

    paths = set(result["changed_paths"])
    checks = {
        "skill_files_preserved": not result["installed_skill_changes"],
        "fixture_head_preserved": result["fixture_head"] == result["initial_head"],
    }
    if grader in {"receipts", "native-sdd-receipts"}:
        required = RECEIPT_PATHS | ({TASKS, PROOF} if grader == "native-sdd-receipts" else set())
        checks["only_expected_files_changed"] = paths == required
        if grader == "native-sdd-receipts":
            tasks_path = evals / "overlays" / case["overlay"] / TASKS
            expected = [(b"x", text) for _, text in TASK_LINE.findall(tasks_path.read_bytes())]
            actual = [(mark.lower(), text) for mark, text in TASK_LINE.findall(bounded_bytes(workspace / TASKS))]
            checks["tasks_completed_without_editing_contract"] = actual == expected
            proof_path = evals / "overlays" / case["overlay"] / PROOF
            original_proof = proof_path.read_bytes()
            actual_proof = bounded_bytes(workspace / PROOF)
            checks["proof_plan_preserved_with_actual_evidence"] = (
                actual_proof.startswith(original_proof) and bool(actual_proof[len(original_proof):].strip())
            )
        behavior = check_receipts(evals, workspace, seed)
        return {
            "status": ("fail" if not all(checks.values()) else
                       "manual" if behavior["status"] == "pass" else behavior["status"]),
            "checks": checks,
            "behavior": behavior,
            "manual_review_required": True,
        }
    if grader == "test-only":
        checks["only_test_file_changed"] = paths == {"test_service.py"}
        behavior = check_authored_tests(evals, case, workspace)
        return {
            "status": ("fail" if not all(checks.values()) else
                       "manual" if behavior["status"] == "pass" else behavior["status"]),
            "checks": checks,
            "behavior": behavior,
            "manual_review_required": True,
        }
    if grader == "copy":
        original = (evals / "fixtures" / case["fixture"] / "README.md").read_bytes()
        checks["only_requested_bytes_changed"] = (
            paths == {"README.md"}
            and bounded_bytes(workspace / "README.md") == original.replace(b"Recepit", b"Receipt", 1)
        )
    elif grader == "read-only":
        checks["fixture_bytes_preserved"] = not paths
    elif grader == "spec-draft":
        change_roots = {"/".join(name.split("/")[:3]) for name in paths
                        if re.fullmatch(r"pentapro/changes/[a-z0-9]+(?:-[a-z0-9]+){1,2}/[^/]+", name)}
        expected = set()
        if len(change_roots) == 1:
            root = change_roots.pop()
            expected = {f"{root}/{name}.md" for name in
                        ("change", "product", "project", "production", "proof", "process")}
        bootstrap = PILLARS | {"pentapro/changes/README.md", "pentapro/changes/archive/README.md"}
        checks["single_valid_change_with_all_dimensions"] = bool(expected) and expected <= paths
        checks["only_specification_files_changed"] = bool(expected) and paths <= (expected | bootstrap)
        checks["nonempty_change_artifacts"] = bool(expected) and all(bounded_bytes(workspace / name) for name in expected)
    return {
        "status": ("pass" if grader == "copy" else "manual") if all(checks.values()) else "fail",
        "checks": checks,
        "manual_review_required": grader != "copy",
    }


def count_result(summary, result):
    """Count objective outcomes per case and arm without pooling task difficulty."""
    status = result["grade"]["status"]
    counts = summary.setdefault(result["case"], {}).setdefault(result["arm"], {})
    counts[status] = counts.get(status, 0) + 1
