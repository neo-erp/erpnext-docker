# erpnext-docker

Linux・WSL環境でERPNextを自己管理するために、Docker Compose構成を確認・調整できます。NERP本体とは独立した配備例です。

## 利用前の確認

実装済みの範囲、必要な依存関係、検証コマンドを以下の英語説明に併記しています。操作・配備・公開は、それぞれの権限と設定を確認してから実施してください。

## 使い方

リポジトリ内のサンプル・スキーマ・実装を確認し、用途に必要な入力を明示して利用します。下記のGetting startedに、現行設定に対応する検証コマンドを示しています。

検証結果は実行した範囲だけを示します。未実装の機能、未設定の接続、配備環境の確認を合格扱いにしないでください。

## English

Review and adapt an ERPNext Docker Compose deployment for a self-managed Linux or WSL environment.

## What you can do

- Understand the database, Redis, backend and frontend service composition.
- Choose routing and persistent-storage settings before deployment.

## Current scope

This is an ERPNext deployment example, maintained independently of NERP. Replace example passwords and review image versions, exposure and backups before starting services.

Package distribution is not activated by this documentation. Use the checked-in source and the declared dependency versions; published availability must be verified separately.

## Getting started

Start with the implementation and examples linked below. Review registered configuration and prerequisites before running a command that writes state or contacts a service.

## Documentation and source

[Usage guide](docs/getting-started.md)

[Contributing](CONTRIBUTING.md) · [Security reporting](SECURITY.md) · [License](LICENSE) · [Attribution notices](NOTICE)

## Project-scoped reset

`bash reset-all.sh --project erpnext --dry-run` lists only Docker resources
with the exact `com.docker.compose.project=erpnext` label. Specify additional
`--project NAME` options only for projects you intend to remove. The default
is dry-run; `--execute` requires typing the selected project names before any
deletion. Cancellation or discovery failure stops the script.

Shared or unlabelled images and host-wide caches are retained. Images, volumes
and networks still in use are not forcibly removed. This operation deletes the
selected project's data volumes; inspect the dry-run output and back up data.
No host-wide prune is performed.

Regression checks: `python3 tests/test_reset_all.py` (isolated Docker command fixture).

[OSS responsibility and source completion](docs/oss-source-contract.md) defines the supported package boundary and required acceptance. It does not declare unexecuted source, distribution or production checks complete.
