# Arcel Contributor License Agreement (CLA)

This repository holds the **canonical Contributor License Agreement** for all
Arcel LLC open-source projects, and is the storage backend for CLA
enforcement across the org.

| File | Purpose |
|---|---|
| `cla.md` | The agreement text contributors agree to. |
| `signatures/cla.json` | Central record of signed contributors (written by the CLA action). |

## Why a CLA

Arcel projects are distributed under open-source licenses (MIT, Apache-2.0,
or AGPL-3.0, per project) **and**, where applicable, under proprietary
commercial licenses. Without a CLA, Arcel cannot include an external
contribution in a commercial release, which means we'd have to reject the PR.
The CLA lets anyone contribute while preserving Arcel's ability to sustain
projects commercially.

## How contributors sign

Every Arcel project runs a `.github/workflows/cla.yml` workflow that uses the
[`contributor-assistant/github-action`](https://github.com/contributor-assistant/github-action)
to enforce this CLA. It runs on pull requests, prompts the author to sign,
records signatures in `signatures/cla.json` (this repo), and posts a status
that branch protection can require before merge. No GitHub App install is
needed — it runs entirely in Actions.

A maintainer can also sign a contributor in by adding their GitHub username
to `signatures/cla.json` directly.

## Setting up a project (maintainers)

Add `.github/workflows/cla.yml`:

```yaml
name: CLA Check

on:
  issue_comment:
    types: [created]
  pull_request_target:
    types: [opened, closed, synchronize]

permissions:
  actions: write
  contents: write
  pull-requests: write
  statuses: write

jobs:
  cla:
    name: CLA Assistant
    runs-on: ubuntu-latest
    steps:
      - uses: contributor-assistant/github-action@v2.6.1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          PERSONAL_ACCESS_TOKEN: ${{ secrets.CLA_TOKEN }}
        with:
          path-to-signatures: signatures/cla.json
          path-to-document: https://raw.githubusercontent.com/Arcel-Org/cla/main/cla.md
          branch: main
          allowlist: bot*,*[bot],dependabot*
          remote-organization-name: Arcel-Org
          remote-repo-name: cla
```

And set the `CLA_TOKEN` secret on the project to a token with **write
access to this repo** (e.g. the org admin's PAT or a fine-grained token
scoped to `Arcel-Org/cla`, contents: write). To make the CLA mandatory, add
the CLA status as a required check in the project's branch protection.

## License

The agreement text in `cla.md` is provided for use by Arcel LLC and its
projects. Questions: [legal@arcel.org](mailto:legal@arcel.org).
