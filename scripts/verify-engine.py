#!/usr/bin/env python3
"""
Verify a published engine build and keep the manifest the launcher reads honest.

HollowLauncher does not bundle Minecraft's engine: it downloads a PrismLauncher build on first
run and runs it with `--dir`, so a player's own PrismLauncher (or MultiMC, or CurseForge) is
never touched. That download is a binary the launcher then executes, which is the one place a
launcher can hand someone else's code the keys — so it is refused outright unless it matches a
published hash. This script is what publishes that hash.

The engine is published here, on `PrimeEcto/hollow-archive-downloads`, rather than served by the
website: the site is a Vercel deployment and a prerequisite download must not depend on it being
up. `engine.json` at the repository root is the document the launcher fetches, and it is written
from the published bytes rather than from a build machine, so it cannot describe a build that
was never uploaded.

Contract for engine.json, which is also what the launcher's `provision.ts` consumes:

    {
      "linux":   { "x64": { "url": "...", "sha256": "..." } },
      "windows": { "x64": { "url": "...", "sha256": "..." } }
    }

`version`, `tag`, `released`, `source` and the per-platform `file`/`size` are carried alongside
for anyone reading the file by hand; the launcher ignores what it does not recognise, and an
architecture with no entry (arm64, today) is a platform the launcher will say it cannot install.

Usage:

    # refresh the manifest from freshly built or downloaded engine assets
    python3 scripts/verify-engine.py --assets /path/holding/the/assets \\
        --repo PrimeEcto/hollow-archive-downloads --tag engine-11.1.0 --write

    # check the published asset; exits non-zero if the manifest disagrees
    python3 scripts/verify-engine.py --assets assets \\
        --repo PrimeEcto/hollow-archive-downloads --tag engine-11.1.0 --check
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import sys

# Upstream's own file names, kept verbatim: these are re-published PrismLauncher builds, not
# repacked ones, so renaming them would only make the provenance harder to check.
LINUX_PATTERN = re.compile(r"^PrismLauncher-Linux-x86_64\.AppImage$")
WINDOWS_PATTERN = re.compile(r"^PrismLauncher-Windows-MinGW-w64-Portable-.*\.zip$")
MANIFEST_NAME = "engine.json"
TAG_PREFIX = "engine-"
# The launcher's EngineManifest keys are `process.platform`, and its inner keys `process.arch`.
PLATFORMS = (
    ("linux", LINUX_PATTERN, "x64"),
    ("windows", WINDOWS_PATTERN, "x64"),
)


def sha256_of(path, chunk=1 << 20):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(chunk)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def read_released(path, tag):
    """Keep the release date stable across re-runs of the same tag rather than stamping
    today's date every time the workflow touches the manifest. A different tag is a
    different engine build, so its date must not be inherited."""
    try:
        with open(path, encoding="utf-8") as handle:
            manifest = json.load(handle)
    except (OSError, ValueError):
        return None
    if manifest.get("tag") != tag:
        return None
    return manifest.get("released")


def find_asset(directory, pattern, platform):
    matches = [name for name in sorted(os.listdir(directory)) if pattern.match(name)]
    if not matches:
        raise SystemExit(f"no {platform} engine asset matching {pattern.pattern} in {directory}")
    if len(matches) > 1:
        raise SystemExit(f"more than one {platform} engine asset in {directory}: {', '.join(matches)}")
    return matches[0]


def build_manifest(assets, repo, tag, released):
    if not tag.startswith(TAG_PREFIX):
        raise SystemExit(f"tag {tag} is not an engine release; engine tags start with {TAG_PREFIX}")

    version = tag[len(TAG_PREFIX):]
    if not version:
        raise SystemExit(f"tag {tag} carries no version after {TAG_PREFIX}")
    # The Windows asset carries the version in its name and the AppImage does not, so the
    # check is "at least one of them agrees with the tag", which catches a tag pointing at
    # the wrong build while still allowing upstream's own file names through.
    if not any(version in name for name in os.listdir(assets)):
        raise SystemExit(
            f"tag {tag} names version {version}, which none of the assets in {assets} carries: "
            f"{', '.join(sorted(os.listdir(assets)))}"
        )

    manifest = {
        "version": version,
        "tag": tag,
        "released": released,
        "source": f"https://github.com/PrismLauncher/PrismLauncher/releases/tag/{version}",
        "license": "GPL-3.0",
    }
    for platform, pattern, arch in PLATFORMS:
        name = find_asset(assets, pattern, platform)
        path = os.path.join(assets, name)
        manifest[platform] = {
            arch: {
                "file": name,
                "url": f"https://github.com/{repo}/releases/download/{tag}/{name}",
                "size": os.path.getsize(path),
                "sha256": sha256_of(path),
            }
        }

    return json.dumps(manifest, indent=2) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--assets", required=True, help="directory holding the published engine assets")
    parser.add_argument("--repo", required=True, help="owner/name, used to build the asset URLs")
    parser.add_argument("--tag", required=True, help="release tag, e.g. engine-11.1.0")
    parser.add_argument("--out", default=".", help="directory for engine.json")
    parser.add_argument("--released", help="ISO date for engine.json (default: keep, else today)")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="write engine.json")
    mode.add_argument("--check", action="store_true", help="fail if engine.json is stale")
    args = parser.parse_args()

    manifest_path = os.path.join(args.out, MANIFEST_NAME)
    released = args.released or read_released(manifest_path, args.tag) or datetime.date.today().isoformat()
    manifest = build_manifest(args.assets, args.repo, args.tag, released)

    if args.check:
        try:
            with open(manifest_path, encoding="utf-8") as handle:
                actual = handle.read()
        except OSError:
            print(f"stale: {manifest_path} is missing", file=sys.stderr)
            return 1
        if actual != manifest:
            print(f"stale: {manifest_path} does not match the published engine", file=sys.stderr)
            print("run with --write and commit the result, then re-run this check", file=sys.stderr)
            return 1
        print(f"ok: {manifest_path} matches the published engine")
        return 0

    if args.write:
        with open(manifest_path, "w", encoding="utf-8") as handle:
            handle.write(manifest)
        entry = json.loads(manifest)
        print(f"wrote {manifest_path}")
        print(f"  engine {entry['version']}")
        for platform, _, arch in PLATFORMS:
            release = entry[platform][arch]
            print(f"  {platform:8s} {arch:5s} {release['file']}  "
                  f"{release['size'] // 1024 // 1024} MB  {release['sha256']}")
        return 0

    print(manifest, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
