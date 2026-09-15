# Releasing HollowLauncher

How v0.9.0 was cut, written down so the next one is the same. The build side lives in the
launcher's own source tree (`HollowLauncher/app`); this repository is the download host, and it
never builds anything itself.

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

## Known gaps

- **No code signing.** SmartScreen and any Linux trust prompt will describe the publisher as
  unknown. The hashes here are the only integrity guarantee, which is why they exist.
- **No macOS build.** Notarisation is the blocker, not the build.
- **No auto-update.** `latest.json` publishes the URL and hash an updater would need; nothing in
  the launcher consumes it yet.
- **No `copyright` file in the deb.** Debian policy expects `/usr/share/doc/hollowlauncher/copyright`
  summarising the licences; the package carries the licence field and the app carries the notices,
  but the file itself is not shipped yet.
