---
description: Generates Swift network code (Models, Endpoints, Services) from a Swagger/OpenAPI source for a Tuist module.
---

# Generate from Swagger Workflow

This workflow automates the creation of networking code from Swagger documentation, enforcing the TMA architecture (DTOs in Implementation, Domain Models in Interface).

## Pre-requisites

- **Target Module**: Must be an existing Kit or Feature (e.g., `AuthKit`).

## Steps

1.  **Identify Resources**
    - Ask the user for the **Swagger UI** or **JSON** URL.
    - Note: Agent must locate the actual `.json` endpoint (e.g. `/v1/swagger.json` or via network inspection) if a UI URL is provided.

2.  **Fetch Swagger JSON**
    - Use `curl` to download the JSON schema.
    - Example:
      ```bash
      curl [JSON_URL] > swagger.json
      # If auth is required:
      # curl -u "username:password" [JSON_URL] > swagger.json
      ```

3.  **Analyze & Plan**
    - Read `swagger.json`.
    - Ask the user **which tags/controllers** to generate (e.g., "Only generate `Auth` endpoints").
    - Map out the files to be created:
        - `Interface/Models/[ModelName].swift` (Public Domain Models)
        - `Interface/Services/[ServiceName]Interface.swift` (Protocol)
        - `Sources/DTOs/[ModelName]DTO.swift` (Internal Decodable structs)
        - `Sources/Services/[ServiceName].swift` (Implementation)
        - `Sources/Endpoints/[ServiceName]Endpoint.swift` (EndpointProtocol)

4.  **Generate Code (Iterative)**

    ### A. Domain Models (Interface)
    - Create clean Swift structs.
    - **Rules**:
        - `public` access modifier.
        - No `Codable` (unless necessary), prefer simple `struct`.
        - usage of `Foundation` types (Date, URL).

    ### B. DTOs (Implementation)
    - Create structs matching the JSON exactly.
    - **Rules**:
        - `internal` access modifier.
        - Conforms to `Decodable` / `Encodable`.
        - Use `CodingKeys` if JSON naming differs from Swift guidelines.

    ### C. Mappers (Implementation)
    - Create extensions on Domain Models to initialize from DTOs.
    - Example:
      ```swift
      extension User {
          init(dto: UserDTO) {
              self.id = dto.id
              self.name = dto.userName
          }
      }
      ```

    ### D. Endpoints (Implementation)
    - Create `enum` conforming to `EndpointProtocol`.
    - Define `path`, `method`, `task` (body/query).

    ### E. Service Implementation
    - Implement the protocol defined in Interface.
    - Inject `NetworkClientProtocol`.
    - Call `client.request(...)`, map DTO to Domain, and return.

5.  **Cleanup**
    - Delete the temporary `swagger.json`.
    - Run `tuist generate` to ensure file references are picked up (though typically source file addition doesn't require regen if globs are used).

6.  **Verification**
    - Ask user to review the generated files.
