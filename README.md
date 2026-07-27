# act-clients

Small, typed clients for the public Anticapitalist Tradition service probes.
The repository is intentionally polyglot: each package under `clients/` can be
released through its native package manager and as an isolated zed package,
while the complete repository is also available as a zed package.

## Packages

| Language | Directory | Native registry |
| --- | --- | --- |
| TypeScript | `clients/typescript` | npm |
| Rust | `clients/rust` | crates.io |
| Dart | `clients/dart` | pub.dev |

All three clients expose `health` (`GET /health`) and `ready` (`GET /ready`).
They reject redirects and turn non-success responses into typed errors.

## Publishing model

- GitHub remains the source repository and tag provenance anchor.
- `anticaptrad/act-clients-repository` is the complete zed snapshot.
- The `nodejs`, `rust`, and `dart` targets are independently installable zed
  packages with only that language's files.
- Native package metadata remains in each language directory, so npm, Cargo,
  and pub can publish the same release separately.

The `Zed package interoperability` workflow performs a no-upload zed publish
dry run and inspects every generated artifact. Native release commands remain
credential-gated and are not run from pull requests.
