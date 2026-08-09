#!/usr/bin/env python3
"""Validate the Anticaptrad Zed manifest and packed target artifacts."""

from __future__ import annotations

import argparse
import io
import pathlib
import tarfile
import tomllib

NATIVE_MANIFESTS = {
    "nodejs": ("package.json",),
    "python": ("pyproject.toml",),
    "golang": ("go.mod",),
    "rust": ("Cargo.toml",),
    "dart": ("pubspec.yaml",),
    "gleam": ("gleam.toml",),
    "erlang": ("rebar.config",),
    "elixir": ("mix.exs",),
    "java": ("pom.xml",),
    "kotlin": ("build.gradle.kts",),
    "ruby": ("anticaptrad-client.gemspec",),
    "php": ("composer.json",),
    "swift": ("Package.swift",),
}


def read_toml(path: pathlib.Path) -> dict:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def validate_manifest(root: pathlib.Path) -> tuple[dict, dict]:
    manifest = read_toml(root / ".zpkg.toml")
    if (root / ".zpkg.lock").read_text(encoding="utf-8").strip() != "version = 1":
        raise ValueError(".zpkg.lock must contain exactly 'version = 1'")

    nested = sorted(
        path.relative_to(root)
        for path in root.rglob(".zpkg.toml")
        if path != root / ".zpkg.toml" and ".vendor" not in path.parts
    )
    if nested:
        raise ValueError(f"nested Zed package envelopes are forbidden: {nested}")

    package = manifest["package"]
    if package.get("org") != "anticaptrad" or package.get("name") != "act-clients":
        raise ValueError("unexpected package identity")

    targets = manifest.get("targets", {})
    required = {"repository", *NATIVE_MANIFESTS}
    missing = sorted(required.difference(targets))
    extras = sorted(set(targets).difference(required))
    if missing or extras:
        raise ValueError(f"target drift: missing={missing}, extras={extras}")
    if targets["repository"].get("dir") != ".":
        raise ValueError("repository target must package the repository root")

    for target, names in NATIVE_MANIFESTS.items():
        source = root / targets[target]["dir"]
        if not source.is_dir():
            raise ValueError(f"missing {target} source directory: {source}")
        for name in names:
            if not (source / name).is_file():
                raise ValueError(f"{target} is missing native manifest {name}")

    return manifest, targets


def validate_artifacts(
    root: pathlib.Path,
    artifacts: pathlib.Path,
    manifest: dict,
    targets: dict,
) -> None:
    package = manifest["package"]
    expected: dict[str, pathlib.Path] = {}
    for target, section in targets.items():
        name = section.get("name", f"{package['name']}-{target}")
        expected[target] = artifacts / f"{package['org']}-{name}-{package['version']}.tar.gz"

    missing = sorted(archive.name for archive in expected.values() if not archive.is_file())
    if missing:
        raise ValueError(f"missing packed artifacts: {missing}")
    actual = set(artifacts.glob("*.tar.gz"))
    if actual != set(expected.values()):
        raise ValueError(f"unexpected artifact count: expected {len(expected)}, got {len(actual)}")

    members: dict[str, list[str]] = {}
    for target, archive in expected.items():
        with tarfile.open(archive, "r:gz") as packed:
            names = packed.getnames()
            if not names or not all(name == "pkg" or name.startswith("pkg/") for name in names):
                raise ValueError(f"{target} artifact contains entries outside pkg/")
            if any(".." in pathlib.PurePosixPath(name).parts for name in names):
                raise ValueError(f"{target} artifact contains path traversal")
            derived_file = packed.extractfile("pkg/.zpkg.toml")
            if derived_file is None:
                raise ValueError(f"{target} artifact omitted its derived manifest")
            derived = tomllib.load(io.BytesIO(derived_file.read()))
        expected_name = targets[target].get("name", f"{package['name']}-{target}")
        if derived["package"]["name"] != expected_name:
            raise ValueError(f"{target} artifact has the wrong package name")
        if derived.get("targets"):
            raise ValueError(f"{target} artifact is still polyglot")
        members[target] = names

    repository_members = members["repository"]
    for target, native_names in NATIVE_MANIFESTS.items():
        source = root / targets[target]["dir"]
        if not any(
            f"pkg/{(source / name).relative_to(source).as_posix()}" in members[target]
            for name in native_names
        ):
            raise ValueError(f"{target} artifact omitted its native manifest")

        source_root = f"pkg/{targets[target]['dir'].strip('./')}"
        source_prefix = f"{source_root}/"
        if not any(name == source_root or name.startswith(source_prefix) for name in repository_members):
            raise ValueError(f"repository artifact omitted the {target} source")
        if any(name == source_root or name.startswith(source_prefix) for name in members[target]):
            raise ValueError(f"{target} artifact was not re-rooted")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-only", action="store_true")
    parser.add_argument("--artifacts", type=pathlib.Path)
    args = parser.parse_args()
    if not args.manifest_only and args.artifacts is None:
        parser.error("provide --manifest-only or --artifacts")

    root = pathlib.Path(__file__).resolve().parents[1]
    manifest, targets = validate_manifest(root)
    if args.artifacts is not None:
        validate_artifacts(root, args.artifacts.resolve(), manifest, targets)
    print(f"validated {len(targets)} Zed targets")


if __name__ == "__main__":
    main()
