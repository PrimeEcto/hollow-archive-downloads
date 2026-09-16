#!/usr/bin/env python3
"""
Verify a published preset and keep the manifest the launcher reads honest.

The curated preset the launcher installs is a Prism instance export — one zip — and it is
published here rather than with the website, so that installing it does not depend on the
site being up. That makes two documents that have to agree: the archive that was actually
uploaded, and `preset.json`, which is the file the launcher fetches before downloading
anything and checks the archive against.

This script hashes the published zip and writes `preset.json` from those bytes, so the
manifest cannot describe a build that was never published. The launcher reads it from
`raw.githubusercontent.com/<repo>/main/preset.json`, which means a new preset — a mod
added, a config retuned — is a release here and needs no launcher release and no website
deploy.

Contract for preset.json, which is also what the launcher's `import.ts` consumes:

    {
      "version": "1.0.0",
      "url": "https://github.com/<owner>/<repo>/releases/download/preset-1.0.0/hollow-archive.zip",
      "sha256": "...",
      "instanceId": "hollow-archive"
    }

`tag`, `released` and `size` are carried alongside for anyone reading the file by hand;
the launcher ignores what it does not recognise.

Usage:

    # refresh the manifest from a locally built preset (see the launcher's build-prism.mjs)
    python3 scripts/verify-preset.py --assets /path/holding/hollow-archive.zip \\
        --repo PrimeEcto/hollow-archive-downloads --tag preset-1.0.0 --write

    # check the published asset; exits non-zero if the manifest disagrees
    python3 scripts/verify-preset.py --assets assets \\
        --repo PrimeEcto/hollow-archive-downloads --tag preset-1.0.0 --check
"""
import argparse
import datetime
import hashlib
import json
import os
import sys

ASSET_NAME = "hollow-archive.zip"
MANIFEST_NAME = "preset.json"
TAG_PREFIX = "preset-"
DEFAULT_INSTANCE_ID = "hollow-archive"


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
    different preset, so its date must not be inherited."""
    try:
        with open(path, encoding="utf-8") as handle:
            manifest = json.load(handle)
    except (OSError, ValueError):
        return None
    if manifest.get("tag") != tag:
        return None
    return manifest.get("released")


def build_manifest(assets, repo, tag, instance_id, released):
    path = os.path.join(assets, ASSET_NAME)
    if not os.path.isfile(path):
        raise SystemExit(f"no {ASSET_NAME} in {assets}; build it with the launcher's build-prism.mjs")

    if not tag.startswith(TAG_PREFIX):
        raise SystemExit(f"tag {tag} is not a preset release; preset tags start with {TAG_PREFIX}")

    version = tag[len(TAG_PREFIX):]
    if not version:
        raise SystemExit(f"tag {tag} carries no version after {TAG_PREFIX}")

    manifest = {
        "version": version,
        "url": f"https://github.com/{repo}/releases/download/{tag}/{ASSET_NAME}",
        "sha256": sha256_of(path),
        "instanceId": instance_id,
        "tag": tag,
        "released": released,
        "size": os.path.getsize(path),
    }
    return json.dumps(manifest, indent=2) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--assets", required=True, help="directory holding the published preset zip")
    parser.add_argument("--repo", required=True, help="owner/name, used to build the asset URL")
    parser.add_argument("--tag", required=True, help="release tag, e.g. preset-1.0.0")
    parser.add_argument("--instance-id", default=DEFAULT_INSTANCE_ID, help="the instance the launcher installs it as")
    parser.add_argument("--out", default=".", help="directory for preset.json")
    parser.add_argument("--released", help="ISO date for preset.json (default: keep, else today)")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="write preset.json")
    mode.add_argument("--check", action="store_true", help="fail if preset.json is stale")
    args = parser.parse_args()

    manifest_path = os.path.join(args.out, MANIFEST_NAME)
    released = args.released or read_released(manifest_path, args.tag) or datetime.date.today().isoformat()
    manifest = build_manifest(args.assets, args.repo, args.tag, args.instance_id, released)

    if args.check:
        try:
            with open(manifest_path, encoding="utf-8") as handle:
                actual = handle.read()
        except OSError:
            print(f"stale: {manifest_path} is missing", file=sys.stderr)
            return 1
        if actual != manifest:
            print(f"stale: {manifest_path} does not match the published preset", file=sys.stderr)
            print("run with --write and commit the result, then re-run this check", file=sys.stderr)
            return 1
        print(f"ok: {manifest_path} matches the published preset")
        return 0

    if args.write:
        with open(manifest_path, "w", encoding="utf-8") as handle:
            handle.write(manifest)
        entry = json.loads(manifest)
        print(f"wrote {manifest_path}")
        print(f"  {entry['version']}  {entry['size'] // 1024 // 1024} MB  {entry['sha256']}")
        return 0

    print(manifest, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
