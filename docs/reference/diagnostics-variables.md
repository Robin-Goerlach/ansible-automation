# Diagnostics variable reference

## Shared orchestration

| Variable | Default | Purpose |
|---|---|---|
| `sasd_diagnostics_run_id` | generated UTC identifier | correlate one run |
| `sasd_diagnostics_report_root` | `reports/diagnostics` | controller report root |

Run IDs may contain letters, digits, dot, underscore, and hyphen.

## Resources

- `sasd_resource_diagnostics_load_warning_per_cpu`: 1-minute load threshold per logical CPU;
- `sasd_resource_diagnostics_memory_available_warning_percent`: low-memory threshold;
- `sasd_resource_diagnostics_swap_used_warning_percent`: swap-use threshold;
- `sasd_resource_diagnostics_filesystem_used_warning_percent`: capacity threshold;
- `sasd_resource_diagnostics_inode_used_warning_percent`: inode threshold;
- `sasd_resource_diagnostics_top_process_count`: bounded CPU and memory lists;
- `sasd_resource_diagnostics_excluded_filesystem_types`: pseudo-filesystem exclusions.

## Services

- `sasd_service_diagnostics_monitored_services`: exact service-fact keys to report;
- `sasd_service_diagnostics_fail_on_missing_monitored`: classify a missing declaration as critical.

## Packages

- `sasd_package_diagnostics_selected_packages`: packages whose versions are reported;
- `sasd_package_diagnostics_collect_pending_updates`: enable read-only update query;
- `sasd_package_diagnostics_maximum_update_items`: bounded output length;
- `sasd_package_diagnostics_lock_paths`: known package-manager lock and PID paths.

## Network

- `sasd_network_diagnostics_dns_names`: explicit names to resolve;
- `sasd_network_diagnostics_tcp_targets`: dictionaries with `name`, `host`, and `port`;
- `sasd_network_diagnostics_timeout_seconds`: DNS/TCP timeout boundary;
- `sasd_network_diagnostics_include_loopback`: retain or omit the loopback interface.

## Certificates

- `sasd_certificate_diagnostics_files`: dictionaries with `name` and absolute `path`;
- `sasd_certificate_diagnostics_endpoints`: `name`, `host`, optional `port`, `server_name`, and `validate_certs`;
- `sasd_certificate_diagnostics_minimum_remaining_days`: expiry warning threshold;
- `sasd_certificate_diagnostics_timeout_seconds`: TLS connection timeout.

## Bundles

- `sasd_diagnostic_bundle_source_root`: repository-relative diagnostics root;
- `sasd_diagnostic_bundle_output_root`: repository-relative archive directory;
- `sasd_diagnostic_bundle_maximum_file_bytes`: per-file inclusion limit;
- `sasd_diagnostic_bundle_redacted_key_patterns`: case-insensitive JSON key fragments;
- `sasd_diagnostic_bundle_report_root`: bundle result-contract directory.
