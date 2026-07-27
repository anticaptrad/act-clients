# act-clients agent instructions

## Repository restrictions and package invariants

- Do not run `git reset`, `git filter-repo`, or `git clean`.
- Do not run `rm` except when explicitly deleting known temporary or scratch files.
- `dotenv` is blacklisted. Do not install or use it.
- Keep TypeScript, Rust, and Dart client behavior and versions aligned with the root `.zpkg.toml` and native manifests.
- Preserve redirect rejection, typed/bounded non-success errors, and exact `/health` and `/ready` contracts across all clients.
- GitHub tags remain the provenance anchor. Whole-repository and isolated-language Zed artifacts must contain the correct derived manifests, native package manifests, safe paths, and re-rooted layouts.
- Native publishing remains credential-gated and must not run from untrusted pull requests. Pin external GitHub Actions and Zed tool/interface revisions.
- Run native tests/package dry runs and the Zed pack/publish dry-run interoperability workflow before release.

## Instruction discovery

Resolve `$PWD`, walk upward through every parent directory to the filesystem root, read every readable lowercase `agents.md` on that ancestor chain, and apply them root-to-leaf. Do not search siblings. Deduplicate resolved paths/inodes, avoid symlink cycles, and report unreadable files.

## Synchronize with the remote

Before editing, inspect `git status`, current branch, remotes, and default branch. Run `git fetch --all --prune` and create the feature branch from the latest remote default branch. Fetch again before pushing and incorporate upstream changes using repository merge policy.

- avoid git rebase in favor of git merge.
- Never discard remote commits, force-push, rewrite shared history, bypass review, or bypass required CI.

## Resolve Git conflicts semantically

Resolve conflicts by understanding and combining both sides' intent. Do not mechanically choose `ours`, `theirs`, current, or incoming changes. Produce the conceptually correct result while preserving cross-language API parity, package versions, native manifests, Zed whole-repository and isolated-target semantics, redirect/error behavior, provenance, pinned tooling, tests, documentation, configuration, and release behavior. Regenerate or repack artifacts from the merged source rather than selecting one generated output. If intentions are incompatible, make the smallest explicit design decision and document it in the pull request.

After resolving, reread every affected file from the top, run all native package checks and Zed artifact verification, then search the entire worktree for conflict markers:

```sh
grep -RInE '^(<<<<<<<|=======|>>>>>>>)' --exclude-dir=.git .
```

If any marker or suspicious partial resolution remains, repeat semantic resolution from the top and rerun validation. A conflict is resolved only when the result is conceptually coherent and verified, not merely accepted by Git.