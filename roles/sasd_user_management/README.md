# Role: `sasd_user_management`

Manages only explicitly declared local groups and users. It never removes undeclared accounts. Authorized keys are managed as an exclusive file only when a non-empty `authorized_keys` list is declared for that user.

Apply mode requires the global Milestone 2 confirmation token. Review UID/GID, primary group, home path, and SSH keys before execution.
