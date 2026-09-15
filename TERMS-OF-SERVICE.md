# HollowLauncher Terms of Service

**The Hollow Archive — www.hollowarchive.online**

Version 1.0 — effective 2026-09-15

Please read this agreement before installing HollowLauncher. The Windows installer will not
continue until you accept it. The canonical copy of this text lives with the launcher's source
(`build/TERMS-OF-SERVICE.txt`), and the agreement page in the installer is generated from it, so
the two cannot drift apart.

## In short

HollowLauncher is a free launcher for the Hollow Archive, a Minecraft server. It installs a
Minecraft launcher engine and a curated set of mods and shaders into a folder of its own, keeps
them up to date, and signs you in with your Microsoft account so you can play. It does not touch a
Minecraft or PrismLauncher installation you already have, it does not send us telemetry, and it
does not give you a copy of Minecraft — you still need a Minecraft account of your own.

The sections below are the parts of that summary that matter legally.

## 1. Acceptance

By installing, copying, or using HollowLauncher you agree to these terms. If you are accepting
them for an organisation, you confirm you are allowed to accept them for that organisation. If you
are under the age of majority where you live, you may use HollowLauncher only with the involvement
of a parent or guardian.

## 2. What the launcher installs, and where

**2.1** HollowLauncher installs application files into the folder you choose, and creates Start
menu and desktop shortcuts if you ask it to during setup.

**2.2** On first run it downloads, into a private data folder under your own user profile, a build
of the PrismLauncher engine and the Hollow Archive preset — the Fabric loader, a curated set of
mods, the Complementary Reimagined shader pack, and tuned configuration files.

**2.3** Every download it makes is checked against a published cryptographic hash before it is
used. A download that does not match is discarded rather than installed.

**2.4** HollowLauncher deliberately does not read or write another launcher's data. An existing
PrismLauncher, MultiMC, CurseForge, or vanilla installation on the same computer is left exactly
as it is, and its worlds, accounts, and settings are outside the scope of this agreement.

## 3. Your Minecraft account

**3.1** HollowLauncher does not include, sell, or license Minecraft. You need your own Minecraft:
Java Edition account, and you must comply with the Minecraft End User Licence Agreement and the
Microsoft Services Agreement. HollowLauncher is not affiliated with, endorsed by, or sponsored by
Mojang Studios, Microsoft, or PrismLauncher.

**3.2** Sign-in happens through Microsoft's own device-code flow, in the browser you already use.
Your password is never seen by HollowLauncher and is never stored by it. The launcher stores only
the resulting session token, in the engine's account file inside the private data folder described
above, so the engine can refresh and use it. You can remove it at any time by signing out or by
deleting that folder.

## 4. Acceptable use

You agree not to:

- **(a)** use HollowLauncher or the Hollow Archive server to break any law, or to harass, threaten,
  or defraud anyone;
- **(b)** cheat, exploit, or automate gameplay in ways the server rules forbid, including using
  modified clients to gain an unfair advantage;
- **(c)** redistribute, resell, or repackage the Hollow Archive's own art, world data,
  configuration, or preset files outside the launcher without written permission;
- **(d)** interfere with the server, its launcher, or its download host, including by flooding
  them, probing them, or attempting to make them serve modified content to other players; or
- **(e)** remove or obscure licence notices in HollowLauncher or in any component it downloads.

Server rules are published in the Hollow Archive community and apply on top of these terms while
you play. A breach of the server rules is handled by the server; a breach of this section is a
breach of this agreement.

## 5. Your data and your privacy

**5.1** HollowLauncher does not send analytics, telemetry, advertising identifiers, or crash
reports to the Hollow Archive. There is no "online" beacon of any kind.

**5.2** To do its work, the launcher makes network requests to: the Hollow Archive site (for the
preset and the launcher's own update manifests), Mojang's and Fabric's public APIs (for the game
version and loader metadata), Microsoft's login endpoints (for sign-in), Modrinth, and — only if
you supply an API key yourself — CurseForge. Those services receive what any web request carries,
including your IP address, and their own terms and privacy policies apply to them.

**5.3** Everything the launcher stores is stored locally, under your user profile: the installed
engine and preset, its own small configuration, and your launcher settings. The server keeps the
ordinary gameplay records any Minecraft server keeps, such as your account name, session times,
and in-game actions, as described in the community rules.

## 6. Third-party components and licences

**6.1** The HollowLauncher application is distributed under the licences recorded in its `license`
field: LGPL-3.0-or-later and BSD-3-Clause.

**6.2** The PrismLauncher engine, which HollowLauncher downloads and runs but does not bundle, is a
separate program licensed under GPL-3.0. Its source is available from the PrismLauncher project.
HollowLauncher's own notices, and the notices of the mods, shader packs, and libraries the preset
contains, are installed alongside the files they apply to.

**6.3** Nothing in this agreement grants you rights in the Hollow Archive name, logo, or art beyond
installing and using the launcher.

## 7. Updates

HollowLauncher may update itself, the engine, and the preset. Updates are downloaded from the
sources in section 5.2 and are hash-verified as described in section 2.3. If you do not want an
update, you may stop using the launcher; the installed copy keeps working until its manifests
change shape.

## 8. No warranty

HOLLOWLAUNCHER IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE, AND
NON-INFRINGEMENT. THE AUTHORS AND CONTRIBUTORS DO NOT WARRANT THAT HOLLOWLAUNCHER WILL BE
UNINTERRUPTED, ERROR-FREE, OR COMPATIBLE WITH ANY PARTICULAR COMPUTER, MOD, OR SERVER, AND DO NOT
WARRANT THAT THE HOLLOW ARCHIVE SERVER WILL BE AVAILABLE AT ANY PARTICULAR TIME. THE SERVER IS IN
PREPARATION AND MAY BE TAKEN OFFLINE FOR MAINTENANCE OR CHANGED WITHOUT NOTICE.

## 9. Limitation of liability

TO THE MAXIMUM EXTENT PERMITTED BY LAW, THE AUTHORS, CONTRIBUTORS, AND OPERATORS OF HOLLOWLAUNCHER
AND THE HOLLOW ARCHIVE ARE NOT LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES, OR FOR ANY LOSS OF DATA, PROFITS, OR GOODWILL, ARISING FROM YOUR USE OF OR
INABILITY TO USE HOLLOWLAUNCHER — INCLUDING DAMAGE TO A MINECRAFT WORLD, A MOD PACK, OR SAVED
CONFIGURATION. WHERE LIABILITY CANNOT BE EXCLUDED, IT IS LIMITED TO THE AMOUNT YOU PAID FOR
HOLLOWLAUNCHER, WHICH IS NOTHING.

**9.1** You are responsible for keeping your own backups of anything you care about, including
single-player worlds, and for any modification you make to the preset.

## 10. Termination

You may stop using HollowLauncher at any time by uninstalling it and deleting its data folder.
These terms end when you stop using it, except for the sections that by their nature survive:
licences to third-party components, the disclaimers in sections 8 and 9, and the attribution
requirements in section 6.

## 11. Changes to these terms

These terms may be updated for future versions of HollowLauncher. The version shown at the top of
this document identifies the text you accepted. A later version will be presented for acceptance
again rather than assumed.

## 12. Contact

Questions about these terms, the launcher, or the server:
**[contact@hollowarchive.online](mailto:contact@hollowarchive.online)** ·
[www.hollowarchive.online](https://www.hollowarchive.online)
