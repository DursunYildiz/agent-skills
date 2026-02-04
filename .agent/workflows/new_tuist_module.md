---
description: Scaffolds a new Tuist module (Feature or Kit) with standard configuration.
---

# New Tuist Module Workflow

Use this workflow when the user runs `/new_tuist_module` or asks to create a new module.

## Steps

1.  **Gather Information**
    - Ask the user for the **Module Name** (e.g., `Profile`, `NetworkKit`).
    - Ask for the **Module Type**:
        - `Feature` (Business logic, screens)
        - `Kit` (Shared logic, core utilities)
    - **Architecture Check**: MUST consult the `ios-tuist-architect` skill to ensure compliance with strict 5-target structure and dependency rules.

2.  **Create Directory Structure**
    - Determine the path:
        - If Feature: `Projects/Features/[ModuleName]`
        - If Kit: `Projects/Kits/[ModuleName]`
    - Run command to create folders:
      ```bash
      # 5-Target Structure Directories
      mkdir -p Projects/[Type]s/[ModuleName]/Interface
      mkdir -p Projects/[Type]s/[ModuleName]/Sources
      mkdir -p Projects/[Type]s/[ModuleName]/Testing
      mkdir -p Projects/[Type]s/[ModuleName]/Tests
      mkdir -p Projects/[Type]s/[ModuleName]/Example/Sources
      mkdir -p Projects/[Type]s/[ModuleName]/Example/Resources
      # Optional: Resources for Implementation
      mkdir -p Projects/[Type]s/[ModuleName]/Resources
      ```

3.  **Generate Project.swift**
    - Write a `Project.swift` file in the module root.
    - **Template**:
      ```swift
      import ProjectDescription
      import ProjectDescriptionHelpers

      let project = Project.makeModule(
          name: "[ModuleName]",
          type: .[type], // .feature or .kit
          dependencies: [
              // Add dependencies to Interface targets of other modules
              // .project(target: "DesignKitInterface", path: "../../Kits/DesignKit"),
          ]
      )
      ```
      *(Note: Use `Project.makeModule` which automatically generates the 5-target structure: Interface, Implementation, Testing, Tests, Example)*

4.  **Create Initial Source Files**
    - **Interface**: Create `Projects/[Type]s/[ModuleName]/Interface/[ModuleName]Protocol.swift`:
      ```swift
      import Foundation

      public protocol [ModuleName]Protocol {
          // Define public API here
      }
      ```
    - **Implementation**: Create `Projects/[Type]s/[ModuleName]/Sources/[ModuleName].swift`:
      ```swift
      import Foundation
      import [ModuleName]Interface

      public struct [ModuleName]: [ModuleName]Protocol {
          public init() {}
      }
      ```
    - **Testing**: Create `Projects/[Type]s/[ModuleName]/Testing/[ModuleName]Testing.swift`:
      ```swift
      import Foundation
      import [ModuleName]Interface

      public class [ModuleName]Testing {
          public init() {}
      }
      ```
    - **Example App**: Create `Projects/[Type]s/[ModuleName]/Example/Sources/[ModuleName]ExampleApp.swift`:
      ```swift
      import SwiftUI
      import [ModuleName]

      @main
      struct [ModuleName]ExampleApp: App {
          var body: some Scene {
              WindowGroup {
                  VStack {
                      Text("[ModuleName] Example")
                  }
              }
          }
      }
      ```

5.  **Regenerate Project**
    - Run `tuist generate` to link the new module into the workspace.
    - If it fails, check `Workspace.swift` to ensure it includes `Projects/**` or explicitly register the new project.

6.  **Confirmation**
    - Open the specific folder if possible or just notify the user that the module is ready.
