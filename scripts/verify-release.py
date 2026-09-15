#!/usr/bin/env python3
"""
Verify a release's assets and keep this repository's manifests honest.

The assets are the source of truth. This script hashes the files that were actually
published, writes SHA256SUMS from them, and writes latest.json from the same hashes, so
the website, the launcher's own updater, and a suspicious player are all reading numbers
that came from the bytes rather than from a build log.

Contract for latest.json (published at the repository root, and as a release asset, so
`releases/latest/download/latest.json` is a stable URL):

    {
      "version": "0.9.0",
      "tag": "v0.9.0",
      "released": "2026-09-15",
      "release_url": "https://github.com/<owner>/<repo>/releases/tag/v0.9.0",
      "windows": { "file": ..., "url": ..., "size": ..., "sha256": ... },
      "linux":   { "file": ..., "url": ..., "size": ..., "sha256": ... }
    }

The per-platform object is the shape the launcher's `selfUpdateUrl` reads: a URL and a
hash for the platform being updated.

Usage:

    # refresh the manifests from a local build (HollowLauncher/app/release)
    python3 scripts/verify-release.py --assets ../HollowLauncher/app/release \
        --repo PrimeEcto/hollow-archive-downloads --tag v0.9.0 --write

    # check the published assets in CI; exits non-zero if a manifest disagrees
    python3 scripts/verify-release.py --assets assets \
        --repo PrimeEcto/hollow-archive-downloads --tag v0.9.0 --check
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import sys

WINDOWS_PATTERN = re.compile(r"^HollowLauncher-(?P<version>[0-9][^-]*)-setup\.exe$")
LINUX_PATTERN = re.compile(r"^hollowlauncher_(?P<version>[^_]+)_amd64\.deb$")
CHECKSUMS_NAME = "SHA256SUMS"
MANIFEST_NAME = "latest.json"


def sha256_of(path, chunk=1 << 20):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(chunk)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def find_asset(directory, pattern, platform):
    matches = [name for name in sorted(os.listdir(directory)) if pattern.match(name)]
    if not matches:
        raise SystemExit(f"no {platform} asset matching {pattern.pattern} in {directory}")
    if len(matches) > 1:
        raise SystemExit(f"more than one {platform} asset in {directory}: {', '.join(matches)}")
    return matches[0]


def describe(directory, name, version, repo, tag):
    path = os.path.join(directory, name)
    return {
        "file": name,
        "url": f"https://github.com/{repo}/releases/download/{tag}/{name}",
        "size": os.path.getsize(path),
        "sha256": sha256_of(path),
    }


def read_released(path):
    """Keep the release date stable across re-runs rather than stamping today's date
    every time the workflow touches the manifest."""
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle).get("released")
    except (OSError, ValueError):
        return None


def build_manifests(assets, repo, tag, released):
    windows_name = find_asset(assets, WINDOWS_PATTERN, "windows")
    linux_name = find_asset(assets, LINUX_PATTERN, "linux")

    windows_version = WINDOWS_PATTERN.match(windows_name).group("version")
    linux_version = LINUX_PATTERN.match(linux_name).group("version")
    if windows_version != linux_version:
        raise SystemExit(
            f"the assets disagree about the version: {windows_version} (windows) vs "
            f"{linux_version} (linux)"
        )
    if tag.lstrip("v") != windows_version:
        raise SystemExit(f"tag {tag} does not match the assets' version {windows_version}")

    checksums = "\n".join(
        f"{entry['sha256']}  {entry['file']}"
        for entry in (
            describe(assets, windows_name, windows_version, repo, tag),
            describe(assets, linux_name, linux_version, repo, tag),
        )
    ) + "\n"

    manifest = {
        "version": windows_version,
        "tag": tag,
        "released": released,
        "release_url": f"https://github.com/{repo}/releases/tag/{tag}",
        "windows": describe(assets, windows_name, windows_version, repo, tag),
        "linux": describe(assets, linux_name, linux_version, repo, tag),
    }
    return checksums, json.dumps(manifest, indent=2) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--assets", required=True, help="directory holding the published assets")
    parser.add_argument("--repo", required=True, help="owner/name, used to build asset URLs")
    parser.add_argument("--tag", required=True, help="release tag, e.g. v0.9.0")
    parser.add_argument("--out", default=".", help="directory for SHA256SUMS and latest.json")
    parser.add_argument("--released", help="ISO date for latest.json (default: keep, else today)")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="write the manifests")
    mode.add_argument("--check", action="store_true", help="fail if the manifests are stale")
    args = parser.parse_args()

    manifest_path = os.path.join(args.out, MANIFEST_NAME)
    checksums_path = os.path.join(args.out, CHECKSUMS_NAME)

    released = args.released or read_released(manifest_path) or datetime.date.today().isoformat()
    checksums, manifest = build_manifests(args.assets, args.repo, args.tag, released)

    if args.check:
        stale = []
        for path, expected in ((checksums_path, checksums), (manifest_path, manifest)):
            try:
                with open(path, encoding="utf-8") as handle:
                    actual = handle.read()
            except OSError:
                stale.append(f"{path} is missing")
                continue
            if actual != expected:
                stale.append(f"{path} does not match the published assets")
        if stale:
            for problem in stale:
                print(f"stale: {problem}", file=sys.stderr)
            print(
                "run with --write and commit the result, then re-run this check",
                file=sys.stderr,
            )
            return 1
        print(f"ok: {checksums_path} and {manifest_path} match the published assets")
        return 0

    if args.write:
        with open(checksums_path, "w", encoding="utf-8") as handle:
            handle.write(checksums)
        with open(manifest_path, "w", encoding="utf-8") as handle:
            handle.write(manifest)
        print(f"wrote {checksums_path}")
        print(f"wrote {manifest_path}")
        for platform in ("windows", "linux"):
            entry = json.loads(manifest)[platform]
            print(f"  {platform:8s} {entry['file']}  {entry['size'] // 1024 // 1024} MB  {entry['sha256']}")
        return 0

    print(checksums, end="")
    print(manifest, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
