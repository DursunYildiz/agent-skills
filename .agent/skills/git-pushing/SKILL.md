---
name: git-pushing
description: Stage, commit, and push git changes with conventional commit messages. Use when user wants to commit and push changes, mentions pushing to remote, or asks to save and push their work. Also activates when user says "push changes", "commit and push", "push this", "push to github", or similar git workflow requests.
---

# Git Push Workflow

Stage all changes, create a conventional commit, and push to the remote branch.

## When to Use

Automatically activate when the user:

- Explicitly asks to push changes ("push this", "commit and push")
- Mentions saving work to remote ("save to github", "push to remote")
- Completes a feature and wants to share it
- Says phrases like "let's push this up" or "commit these changes"

## Workflow

Since external scripts are not available, use the `run_command` tool to execute the standard git workflow:

1. **Stage Changes**:
```bash
git add .
```

2. **Commit**:
Generate a conventional commit message based on the changes.
```bash
git commit -m "type(scope): description"
```
*Types*: feat, fix, chore, docs, refactor, style, test

3. **Push**:
Push to the current branch.
```bash
git push
```
