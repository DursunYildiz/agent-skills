---
name: ios-tuist-architect
description: Expert in iOS Architecture using SwiftUI and Tuist Modular Architecture (TMA). Enforces strict 5-target module structure and interface-based dependencies. Use when creating new iOS modules, setting up Tuist projects, managing module dependencies, implementing DependencyKit service locator, or asking about Interface vs Implementation separation.
---

# iOS Tuist TMA Architect Skill

This skill is designed to manage an iOS project using **SwiftUI** and **Tuist** following the **The Modular Architecture (TMA)**.

## 🏗 Architecture Overview

The project strictly follows the TMA principle where every "Module" (Feature or Kit) is a composition of **5 Targets**.

### 1. The 5-Target Structure
For a module named `[Name]`, the following targets MUST exist:

1.  **`[Name]`** (Implementation)
    -   **Type**: `framework` (dev) / `staticLibrary` (release)
    -   **Contains**: Business logic, Views, ViewModels, Resources.
    -   **Depends On**: `[Name]Interface`.
2.  **`[Name]Interface`** (Public API)
    -   **Type**: `framework` (dev) / `staticLibrary` (release)
    -   **Contains**: Public protocols, Models, Dependency Injection protocols.
    -   **Depends On**: *Nothing* (or very minimal core types).
3.  **`[Name]Testing`** (Mocks & Spies)
    -   **Type**: `staticLibrary`
    -   **Contains**: Mock implementations of the Interface for testing other modules.
    -   **Depends On**: `[Name]Interface`.
4.  **`[Name]Tests`** (Unit Tests)
    -   **Type**: `unitTests`
    -   **Contains**: XCTest cases.
    -   **Depends On**: `[Name]` (Implementation), `[Name]Testing` (for mocks).
5.  **`[Name]Example`** (Demo App)
    -   **Type**: `app`
    -   **Contains**: A minimal app delegate to run the feature in isolation.
    -   **Depends On**: `[Name]`, `[Name]Testing`.

### 2. Dependency Graph Rules
> [!CRITICAL]
> **NEVER** import a Feature's *Implementation* target from another Feature.

-   **Correct**: `FeatureA` depends on `FeatureBInterface`.
-   **Incorrect**: `FeatureA` depends on `FeatureB`.
-   **Correct**: `FeatureA` tests depend on `FeatureBTesting` (to mock B).

## 🛠 Capabilities

### 1. Creating a New Module
When asked to create a new module (Feature or Kit):

1.  **Directory**: Create `Projects/[Features|Kits]/[ModuleName]`.
2.  **Project.swift**: Create a `Project.swift` that defines the **5 targets**.
    -   Use a helper if available, e.g., `Project.makeModule(name: "Home", ...)`.
    -   If no helper exists, define all 5 targets explicitly as per the structure above.
3.  **Populate Targets**:
    -   **Interface**: Create `[Name]InterfaceProtocol.swift`.
    -   **Implementation**: Create `[Name].swift`.
    -   **Testing**: Create `[Name]Testing.swift` (dummy class if needed).
    -   **Example**: Create `[Name]ExampleApp.swift` with `@main`.
    -   *Crucial*: Tuist will fail to link if targets are empty.
4.  **Register**: Ensure `Workspace.swift` includes the new project.

### 2. Dependency Management
-   **Static Dependencies (Module Linking)**:
    -   **To use Feature B in Feature A**:
        -   In `FeatureA` target: dependency is `.project(target: "FeatureBInterface", path: "../FeatureB")`.
        -   In `FeatureATests` target: dependency is `.project(target: "FeatureBTesting", path: "../FeatureB")`.
-   **Runtime Dependencies (Service Injection)**:
    -   Use `DependencyKit` to register and resolve implementations at runtime.
    -   **Protocol**: Defined in `FeatureInterface`.
    -   **Registration**: In `App` entry point.
    -   IMPORTANT: Do not introduce static linking between Implementation targets just to instantiate a class. Use the `DependencyEngine` or passing via `init`.

### 3. SwiftUI + MVVM Patterns
-   **Views**: Internal to the `[Name]` (Implementation) target.
-   **ViewModels**: Internal to the `[Name]` (Implementation) target.
-   **Navigation**: Handled via FlowCoordinators or Routers defined in the `Interface` and implemented in the `Implementation`.

### 4. Dependency Injection & Service Locator
We use a **Service Locator** pattern provided by `DependencyKit`.

1.  **Define Interface**: `public protocol MyServiceProtocol: AnyObject { ... }` in `MyKitInterface`.
2.  **Implement**: `class MyService: MyServiceProtocol { ... }` in `MyKit`.
3.  **Register (Main App)**: `DependencyEngine.shared.register(interface: MyServiceProtocol.self, implementation: MyService())`.
4.  **Inject**: `init(service: MyServiceProtocol) { ... }`.
5.  **Resolve (Composition Root)**: `let service = DependencyEngine.shared.resolve(MyServiceProtocol.self)`.

## 🚨 Common Pitfalls
-   **Linking Issues**: If you get "symbol not found", check if you are linking the `Interface` but trying to access an internal class. Move shared types to `Interface`.
-   **Circular Dependencies**: If `FeatureA` needs `FeatureB` and `FeatureB` needs `FeatureA`:
    -   Check if they only need the *Interface*. `Interface` A can depend on `Interface` B without causing a cycle in implementations.
    -   If Interfaces cycle, extract the shared model to a Core/Common Kit.
