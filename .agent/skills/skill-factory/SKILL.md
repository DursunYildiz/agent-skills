---
name: skill-factory
description: Create, validate, and manage Agent Skills with best practices. Use when creating new skills, updating existing SKILL.md files, validating skill structure, troubleshooting skill discovery issues, or asking about skill frontmatter and triggers.
---

# Skill Factory

Complete toolkit for creating, validating, and managing Agent Skills. Combines best practices from skill-writer (Claude Code) and skill-creator (OpenAI Codex).

## When to Use

- Creating a new Agent Skill from scratch
- Updating or improving existing SKILL.md files
- Validating skill structure and frontmatter
- Troubleshooting skill discovery issues
- Converting prompts or workflows into Skills

## Skill Creation Process

### Step 1: Understand Requirements

Ask clarifying questions:
- What specific capability should this Skill provide?
- When should the agent use this Skill? (triggers)
- Is this for personal use or team sharing?
- What resources does it need? (scripts, references, assets)

**Key Principle**: One Skill = One Capability

### Step 2: Choose Location

| Location | Use For |
|----------|---------|
| `.agent/skills/` or `.claude/skills/` | Project-specific, team workflows (committed to git) |
| `~/.claude/skills/` | Personal, experimental |

### Step 3: Create Structure

```bash
mkdir -p .agent/skills/skill-name
```

**Multi-file Skills:**
```
skill-name/
├── SKILL.md (required)
├── references/ (optional - detailed docs)
├── scripts/ (optional - helper scripts)
└── assets/ (optional - templates, images)
```

### Step 4: Write Frontmatter

```yaml
---
name: skill-name
description: What it does. Use when [specific triggers].
---
```

**Field Rules:**

| Field | Requirements |
|-------|-------------|
| `name` | lowercase, hyphens only, max 64 chars, must match directory |
| `description` | max 1024 chars, include "what" AND "when to use" triggers |

**Optional Fields:**
- `allowed-tools`: Restrict to specific tools (e.g., `Read, Grep, Glob`)
- `metadata`: Additional info (platforms, version)

### Step 5: Write Effective Description

**Formula**: `[What it does] + [When to use] + [Key triggers]`

✅ **Good:**
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

❌ **Bad:**
```yaml
description: Helps with documents
```

**Tips:**
- Include file extensions (.pdf, .swift, .ts)
- Mention common user phrases ("analyze", "create", "fix")
- Add "Use when..." clause
- List specific operations

### Step 6: Structure Content

```markdown
# Skill Name

Brief overview of what this Skill does.

## Quick Start

Simple example to get started immediately.

## Instructions

Step-by-step guidance:
1. First step with clear action
2. Second step with expected outcome
3. Handle edge cases

## Examples

Concrete usage examples with code.

## Best Practices

- Key conventions to follow
- Common pitfalls to avoid

## Requirements (if any)

List dependencies or prerequisites.
```

### Step 7: Validate

Run validation checklist:

**Frontmatter:**
- [ ] `name` is lowercase, hyphens only, max 64 chars
- [ ] `name` matches directory name
- [ ] `description` < 1024 chars
- [ ] `description` includes "what" AND "when to use"
- [ ] Valid YAML (no tabs, proper indentation)

**Content:**
- [ ] Clear instructions for agent
- [ ] Concrete examples provided
- [ ] Edge cases handled
- [ ] Dependencies listed

**Discovery:**
- [ ] Specific trigger words in description
- [ ] File types mentioned if relevant
- [ ] "Use when..." clause present

### Step 8: Test

1. Restart agent to load the Skill
2. Ask questions matching the description triggers
3. Verify Skill activates automatically
4. Confirm agent follows instructions correctly

## Validation Script

For quick validation, use:

```python
#!/usr/bin/env python3
import re, sys, yaml
from pathlib import Path

def validate(path):
    skill_md = Path(path) / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"
    
    content = skill_md.read_text()
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter"
    
    fm = yaml.safe_load(match.group(1))
    name = fm.get("name", "")
    desc = fm.get("description", "")
    
    # Name checks
    if not re.match(r"^[a-z0-9-]+$", name):
        return False, f"Name '{name}' must be lowercase with hyphens only"
    if len(name) > 64:
        return False, f"Name too long ({len(name)} > 64)"
    if name != Path(path).name:
        return False, f"Name '{name}' doesn't match directory"
    
    # Description checks
    if len(desc) > 1024:
        return False, f"Description too long ({len(desc)} > 1024)"
    if not any(t in desc.lower() for t in ["use when", "use for", "use this"]):
        return False, "Description missing 'when to use' triggers"
    
    return True, "Valid!"

if __name__ == "__main__":
    ok, msg = validate(sys.argv[1])
    print(msg)
    sys.exit(0 if ok else 1)
```

## Common Patterns

### Read-Only Skill
```yaml
---
name: code-reader
description: Read and analyze code without changes. Use when reviewing code or understanding codebases.
allowed-tools: Read, Grep, Glob
---
```

### Script-Based Skill
```yaml
---
name: pdf-processor
description: Process PDF files with Python. Use when extracting text, filling forms, or merging PDFs.
---

# PDF Processor

## Instructions

Run the helper script:
```bash
python scripts/process.py input.pdf --output result.pdf
```
```

### Multi-File Skill
```
api-designer/
├── SKILL.md (overview)
├── references/
│   ├── rest-patterns.md
│   └── openapi-spec.md
└── examples/
    └── sample-api.yaml
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Skill doesn't activate | Add more specific triggers to description |
| Multiple Skills conflict | Make descriptions more distinct |
| YAML errors | Check indentation, no tabs |
| Name mismatch | Ensure name matches directory |

## Bundled Scripts

This skill includes helper scripts in `scripts/`:

### 1. validate.py - Validate Skills

```bash
# Validate single skill
python3 scripts/validate.py .agent/skills/my-skill

# Validate all skills
python3 scripts/validate.py --all .agent/skills/
```

### 2. init_skill.py - Initialize New Skill

```bash
# Basic skill
python3 scripts/init_skill.py my-new-skill --path .agent/skills

# With resources
python3 scripts/init_skill.py my-new-skill --path .agent/skills --resources scripts,references,assets

# With examples
python3 scripts/init_skill.py my-new-skill --path .agent/skills --include-examples
```

### 3. generate_openai_yaml.py - Generate UI Metadata

```bash
# Generate agents/openai.yaml for a skill
python3 scripts/generate_openai_yaml.py .agent/skills/my-skill

# With custom overrides
python3 scripts/generate_openai_yaml.py .agent/skills/my-skill \
  --interface display_name="My Skill" \
  --interface short_description="Does cool things"
```

## References

- `references/openai_yaml.md` - OpenAI YAML format documentation

## Quick Reference

```
✅ name: lowercase-with-hyphens (max 64)
✅ description: What + When + Triggers (max 1024)
✅ directory name = frontmatter name
✅ "Use when..." in description
✅ Specific file types/operations mentioned
✅ Clear step-by-step instructions
```
