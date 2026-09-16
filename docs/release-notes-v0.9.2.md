The same launcher, saying what it does in a player's words instead of a modder's. And the curated
preset now includes proximity voice chat.

## Downloads

| Platform | File | SHA-256 |
| --- | --- | --- |
| Windows 10 / 11, 64-bit | `HollowLauncher-0.9.2-setup.exe` | `b7c42b7f6ea3b6ddcff18c983523bb8c1b9827dde0a8ad61dd5701536be6e8cc` |
| Linux x86-64 | `hollowlauncher_0.9.2_amd64.deb` | `3e19237ca701e377d8331f50c221b89fb5ce8b7042a67ae8ec7803a17ce54947` |

## The first screen stopped talking about mods

The line a new player reads before anything else used to be four true facts written in the
vocabulary of installing mods — a loader version, a file count, a shader pack's name:

```
Fabric 1.21.4 · 48 mods
```

To someone who has never installed a mod, that is a reason to close the window. It now says what
they are getting:

```
Hollow — Complementary
Fabric 1.21.4 · Hollow Client
49 components · Performance + Visuals
```

The rest of the chrome follows the same rule:

- **Navigation** reads *Play · Add-ons · Graphics · Setup · Details · Settings* (was *Server ·
  Mods · Shaders · Updates · Ledger*).
- **The status strip** says "Ready to play · 49 components" instead of "Preset verified · 48 mods",
  and "Hollow Client is not installed yet" instead of naming the engine under the hood.
- **First run** is "Step 1 of 2 — getting the client ready", not a paragraph about engine
  provenance and hashes.
- **Details** lists *You play · Version · Components · Graphics · Memory it may use · Where to
  join · Last played · Signed in as*. The loader build, the raw engine path and the managed flag
  are gone; the client row reads "installed by HollowLauncher" or "your own copy, left as it was".
- **Setup** buttons say *Install the client*, *Install the pack*, *Show me the files*. The two raw
  download-address rows are gone.

Nothing is rounded up or invented to sound friendly: an instance that is not ours is never called
a Hollow Client, and an empty launcher says "Nothing installed yet". The **Settings** form is
deliberately left alone — JVM flags, Java path and launch hooks are still there for whoever wants
them. The point is that no first screen asks a player to know what they mean.

## Simple Voice Chat is in the preset

The curated preset was republished as **preset-1.0.1** with `voicechat-fabric-1.21.4-2.6.22` added
(the current release, not the newer beta), so proximity chat is possible on the server side
without anyone installing a mod by hand. It arrives through the preset, not through this launcher
release: an existing install picks it up on the next preset install or update.

Two honest notes about it: the mod is the *client* half, and proximity chat does nothing until the
server runs the matching `voicechat` plugin, which is not live yet. And the preset is on its own
release track, so this launcher build and the preset version move independently — this release
does not require a preset reinstall, and a preset change does not require a launcher release.

## Read before you run

- **These builds are still not code-signed.** Windows will show "Windows protected your PC" the
  first time; *More info* → *Run anyway*. The SHA-256 above is the integrity guarantee, and the two
  numbers are regenerated from the published files by this repository's release workflow.
- **The engine build is still not published.** The launcher will use a PrismLauncher you already
  have installed (without touching its instances, accounts or config), and refuses to download one
  it cannot verify against a published hash. Until that manifest and build exist, a machine with no
  PrismLauncher on it cannot finish the engine step. This is the next gap on the list, and it is
  written down in the launcher's own README rather than only here.
- On Linux the package manager has no page for an agreement. The same
  [terms](https://github.com/PrimeEcto/hollow-archive-downloads/blob/main/TERMS-OF-SERVICE.md)
  apply; installing the package means accepting them.

## Licensing

HollowLauncher's front end is LGPL-3.0-or-later AND BSD-3-Clause. The PrismLauncher engine is
GPL-3.0 software, downloaded at first run and not bundled in these installers. See
[LICENSE.md](https://github.com/PrimeEcto/hollow-archive-downloads/blob/main/LICENSE.md).

HollowLauncher is not affiliated with Mojang Studios, Microsoft, or PrismLauncher. The Hollow
Archive name, logo and art belong to the Archive.
