# Tuist Modular Architecture (TMA) Rules

This project strictly follows the **Tuist Modular Architecture (TMA)**. This document acts as the source of truth for creating and managing modules.

## 🏗 Core Principle: The 5-Target Module

Every Feature or Kit in this project is NOT a single target. It is a **Module** composed of **5 Targets**.
This separation ensures that features are independent, build times are fast, and tests are isolated.

### The Structure

For a module named `Payment`:

| Target Name | Type | Description | Dependencies |
| :--- | :--- | :--- | :--- |
| **`Payment`** | `Framework` / `StaticLibrary` | **Implementation**. Contains all the "real" code: Views, ViewModels, Business Logic. | `PaymentInterface` |
| **`PaymentInterface`** | `Framework` / `StaticLibrary` | **Public API**. Contains protocols, models, and DI containers. This is what *other* modules import. | *None* |
| **`PaymentTesting`** | `StaticLibrary` | **Test Helpers**. Contains Mocks and Spies implementing the Interface. Used by *other* modules' tests. | `PaymentInterface` |
| **`PaymentTests`** | `UnitTests` | **Tests**. Helper unit tests for the implementation. | `Payment`, `PaymentTesting` |
| **`PaymentExample`** | `App` | **Demo App**. A standalone app to run this feature in isolation during development. | `Payment`, `PaymentTesting` |

> [!WARNING]
> **Empty Targets Break Builds**: Every target (Interface, Testing, Example, etc.) MUST have at least one Swift file in its source directory. An empty target will fail to link.

---

## 🔗 Dependency Rules

### 1. Depend on Interfaces, NOT Implementations
When **Module A** needs **Module B**, it must ONLY depend on `ModuleBInterface`.

> ❌ **WRONG:** `ModuleA` depends on `ModuleB`
>
> ✅ **RIGHT:** `ModuleA` depends on `ModuleBInterface`

**Why?**
- Prevents spaghetti code (strong coupling).
- Allows `ModuleB` implementation to change without recompiling `ModuleA`.
- Breaks circular dependencies (A needs B, B needs A is possible via Interfaces).

### 3. Dependency Injection (DI)
The project uses a Service Locator pattern provided by `DependencyKit`.

-   **Define Protocols**: In the `Interface` target.
-   **Implement Services**: In the `Implementation` target (or main App for core services).
-   **Register**: In the Application Entry Point (`App.swift` or `AppDelegate`), register concrete implementations against protocols using `DependencyEngine.shared.register`.
-   **Resolve**: Inject dependencies via registration. Do NOT hold strong references to the Engine inside your business logic classes if possible; prefer passing dependencies via `init` (Dependency Injection) after resolving them at the composition root.

Example:
```swift
// Feature A Interface
public protocol FeatureAServiceProtocol {}

// App Entry Point
DependencyEngine.shared.register(interface: FeatureAServiceProtocol.self, implementation: RealFeatureAService())

// Feature B Usage
let service = DependencyEngine.shared.resolve(FeatureAServiceProtocol.self)
```

---

## 🚀 Creating a New Module

1.  **Folder**: Create a new folder in `Projects/Features/` or `Projects/Kits/`.
2.  **Project.swift**: Define the 5 targets.
3.  **Registration**: The `Workspace.swift` (usually via glob `Projects/**`) will pick it up automatically.
4.  **Run**: `tuist generate` to update the Xcode project.
