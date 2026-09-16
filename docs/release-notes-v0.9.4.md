Pressing Play used to hand the game to the engine's own first-run wizard. It no longer does:
HollowLauncher prepares the engine's settings before it starts it, so the game is what opens.

## Downloads

| Platform | File | SHA-256 |
| --- | --- | --- |
| Windows 10 / 11, 64-bit | `HollowLauncher-0.9.4-setup.exe` | `5c6ed5a0377b46c3da24c63b649867f8e4809803fb5b90c92a9c121303a63b90` |
| Linux x86-64 | `hollowlauncher_0.9.4_amd64.deb` | `737f5fe94ba1d317851a89377009af7ab4c65026b9cfea7bb013cde48fd79fc3` |

**Install this build if pressing Play opened a "Prism Launcher Quick Setup" window asking you to
pick a language.** That window was not a missing setting; it was the game waiting.

## Fixed: the first click on Play opened a stock setup wizard instead of the game

The engine HollowLauncher runs the game on is PrismLauncher, and PrismLauncher has no "have I run
before?" flag. `Application::createSetupWizard()` inspects the state it finds and opens Quick Setup
when any of these is true:

| Condition | True when |
| --- | --- |
| language required | `Language` is empty |
| theme required | `ApplicationTheme` / `IconTheme` is not a theme the build ships — and an empty value does not count as one, so every fresh config trips this |
| Java required | `IgnoreJavaWizard` is false *and* the hostname has changed since `LastHostname`, or `JavaPath` does not resolve |
| paste service required | `PastebinURL` is not empty |
| sign-in required | the engine has no account that owns Minecraft |

The dialog itself is the visible half. The damage was the next line: `if (createSetupWizard())
return;` runs *before* `performMainStartupAction()`, which is where the `--launch` we passed is
handled. While that wizard was open the launch was dropped, so the wizard appeared on *every*
launch on an affected machine — and on Windows the Java condition was true from the first run,
because no `JavaPath` had ever been recorded there.

HollowLauncher now writes the engine's own `prismlauncher.cfg` **in its own engine root** before
every launch, and again the moment the engine finishes installing. Four keys:

- `Language` — from the system locale, as a Qt locale name (`en_US`, `pt_BR`, `zh_Hans`).
- `ApplicationTheme` / `IconTheme` — `dark` and `pe_colored`, both themes the build ships.
- `IgnoreJavaWizard` — set only when a Java 21+ for 1.21.4 is actually found, searching `PATH`, the
  vendor JDK directories, and the Mojang runtime folders the game installs. With no Java present
  the page is left alone, because that page is the only place that says what is missing.

These are defaults, not overrides: a key the engine already has a non-empty value for is left
exactly as it is, so a setting you changed in the engine's own window survives. `IgnoreJavaWizard`
is the one exception — it is a statement about this machine, and a stale one would hide a page you
need. The file is written atomically and only when something is actually missing, so a launch
costs one read. If it cannot be written, the game still starts and the launcher says so rather than
failing silently.

Since every engine invocation passes `--dir` at the launcher's own root, this never reads or
modifies a PrismLauncher, MultiMC or CurseForge installation you already have — including the case
where the launcher is using one, which is what the `10.0.5` title on some Windows machines was.

## Deliberately not changed: window behaviour

Seeding `CloseAfterLaunch` looked like the obvious next line, and it is the wrong one. Prism reads
that setting on *game exit* to bring its main window back, so setting it would pop a PrismLauncher
window every time you quit Minecraft. It is also unnecessary: a Play press passes `--launch`
without `--show-window`, and Prism only creates its main window when that flag is set. What a
player sees while the game prepares is Prism's own progress dialog, which closes itself.

## From 0.9.3, in case you skipped it

0.9.3 published the **engine** — the PrismLauncher build the launcher downloads and runs the game
on — and moved both prerequisite manifests (the engine and the preset) from the website to
`raw.githubusercontent.com/PrimeEcto/hollow-archive-downloads`. Nothing the launcher installs
depends on the marketing site being up. Before 0.9.3 a machine with no PrismLauncher already
installed could not finish setting up at all.

## Read before you run

- **Still not code-signed.** Windows shows "Windows protected your PC" the first time; *More
  info* → *Run anyway*. The SHA-256 above is the integrity guarantee.
- **No preset change in this release.** The preset is on its own track and stays at
  `preset-1.0.1` (49 components, Simple Voice Chat included); installing this build does not
  reinstall or redownload it.
- **Only x86-64 engines are published.** Linux on `arm64` is told plainly that there is no build
  for it rather than being handed one that cannot run.
- **Proximity chat is still client-side only.** The preset carries Simple Voice Chat; the server
  does not run the matching plugin yet, so there is nothing to hear until it does.
- On Linux the package manager has no page for an agreement. The same
  [terms](https://github.com/PrimeEcto/hollow-archive-downloads/blob/main/TERMS-OF-SERVICE.md)
  apply; installing the package means accepting them.

## Licensing

HollowLauncher's front end is LGPL-3.0-or-later AND BSD-3-Clause. The PrismLauncher engine is
GPL-3.0 software, downloaded at first run, not bundled in these installers, and published on this
repository's `engine-*` track; the corresponding source is
<https://github.com/PrismLauncher/PrismLauncher/releases/tag/11.1.0>. See
[LICENSE.md](https://github.com/PrimeEcto/hollow-archive-downloads/blob/main/LICENSE.md).

HollowLauncher is not affiliated with Mojang Studios, Microsoft, or PrismLauncher. The Hollow
Archive name, logo and art belong to the Archive.
