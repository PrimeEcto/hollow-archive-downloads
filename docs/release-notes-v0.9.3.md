The engine HollowLauncher needs is published at last, and the launcher now fetches it — and the
preset — from GitHub instead of from the website.

## Downloads

| Platform | File | SHA-256 |
| --- | --- | --- |
| Windows 10 / 11, 64-bit | `HollowLauncher-0.9.3-setup.exe` | `cc75a1cc1772d31b3b9e96efcfe7db3bec6ea4c83deafcf294b4189b9a939135` |
| Linux x86-64 | `hollowlauncher_0.9.3_amd64.deb` | `1ff1617b917660c53301773ff8b20efc4ed6ceab7a1da9b17acc59f77ad68561` |

**Install this build if you were stuck on "No engine build published".** Nothing before it can
finish setting up a client on a machine that has no PrismLauncher already, and that is not a
configuration problem — the file the launcher was looking for had never been published.

## Fixed: there was no engine to install

Setting up a client stopped at:

```
No engine build published for linux/x64. Publish .../launcher/prism/engine.json as
{ "linux": { "x64": { "url": "...", "sha256": "..." } } } and try again.
```

Both halves of that message were true. HollowLauncher does not bundle the engine it runs the game
on — it downloads one and verifies it against a published hash, which is the right default for a
binary a launcher executes. What was missing was the manifest carrying that hash, and the URLs the
launcher had been written to name were worse than missing: `config.ts` pinned PrismLauncher
`12.0.0`, a release that does not exist, so even a manifest would have pointed at 404s.

The engine is now published on its own release track — [`engine-11.1.0`](https://github.com/PrimeEcto/hollow-archive-downloads/releases/tag/engine-11.1.0) —
and [`engine.json`](https://raw.githubusercontent.com/PrimeEcto/hollow-archive-downloads/main/engine.json)
names the URL and hash per platform. It is unmodified upstream **PrismLauncher 11.1.0**: not
patched, not repacked, just re-hosted so the URL and the hash are ours, checked against upstream's
own `.zsync` checksum before publishing. PrismLauncher is GPL-3.0 and the corresponding source is
at <https://github.com/PrismLauncher/PrismLauncher/releases/tag/11.1.0>.

The launcher still refuses anything it cannot verify: a download whose hash does not match is
discarded, not run.

## Changed: nothing the launcher installs comes from the website

The engine manifest was fetched from `www.hollowarchive.online`. The preset already came from
GitHub, and now both do — `raw.githubusercontent.com/PrimeEcto/hollow-archive-downloads` — for the
same reason the preset moved there first: the site is a Vercel deployment, and a first-run
prerequisite should not be able to fail because the marketing site is down. Which manifest a build
reads is now a test in the launcher, not a convention.

Both manifests are written from the published bytes' own hashes by this repository's release
workflow, so neither can describe a build that was never uploaded:

| Manifest | Names | Written by |
| --- | --- | --- |
| `latest.json` | these installers | `scripts/verify-release.py` |
| `preset.json` | the curated preset | `scripts/verify-preset.py` |
| `engine.json` | the engine build | `scripts/verify-engine.py` |

## Read before you run

- **Still not code-signed.** Windows will show "Windows protected your PC" the first time;
  *More info* → *Run anyway*. The SHA-256 above is the integrity guarantee.
- **Only x86-64 engines are published.** On Linux, `arm64` is told plainly that there is no build
  for it rather than being handed something that cannot run. An engine you provide yourself with
  `HOLLOW_PRISM_BINARY`, or an existing PrismLauncher (used without touching its instances,
  accounts or config), still works.
- **This release changes no preset.** The preset is on its own track and stays at
  `preset-1.0.1`; installing this build does not reinstall it or redownload it.
- On Linux the package manager has no page for an agreement. The same
  [terms](https://github.com/PrimeEcto/hollow-archive-downloads/blob/main/TERMS-OF-SERVICE.md)
  apply; installing the package means accepting them.

## Licensing

HollowLauncher's front end is LGPL-3.0-or-later AND BSD-3-Clause. The PrismLauncher engine is
GPL-3.0 software, downloaded at first run, not bundled in these installers, and published on this
repository's `engine-*` track. See
[LICENSE.md](https://github.com/PrimeEcto/hollow-archive-downloads/blob/main/LICENSE.md).

HollowLauncher is not affiliated with Mojang Studios, Microsoft, or PrismLauncher. The Hollow
Archive name, logo and art belong to the Archive.
