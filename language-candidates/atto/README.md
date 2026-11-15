# AttoLang candidate client projection

`status_probe.atto` is a real `.atto` source fixture for the **public** health
and readiness probe status policy. It models HTTP 2xx success and explicitly
recognizes 3xx redirects, matching the existing TypeScript client. It does
**not** perform networking, marshal JSON, hold credentials, or offer a usable SDK.

`candidate.json` is deliberately marked `candidate` and `unverified`.
Do **not** add this directory to the production SDK matrix, package/zed publish
targets, or the required-target count before the Rust/Wasm Atto compiler emits
and executes this fixture and the full client implementation satisfies
contract-admission, transport, error, and schema-parity checks.

Run `rustc --edition=2021 --test tests/atto_projection.rs -o /tmp/atto-projection-tests && /tmp/atto-projection-tests` from the repository root
to check the candidate against existing runtime rules and negative canaries.
This is **source/manifest boundary validation**, not Atto compiler verification.
