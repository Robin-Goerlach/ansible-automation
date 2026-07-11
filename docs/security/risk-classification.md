# Risk classification

## Level 0: diagnostic

Read-only information gathering. The playbook must still avoid leaking sensitive content.

## Level 1: low-risk correction

A reversible action with limited scope, such as starting a known service after validation.

## Level 2: controlled change

Configuration changes, package changes, firewall changes, or service disruption. Requires backup and objective validation. Explicit confirmation is normally required for remediation.

## Level 3: potentially destructive

Actions that may delete data, alter storage, perform restore operations, or create significant outage risk. Requires explicit confirmation, a maintenance window, verified backup, and a detailed runbook.
