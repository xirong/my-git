#!/usr/bin/env python3
"""Run a fully local Agent change-control exercise with real Git and HTTP evidence."""

from __future__ import annotations

import argparse
import ast
import hashlib
import io
import json
import os
import select
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.request
from pathlib import Path
from textwrap import dedent


MARKER_NAME = ".ai-change-control-lab-marker"
MARKER_VALUE = "ai-change-control-lab-v1\n"
EXPECTED_NEGATIVE_MESSAGE = (
    "empty timeout must default to 30; got SERVICE_TIMEOUT must be set"
)
BASE_NOTE = "owner=human\nnote=keep this unrelated edit out of the candidate\n"
DIRTY_NOTE = "owner=human\nnote=unrelated-local-edit\n"


BASE_APP = dedent(
    """
    import argparse
    import json
    import os
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    from pathlib import Path
    from urllib.parse import urlparse


    APP_VERSION = "baseline-explicit-timeout"


    def resolve_timeout(raw):
        if raw is None or raw == "":
            raise ValueError("SERVICE_TIMEOUT must be set")
        try:
            value = int(raw)
        except ValueError as error:
            raise ValueError("SERVICE_TIMEOUT must be an integer") from error
        if value <= 0:
            raise ValueError("SERVICE_TIMEOUT must be positive")
        return value


    def load_build_info():
        build_info_path = Path(__file__).with_name("build-info.json")
        if not build_info_path.exists():
            return {"candidate_commit": "source-tree"}
        return json.loads(build_info_path.read_text(encoding="utf-8"))


    def append_event(state_file, payload):
        state_file.parent.mkdir(parents=True, exist_ok=True)
        with state_file.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, sort_keys=True) + "\\n")


    def event_count(state_file):
        if not state_file.exists():
            return 0
        return len(state_file.read_text(encoding="utf-8").splitlines())


    def make_handler(state_file):
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                return

            def write_json(self, status, payload):
                body = json.dumps(payload, sort_keys=True).encode("utf-8")
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_GET(self):
                if urlparse(self.path).path != "/health":
                    self.write_json(404, {"error": "not found"})
                    return
                try:
                    timeout = resolve_timeout(os.environ.get("SERVICE_TIMEOUT"))
                except ValueError as error:
                    self.write_json(400, {"error": str(error), "version": APP_VERSION})
                    return
                build_info = load_build_info()
                event = {
                    "candidate_commit": build_info["candidate_commit"],
                    "timeout": timeout,
                    "version": APP_VERSION,
                }
                append_event(state_file, event)
                self.write_json(
                    200,
                    {
                        "candidate_commit": build_info["candidate_commit"],
                        "event_count": event_count(state_file),
                        "ok": True,
                        "timeout": timeout,
                        "version": APP_VERSION,
                    },
                )

        return Handler


    def main():
        parser = argparse.ArgumentParser()
        parser.add_argument("--serve", action="store_true")
        parser.add_argument("--port", type=int, default=0)
        parser.add_argument("--state-file")
        args = parser.parse_args()
        if not args.serve:
            return
        if not args.state_file:
            raise SystemExit("--state-file is required with --serve")
        server = ThreadingHTTPServer(
            ("127.0.0.1", args.port), make_handler(Path(args.state_file))
        )
        print(
            json.dumps(
                {
                    "event": "listening",
                    "host": "127.0.0.1",
                    "port": server.server_address[1],
                },
                sort_keys=True,
            ),
            flush=True,
        )
        try:
            server.serve_forever(poll_interval=0.1)
        finally:
            server.server_close()


    if __name__ == "__main__":
        main()
    """
).lstrip()

FIXED_APP = BASE_APP.replace(
    'APP_VERSION = "baseline-explicit-timeout"',
    'APP_VERSION = "timeout-default-30"',
).replace(
    '    if raw is None or raw == "":\n'
    '        raise ValueError("SERVICE_TIMEOUT must be set")\n',
    '    if raw is None or raw == "":\n'
    '        return 30\n',
)

