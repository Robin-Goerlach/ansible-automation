#!/usr/bin/env bash
set -Eeuo pipefail

readonly DEFAULT_REPO_URL="https://github.com/SASD-Sysadmin/ansible-automation.git"
readonly DEFAULT_BRANCH="main"
readonly DEFAULT_TARGET_DIR="${HOME}/.local/src/ansible-automation"
readonly DEFAULT_VENV_DIR="${HOME}/.local/share/sasd-ansible/venv"
readonly MINIMUM_PYTHON_MAJOR=3
readonly MINIMUM_PYTHON_MINOR=12

repo_url="${DEFAULT_REPO_URL}"
branch="${DEFAULT_BRANCH}"
target_dir="${DEFAULT_TARGET_DIR}"
venv_dir="${DEFAULT_VENV_DIR}"
update_existing=false
skip_os_packages=false
skip_collections=false

log() { printf '[sasd-ansible] %s\n' "$*"; }
warn() { printf '[sasd-ansible] WARNING: %s\n' "$*" >&2; }
fail() { printf '[sasd-ansible] ERROR: %s\n' "$*" >&2; exit 1; }

usage() {
  cat <<'EOF'
Usage: bootstrap-control-node.sh [options]

Prepare a supported Linux/WSL control node, clone or update this repository,
create an isolated virtual environment, install the Milestone 2 toolchain, and
optionally install external Ansible collections.

Options:
  --repo-url URL        Git repository URL
  --branch NAME         Branch to clone or update (default: main)
  --target-dir PATH     Repository destination
  --venv-dir PATH       Python virtual environment destination
  --update              Fast-forward an existing clean checkout
  --skip-os-packages    Do not invoke the operating-system package manager
  --skip-collections    Do not contact Ansible Galaxy
  -h, --help            Show this help

Security notes:
  * Review this script before executing it.
  * It never disables SSH host-key checking.
  * It refuses to update a checkout containing local changes.
  * Python packages are installed only in the selected virtual environment.
EOF
}

