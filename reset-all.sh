#!/usr/bin/env bash
# Delete only resources explicitly labelled for the selected Compose projects.
set -euo pipefail
projects=()
execute=false
while (($#)); do
    case "$1" in
        --project)
            [[ $# -ge 2 && "$2" =~ ^[a-z0-9][a-z0-9_-]*$ ]] || { echo 'Invalid project name' >&2; exit 64; }
            projects+=("$2"); shift 2 ;;
        --execute) execute=true; shift ;;
        --dry-run) execute=false; shift ;;
        *) echo 'Usage: reset-all.sh --project NAME [--project NAME ...] [--dry-run|--execute]' >&2; exit 64 ;;
    esac
done
((${#projects[@]})) || { echo 'At least one explicit --project is required' >&2; exit 64; }
containers=(); images=(); volumes=(); networks=()
for project in "${projects[@]}"; do
    filter="label=com.docker.compose.project=$project"
    # Complete discovery before allowing any deletion; propagate discovery failures.
    found=$(docker ps --all --quiet --filter "$filter")
    while IFS= read -r id; do [[ -z "$id" ]] || containers+=("$id"); done <<< "$found"
    found=$(docker image ls --quiet --filter "$filter")
    while IFS= read -r id; do [[ -z "$id" ]] || images+=("$id"); done <<< "$found"
    found=$(docker volume ls --quiet --filter "$filter")
    while IFS= read -r id; do [[ -z "$id" ]] || volumes+=("$id"); done <<< "$found"
    found=$(docker network ls --quiet --filter "$filter")
    while IFS= read -r id; do [[ -z "$id" ]] || networks+=("$id"); done <<< "$found"
done
printf 'Projects: %s\n' "${projects[*]}"
for kind in containers images volumes networks; do
    declare -n resources="$kind"
    printf '%s:\n' "$kind"
    if ((${#resources[@]})); then printf '  %s\n' "${resources[@]}"; fi
done
$execute || exit 0
read -r -p "Type '${projects[*]}' to delete these resources: " confirmation || exit 1
[[ "$confirmation" == "${projects[*]}" ]] || { echo 'Cancelled'; exit 1; }
# Never force image/volume/network removal: resources still used elsewhere survive.
((${#containers[@]} == 0)) || docker rm --force "${containers[@]}"
((${#images[@]} == 0)) || docker image rm "${images[@]}"
((${#volumes[@]} == 0)) || docker volume rm "${volumes[@]}"
((${#networks[@]} == 0)) || docker network rm "${networks[@]}"
