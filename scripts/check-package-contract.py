#!/usr/bin/env python3
"""Validate the Anticaptrad polyglot Zed package and implementation matrix."""

from __future__ import annotations

import json
import pathlib
import sys
import tomllib

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXPECTED_DEPS = {"anticaptrad/act-interfaces", "anticaptrad/act-lib"}
REQUIRED: dict[str, tuple[str, tuple[str, ...], tuple[str, ...]]] = {
    "c": ("clients/c", ("CMakeLists.txt", "Makefile", "meson.build"), (".c", ".h")),
    "cpp": ("clients/cpp", ("CMakeLists.txt", "Makefile", "meson.build"), (".cc", ".cpp", ".cxx", ".hpp", ".h")),
    "zig": ("clients/zig", ("build.zig", "build.zig.zon"), (".zig",)),
    "gleam": ("clients/gleam", ("gleam.toml",), (".gleam",)),
    "erlang": ("clients/erlang", ("rebar.config", "erlang.mk"), (".erl", ".hrl")),
    "elixir": ("clients/elixir", ("mix.exs",), (".ex", ".exs")),
    "dart": ("clients/dart", ("pubspec.yaml",), (".dart",)),
    "rust": ("clients/rust", ("Cargo.toml",), (".rs",)),
    "java": ("clients/java", ("pom.xml", "build.gradle", "build.gradle.kts"), (".java",)),
    "golang": ("clients/go", ("go.mod",), (".go",)),
    "python": ("clients/python", ("pyproject.toml", "setup.py", "setup.cfg"), (".py",)),
    "ruby": ("clients/ruby", ("*.gemspec", "Gemfile"), (".rb",)),
    "php": ("clients/php", ("composer.json",), (".php",)),
    "nodejs": ("clients/typescript", ("package.json", "tsconfig.json"), (".ts", ".tsx", ".js", ".mjs")),
    "kotlin": ("clients/kotlin", ("build.gradle.kts", "build.gradle", "pom.xml"), (".kt",)),
    "swift": ("clients/swift", ("Package.swift",), (".swift",)),
}


def load(path: pathlib.Path) -> dict:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def has_marker(base: pathlib.Path, patterns: tuple[str, ...]) -> bool:
    return any(any(base.glob(pattern)) for pattern in patterns)


def has_source(base: pathlib.Path, suffixes: tuple[str, ...]) -> bool:
    return any(path.is_file() and path.suffix.lower() in suffixes for path in base.rglob("*"))


def main() -> int:
    errors: list[str] = []
    manifest = load(ROOT / ".zpkg.toml")
    lock = load(ROOT / ".zpkg.lock")
    package = manifest.get("package", {})
    dependencies = manifest.get("dependencies", {})
    targets = manifest.get("targets", {})
    if package.get("org") != "anticaptrad" or package.get("name") != "act-clients":
        errors.append("package identity must be anticaptrad/act-clients")
    if package.get("repository", {}).get("url") != "https://github.com/anticaptrad/act-clients":
        errors.append("package.repository.url must match the canonical repository")
    if not isinstance(dependencies, dict) or not EXPECTED_DEPS.issubset(dependencies):
        errors.append("act-clients must depend on act-interfaces and act-lib")
        dependencies = dependencies if isinstance(dependencies, dict) else {}
    for dependency in dependencies:
        if dependency.rsplit("/", 1)[-1].endswith(("-cli", "-infra")):
            errors.append(f"forbidden client dependency: {dependency}")
    if lock.get("version") != 1:
        errors.append(".zpkg.lock must use version = 1")
    if not isinstance(targets, dict):
        errors.append("[targets] must be a table")
        targets = {}
    for target, (directory, markers, suffixes) in REQUIRED.items():
        record = targets.get(target)
        if not isinstance(record, dict):
            errors.append(f"missing [targets.{target}]")
            continue
        if record.get("dir") != directory:
            errors.append(f"targets.{target}.dir must be {directory!r}")
            continue
        base = ROOT / directory
        if not base.is_dir():
            errors.append(f"{target}: missing {directory}")
            continue
        if not has_marker(base, markers):
            errors.append(f"{target}: missing native build/package marker from {markers!r}")
        if not has_source(base, suffixes):
            errors.append(f"{target}: missing implementation source with suffixes {suffixes!r}")
    for runtime in ("nodejs", "deno", "bun", "edge"):
        record = targets.get(runtime)
        if not isinstance(record, dict) or record.get("dir") != "clients/typescript":
            errors.append(f"TypeScript runtime target {runtime!r} is missing or misrouted")
    matrix_path = ROOT / "clients/typescript/runtime-matrix.json"
    try:
        matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid or missing TypeScript runtime matrix: {exc}")
    else:
        runtimes = matrix.get("runtimes", {})
        for runtime in ("node", "deno", "bun", "edge"):
            record = runtimes.get(runtime)
            if not isinstance(record, dict) or record.get("supported") is not True or not str(record.get("smoke", "")).strip():
                errors.append(f"TypeScript runtime {runtime!r} lacks support and a smoke command")
    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    if errors:
        return 1
    print(f"validated {len(REQUIRED)} real client slices plus Node, Deno, Bun, and edge runtimes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
