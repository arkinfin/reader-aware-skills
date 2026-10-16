#!/usr/bin/env python3
"""Static release checks; no network, model calls, or runtime installation."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


def digest(data):
    return hashlib.sha256(data).hexdigest()


def validate(root, source_workspace=None):
    report = {"passed": [], "failed": [], "skipped": [], "limits": [
        "Static checks do not establish teaching-runtime behavior or model availability.",
        "Pattern scanning cannot prove absence of secrets, privacy issues, or copyright risk.",
        "No generated text quality, correctness, learning gain, or experimental result is evaluated.",
        "The simple frontmatter parser supports this package's scalar fields, not general YAML."]}

    def check(name, condition):
        report["passed" if condition else "failed"].append(name)

    try:
        record = json.loads((root / "docs/preservation.json").read_text())
        text = (root / record["skill"]).read_bytes().decode("utf-8")
        notice = record["notice_exact"]
        check("original_notice_once", text.count(notice) == 1)
        restored = text.replace(notice, record["notice_original_replacement"], 1)
        for item in record["replacements"]:
            check("adaptation_once:" + item["original"], restored.count(item["packaged"]) == 1)
            restored = restored.replace(item["packaged"], item["original"], 1)
        check("original_skill_sha256", digest(restored.encode()) == record["source_skill_sha256"])
        check("original_metadata_sha256", digest((root / record["metadata"]).read_bytes()) == record["metadata_sha256"])
        if source_workspace:
            for item in record["sources"]:
                path = source_workspace / item["path"]
                check("source_hash:" + item["path"], path.is_file() and digest(path.read_bytes()) == item["sha256"])
            for rel in record["external_paths"]:
                check("external_path:" + rel, (source_workspace / rel).is_file())
            report["skipped"].append("External files located; runtime execution and dependency health were not tested.")
        else:
            report["skipped"].append("External runtime availability and seven source hashes: use --source-workspace to inspect an existing installation.")
    except (OSError, ValueError, KeyError, UnicodeError) as exc:
        report["failed"].append("preservation_record:" + type(exc).__name__)

    for name in ("pedagogical-readability", "reader-aware-writing"):
        path = root / "skills" / name / "SKILL.md"
        try:
            content = path.read_text()
            match = re.match(r"\A---\n(.*?)\n---\n", content, re.S)
            fields = {}
            if match:
                for line in match[1].splitlines():
                    key, sep, value = line.partition(":")
                    if sep:
                        fields[key.strip()] = value.strip()
            check("frontmatter:" + name, bool(match) and fields.get("name") == name and bool(fields.get("description")))
        except (OSError, UnicodeError):
            check("frontmatter:" + name, False)

    excluded = {".git", ".workflow", ".venv", "__pycache__", "build", "dist"}
    files = {p for p in root.rglob("*") if p.is_file() and not excluded.intersection(p.relative_to(root).parts)}
    git = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=root, capture_output=True)
    if git.returncode == 0:
        files.update(root / x for x in git.stdout.decode().split("\0") if x)
    else:
        report["skipped"].append("Git candidate enumeration unavailable; ordinary project files were scanned.")
    secret_patterns = [re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
                       re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{24,}\b")]
    private_names = re.compile(r"(?:chat[-_ ]?(?:history|export|transcript)|conversation[-_ ]?(?:export|transcript)|私聊|聊天记录)", re.I)
    scaffolds = re.compile(r"(?:\[INSERT [A-Z_ ]+\]|\{\{PROJECT_NAME\}\}|YOUR_PROJECT_NAME|REPLACE_ME)")
    for path in sorted(files):
        rel = str(path.relative_to(root))
        if excluded.intersection(Path(rel).parts):
            continue
        if path.is_symlink():
            inside = path.resolve().is_relative_to(root.resolve())
            check("no_symlink_escape:" + rel, inside)
            if not inside:
                continue
        check("no_private_filename:" + rel, not private_names.search(path.name))
        check("no_textbook_source:" + rel, path.suffix.lower() not in {".tex", ".pdf", ".epub", ".docx"})
        try:
            raw = path.read_bytes()
        except OSError:
            check("readable_candidate:" + rel, False)
            continue
        content = raw.decode("utf-8", errors="replace")
        check("no_obvious_credential:" + rel, not any(p.search(content) for p in secret_patterns))
        # The validator necessarily contains its own scaffold and filename patterns.
        if rel != "scripts/validate_release.py":
            check("no_unfinished_scaffold:" + rel, not scaffolds.search(content))
        check("no_large_source_material:" + rel, not (len(raw) > 100_000 and path.suffix.lower() in {".md", ".txt", ".rst"} and not rel.startswith("evaluations/")))
        if path.suffix.lower() == ".md":
            prose = re.sub(r"^```[^\n]*\n.*?^```[^\n]*$", "", content, flags=re.M | re.S)
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", prose):
                target = target.split("#", 1)[0].strip("<>")
                if not target or re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target) or "$" in target:
                    continue
                resolved = path.parent / target
                check("relative_link:" + rel + ":" + target, not target.startswith("/") and resolved.exists())
    report["scanned_files"] = len(files)
    report["status"] = "passed" if not report["failed"] else "failed"
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--source-workspace", type=Path)
    args = parser.parse_args()
    report = validate(args.root.resolve(), args.source_workspace)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(bool(report["failed"]))


if __name__ == "__main__":
    main()
