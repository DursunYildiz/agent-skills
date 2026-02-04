#!/usr/bin/env python3
"""
Skill Factory Validator
Validates skill structure and frontmatter based on skill-writer + skill-creator rules.
"""

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Run: pip3 install pyyaml")
    sys.exit(1)


def validate_skill(skill_path: str) -> tuple[bool, list[str]]:
    """Validate a skill directory against all rules."""
    path = Path(skill_path)
    errors = []
    warnings = []
    
    # Check SKILL.md exists
    skill_md = path / "SKILL.md"
    if not skill_md.exists():
        return False, ["SKILL.md not found"]
    
    content = skill_md.read_text()
    
    # Check frontmatter exists
    fm_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not fm_match:
        return False, ["Invalid or missing YAML frontmatter"]
    
    try:
        frontmatter = yaml.safe_load(fm_match.group(1))
    except yaml.YAMLError as e:
        return False, [f"YAML parse error: {e}"]
    
    if not isinstance(frontmatter, dict):
        return False, ["Frontmatter must be a YAML mapping"]
    
    # Check required fields
    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    
    if not name:
        errors.append("Missing required field: name")
    if not description:
        errors.append("Missing required field: description")
    
    # Validate name format (lowercase, hyphens, digits only)
    if name and not re.match(r"^[a-z0-9-]+$", name):
        errors.append(f"Name '{name}' must be lowercase letters, digits, and hyphens only")
    
    # Validate name length
    if name and len(name) > 64:
        errors.append(f"Name too long: {len(name)} chars (max 64)")
    
    # Validate name matches directory
    if name and name != path.name:
        errors.append(f"Name '{name}' doesn't match directory '{path.name}'")
    
    # Validate description length
    if description and len(description) > 1024:
        errors.append(f"Description too long: {len(description)} chars (max 1024)")
    
    # Check for trigger words
    trigger_patterns = ["use when", "use for", "use this", "trigger", "activate"]
    has_trigger = any(t in description.lower() for t in trigger_patterns)
    if description and not has_trigger:
        warnings.append("Description missing 'when to use' triggers (recommended)")
    
    # Check for allowed frontmatter keys
    allowed_keys = {"name", "description", "allowed-tools", "metadata", "license"}
    unknown_keys = set(frontmatter.keys()) - allowed_keys
    if unknown_keys:
        warnings.append(f"Non-standard frontmatter keys: {unknown_keys}")
    
    # Return results
    if errors:
        return False, errors + warnings
    return True, warnings


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate.py <skill_path>")
        print("       python validate.py --all <skills_dir>")
        sys.exit(1)
    
    if sys.argv[1] == "--all":
        skills_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(".")
        all_valid = True
        
        for skill_path in sorted(skills_dir.iterdir()):
            if skill_path.is_dir() and not skill_path.name.startswith("."):
                valid, messages = validate_skill(str(skill_path))
                status = "✅" if valid else "❌"
                print(f"{status} {skill_path.name}")
                for msg in messages:
                    prefix = "  ⚠️ " if "recommended" in msg.lower() else "  ❌ "
                    print(f"{prefix}{msg}")
                if not valid:
                    all_valid = False
        
        sys.exit(0 if all_valid else 1)
    else:
        valid, messages = validate_skill(sys.argv[1])
        for msg in messages:
            print(msg)
        if valid:
            print("✅ Skill is valid!")
        sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
