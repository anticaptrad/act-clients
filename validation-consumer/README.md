# lib-core validation consumer

These client request-boundary adapters import the public validation packages from `act-lib-core`; they do not copy schemas and cannot import server-only packages.

Requests validate `RequestMeta` before transport. Problem responses validate `ProblemDetails` after transport. Route-specific payload validators are selected by `ORESoftware/api-docs` operation IDs once reviewed bindings exist in `act-interfaces`.
