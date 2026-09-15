The first published HollowLauncher installers. Two files, one launcher: a Windows setup wizard and
a Debian package.

## Downloads

| Platform | File | SHA-256 |
| --- | --- | --- |
| Windows 10 / 11, 64-bit | `HollowLauncher-0.9.0-setup.exe` | `c2c8c9e2b34f99c46b9c2157b3767ff38abfa3d1a7a34769df29db81e3720085` |
| Linux x86-64 | `hollowlauncher_0.9.0_amd64.deb` | `7b068b786fd9184a5d759eb31115a248bb57feae3828f5740787e956852325ec` |

## The Windows installer

- The agreement is a real page now. It comes from the same file the repository holds, and **Next**
  stays disabled until it is accepted.
- You choose who it is installed for (just you, the default, or every user) and where it goes.
  Per-user installs need no administrator rights.
- A new **Installation options** page asks about a desktop shortcut and a Start menu entry. Both
  are ticked by default, both can be unticked, and the uninstaller removes exactly what it created.
- Branded throughout: the archive's own emblem and palette on the wizard's header and welcome
  page, an icon set from 16 px to 512 px, and "The Hollow Archive" as the window's brand line.
- Add/Remove Programs now shows a proper publisher, version, support link, and display name.

## The Linux package

- Installs through your distribution's package store — on Pop!_OS, double-clicking the file opens
  the COSMIC store — or with `sudo apt install ./hollowlauncher_0.9.0_amd64.deb`.
- Real Debian metadata: `Section: games`, maintainer and homepage, GTK/NSS/X11 dependencies, and
  hicolor icons in every size.
- The desktop entry carries `Categories=Game;RolePlaying;`, keywords for the applications menu, and
  a `StartupWMClass` that matches the window's app id, so the dock links the running launcher to its
  own icon instead of showing a second one.
- `postinst`/`postrm` refresh the desktop and icon caches, and create `/usr/bin/hollowlauncher`.

## What the launcher does, unchanged in this release

Sign in with Microsoft, and it provisions and verifies its own PrismLauncher engine and the curated
Archive preset — Fabric 1.21.4, the mods, and Complementary Reimagined — inside a private data
folder. An existing Minecraft, PrismLauncher, MultiMC, or CurseForge installation is never touched.
No telemetry.

## Read before you run

- **These builds are not code-signed.** Windows will show "Windows protected your PC" the first
  time; *More info* → *Run anyway*. Verify the SHA-256 above if you want certainty about what you
  downloaded.
- The engine and the preset download on first run, so the first launch needs an internet
  connection and about 350 MB of space.
- On Linux, the package manager has no page for an agreement. The same
  [terms](https://github.com/PrimeEcto/hollow-archive-downloads/blob/main/TERMS-OF-SERVICE.md) apply;
  installing the package means accepting them.

## Licensing

HollowLauncher's front end is LGPL-3.0-or-later AND BSD-3-Clause. The PrismLauncher engine is
GPL-3.0 software, downloaded at first run and not bundled in these installers. See
[LICENSE.md](https://github.com/PrimeEcto/hollow-archive-downloads/blob/main/LICENSE.md).

HollowLauncher is not affiliated with Mojang Studios, Microsoft, or PrismLauncher.
