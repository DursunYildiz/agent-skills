---
description: Automatically builds and packages the project SDK as an XCFramework
---

# Build XCFramework Workflow

This workflow executes the build script to generate the XCFramework (e.g., `[TargetName].xcframework`).

// turbo-all

## Steps

1.  **Generate Project**
    Ensure the project graph is up to date.
    ```bash
    tuist generate
    ```

2.  **Execute Build Script**
    Run the build script to archive and package the framework.
    ```bash
    ./scripts/build_xcframework.sh
    ```

3.  **Completion**
    The process will cleanly output the checksum and path.
