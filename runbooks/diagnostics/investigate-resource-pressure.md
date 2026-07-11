# Investigate resource pressure

Start with `resources.json`. Compare load per CPU, available memory, swap use, filesystem
capacity, inode use, and bounded process samples. High load does not prove CPU saturation;
check memory pressure, blocked I/O, and process state before drawing a conclusion.

Do not kill processes or remove files from this runbook. Preserve evidence and move any
corrective action into a reviewed Milestone 5 remediation procedure.
