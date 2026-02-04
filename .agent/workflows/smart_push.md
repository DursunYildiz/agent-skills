---
description: Analyzes git changes and creates a human-readable conventional commit message.
---

# Smart Push Workflow

This workflow analyzes your current changes, stages them, and proposes a meaningful conventional commit message before pushing.

## Steps

1. **Analyze Changes**
   - Run `git status` and `git diff` to understand what has changed.
   - Look for added files, modified logic, and refactors.

2. **Stage Changes**
   - Run `git add .` to stage all changes.
     *(If you only want to commit specific files, ask the user to stage them manually first, then remove this step)*.

3. **Generate Message**
   - Create a **Conventional Commit** message (`type(scope): description`).
   - Rules:
     - **feat**: New feature (e.g., "feat(auth): add login screen")
     - **fix**: Bug fix (e.g., "fix(api): handle 404 error")
     - **docs**: Documentation only
     - **style**: Formatting, missing semi-colons, etc
     - **refactor**: Code change that neither fixes a bug nor adds a feature
     - **test**: Adding missing tests
     - **chore**: Build process, auxiliary tools, libraries

4. **Commit & Push**
   - Propose the command: `git commit -m "your_generated_message" && git push`
   - **CRITICAL**: The message MUST be in English but simple and descriptive.
   - **CRITICAL**: Do NOT auto-run the commit/push command. Let the user approve the message.
