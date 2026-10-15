#!/usr/bin/env python3
"""Arcel CLA bot — enforce the Contributor License Agreement on pull requests.

Runs from a GitHub Actions workflow in any Arcel project repo. It:

  1. Resolves the PR author + head commit.
  2. If the event is a comment containing the agreement phrase from the PR
     author, records their signature in the cla repo
     (signatures/contributors.json) using CLA_TOKEN.
  3. Reads the central signature list and posts a CLA status (commit status,
     usable as a required check in branch protection) plus a comment.

Environment (provided by the calling workflow):
  REPO        owner/repo of the project
  PR_NUMBER   pull request number
  EVENT       'pull_request' or 'issue_comment'
  COMMENTER   login of the commenter (issue_comment only)
  BODY        comment body (issue_comment only)
  GH_TOKEN    the project's GITHUB_TOKEN (status + comments in its own repo)
  CLA_TOKEN   a token with write access to the cla repo (optional; only
              needed for the signature-recording step)
"""

import base64
import json
import os
import urllib.request

REPO = os.environ["REPO"]
PR_NUMBER = os.environ["PR_NUMBER"]
EVENT = os.environ["EVENT"]
CLA_REPO = "Arcel-Org/cla"
SIGNATURES_PATH = "signatures/contributors.json"
AGREEMENT = "I agree to the Arcel Contributor License Agreement"
BOT_NAME = "Arcel CLA bot"
BOT_EMAIL = "maintainers@arcel.org"


def gh(method, path, data=None, token=None):
    tok = token or os.environ["GH_TOKEN"]
    req = urllib.request.Request(
        "https://api.github.com" + path,
        method=method,
        headers={
            "Authorization": f"token {tok}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "arcel-cla-bot",
        },
        data=json.dumps(data).encode() if data is not None else None,
    )
    with urllib.request.urlopen(req) as r:
        body = r.read()
        return json.loads(body) if body else None


def gh_file(token):
    """Return (sha, data) for the central signatures file, or (None, None)."""
    try:
        cur = gh("GET", f"/repos/{CLA_REPO}/contents/{SIGNATURES_PATH}", token=token)
        return cur["sha"], json.loads(base64.b64decode(cur["content"]).decode())
    except Exception:
        return None, None


def read_signed(token=None):
    """Read the central signed list. Prefers authenticated (fresh) read."""
    if token:
        _, data = gh_file(token)
        if data and isinstance(data.get("signed"), list):
            return data["signed"]
    try:
        raw = urllib.request.urlopen(
            f"https://raw.githubusercontent.com/{CLA_REPO}/main/{SIGNATURES_PATH}",
            timeout=20,
        ).read()
        return json.loads(raw).get("signed", [])
    except Exception:
        return []


def main():
    pr = gh("GET", f"/repos/{REPO}/pulls/{PR_NUMBER}")
    author = pr["user"]["login"]
    head_sha = pr["head"]["sha"]

    cla_token = os.environ.get("CLA_TOKEN", "")

    # ── Record a signature: an "I agree" comment from the PR author ────────
    if EVENT == "issue_comment":
        commenter = os.environ.get("COMMENTER", "")
        body = os.environ.get("BODY", "")
        if commenter == author and AGREEMENT in body:
            if not cla_token:
                print("::warning::CLA_TOKEN not set — signature not recorded")
            else:
                sha, data = gh_file(cla_token)
                if data is None:
                    data = {"signed": []}
                if commenter not in data.setdefault("signed", []):
                    data["signed"].append(commenter)
                    payload = {
                        "message": f"cla: record signature for {commenter}",
                        "content": base64.b64encode(
                            json.dumps(data, indent=2).encode()
                        ).decode(),
                        "author": {"name": BOT_NAME, "email": BOT_EMAIL},
                        "committer": {"name": BOT_NAME, "email": BOT_EMAIL},
                    }
                    if sha:
                        payload["sha"] = sha
                    gh(
                        "PUT",
                        f"/repos/{CLA_REPO}/contents/{SIGNATURES_PATH}",
                        payload,
                        token=cla_token,
                    )
                    print(f"::notice::Recorded CLA signature for {commenter}")

    signed = read_signed(cla_token)
    is_signed = author in signed
    state = "success" if is_signed else "failure"
    desc = (
        "CLA signed — thanks for contributing!"
        if is_signed
        else f"@{author} must sign the CLA before this can merge (see comment)."
    )

    # ── Post / update one bot comment (keeps PR thread clean) ──────────────
    comment_body = (
        f"✅ **CLA signed** — thanks @{author}!"
        if is_signed
        else (
            f"📝 **CLA required** — to merge this PR, @{author} must sign the "
            f"[Arcel Contributor License Agreement](https://github.com/{CLA_REPO}/blob/main/cla.md). "
            f"Reply on this PR with:\n\n```\n{AGREEMENT}\n```"
        )
    )
    comments = gh("GET", f"/repos/{REPO}/issues/{PR_NUMBER}/comments")
    bot = [c for c in comments if c["body"].startswith(("✅ **CLA", "📝 **CLA"))]
    if bot:
        gh("PATCH", f"/repos/{REPO}/issues/comments/{bot[-1]['id']}", {"body": comment_body})
    else:
        gh("POST", f"/repos/{REPO}/issues/{PR_NUMBER}/comments", {"body": comment_body})

    # ── Commit status (usable as a required check in branch protection) ────
    gh(
        "POST",
        f"/repos/{REPO}/statuses/{head_sha}",
        {
            "state": state,
            "context": "CLA",
            "description": desc[:140],
            "target_url": f"https://github.com/{CLA_REPO}/blob/main/cla.md",
        },
    )
    print(f"CLA status for @{author}: {state}")


if __name__ == "__main__":
    main()
