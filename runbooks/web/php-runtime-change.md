# Runbook: Change PHP runtime settings

Determine active CLI and FPM configuration scan directories first. Declare an explicit managed drop-in path; do not replace the distribution's primary `php.ini`. Preview the change, apply to one laboratory host, confirm CLI and FPM tests, reload FPM, and exercise an application health endpoint. Roll back by reverting or retiring the managed drop-in and reapplying.
