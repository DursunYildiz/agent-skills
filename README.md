# Agent Skills Collection

A curated collection of Agent Skills for AI-powered development workflows.

## Skills Included

| Skill | Description |
|-------|-------------|
| **axiom-swiftui-architecture** | SwiftUI architecture patterns (MVVM, TCA, Coordinator) |
| **brainstorming** | Structured idea validation and design process |
| **code-reviewer** | Professional code review for PRs and local changes |
| **crash-safety** | Audit for crash risks in Swift/iOS apps |
| **docs-writer** | Technical documentation writing |
| **environment-setup-guide** | Dev environment setup assistance |
| **git-pushing** | Git commit/push with conventional commits |
| **ios-tuist-architect** | iOS Tuist Modular Architecture (TMA) |
| **mobile-design** | Mobile-first design principles |
| **mobile-ios-design** | iOS HIG and SwiftUI patterns |
| **senior-architect** | System architecture design |
| **skill-factory** | Create, validate, and manage Agent Skills |
| **tdd-workflow** | Test-Driven Development workflow |
| **theme-factory** | Professional theme styling |
| **ui-ux-pro-max** | UI/UX design intelligence |

## Usage

Skills are located in `.agent/skills/` directory.

### Validate All Skills

```bash
python3 .agent/skills/skill-factory/scripts/validate.py --all .agent/skills/
```

### Create New Skill

```bash
python3 .agent/skills/skill-factory/scripts/init_skill.py my-skill --path .agent/skills
```

## Workflows

Located in `.agent/workflows/`:

- `brainstorm.md` - Structured brainstorming
- `build_xcframework.md` - XCFramework build automation
- `generate_from_swagger.md` - Generate code from Swagger
- `new_tuist_module.md` - Create Tuist modules
- `smart_push.md` - Smart git commit/push

## License

MIT
