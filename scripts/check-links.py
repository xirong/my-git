#!/usr/bin/env python3
from __future__ import annotations

import argparse
import concurrent.futures
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

DOC_ROOTS = [
    "README.md",
    "README_zh.md",
    "README.zh-CN.md",
    "CONTRIBUTING.md",
    "ROADMAP.md",
    "MAINTAINERS.md",
    ".github",
    "00-meta",
    "01-getting-started",
    "02-daily-workflow",
    "03-team-collaboration",
    "04-github-engineering",
    "05-ai-native-development",
    "06-troubleshooting",
    "07-large-repo",
    "08-templates",
    "09-resources",
    "10-company-practices",
]

SKIP_PARTS = {
    ".git",
    "09-resources/legacy",
}

LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
USER_AGENT = "my-git-link-check/1.0 (+https://github.com/xirong/my-git)"
HTTP_TIMEOUT_SECONDS = 12
MAX_WORKERS = 8

# These statuses generally mean the URL exists but the site refuses automated
# checks, requires authentication, or rate-limits the runner.
SOFT_HTTP_STATUSES = {401, 403, 429}
SOFT_ERROR_HOSTS = {
    "about.gitlab.com",
}


@dataclass(frozen=True)
class LinkOccurrence:
    path: Path
    line: int
    raw: str


@dataclass(frozen=True)
class ExternalCheckResult:
    url: str
    ok: bool
    message: str
    soft: bool = False


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def is_skipped(path: Path) -> bool:
    rel_path = rel(path)
    return any(rel_path == part or rel_path.startswith(part + "/") for part in SKIP_PARTS)


def markdown_files() -> list[Path]:
    files: list[Path] = []
    for item in DOC_ROOTS:
        path = REPO_ROOT / item
        if not path.exists():
            continue
        if path.is_file() and path.suffix == ".md" and not is_skipped(path):
            files.append(path)
        elif path.is_dir():
            files.extend(
                p for p in path.rglob("*.md")
                if p.is_file() and not is_skipped(p)
            )
    return sorted(set(files))


def normalize_target(raw: str) -> str:
    target = raw.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()
    return target


def strip_fragment(target: str) -> str:
    return target.split("#", 1)[0]


def collect_links(files: list[Path]) -> list[LinkOccurrence]:
    links: list[LinkOccurrence] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        for match in LINK_PATTERN.finditer(text):
            line = text[:match.start()].count("\n") + 1
            links.append(LinkOccurrence(path=path, line=line, raw=match.group(1)))
    return links


def is_external(target: str) -> bool:
    return target.startswith(("http://", "https://"))


def check_empty_links(links: list[LinkOccurrence]) -> list[str]:
    errors: list[str] = []
    for link in links:
        if not normalize_target(link.raw):
            errors.append(f"{rel(link.path)}:{link.line}: empty link target")
    return errors


def check_local_links(links: list[LinkOccurrence]) -> list[str]:
    errors: list[str] = []
    for link in links:
        target = normalize_target(link.raw)
        if not target or target.startswith(("#", "mailto:")) or is_external(target):
            continue

        local_target = urllib.parse.unquote(strip_fragment(target))
        if not local_target:
            continue

        resolved = (link.path.parent / local_target).resolve()
        if not resolved.exists():
            errors.append(f"{rel(link.path)}:{link.line}: broken local link: {target}")
    return errors


def request_url(url: str, method: str) -> tuple[int, str]:
    request = urllib.request.Request(
        url,
        method=method,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT_SECONDS) as response:
        return response.status, response.geturl()


def check_external_url(url: str) -> ExternalCheckResult:
    last_error = ""
    host = urllib.parse.urlparse(url).netloc.lower()
    for attempt in range(2):
        try:
            status, final_url = request_url(url, "HEAD")
            if status < 400:
                suffix = "" if final_url == url else f" -> {final_url}"
                return ExternalCheckResult(url=url, ok=True, message=f"HTTP {status}{suffix}")
            if status in SOFT_HTTP_STATUSES:
                return ExternalCheckResult(url=url, ok=True, message=f"HTTP {status}", soft=True)
            return ExternalCheckResult(url=url, ok=False, message=f"HTTP {status}")
        except urllib.error.HTTPError as error:
            if error.code == 405:
                try:
                    status, final_url = request_url(url, "GET")
                    if status < 400:
                        suffix = "" if final_url == url else f" -> {final_url}"
                        return ExternalCheckResult(url=url, ok=True, message=f"HTTP {status}{suffix}")
                    if status in SOFT_HTTP_STATUSES:
                        return ExternalCheckResult(url=url, ok=True, message=f"HTTP {status}", soft=True)
                    return ExternalCheckResult(url=url, ok=False, message=f"HTTP {status}")
                except Exception as get_error:  # noqa: BLE001
                    last_error = f"{type(get_error).__name__}: {get_error}"
            elif error.code in SOFT_HTTP_STATUSES:
                return ExternalCheckResult(url=url, ok=True, message=f"HTTP {error.code}", soft=True)
            else:
                return ExternalCheckResult(url=url, ok=False, message=f"HTTP {error.code}")
        except Exception as error:  # noqa: BLE001
            last_error = f"{type(error).__name__}: {error}"

        if attempt == 0:
            time.sleep(1)

    if host in SOFT_ERROR_HOSTS:
        return ExternalCheckResult(url=url, ok=True, message=last_error or "request failed", soft=True)

    return ExternalCheckResult(url=url, ok=False, message=last_error or "request failed")


def external_urls(links: list[LinkOccurrence]) -> dict[str, list[LinkOccurrence]]:
    urls: dict[str, list[LinkOccurrence]] = {}
    for link in links:
        target = normalize_target(link.raw)
        if not is_external(target):
            continue
        url = strip_fragment(target)
        if not url:
            continue
        urls.setdefault(url, []).append(link)
    return urls


def check_external_links(links: list[LinkOccurrence]) -> tuple[list[str], list[str]]:
    urls = external_urls(links)
    errors: list[str] = []
    warnings: list[str] = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        results = list(executor.map(check_external_url, sorted(urls)))

    for result in results:
        occurrences = urls[result.url]
        first = occurrences[0]
        locations = ", ".join(f"{rel(item.path)}:{item.line}" for item in occurrences[:3])
        if len(occurrences) > 3:
            locations += f", ... {len(occurrences)} total"

        if result.ok and result.soft:
            warnings.append(f"{locations}: external link blocked or rate-limited: {result.url} ({result.message})")
        elif not result.ok:
            errors.append(f"{rel(first.path)}:{first.line}: broken external link: {result.url} ({result.message})")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Markdown local and external links.")
    parser.add_argument(
        "--no-external",
        action="store_true",
        help="Only check empty and local links.",
    )
    args = parser.parse_args()

    files = markdown_files()
    links = collect_links(files)

    errors: list[str] = []
    warnings: list[str] = []

    errors.extend(check_empty_links(links))
    errors.extend(check_local_links(links))

    if not args.no_external:
        external_errors, external_warnings = check_external_links(links)
        errors.extend(external_errors)
        warnings.extend(external_warnings)

    for warning in warnings:
        print(f"warning: {warning}")

    if errors:
        print("failed: links")
        for error in errors:
            print(f"  {error}")
        return 1

    print(f"ok: checked {len(files)} markdown files and {len(links)} links")
    return 0


if __name__ == "__main__":
    sys.exit(main())
