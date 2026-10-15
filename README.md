# Arcel Contributor License Agreement (CLA)

This repository holds the **canonical Contributor License Agreement** for all
Arcel LLC open-source projects, and is the storage backend for the
[CLA Assistant](https://cla-assistant.io/) bot.

| File | Purpose |
|---|---|
| `cla.md` | The agreement text contributors agree to. |
| `signatures/contributors.json` | Central record of signed contributors (maintained by the CLA bot). |
| `cla-bot.py` | The CLA enforcement bot, run by each project's `cla.yml` workflow. |
| `signatures/cla.json` | Reserved for CLA Assistant (kept for compatibility). |

## Why a CLA

Arcel projects are distributed under open-source licenses (MIT, Apache-2.0,
or AGPL-3.0, per project) **and**, where applicable, under proprietary
commercial licenses. Without a CLA, Arcel cannot include an external
contribution in a commercial release, which means we'd have to reject the PR.
The CLA lets anyone contribute while preserving Arcel's ability to sustain
projects commercially.

## How contributors sign

Contributors must sign before their contribution is merged. The org runs a
**self-hosted CLA bot** (no external service): each project's
`.github/workflows/cla.yml` runs `cla-bot.py` on every pull request. It:

1. Posts a **CLA** status (required by branch protection) and a comment
   prompting the author to sign.
2. When the author replies `I agree to the Arcel Contributor License
   Agreement`, records their GitHub username in
   `signatures/contributors.json` and flips the status to green.

A maintainer can also sign a contributor in by adding their username to
`signatures/contributors.json` (and keeping `cla-bot.py`'s fields intact).

The alternative third-party path ([CLA Assistant](https://cla-assistant.io/))
remains available if the org ever prefers it.