BASE_TEST = dedent(
    """
    import unittest

    from app import resolve_timeout


    class TimeoutTests(unittest.TestCase):
        def test_explicit_timeout_is_used(self):
            self.assertEqual(resolve_timeout("15"), 15)

        def test_missing_timeout_is_rejected(self):
            with self.assertRaisesRegex(
                ValueError, "^SERVICE_TIMEOUT must be set$"
            ):
                resolve_timeout(None)

        def test_empty_timeout_is_rejected(self):
            with self.assertRaisesRegex(
                ValueError, "^SERVICE_TIMEOUT must be set$"
            ):
                resolve_timeout("")

        def test_non_integer_timeout_is_rejected(self):
            with self.assertRaisesRegex(
                ValueError, "^SERVICE_TIMEOUT must be an integer$"
            ):
                resolve_timeout("not-a-number")

        def test_non_positive_timeouts_are_rejected(self):
            for raw in ("0", "-1"):
                with self.subTest(raw=raw):
                    with self.assertRaisesRegex(
                        ValueError, "^SERVICE_TIMEOUT must be positive$"
                    ):
                        resolve_timeout(raw)


    if __name__ == "__main__":
        unittest.main()
    """
).lstrip()

TARGET_TEST = dedent(
    """
    import unittest

    from app import resolve_timeout


    class TimeoutTests(unittest.TestCase):
        def test_explicit_timeout_is_used(self):
            self.assertEqual(resolve_timeout("15"), 15)

        def test_missing_timeout_defaults_to_30(self):
            self.assertEqual(resolve_timeout(None), 30)

        def test_empty_timeout_defaults_to_30(self):
            try:
                actual = resolve_timeout("")
            except ValueError as error:
                self.fail(f"empty timeout must default to 30; got {error}")
            self.assertEqual(actual, 30, "empty timeout must default to 30")

        def test_non_integer_timeout_is_rejected(self):
            with self.assertRaisesRegex(
                ValueError, "^SERVICE_TIMEOUT must be an integer$"
            ):
                resolve_timeout("not-a-number")

        def test_non_positive_timeouts_are_rejected(self):
            for raw in ("0", "-1"):
                with self.subTest(raw=raw):
                    with self.assertRaisesRegex(
                        ValueError, "^SERVICE_TIMEOUT must be positive$"
                    ):
                        resolve_timeout(raw)


    if __name__ == "__main__":
        unittest.main()
    """
).lstrip()


class LabError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise LabError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True) + "\n")


