---
description: Structured brainstorming for projects and features. Explores multiple options before implementation.
---

# Brainstorming Workflow

This workflow activates the `brainstorming` skill to guide the user through a structured idea validation and design process.

## Steps

1.  **Activate Skill**
    -   Use `view_file` to read `.agent/skills/brainstorming/SKILL.md`.
    -   Follow the instructions in the skill exactly.

2.  **Phase 1: Understanding**
    -   Ask questions one by one (or in small batches).
    -   Clarify intent, audience, and constraints.
    -   Identify Non-Functional Requirements (NFRs).
    -   **Checkpoint**: Reach "Understanding Lock" (summary + confirmation).

3.  **Phase 2: Exploration**
    -   Propose 2–3 viable design options.
    -   Highlight trade-offs (Complexity vs. Speed vs. Extensibility).
    -   Recommend an approach.

4.  **Phase 3: Design Definition**
    -   Detail the chosen approach incrementally.
    -   Validate architecture, components, and data flow.
    -   Keep a "Decision Log".

5.  **Phase 4: Documentation**
    -   Create a design document (Markdown) with:
        -   Summary
        -   Assumptions
        -   Decision Log
        -   Final Design Specifications

6.  **Exit**
    -   Only exit when the design is fully validated and documented.
    -   Ask if the user is ready for implementation planning.
