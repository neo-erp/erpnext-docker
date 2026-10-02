#!/usr/bin/env bash
set -euo pipefail
repository_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
dependency_root="$repository_root/frappe_docker"
if [ -e "$dependency_root" ] && [ ! -d "$dependency_root/.git" ]; then
  rmdir -- "$dependency_root"
fi
if [ ! -d "$dependency_root/.git" ]; then
  git clone --no-checkout --filter=blob:none https://github.com/frappe/frappe_docker.git "$dependency_root"
fi
test "$(git -C "$dependency_root" remote get-url origin)" = https://github.com/frappe/frappe_docker.git
test -z "$(git -C "$dependency_root" status --porcelain)"
git -C "$dependency_root" fetch origin 9a54fb709d400791700622128130b7f16e141ad7
git -C "$dependency_root" checkout --detach 9a54fb709d400791700622128130b7f16e141ad7
