# Licensing and attribution

What ships in a HollowLauncher release, who wrote it, and under what licence. Where a licence
requires source or notices to travel with a binary, this file names where they are.

## The launcher itself

HollowLauncher's front end is the Electron application that these installers contain. It is
distributed under **LGPL-3.0-or-later AND BSD-3-Clause**, the dual licence carried by the SKCraft
Launcher fork that HollowLauncher descends from. That licence text, and the per-file headers,
travel with the launcher source; the `license` field of the packaged application records the same
two licences.

Nothing in the installers is derived from Mojang or Microsoft code.

## The engine (not bundled)

The launcher runs on the **PrismLauncher** engine, which is licensed **GPL-3.0**. The engine is
**not** included in these installers: the launcher downloads its own hash-verified build of it on
first run and runs it against a private data folder. Source for the engine is available from the
[PrismLauncher project](https://github.com/PrismLauncher/PrismLauncher), as GPL-3.0 requires.

This is also why these installers are distributed as a front end over a separately provisioned
engine rather than as one combined binary: the two programs keep their own licences, and a user
who already has PrismLauncher installed keeps that installation untouched.

## The curated preset (not bundled)

The Archive preset is assembled from third-party work, each piece under its own licence:

- **Mods** are downloaded from [Modrinth](https://modrinth.com) and, optionally, CurseForge,
  under the licence each mod's author chose. The launcher installs them unmodified and lists them
  in the launcher's own Mods panel, where each entry keeps its provider metadata.
- **The shader pack** (Complementary Reimagined) is distributed by its author under the terms
  published with it. The launcher does not relicense it.
- **FancyMenu, Konkrete, and Melody** are included in the preset because the Archive's title screen
  layout requires them; they keep their own licences and their notices travel with the jars.

The launcher's add-on browser does not repackage anything: a file installed through it is the
author's own jar or zip, downloaded from the provider's own endpoint and hash-verified.

## Minecraft

Minecraft is Mojang Studios' product. HollowLauncher does not include, sell, or license it, and you
need your own **Minecraft: Java Edition** account to play. Your use of the game is governed by the
Minecraft End User Licence Agreement and the Microsoft Services Agreement.

HollowLauncher is **not** affiliated with, endorsed by, or sponsored by Mojang Studios, Microsoft,
or PrismLauncher. "Minecraft" is a trademark of Mojang Synergies AB.

## The Hollow Archive's own work

The Archive's name, logo, world data, configuration, and art are the Archive's own and are not
licensed for redistribution. Installing the launcher and playing on the server is permission to
*use* them, not to republish them — see section 4(c) of the [terms](TERMS-OF-SERVICE.md).

## These installers are not code-signed

Windows builds carry no Authenticode signature and Linux builds are not signed by a distribution
key, so both report themselves as coming from an unknown publisher. The SHA-256 for each published
file is in [`SHA256SUMS`](SHA256SUMS) and in [`latest.json`](latest.json). Verify before you run,
especially if you did not get the file from this repository.
