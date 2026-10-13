# OSS source contract: neo-erp/erpnext-docker

Linux・WSL環境でERPNextを自己管理するために、Docker Compose構成を確認・調整できます。NERP本体とは独立した配備例です。 / Review and adapt an ERPNext Docker Compose deployment for a self-managed Linux or WSL environment.

## Responsibility boundary

Own only the documented product/interface scope. Reuse applicable managed common components without forcing unrelated dependencies. Separate synthetic source acceptance from actual account, data and deployment acceptance.

Same-function managed packages take priority when their actual capabilities fit. Do not add an unrelated dependency merely to connect organizations. Preserve upstream LICENSE/NOTICE and immutable release/history evidence; unused compatibility sources belong in Git history, not the supported API.

## Package ownership

| Manifest | Package | Distribution policy |
| --- | --- | --- |
| No npm/Cargo package manifest | Repository-owned tools/configuration | Source/image adoption follows the documented owner path |

Manifest versions and publish flags are declarations, not proof of published availability. Public npm exports and Rust implementation/docs belong to the manifests above; generated dist and sibling checkouts are not source-of-truth implementations.

## Source completion criteria

1. The documented purpose, public exports, validators/schema and actual implementation agree. Remove only confirmed-unused aliases, schemas and compatibility adapters after checking consumers; a shared field name does not imply a shared trust responsibility.
2. Runtime and official dependency resolution work from an independent checkout with committed locks. No local sibling artifact, private registry or ambient owner credential is required for the OSS source path.
3. Supported behavior has reproducible examples/playground and functional tests, including invalid input and relevant failure/cancellation/replay/tenant boundaries. A policy-only CI or planning fixture does not prove external effects.
4. CI runs the declared functional acceptance without disguising skipped/unavailable checks as success. Changed public package bytes receive a new reviewed release; immutable old versions are never overwritten.
5. License/NOTICE, security reporting, usage and the actual supported/unsupported scope stay in the owning repository. The owner operates independently of a central private management checkout.
6. Source acceptance, artifact/registry acceptance and production deployment are separate records. This document defines the target; it does not declare unexecuted tests, unreleased APIs or live-account validation completed.

## Existing verification entrypoints

- [.github/workflows/oss-policy.yml](../.github/workflows/oss-policy.yml)
- [.github/workflows/security-regression.yml](../.github/workflows/security-regression.yml)

Use the package scripts/owner CI above and the repository README for exact commands. When schema files exist, their canonical validator and consumer must be checked together; deleting a definition on a text search alone is insufficient.

## Acceptance record

Inventory baseline source: `976744344d1d636e65ac504e0fdb2ecd2ef35fbf`. This baseline records observed files and declared interfaces, not a completed audit. Subsequent source changes are accepted at their exact commit with test evidence. Production hosting, account login, secret custody installation and data migration remain outside source-only acceptance.

## Owned source and acceptance map

[oss-source-map.json](oss-source-map.json) is the tracked map of package
interfaces, declared commands, schemas, functional test sources, examples and CI
jobs. It keeps each responsibility attached to its actual physical source owner.
Public exports are supported only within this repository's responsibility boundary;
a filename or schema declaration does not grant product or cloud authority.

| Package | Canonical manifest | Responsibility/interface |
| --- | --- | --- |
| Repository-owned source/configuration | README and tracked source map | No npm/Cargo package interface is declared |

For source acceptance, run each applicable functional CI job with the committed
locks from an independent checkout. Match public entrypoints to their test/example
sources in the map; test the relevant invalid input and failure boundary as well as
the normal path. Policy-only, skipped and credential-dependent jobs do not establish
functional coverage. Release jobs establish artifact acceptance only when actually
run at the reviewed commit. A source-only/example repository must not be presented
as a complete external service or a released package.

Schema definitions in the map remain owned by their canonical validator and
consumers. An absent schema file means no separate schema file is declared; it does
not mean the runtime interface has no validation. Do not introduce another common
schema solely to mirror an implementation type.
