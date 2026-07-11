#!/usr/bin/env bash
set -Eeuo pipefail

readonly repository_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly ansible_step_timeout="${SASD_ANSIBLE_STEP_TIMEOUT:-420}"
cd "${repository_root}"

required_commands=(ansible-playbook python3 timeout)
for command_name in "${required_commands[@]}"; do
  command -v "${command_name}" >/dev/null 2>&1 || {
    printf 'ERROR: required command unavailable: %s\n' "${command_name}" >&2
    exit 1
  }
done

run_playbook() {
  local temporary_directory exit_code
  temporary_directory="$(mktemp -d "${TMPDIR:-/tmp}/sasd-ansible-m3.XXXXXX")"
  set +e
  ANSIBLE_FORKS=1 \
    ANSIBLE_PIPELINING=False \
    ANSIBLE_LOCAL_TEMP="${temporary_directory}/local" \
    timeout "${ansible_step_timeout}" \
    ansible-playbook "$@"
  exit_code=$?
  set -e
  rm -rf "${temporary_directory}"
  return "${exit_code}"
}

server_pid=""
temporary_endpoint_directory=""
cleanup() {
  if [[ -n "${server_pid}" ]]; then
    kill "${server_pid}" >/dev/null 2>&1 || true
    wait "${server_pid}" 2>/dev/null || true
  fi
  if [[ -n "${temporary_endpoint_directory}" ]]; then
    rm -rf "${temporary_endpoint_directory}"
  fi
}
trap cleanup EXIT

rm -rf reports/web-services reports/milestone-3-template-test

printf '== Milestone 3 safe localhost role acceptance ==\n'
run_playbook -i inventories/example/hosts.yml playbooks/validation/milestone-3-localhost.yml

printf '\n== Milestone 3 isolated template rendering ==\n'
run_playbook -i inventories/example/hosts.yml tests/web/render-templates.yml

printf '\n== Milestone 3 local HTTP endpoint validation ==\n'
temporary_endpoint_directory="$(mktemp -d "${TMPDIR:-/tmp}/sasd-ansible-m3-endpoint.XXXXXX")"
port_file="${temporary_endpoint_directory}/port"
cat > "${temporary_endpoint_directory}/inventory.yml" <<'INVENTORY'
---
all:
  children:
    webservers:
      hosts:
        localhost:
          ansible_connection: local
INVENTORY
python3 - "${port_file}" <<'PYCODE' &
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b'{"status":"ok"}\n'
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return

server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
Path(sys.argv[1]).write_text(str(server.server_port), encoding='utf-8')
server.serve_forever()
PYCODE
server_pid=$!
for _ in {1..50}; do
  [[ -s "${port_file}" ]] && break
  sleep 0.1
done
[[ -s "${port_file}" ]] || { printf 'ERROR: local endpoint server did not start.\n' >&2; exit 1; }
endpoint_port="$(cat "${port_file}")"
endpoint_log="${temporary_endpoint_directory}/endpoint-validation.log"
set +e
run_playbook \
  -i "${temporary_endpoint_directory}/inventory.yml" \
  playbooks/validation/web-endpoints.yml \
  -e "{\"sasd_web_validation_endpoints\":[{\"name\":\"local-health\",\"url\":\"http://127.0.0.1:${endpoint_port}/health\",\"status_codes\":[200],\"headers\":{\"X-SASD-Test-Secret\":\"must-not-be-reported\"}}]}" \
  >"${endpoint_log}" 2>&1
endpoint_exit_code=$?
set -e
cat "${endpoint_log}"
if [[ ${endpoint_exit_code} -ne 0 ]]; then
  printf 'ERROR: endpoint validation playbook failed with status %s.\n' "${endpoint_exit_code}" >&2
  exit "${endpoint_exit_code}"
fi
if grep -Fq 'must-not-be-reported' "${endpoint_log}" || \
   grep -Fq 'X-SASD-Test-Secret' "${endpoint_log}"; then
  printf 'ERROR: endpoint validation log leaked request header content.\n' >&2
  exit 1
fi

python3 - <<'PYCODE'
from pathlib import Path
import json

root = Path('reports')
required_reports = {
    'web-services/localhost.json': 'sasd.web-services.v1',
    'web-services/apache/localhost.json': 'sasd.apache.v1',
    'web-services/nginx/localhost.json': 'sasd.nginx.v1',
    'web-services/php/localhost.json': 'sasd.php.v1',
    'web-services/certificates/localhost.json': 'sasd.certificate-management.v1',
    'web-services/endpoints/localhost.json': 'sasd.web-endpoint-validation.v1',
}
for relative, schema in required_reports.items():
    path = root / relative
    if not path.is_file():
        raise SystemExit(f'missing report: {path}')
    payload = json.loads(path.read_text(encoding='utf-8'))
    if payload.get('schema') != schema:
        raise SystemExit(f'unexpected schema in {path}: {payload.get("schema")!r}')

endpoint_report_path = root / 'web-services/endpoints/localhost.json'
endpoint_text = endpoint_report_path.read_text(encoding='utf-8')
if 'must-not-be-reported' in endpoint_text or 'X-SASD-Test-Secret' in endpoint_text:
    raise SystemExit('endpoint report leaked request header content')
endpoint_report = json.loads(endpoint_text)
if endpoint_report.get('results', [{}])[0].get('status') != 200:
    raise SystemExit('local endpoint validation did not report HTTP 200')

rendered = root / 'milestone-3-template-test'
expected = {
    'apache-http.conf': 'ServerName example.test',
    'apache-tls.conf': 'SSLEngine on',
    'nginx-http.conf': 'server_name example.test www.example.test;',
    'nginx-tls-php.conf': 'fastcgi_pass unix:/run/php/php-fpm.sock;',
    '99-sasd.ini': 'memory_limit = 256M',
}
for filename, marker in expected.items():
    path = rendered / filename
    if marker not in path.read_text(encoding='utf-8'):
        raise SystemExit(f'missing template marker {marker!r} in {path}')

print(f'Validated {len(required_reports)} JSON reports, endpoint redaction, and {len(expected)} templates.')
PYCODE

printf '\nMilestone 3 safe localhost runtime verification passed.\n'
