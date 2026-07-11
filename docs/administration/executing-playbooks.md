# Executing playbooks

Always identify the inventory and limit the target scope deliberately.

```bash
ansible-playbook -i inventories/lab-local/hosts.yml PLAYBOOK --limit HOST_OR_GROUP
```

For modifying automation, begin with:

```bash
ansible-playbook -i INVENTORY PLAYBOOK --check --diff --limit TARGET
```

Check mode is a prediction and cannot prove that every external command, API, package transaction, or service action will succeed. Review the playbook's documentation before relying on it.
