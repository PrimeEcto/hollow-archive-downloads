# Releasing HollowLauncher

How v0.9.0 was cut, written down so the next one is the same. The build side lives in the
launcher's own source tree (`HollowLauncher/app`); this repository is the download host, and it
never builds anything itself.

Three things are published here, on separate tracks: **launcher builds** (§1–§6 below), **the
curated preset** (§7), which the launcher installs into its engine, and **the engine build**
(§8), which is the launcher that runs the game at all. The preset changes far more often than
the launcher does, and the engine far less.

## What is needed

- The launcher source, with `app/node_modules` installed (`npm install`).
- `python3` with **Pillow** (the installer art generator uses it).
- On Linux, `dpkg` and `fakeroot`. For the Windows installer on Linux, `wine` — electron-builder
  uses it to write the installer's icon and version resources.
- `gh`, authenticated, with permission to write releases here.

## 1. Bump the version, once

`version` in `HollowLauncher/app/package.json` is the only place it is written. It drives both
artifact names (`HollowLauncher-<version>-setup.exe`, `hollowlauncher_<version>_amd64.deb`), the
`DisplayVersion` in Add/Remove Programs, the Debian package version, and `latest.json`. The tag is
`v` + that version.

## 2. Build the installers

```bash
cd HollowLauncher/app
npm install                     # first time only
npm run dist:deb                # Linux: release/hollowlauncher_<version>_amd64.deb
npm run dist:win                # Windows: release/HollowLauncher-<version>-setup.exe
```

Each `dist:` script runs `npm run art` first, which regenerates the installer bitmaps, the icon
set, and the installer's licence page from `build/TERMS-OF-SERVICE.txt`. The artwork is generated,
not hand-drawn: see `app/scripts/make-installer-art.py` for its provenance, and never edit a file
under `app/build/` by hand.

`electron-builder.yml` is the packaging contract: NSIS options (agreement page, folder choice,
shortcut checkboxes, per-user default) and Debian metadata (maintainer, section, dependencies,
desktop entry, icons).

## 3. Check the packages before publishing them

The things worth looking at, because they are the things a package manager and a store actually
read:

```bash
# Linux
dpkg-deb -I release/hollowlauncher_<version>_amd64.deb      # control fields
dpkg-deb -c release/hollowlauncher_<version>_amd64.deb | head
mkdir -p /tmp/hl-deb && dpkg-deb -x release/hollowlauncher_<version>_amd64.deb /tmp/hl-deb
cat /tmp/hl-deb/usr/share/applications/hollowlauncher.desktop
```

Expect: `Section: games`, a real `Maintainer`, `Homepage`, an icon in every hicolor size from
16 px to 512 px, a desktop entry whose `Categories` line is `Game;RolePlaying;` and whose
`StartupWMClass` matches the desktop file name (`hollowlauncher`), and a `postinst` that creates
`/usr/bin/hollowlauncher`.

For Windows, the installer is a GUI and has to be walked through on a real machine or VM: accept
the agreement, confirm the folder page appears, confirm both shortcut checkboxes, install, and
confirm the shortcuts exist, the app launches, and the uninstaller removes both. **This is the one
step that cannot be done on the Linux build machine.** electron-builder's installer will not
complete a silent install under Wine, and neither will a stock electron-builder installer, so a
Wine smoke test proves nothing either way.

## 4. Publish

```bash
cd HollowLauncher/app
gh release create v<version> \
  --repo PrimeEcto/hollow-archive-downloads \
  --title "HollowLauncher <version>" \
  --notes-file docs/release-notes-v<version>.md \
  release/HollowLauncher-<version>-setup.exe \
  release/hollowlauncher_<version>_amd64.deb
```

Write the notes first, in this repository, next to the previous release's
(`docs/release-notes-v0.9.0.md` is the one to copy the shape from). They are the changelog of
record: the download table, what changed, what to read before running, and the licence summary.

## 5. Let the manifests catch up

Publishing the release triggers [`verify-release`](../.github/workflows/verify-release.yml), which
downloads the assets back out of the release, re-hashes them, and rewrites `SHA256SUMS` and
`latest.json` if they disagree with what was published. A green run means the two files in this
repository describe the bytes in the release.

The same run then attaches both files to the release itself, which is what keeps
`releases/latest/download/latest.json` and `.../SHA256SUMS` resolving to the newest manifests. Do
not upload them by hand as part of a release: the workflow writes them *after* it has hashed the
published bytes, so a hand-uploaded copy is written from the local build and can disagree with
what is in the release. (v0.9.2 shipped without them — the link 404'd until it was noticed — and
v0.9.1 shipped with only `latest.json`, which is why the step exists.)

To do the same thing by hand, from a directory holding the two assets:

```bash
python3 scripts/verify-release.py --assets . \
  --repo PrimeEcto/hollow-archive-downloads --tag v<version> --write
```

Then update the download table at the top of [`README.md`](../README.md) with the new sizes and
hashes, and add a row to its version history.

## 6. Afterwards

- Update the site's `/launcher` page if it links a specific file name — it should prefer the
  `releases/latest/download/latest.json` manifest over a hard-coded asset name, so a release needs
  no site change.
- Older releases stay published. Rolling back is pointing a link at an earlier tag, not deleting
  anything.

## 7. The curated preset

