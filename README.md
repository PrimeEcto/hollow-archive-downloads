# HollowLauncher downloads

The download host for **HollowLauncher**, the official launcher for
**[The Hollow Archive](https://www.hollowarchive.online)** — a fantasy Minecraft server on
`play.hollowarchive.online`.

This repository holds releases and nothing else. The installers are built from the launcher's
source, published here as release assets, and linked from
[hollowarchive.online/launcher](https://www.hollowarchive.online/launcher). Every asset below is
hash-verified by [`scripts/verify-release.py`](scripts/verify-release.py), which runs automatically
on each release, and the machine-readable result lives in [`latest.json`](latest.json).

## Download

**Latest release: [v0.9.0](https://github.com/PrimeEcto/hollow-archive-downloads/releases/tag/v0.9.0)**

| Platform | Package | Size | SHA-256 |
| --- | --- | --- | --- |
| Windows 10 / 11, 64-bit | [HollowLauncher-0.9.0-setup.exe](https://github.com/PrimeEcto/hollow-archive-downloads/releases/download/v0.9.0/HollowLauncher-0.9.0-setup.exe) | 114 MB | `c2c8c9e2b34f99c46b9c2157b3767ff38abfa3d1a7a34769df29db81e3720085` |
| Linux x86-64 (Debian, Ubuntu, Pop!_OS, Mint) | [hollowlauncher_0.9.0_amd64.deb](https://github.com/PrimeEcto/hollow-archive-downloads/releases/download/v0.9.0/hollowlauncher_0.9.0_amd64.deb) | 102 MB | `7b068b786fd9184a5d759eb31115a248bb57feae3828f5740787e956852325ec` |

One launcher, one job: sign in with Microsoft, and it installs and keeps updated a curated
Fabric 1.21.4 client — the Archive preset, its mods, and the Complementary Reimagined shader
pack — then starts the game with the server already in your multiplayer list. Java Edition is
what this launcher runs.

## Windows

Run `HollowLauncher-0.9.0-setup.exe`. The wizard asks you four things, in this order:

1. **The agreement.** The terms you are accepting are in
   [`TERMS-OF-SERVICE.md`](TERMS-OF-SERVICE.md), shown in full in the installer. **Next** stays
   disabled until you accept them.
2. **Who it is installed for.** *Only me* (the default) or *all users on this computer*. The
   all-users option asks for administrator rights; the default one never does.
3. **Where it goes.** Default is `%LOCALAPPDATA%\Programs\HollowLauncher` for a per-user
   install. Change it if you keep your games somewhere else.
4. **Which shortcuts to create.** A desktop shortcut and a Start menu entry, both ticked. You
   can untick either.

Then it installs, and offers to launch the launcher. Uninstalling is the normal route: **Settings
→ Apps → Installed apps → HollowLauncher → Uninstall**. The uninstaller removes the shortcuts it
created and leaves your worlds, screenshots, and launcher data alone.

**Windows will warn you about this file.** Builds are not code-signed yet, so SmartScreen shows a
"Windows protected your PC" panel the first time. *More info* → *Run anyway* is the honest
description of what that panel means here; check the SHA-256 above if you want to be sure the
file is the one published here. Signing is planned, and this paragraph will be replaced when it
happens.

## Linux

The `.deb` installs like any other package, which means your distribution's own software store
handles it — on Pop!_OS, double-clicking the file opens the COSMIC store and installs it from
there. From a terminal, the same thing:

```bash
sudo apt install ./hollowlauncher_0.9.0_amd64.deb
```

It goes where Debian packages go, not into a directory you pick:

| Path | What it is |
| --- | --- |
| `/opt/HollowLauncher/` | the application |
| `/usr/bin/hollowlauncher` | the command, so `hollowlauncher` works from a terminal |
| `/usr/share/applications/hollowlauncher.desktop` | the menu entry |
| `/usr/share/icons/hicolor/*/apps/hollowlauncher.png` | icons from 16 px to 512 px |

Remove it with `sudo apt remove hollowlauncher`.

A package manager has no page to put an agreement on, so you are not asked to accept one during
the install. The same [terms](TERMS-OF-SERVICE.md) apply to the Linux build as to the Windows
one; installing the package means accepting them, and they are the first thing to read if
anything about the launcher surprises you.

## Verify what you downloaded

```bash
# Linux
sha256sum hollowlauncher_0.9.0_amd64.deb
```

```powershell
# Windows (PowerShell)
Get-FileHash .\HollowLauncher-0.9.0-setup.exe -Algorithm SHA256
```

Compare the result with the table above, or with [`SHA256SUMS`](SHA256SUMS) in this repository,
which is regenerated from the published assets on every release. A mismatch means the file is not
the one published here — do not run it.

### For the site and the launcher

Two generated files describe the current release without anyone having to edit a page by hand:
[`latest.json`](latest.json) (version, per-platform URL, size, SHA-256) and
[`SHA256SUMS`](SHA256SUMS). Both are attached to every release as well, so
`.../releases/latest/download/latest.json` is a link that always resolves to the newest manifest,
and `.../releases/download/<tag>/<file>` is the pattern for one specific file.

## What it needs

- **Windows:** Windows 10 or 11, 64-bit, and a Minecraft: Java Edition account. No Java
  installation needed — the launcher provisions its own engine and runtime.
- **Linux:** a 64-bit distribution with GTK 3 (Debian 12+, Ubuntu 22.04+, Pop!_OS 22.04+,
  Linux Mint 21+). Same account requirement.
- **Space:** about 350 MB once the engine and the curated preset are in place (the installers you
  download are roughly a third of that).
- **Sign-in:** Microsoft. The launcher runs the device-code flow in your browser; your password is
  never seen or stored by it.

## What it installs, and what it never touches

Everything the launcher installs lives in its own folder under your user profile: the PrismLauncher
engine it runs on, the curated preset, and its own settings. A Minecraft, PrismLauncher, MultiMC,
or CurseForge installation you already have is never read or modified, including its worlds and
its accounts. No telemetry is sent anywhere, and there is no "players online" badge on any of this
because there is no honest number to put in one yet.

Prerequisite downloads — the engine and the preset — are verified against published hashes before
they are used. If a download does not match, it is discarded rather than installed.

## Version history

| Version | Date | Windows | Linux | Notes |
| --- | --- | --- | --- | --- |
| 0.9.0 | 2026-09-15 | `HollowLauncher-0.9.0-setup.exe` | `hollowlauncher_0.9.0_amd64.deb` | First published installers: branded setup wizard with the agreement and shortcut options, and a package-manager-ready Linux build. |

## Licensing and attribution

HollowLauncher's front end is distributed under **LGPL-3.0-or-later AND BSD-3-Clause**. The
PrismLauncher engine it runs on is **GPL-3.0** software, downloaded on first run and not bundled in
these installers. The mods, the shader pack, and the games' own licences are described in
[`LICENSE.md`](LICENSE.md). HollowLauncher is not affiliated with, endorsed by, or sponsored by
Mojang Studios, Microsoft, or PrismLauncher.

The Hollow Archive name, logo, and art belong to the Archive.
