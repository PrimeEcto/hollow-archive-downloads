A Windows sign-in fix, a way to sign out, and the curated preset is published at last.

## Downloads

| Platform | File | SHA-256 |
| --- | --- | --- |
| Windows 10 / 11, 64-bit | `HollowLauncher-0.9.1-setup.exe` | `1a796a9917a5e310427a9609d8c97f1916935270ef7af73ae8a8309ffa0e85ab` |
| Linux x86-64 | `hollowlauncher_0.9.1_amd64.deb` | `50b3f773822e11c52d3b88a4e2d66592b8730d6c6adfb785949beadd17a9b375` |

## Fixed: signing in failed on Windows

Signing in on a fresh install reported:

```
Sign-in failed: Error: ENOENT: no such file or directory, open
'C:\Users\<you>\AppData\Roaming\HollowLauncher\engine\accounts.json.hollow-tmp'
```

The account is written where the engine reads it, and on a fresh install nothing had created
that folder yet — the engine makes it itself, the first time it is launched, and signing in
happens before that. Linux usually escaped it because the folder tends to already exist there.
The write now creates the folder it is writing into. If you saw that message, this build signs
in; nothing else needs doing.

## New: signing out

**Settings → Account** now has **Sign out** (and **Sign in with Microsoft** when you are not
signed in, which brings up the code dialog). Signing out:

- removes the account you are using from the engine's account file, so the credential stored on
  this machine is gone;
- keeps every *other* account that is in there — if you added one through the engine's own
  account manager, it stays, and the notification names the one that takes over;
- does **not** revoke anything at Microsoft. The token was only ever a file on your machine, and
  deleting it is all a launcher can honestly promise. A game you already started keeps its
  session until that token expires;
- is refused while a sign-in is still waiting for its code, rather than racing with it.

The account chip in the title bar also follows what it says on hover now: signed in, it opens the
engine's account manager; signed out, it starts the sign-in.

## The preset is published

`No verified preset published at ...` is gone. The curated preset — Fabric 1.21.4, 48 mods, the
tuned configs, Complementary Reimagined, the Archive title screen, and `play.hollowarchive.online`
already in your multiplayer list — is published on its own release track beside these installers,
with a manifest the launcher checks the download against before it unpacks anything. Installing it
is now part of the first run with nothing configured.

It is published here rather than with the website on purpose: installing should not depend on the
site being up, and a preset change needs no launcher release and no website deploy.

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