def run_command(
    command: list[str],
    *,
    env: dict[str, str],
    cwd: Path | None = None,
    expected: int | None = 0,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if expected is not None and result.returncode != expected:
        command_text = " ".join(command)
        raise LabError(
            f"command exited {result.returncode}, expected {expected}: {command_text}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def run_command_bytes(
    command: list[str], *, env: dict[str, str], expected: int = 0
) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        command,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != expected:
        command_text = " ".join(command)
        raise LabError(
            f"command exited {result.returncode}, expected {expected}: {command_text}\n"
            f"stderr:\n{result.stderr.decode('utf-8', errors='replace')}"
        )
    return result


def ensure_safe_archive_members(archive: tarfile.TarFile, destination: Path) -> None:
    root = destination.resolve()
    for member in archive.getmembers():
        target = (destination / member.name).resolve()
        if target != root and root not in target.parents:
            raise LabError(f"archive member escapes destination: {member.name}")


def extract_tar_bytes(value: bytes, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(value), mode="r:") as archive:
        ensure_safe_archive_members(archive, destination)
        archive.extractall(destination)


def extract_tar_gz(path: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    with tarfile.open(path, mode="r:gz") as archive:
        ensure_safe_archive_members(archive, destination)
        archive.extractall(destination)


def app_version_from_source(path: Path) -> str:
    module = ast.parse(path.read_text(encoding="utf-8"))
    for node in module.body:
        if not isinstance(node, ast.Assign):
            continue
        if not isinstance(node.value, ast.Constant) or not isinstance(node.value.value, str):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "APP_VERSION":
                return node.value.value
    raise LabError(f"APP_VERSION not found in {path}")


def lab_root_is_safe(root: Path) -> bool:
    resolved = root.resolve()
    temp_root = Path(tempfile.gettempdir()).resolve()
    home = Path.home().resolve()
    if resolved == Path("/") or resolved == home:
        return False
    if temp_root != resolved and temp_root not in resolved.parents:
        return False
    if not resolved.name.startswith("ai-change-control-"):
        return False
    marker = resolved / MARKER_NAME
    return marker.is_file() and marker.read_text(encoding="utf-8") == MARKER_VALUE


def cleanup_root(root: Path) -> None:
    if not lab_root_is_safe(root):
        raise LabError(f"refusing to remove an unmarked or unsafe lab root: {root}")
    shutil.rmtree(root)


class Exercise:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.repo = root / "agent-worktree"
        self.git_area = root / "git-isolation"
        self.template_dir = self.git_area / "empty-template"
        self.global_config = self.git_area / "empty-global.gitconfig"
        self.artifacts = root / "artifacts"
        self.builds = root / "builds"
        self.runtimes = root / "runtimes"
        self.worktrees = root / "worktrees"
        self.evidence_dir = root / "evidence"
        self.state_file = root / "external-state" / "events.jsonl"
        self.processes: list[subprocess.Popen[str]] = []
        self.env = os.environ.copy()
        self.env.update(
            {
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": str(self.global_config),
                "GIT_EDITOR": "true",
                "GIT_TERMINAL_PROMPT": "0",
                "PYTHONDONTWRITEBYTECODE": "1",
            }
        )

    def prepare(self) -> None:
        require(lab_root_is_safe(self.root), (
            f"lab root is missing its safety marker: {self.root}"
        ))
        remaining = [
            path.name for path in self.root.iterdir() if path.name != MARKER_NAME
        ]
        require(not remaining, (
            f"fresh lab root unexpectedly contains files: {sorted(remaining)}"
        ))
        self.template_dir.mkdir(parents=True)
        write_text(self.global_config, "")
        self.artifacts.mkdir()
        self.builds.mkdir()
        self.runtimes.mkdir()
        self.worktrees.mkdir()
        self.evidence_dir.mkdir()
        run_command(
            [
                "git",
                "-c",
                "init.defaultBranch=main",
                "init",
                "-q",
                f"--template={self.template_dir}",
                str(self.repo),
            ],
            env=self.env,
        )
        hooks = self.repo / ".git" / "lab-hooks"
        hooks.mkdir(parents=True)
        for key, value in (
            ("user.name", "AI Change Control Lab"),
            ("user.email", "lab@example.com"),
            ("commit.gpgSign", "false"),
            ("tag.gpgSign", "false"),
            ("core.hooksPath", str(hooks)),
            ("core.autocrlf", "false"),
            ("gc.auto", "0"),
        ):
            self.git("config", key, value)

    def git(self, *arguments: str, expected: int | None = 0) -> subprocess.CompletedProcess[str]:
        return run_command(
            ["git", "-C", str(self.repo), *arguments],
            env=self.env,
            expected=expected,
        )

    def git_bytes(self, *arguments: str) -> bytes:
        return run_command_bytes(
            ["git", "-C", str(self.repo), *arguments],
            env=self.env,
        ).stdout

    def git_output(self, *arguments: str) -> str:
        return self.git(*arguments).stdout.strip()

    def test_source(self, directory: Path) -> subprocess.CompletedProcess[str]:
        return run_command(
            [sys.executable, "-m", "unittest", "tests.test_timeout"],
            cwd=directory,
            env=self.env,
            expected=None,
        )

    def clean_test_at(self, commit: str, label: str) -> tuple[subprocess.CompletedProcess[str], str]:
        path = self.worktrees / label
        self.git("worktree", "add", "--detach", str(path), commit)
        try:
            status = run_command(
                ["git", "-C", str(path), "status", "--short"],
                env=self.env,
            ).stdout
            require(not status.strip(), f"clean worktree {label} is not clean: {status}")
            tested_sha = run_command(
                ["git", "-C", str(path), "rev-parse", "HEAD"],
                env=self.env,
            ).stdout.strip()
            result = self.test_source(path)
            return result, tested_sha
        finally:
            self.git("worktree", "remove", "--force", str(path))

    def build_artifact(self, commit: str, label: str) -> dict[str, str]:
        build_dir = self.builds / label
        archive_bytes = self.git_bytes(
            "archive", "--format=tar", "--prefix=timeout-service/", commit
        )
        extract_tar_bytes(archive_bytes, build_dir)
        source_dir = build_dir / "timeout-service"
        source_app = source_dir / "app.py"
        source_note = source_dir / "notes" / "agent-scratch.md"
        require(source_app.is_file(), f"{label} archive is missing app.py")
        require(source_note.read_text(encoding="utf-8") == BASE_NOTE, (
            f"{label} artifact included the unrelated working-tree edit"
        ))
        expected_app = self.git_bytes("show", f"{commit}:app.py")
        require(source_app.read_bytes() == expected_app, (
            f"{label} archive app.py does not match commit {commit}"
        ))
        source_version = app_version_from_source(source_app)
        write_json(
            source_dir / "build-info.json",
            {
                "builder": "git-archive",
                "candidate_commit": commit,
                "source_version": source_version,
            },
        )

        artifact_path = self.artifacts / f"{label}-{commit[:12]}.tar.gz"
        with tarfile.open(artifact_path, mode="w:gz") as archive:
            archive.add(source_dir, arcname="timeout-service", recursive=False)
            for path in sorted(
                source_dir.rglob("*"),
                key=lambda current: str(current.relative_to(source_dir)),
            ):
                archive.add(
                    path,
                    arcname=str(Path("timeout-service") / path.relative_to(source_dir)),
                    recursive=False,
                )

        with tarfile.open(artifact_path, mode="r:gz") as archive:
            names = archive.getnames()
        require(
            not any(name.endswith("manifest.json") for name in names),
            f"{label} artifact incorrectly contains its external manifest",
        )

        artifact_sha256 = sha256_file(artifact_path)
        manifest_path = self.artifacts / f"{label}-{commit[:12]}.manifest.json"
        manifest = {
            "artifact_file": artifact_path.name,
            "artifact_sha256": artifact_sha256,
            "candidate_commit": commit,
            "manifest_scope": "external to artifact; not a signature or provenance attestation",
            "source_app_sha256": sha256_bytes(source_app.read_bytes()),
            "source_version": source_version,
        }
        write_json(manifest_path, manifest)
        return {
            "artifact_path": str(artifact_path),
            "artifact_sha256": artifact_sha256,
            "candidate_commit": commit,
            "manifest_path": str(manifest_path),
            "source_version": source_version,
        }

    def verify_artifact(self, record: dict[str, str], label: str) -> Path:
        artifact_path = Path(record["artifact_path"])
        manifest_path = Path(record["manifest_path"])
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        require(
            sha256_file(artifact_path) == manifest["artifact_sha256"],
            f"{label} artifact checksum mismatch: SHA-256 does not match its manifest",
        )
        require(
            manifest["candidate_commit"] == record["candidate_commit"],
            f"{label} manifest has the wrong candidate commit",
        )
        runtime_dir = self.runtimes / label
        extract_tar_gz(artifact_path, runtime_dir)
        source_dir = runtime_dir / "timeout-service"
        build_info = json.loads(
            (source_dir / "build-info.json").read_text(encoding="utf-8")
        )
        require(
            build_info["candidate_commit"] == manifest["candidate_commit"],
            f"{label} build metadata does not match its manifest",
        )
        app_bytes = (source_dir / "app.py").read_bytes()
        require(
            sha256_bytes(app_bytes) == manifest["source_app_sha256"],
            f"{label} runtime app.py hash does not match the manifest",
        )
        expected_app = self.git_bytes(
            "show", f"{manifest['candidate_commit']}:app.py"
        )
        require(
            app_bytes == expected_app,
            f"{label} runtime app.py does not match its recorded Git commit",
        )
        require(
            app_version_from_source(source_dir / "app.py") == manifest["source_version"],
            f"{label} runtime version does not match the manifest",
        )
        return source_dir

    def start_service(self, source_dir: Path, timeout_value: str) -> tuple[subprocess.Popen[str], int]:
        service_env = self.env.copy()
        service_env["SERVICE_TIMEOUT"] = timeout_value
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        process = subprocess.Popen(
            [
                sys.executable,
                "app.py",
                "--serve",
                "--port",
                "0",
                "--state-file",
                str(self.state_file),
            ],
            cwd=str(source_dir),
            env=service_env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.processes.append(process)
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            if process.poll() is not None:
                stderr = process.stderr.read() if process.stderr else ""
                raise LabError(f"artifact service exited before listening: {stderr}")
            require(process.stdout is not None, "service stdout pipe is unavailable")
            ready, _, _ = select.select([process.stdout], [], [], 0.2)
            if not ready:
                continue
            line = process.stdout.readline()
            if not line:
                continue
            try:
                ready_payload = json.loads(line)
            except json.JSONDecodeError as error:
                raise LabError(f"service emitted invalid readiness JSON: {line}") from error
            require(
                ready_payload.get("event") == "listening"
                and ready_payload.get("host") == "127.0.0.1",
                f"unexpected service readiness: {ready_payload}",
            )
            port = ready_payload.get("port")
            require(isinstance(port, int) and port > 0, (
                f"service did not receive a system-assigned port: {ready_payload}"
            ))
            return process, port
        raise LabError("artifact service did not become ready within five seconds")

    def stop_service(self, process: subprocess.Popen[str]) -> None:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
        if process in self.processes:
            self.processes.remove(process)

    def close(self) -> None:
        for process in list(self.processes):
            self.stop_service(process)

    def request_health(self, port: int) -> dict[str, object]:
        url = f"http://127.0.0.1:{port}/health"
        with urllib.request.urlopen(url, timeout=5) as response:
            require(response.status == 200, f"health request returned {response.status}")
            return json.loads(response.read().decode("utf-8"))


def changed_paths(exercise: Exercise, commit: str) -> set[str]:
    output = exercise.git_output(
        "diff-tree", "--no-commit-id", "--name-only", "-r", commit
    )
    return {line for line in output.splitlines() if line}


def dirty_paths(exercise: Exercise) -> set[str]:
    output = exercise.git_output("diff", "--name-only")
    return {line for line in output.splitlines() if line}


def read_events(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]


def reject_tampered_artifact(
    exercise: Exercise, record: dict[str, str]
) -> dict[str, object]:
    source_path = Path(record["artifact_path"])
    tampered_path = source_path.with_name(f"tampered-{source_path.name}")
    shutil.copyfile(source_path, tampered_path)
    with tampered_path.open("ab") as handle:
        handle.write(b"ai-change-control-lab-tamper\n")

    tampered_record = dict(record)
    tampered_record["artifact_path"] = str(tampered_path)
    try:
        exercise.verify_artifact(tampered_record, "tampered candidate")
    except LabError as error:
        message = str(error)
        require(
            "artifact checksum mismatch: SHA-256 does not match its manifest"
            in message,
            f"tampered artifact failed for an unexpected reason: {message}",
        )
        return {
            "artifact_path": str(tampered_path),
            "rejection": message,
        }
    raise LabError("tampered candidate artifact passed startup preflight validation")


def run_exercise(exercise: Exercise) -> dict[str, object]:
    exercise.prepare()

    write_text(exercise.repo / "app.py", BASE_APP)
    write_text(exercise.repo / "tests" / "__init__.py", "")
    write_text(exercise.repo / "tests" / "test_timeout.py", BASE_TEST)
    write_text(exercise.repo / "notes" / "agent-scratch.md", BASE_NOTE)
    exercise.git("add", "app.py", "tests", "notes")
    exercise.git("commit", "-q", "-m", "chore: baseline timeout service")
    baseline_sha = exercise.git_output("rev-parse", "HEAD")

    write_text(exercise.repo / "app.py", FIXED_APP)
    write_text(exercise.repo / "tests" / "test_timeout.py", TARGET_TEST)
    write_text(exercise.repo / "notes" / "agent-scratch.md", DIRTY_NOTE)
    dirty_test = exercise.test_source(exercise.repo)
    require(
        dirty_test.returncode == 0,
        f"dirty worktree test should pass after the local app fix:\n{dirty_test.stderr}",
    )

    exercise.git("add", "tests/test_timeout.py")
    staged_paths = {
        line
        for line in exercise.git_output("diff", "--cached", "--name-only").splitlines()
        if line
    }
    require(staged_paths == {"tests/test_timeout.py"}, (
        f"bad candidate staged unexpected paths: {sorted(staged_paths)}"
    ))
    exercise.git("commit", "-q", "-m", "test: require empty timeout default")
    bad_candidate_sha = exercise.git_output("rev-parse", "HEAD")
    require(
        changed_paths(exercise, bad_candidate_sha) == {"tests/test_timeout.py"},
        "bad candidate did not limit its commit to the target test",
    )
    require(
        dirty_paths(exercise) == {"app.py", "notes/agent-scratch.md"},
        "the source fix and unrelated note were not preserved as working-tree edits",
    )
    require(
        (exercise.repo / "notes" / "agent-scratch.md").read_text(encoding="utf-8")
        == DIRTY_NOTE,
        "the unrelated local note was changed or removed",
    )

    bad_clean_test, bad_tested_sha = exercise.clean_test_at(
        bad_candidate_sha, "bad-candidate"
    )
    bad_output = bad_clean_test.stdout + bad_clean_test.stderr
    require(
        bad_clean_test.returncode == 1,
        f"bad clean candidate returned {bad_clean_test.returncode}, expected 1",
    )
    require(
        EXPECTED_NEGATIVE_MESSAGE in bad_output and "FAIL:" in bad_output,
        "bad clean candidate failed for an unexpected reason",
    )
    require(
        bad_tested_sha == bad_candidate_sha,
        "bad clean test did not execute the recorded bad candidate SHA",
    )

    exercise.git("add", "app.py")
    exercise.git("commit", "-q", "-m", "fix: default empty timeout to 30")
    candidate_sha = exercise.git_output("rev-parse", "HEAD")
    require(
        changed_paths(exercise, candidate_sha) == {"app.py"},
        "fixed candidate commit did not contain only the application fix",
    )
    require(
        dirty_paths(exercise) == {"notes/agent-scratch.md"},
        "the unrelated local note was included or lost after the fixed candidate",
    )

    clean_candidate_test, candidate_tested_sha = exercise.clean_test_at(
        candidate_sha, "good-candidate"
    )
    require(
        clean_candidate_test.returncode == 0,
        f"clean candidate test failed:\n{clean_candidate_test.stderr}",
    )
    require(
        candidate_tested_sha == candidate_sha,
        "clean candidate test did not execute the candidate SHA",
    )

    candidate_artifact = exercise.build_artifact(candidate_sha, "candidate")
    tampered_artifact = reject_tampered_artifact(exercise, candidate_artifact)
    require(
        not exercise.processes and not exercise.state_file.exists(),
        "tampered artifact verification unexpectedly started a service",
    )
    tampered_artifact["external_event_count_before_start"] = 0
    candidate_runtime = exercise.verify_artifact(candidate_artifact, "candidate")
    candidate_process, candidate_port = exercise.start_service(candidate_runtime, "")
    try:
        candidate_response = exercise.request_health(candidate_port)
    finally:
        exercise.stop_service(candidate_process)
    require(candidate_response["timeout"] == 30, "candidate HTTP response did not use 30")
    require(
        candidate_response["version"] == candidate_artifact["source_version"],
        "candidate HTTP version did not match artifact manifest",
    )
    require(
        candidate_response["candidate_commit"] == candidate_sha,
        "candidate HTTP commit did not match the artifact manifest",
    )
    require(
        candidate_response["event_count"] == 1,
        "candidate request did not create exactly one external state event",
    )

    exercise.git("revert", "--no-edit", candidate_sha)
    exercise.git("revert", "--no-edit", bad_candidate_sha)
    rollback_sha = exercise.git_output("rev-parse", "HEAD")
    require(
        exercise.git_bytes("show", f"{rollback_sha}:app.py") == BASE_APP.encode("utf-8"),
        "revert did not restore the baseline application source",
    )
    require(
        exercise.git_bytes("show", f"{rollback_sha}:tests/test_timeout.py")
        == BASE_TEST.encode("utf-8"),
        "revert did not restore the baseline test source",
    )
    require(
        dirty_paths(exercise) == {"notes/agent-scratch.md"},
        "Git reverts changed the unrelated working-tree edit",
    )

    rollback_test, rollback_tested_sha = exercise.clean_test_at(
        rollback_sha, "rollback-candidate"
    )
    require(
        rollback_test.returncode == 0,
        f"clean rollback test failed:\n{rollback_test.stderr}",
    )
    require(
        rollback_tested_sha == rollback_sha,
        "clean rollback test did not execute the rollback SHA",
    )

    rollback_artifact = exercise.build_artifact(rollback_sha, "rollback")
    rollback_runtime = exercise.verify_artifact(rollback_artifact, "rollback")
    rollback_process, rollback_port = exercise.start_service(rollback_runtime, "15")
    try:
        rollback_response = exercise.request_health(rollback_port)
    finally:
        exercise.stop_service(rollback_process)
    require(rollback_response["timeout"] == 15, "rollback HTTP response did not use 15")
    require(
        rollback_response["version"] == rollback_artifact["source_version"],
        "rollback HTTP version did not match artifact manifest",
    )
    require(
        rollback_response["candidate_commit"] == rollback_sha,
        "rollback HTTP commit did not match the artifact manifest",
    )
    require(
        rollback_response["event_count"] == 2,
        "rollback request did not retain the prior external state event",
    )

    events = read_events(exercise.state_file)
    require(len(events) == 2, "external state does not contain two HTTP events")
    require(
        events[0]["candidate_commit"] == candidate_sha
        and events[1]["candidate_commit"] == rollback_sha,
        "Git reverts unexpectedly removed or rewrote the prior external event",
    )
    require(
        (exercise.repo / "notes" / "agent-scratch.md").read_text(encoding="utf-8")
        == DIRTY_NOTE,
        "the unrelated local note was not preserved at the end of the exercise",
    )

    evidence = {
        "baseline_sha": baseline_sha,
        "bad_candidate": {
            "commit_sha": bad_candidate_sha,
            "clean_test_exit_code": bad_clean_test.returncode,
            "clean_test_required_message": EXPECTED_NEGATIVE_MESSAGE,
            "clean_test_stderr": bad_clean_test.stderr,
            "clean_test_stdout": bad_clean_test.stdout,
            "clean_tested_sha": bad_tested_sha,
            "dirty_test_exit_code": dirty_test.returncode,
        },
        "candidate": {
            "artifact": candidate_artifact,
            "clean_test_exit_code": clean_candidate_test.returncode,
            "commit_sha": candidate_sha,
            "http_port": candidate_port,
            "http_response": candidate_response,
            "tested_sha": candidate_tested_sha,
        },
        "external_state": {
            "event_file": str(exercise.state_file),
            "event_count_after_rollback": len(events),
            "events": events,
        },
        "rollback": {
            "artifact": rollback_artifact,
            "clean_test_exit_code": rollback_test.returncode,
            "commit_sha": rollback_sha,
            "http_port": rollback_port,
            "http_response": rollback_response,
            "tested_sha": rollback_tested_sha,
        },
        "scope": {
            "bad_candidate_commit_paths": sorted(
                changed_paths(exercise, bad_candidate_sha)
            ),
            "candidate_commit_paths": sorted(
                changed_paths(exercise, candidate_sha)
            ),
            "unrelated_worktree_path": "notes/agent-scratch.md",
            "unrelated_worktree_value": DIRTY_NOTE.strip(),
        },
        "tampered_artifact": tampered_artifact,
    }
    write_json(exercise.evidence_dir / "exercise-evidence.json", evidence)
    return evidence


def create_root() -> Path:
    root = Path(tempfile.mkdtemp(prefix="ai-change-control-"))
    write_text(root / MARKER_NAME, MARKER_VALUE)
    return root


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the local Agent change-control exercise."
    )
    parser.add_argument(
        "--keep",
        action="store_true",
        help="keep a successful marked temporary root for inspection",
    )
    parser.add_argument(
        "--cleanup",
        metavar="LAB_ROOT",
        help="remove only a marked lab root previously printed by --keep",
    )
    args = parser.parse_args()

    if args.cleanup:
        try:
            cleanup_root(Path(args.cleanup))
        except LabError as error:
            print(f"error: {error}", file=sys.stderr)
            return 1
        print(f"removed lab root: {Path(args.cleanup).resolve()}")
        return 0

    root = create_root()
    exercise = Exercise(root)
    succeeded = False
    try:
        evidence = run_exercise(exercise)
        succeeded = True
        print(
            "ok: scoped commits preserved notes/agent-scratch.md as an unrelated "
            "working-tree edit"
        )
        print(
            "ok: dirty test exited 0 while clean bad candidate exited 1 with the "
            "required timeout message"
        )
        print(
            "ok: clean worktree test passed at candidate "
            f"{evidence['candidate']['commit_sha']}"
        )
        print(
            "ok: candidate artifact SHA-256 "
            f"{evidence['candidate']['artifact']['artifact_sha256']}"
        )
        print(
            "ok: tampered candidate artifact was rejected before start for "
            "checksum mismatch"
        )
        print(
            "ok: candidate artifact HTTP response came from 127.0.0.1 on port "
            f"{evidence['candidate']['http_port']}"
        )
        print(
            "ok: rollback commit "
            f"{evidence['rollback']['commit_sha']} kept external event count "
            f"{evidence['external_state']['event_count_after_rollback']}"
        )
        if args.keep:
            print(f"kept lab root: {root}")
        return 0
    except LabError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    finally:
        exercise.close()
        if not args.keep or not succeeded:
            if root.exists():
                cleanup_root(root)


if __name__ == "__main__":
    raise SystemExit(main())