while (($# > 0)); do
  case "$1" in
    --repo-url) [[ $# -ge 2 ]] || fail "--repo-url requires a value"; repo_url="$2"; shift 2 ;;
    --branch) [[ $# -ge 2 ]] || fail "--branch requires a value"; branch="$2"; shift 2 ;;
    --target-dir) [[ $# -ge 2 ]] || fail "--target-dir requires a value"; target_dir="$2"; shift 2 ;;
    --venv-dir) [[ $# -ge 2 ]] || fail "--venv-dir requires a value"; venv_dir="$2"; shift 2 ;;
    --update) update_existing=true; shift ;;
    --skip-os-packages) skip_os_packages=true; shift ;;
    --skip-collections) skip_collections=true; shift ;;
    -h|--help) usage; exit 0 ;;
    *) fail "Unknown option: $1" ;;
  esac
done

[[ "${target_dir}" = /* ]] || fail "--target-dir must be an absolute path"
[[ "${venv_dir}" = /* ]] || fail "--venv-dir must be an absolute path"
[[ "${target_dir}" != "${venv_dir}" ]] || fail "Repository and virtualenv paths must differ"

run_as_root() {
  if [[ ${EUID} -eq 0 ]]; then "$@"; else sudo "$@"; fi
}

install_os_packages() {
  [[ "${skip_os_packages}" = false ]] || { log "Skipping OS package installation"; return; }
  command -v sudo >/dev/null 2>&1 || [[ ${EUID} -eq 0 ]] || fail "sudo is required"
  [[ -r /etc/os-release ]] || fail "/etc/os-release is unavailable"
  # shellcheck disable=SC1091
  source /etc/os-release
  local distribution=" ${ID:-unknown} ${ID_LIKE:-} "

  case "${distribution}" in
    *" debian "*|*" ubuntu "*)
      run_as_root apt-get update
      run_as_root apt-get install -y ca-certificates curl git openssh-client python3 python3-pip python3-venv rsync
      ;;
    *" fedora "*|*" rhel "*|*" centos "*)
      run_as_root dnf install -y ca-certificates curl git openssh-clients python3 python3-pip rsync
      ;;
    *" suse "*|*" opensuse "*)
      run_as_root zypper --non-interactive refresh
      run_as_root zypper --non-interactive install ca-certificates curl git openssh python3 python3-pip python3-virtualenv rsync
      ;;
    *) fail "Unsupported distribution: ID=${ID:-unknown} ID_LIKE=${ID_LIKE:-}" ;;
  esac
}

require_commands() {
  local command_name
  for command_name in git python3; do
    command -v "${command_name}" >/dev/null 2>&1 || fail "Required command not found: ${command_name}"
  done
}

verify_python_version() {
  python3 - "${MINIMUM_PYTHON_MAJOR}" "${MINIMUM_PYTHON_MINOR}" <<'PYCODE'
import sys
required = tuple(map(int, sys.argv[1:3]))
if sys.version_info[:2] < required:
    raise SystemExit(f"Python {required[0]}.{required[1]}+ required; found {sys.version.split()[0]}")
print(f"Python runtime accepted: {sys.version.split()[0]}")
PYCODE
}

clone_or_update_repository() {
  mkdir -p "$(dirname "${target_dir}")"
  if [[ -d "${target_dir}/.git" ]]; then
    [[ "${update_existing}" = true ]] || { log "Existing checkout left unchanged: ${target_dir}"; return; }
    [[ -z "$(git -C "${target_dir}" status --porcelain)" ]] || fail "Checkout has local changes: ${target_dir}"
    git -C "${target_dir}" fetch --prune origin
    git -C "${target_dir}" checkout "${branch}"
    git -C "${target_dir}" pull --ff-only origin "${branch}"
    return
  fi
  [[ ! -e "${target_dir}" ]] || fail "Target exists but is not a Git checkout: ${target_dir}"
  git clone --branch "${branch}" --single-branch "${repo_url}" "${target_dir}"
}

install_python_tools() {
  mkdir -p "$(dirname "${venv_dir}")"
  python3 -m venv "${venv_dir}"
  "${venv_dir}/bin/python" -m pip install --upgrade pip setuptools wheel
  "${venv_dir}/bin/python" -m pip install -r "${target_dir}/requirements-dev.txt"

  if [[ "${skip_collections}" = false ]]; then
    "${venv_dir}/bin/ansible-galaxy" collection install -r "${target_dir}/requirements.yml"
  else
    warn "External collections were not installed"
  fi
}

expose_commands() {
  local command_name
  mkdir -p "${HOME}/.local/bin"
  for command_name in ansible ansible-config ansible-galaxy ansible-inventory ansible-lint ansible-playbook ansible-vault molecule pytest yamllint; do
    if [[ -x "${venv_dir}/bin/${command_name}" ]]; then
      ln -sfn "${venv_dir}/bin/${command_name}" "${HOME}/.local/bin/${command_name}"
    fi
  done
}

verify_installation() {
  "${venv_dir}/bin/ansible" --version
  "${venv_dir}/bin/ansible-lint" --version
  "${venv_dir}/bin/ansible-inventory" -i "${target_dir}/inventories/example/hosts.yml" --graph >/dev/null
  (cd "${target_dir}" && PATH="${venv_dir}/bin:${PATH}" scripts/check-manifests.py)
}

install_os_packages
require_commands
verify_python_version
clone_or_update_repository
install_python_tools
expose_commands
verify_installation

cat <<EOF

SASD Ansible control node is ready.
Repository: ${target_dir}
Virtualenv: ${venv_dir}

Activate the environment:
  source ${venv_dir}/bin/activate

Verify Milestone 2:
  cd ${target_dir}
  scripts/test.sh
  scripts/verify-milestone-2.sh
EOF
