# sasd_diagnostic_bundle

Creates a repository-local `tar.gz` archive from one diagnostics run.
The builder rejects symlinks, size-limits included files, sanitizes JSON
values whose keys match configured sensitive patterns, and records SHA-256
checksums in a manifest.

This is defense in depth, not a guarantee that every organization-specific
secret is recognized. Review a bundle before sharing it outside the trusted
administration team.
