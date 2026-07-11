SHELL := /bin/bash
PYTHON ?= python3
VENV ?= .venv
INVENTORY ?= inventories/example/hosts.yml

.PHONY: help install collections inventory manifests docs lint syntax test verify verify-m2 verify-m3 connectivity readiness diagnostics baseline-audit baseline-check updates-audit web-audit web-check endpoints vm-test clean

help:
	@printf '%s\n' \
	  'make install          Create .venv and install development tools' \
	  'make collections      Install optional collections' \
	  'make inventory        Display and validate inventory' \
	  'make test             Run all static repository checks' \
	  'make verify           Run safe Milestone 3 localhost acceptance' \
	  'make verify-m2        Run safe Milestone 2 localhost acceptance' \
	  'make web-audit        Audit web services' \
	  'make web-check        Preview web apply mode with check/diff' \
	  'make endpoints        Validate declared HTTP/HTTPS endpoints' \
	  'make clean            Remove generated local files'

install:
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/python -m pip install --upgrade pip setuptools wheel
	$(VENV)/bin/python -m pip install -r requirements-dev.txt

collections:
	$(VENV)/bin/ansible-galaxy collection install -r requirements.yml

inventory:
	ansible-inventory -i $(INVENTORY) --graph
	ansible-inventory -i $(INVENTORY) --list >/dev/null

manifests:
	scripts/check-manifests.py

docs:
	scripts/check-documentation-links.py

lint:
	scripts/lint.sh

syntax:
	INVENTORY=$(INVENTORY) scripts/syntax-check.sh

test:
	INVENTORY=$(INVENTORY) scripts/test.sh

verify: verify-m3

verify-m2:
	scripts/verify-milestone-2.sh

verify-m3:
	scripts/verify-milestone-3.sh

connectivity:
	ansible-playbook -i $(INVENTORY) playbooks/validation/connectivity.yml

readiness:
	ansible-playbook -i $(INVENTORY) playbooks/validation/managed-node-readiness.yml

diagnostics:
	ansible-playbook -i $(INVENTORY) playbooks/diagnostics/system-overview.yml

baseline-audit:
	ansible-playbook -i $(INVENTORY) playbooks/provisioning/linux-baseline.yml

baseline-check:
	ansible-playbook -i $(INVENTORY) playbooks/provisioning/linux-baseline.yml --check --diff \
	  -e sasd_linux_baseline_mode=apply \
	  -e sasd_linux_baseline_apply_confirmation=SASD_APPLY_LINUX_BASELINE

updates-audit:
	ansible-playbook -i $(INVENTORY) playbooks/maintenance/linux-updates.yml

web-audit:
	ansible-playbook -i $(INVENTORY) playbooks/diagnostics/web-services-status.yml

web-check:
	ansible-playbook -i $(INVENTORY) playbooks/provisioning/web-services.yml --check --diff \
	  -e sasd_web_services_mode=apply \
	  -e sasd_web_services_apply_confirmation=SASD_APPLY_WEB_SERVICES

endpoints:
	ansible-playbook -i $(INVENTORY) playbooks/validation/web-endpoints.yml

vm-test:
	cd tests/vm && ./run-matrix.sh

clean:
	rm -rf .cache .molecule .pytest_cache artifacts diagnostic-bundles reports
	find . -name '*.retry' -delete
