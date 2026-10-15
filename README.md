# Arcel Contributor License Agreement (CLA)

This repository holds the **canonical Contributor License Agreement** for all
Arcel LLC open-source projects, and is the storage backend for the
[CLA Assistant](https://cla-assistant.io/) bot.

| File | Purpose |
|---|---|
| `cla.md` | The agreement text contributors agree to. |
| `signatures/cla.json` | CLA Assistant's signature store (populated by the bot). |

## Why a CLA

Arcel projects are distributed under open-source licenses (MIT, Apache-2.0,
or AGPL-3.0, per project) **and**, where applicable, under proprietary
commercial licenses. Without a CLA, Arcel cannot include an external
contribution in a commercial release, which means we'd have to reject the PR.
The CLA lets anyone contribute while preserving Arcel's ability to sustain
projects commercially.

## How contributors sign

Contributors must sign before their contribution is merged. Two paths:

1. **CLA Assistant (automatic).** Once the [CLA Assistant GitHub App][app] is
   installed on the org and configured with this repo as its "CLA repository,"
   the bot prompts contributors to sign directly on their pull requests.
2. **Email (manual).** Until the bot is installed (or as a fallback), a
   contributor emails `legal@arcel.org` with the exact text in `cla.md`'s
   *How to sign* section. The process and wording are documented there.

Project `CONTRIBUTING.md` files should point contributors here — see
Relay / Seam / Fob.

## Setting up CLA Assistant (maintainers)

1. Install the [CLA Assistant GitHub App][app] on the Arcel-Org organization.
2. In the app's settings choose **Arcel-Org/cla** as the CLA repository.
   The CLA text is `cla.md` (default path) and signatures are stored in
   `signatures/cla.json` (default layout — already initialized empty).
3. Select the repositories the bot should manage (Relay, Seam, Fob, …).
4. Open a test PR to confirm the bot posts its status.

Until the app is installed, the manual email path above is the operating
process — keep the wording in `cla.md` accurate.

## License

The agreement text in `cla.md` is provided for use by Arcel LLC and its
projects. Questions: [legal@arcel.org](mailto:legal@arcel.org).

[app]: https://cla-assistant.io/
