---
name: environment-setup-guide
description: Guide developers through setting up development environments with proper tools, dependencies, and configurations. Use when onboarding new team members, switching machines, installing Node.js, Python, Docker, or troubleshooting environment issues like missing dependencies or PATH problems.
---

# Environment Setup Guide

## Overview
Help developers set up complete development environments from scratch. This skill provides step-by-step guidance for installing tools, configuring dependencies, setting up environment variables, and verifying the setup works correctly.

## When to Use This Skill
- Use when starting a new project and need to set up the development environment
- Use when onboarding new team members to a project
- Use when switching to a new machine or operating system
- Use when troubleshooting environment-related issues
- Use when documenting setup instructions for a project
- Use when creating development environment documentation

## How It Works

### Step 1: Identify Requirements
I'll help you determine what needs to be installed:
- Programming language and version (Node.js, Python, Go, etc.)
- Package managers (npm, pip, cargo, etc.)
- Database systems (PostgreSQL, MongoDB, Redis, etc.)
- Development tools (Git, Docker, IDE extensions, etc.)
- Environment variables and configuration files

### Step 2: Check Current Setup
Before installing anything, I'll help you check what's already installed:
```bash
# Check versions of installed tools
node --version
python --version
git --version
docker --version
```

### Step 3: Provide Installation Instructions
I'll give platform-specific installation commands:
- **macOS:** Using Homebrew
- **Linux:** Using apt, yum, or package manager
- **Windows:** Using Chocolatey, Scoop, or direct installers

### Step 4: Configure the Environment
Help set up:
- Environment variables (.env files)
- Configuration files (.gitconfig, .npmrc, etc.)
- IDE settings (VS Code, IntelliJ, etc.)
- Shell configuration (.bashrc, .zshrc, etc.)

### Step 5: Verify Installation
Provide verification steps to ensure everything works:
- Run version checks
- Test basic commands
- Verify database connections
- Check environment variables are loaded

## Best Practices

### ✅ Do This
- **Document Everything** - Write clear setup instructions
- **Use Version Managers** - nvm for Node, pyenv for Python
- **Create .env.example** - Show required environment variables
- **Test on Clean System** - Verify instructions work from scratch
- **Include Troubleshooting** - Document common issues and solutions
- **Use Docker** - For consistent environments across machines
- **Pin Versions** - Specify exact versions in package files
- **Automate Setup** - Create setup scripts when possible
- **Check Prerequisites** - List required tools before starting
- **Provide Verification Steps** - Help users confirm setup works

### ❌ Don't Do This
- **Don't Assume Tools Installed** - Always check and provide install instructions
- **Don't Skip Environment Variables** - Document all required variables
- **Don't Use Sudo with npm** - Fix permissions instead
- **Don't Forget Platform Differences** - Provide OS-specific instructions
- **Don't Leave Out Verification** - Always include test steps
- **Don't Use Global Installs** - Prefer local/virtual environments
- **Don't Ignore Errors** - Document how to handle common errors
- **Don't Skip Database Setup** - Include database initialization steps