The preset the launcher installs is a Prism instance export: one zip holding `instance.cfg`,
`mmc-pack.json` and the game directory. It lives here rather than on the website so that
installing it does not depend on the site being up, and it is versioned on its own track —
`preset-<version>` — because a mod being added or a config retuned has nothing to do with a
launcher build.

Build it from the server repository:

```bash
cd HollowArchiveServer
node scripts/hollow-preset/build-prism.mjs --out /tmp/hollow-preset --version <version> \
  --url https://github.com/PrimeEcto/hollow-archive-downloads/releases/download/preset-<version>/hollow-archive.zip
```

The builder fails rather than warns if the pack is inconsistent (a missing mod dependency, a
missing title-screen mod), and it prints the archive's sha256. Publish it with `--latest=false`:
this repository's *latest* release is the launcher, and the
`releases/latest/download/latest.json` URL the launcher's update check reads depends on that.

```bash
gh release create preset-<version> \
  --repo PrimeEcto/hollow-archive-downloads \
  --latest=false \
  --title "The Hollow Archive preset <version>" \
  --notes "<what changed, and the sha256 below>" \
  /tmp/hollow-preset/hollow-archive.zip
```

Publishing triggers the same workflow, which re-downloads the archive, hashes it and writes
[`preset.json`](../preset.json) — the document the launcher fetches before it downloads anything:

```json
{
  "version": "<version>",
  "url": "https://github.com/PrimeEcto/hollow-archive-downloads/releases/download/preset-<version>/hollow-archive.zip",
  "sha256": "...",
  "instanceId": "hollow-archive"
}
```

The launcher reads it from `raw.githubusercontent.com/PrimeEcto/hollow-archive-downloads/main/preset.json`,
so the published preset is switched by this repository and nothing else — no launcher release, no
website deploy. To do the workflow's work by hand:

```bash
python3 scripts/verify-preset.py --assets /tmp/hollow-preset \
  --repo PrimeEcto/hollow-archive-downloads --tag preset-<version> --write
```

The sha256 in `preset.json` is what the launcher checks the archive against, and a mismatch
means the install is refused and the download discarded. That is the point: the manifest and the
archive are two statements about the same bytes, and this script is what keeps them from
drifting.

## 8. The engine build

HollowLauncher does not bundle an engine. On first run it downloads a PrismLauncher build,
verifies it against a published SHA-256, and drives it with `--dir`, so a PrismLauncher,
MultiMC or CurseForge installation the player already has is never read or modified. Since that
download is a binary the launcher executes, an unverified one is refused outright — which is
why the manifest has to exist before anyone can finish setting up, and why it is published here
rather than served by the website: the site is a Vercel deployment and a prerequisite must not
depend on it being up.

The published build is unmodified upstream PrismLauncher, re-hosted so the URL and hash are
ours and cannot disappear with someone else's release. Bump it by downloading the two assets,
checking the Linux one against upstream's own `.zsync` (whose SHA-1 upstream publishes), and
publishing them on their own track with `--latest=false`:

```bash
gh release create engine-<version> \
  --repo PrimeEcto/hollow-archive-downloads \
  --latest=false \
  --title "Hollow Archive engine <version>" \
  --notes-file docs/release-notes-engine-<version>.md \
  assets/PrismLauncher-Linux-x86_64.AppImage \
  assets/PrismLauncher-Windows-MinGW-w64-Portable-<version>.zip
```

Publishing triggers the same workflow, which re-downloads the assets, re-hashes them and writes
[`engine.json`](../engine.json) — the document the launcher's `provision.ts` fetches. Expect
`linux.x64` and `windows.x64`; the keys are `process.platform` and `process.arch` verbatim, so a
platform with no entry is one the launcher will say it cannot install. To do the workflow's work
by hand:

```bash
python3 scripts/verify-engine.py --assets assets \
  --repo PrimeEcto/hollow-archive-downloads --tag engine-<version> --write
```

Two rules worth stating because they are easy to get wrong: the AppImage is what a Linux install
chmods and runs, and the Windows zip is unpacked *beside* the binary the launcher runs, so the
assets have to stay upstream's own files — a repacked archive whose `prismlauncher.exe` sits in a
subdirectory installs an engine the launcher cannot find. And the release _must_ carry both
platforms: `verify-engine.py` refuses to write a manifest from a single-asset release, which is
the same rule [`verify-release.py`](verify-release.py) enforces for the installers.

## Known gaps

- **No code signing.** SmartScreen and any Linux trust prompt will describe the publisher as
  unknown. The hashes here are the only integrity guarantee, which is why they exist.
- **No macOS build.** Notarisation is the blocker, not the build.
- **No auto-update.** `latest.json` publishes the URL and hash an updater would need; nothing in
  the launcher consumes it yet.
- **The preset's own history is the release list.** Older `preset-*` releases stay published, so a
  rollback is editing `preset.json` back — but nothing does that automatically, and a player
  halfway through an install would be checking against whatever is committed at that moment.
- **The engine is a re-hosted upstream build, not one of ours.** Nothing is patched, so a
  PrismLauncher bug is not something a HollowLauncher release can fix; what the fork buys us is a
  URL and a hash we control. Only x86-64 is published, so `linux/arm64` says it cannot install.
- **No `copyright` file in the deb.** Debian policy expects `/usr/share/doc/hollowlauncher/copyright`
  summarising the licences; the package carries the licence field and the app carries the notices,
  but the file itself is not shipped yet.
