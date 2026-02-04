---
name: ios-swift6-master
description: Master iOS development with Swift 6. Quick reference for concurrency, strict mode, actors, Sendable, macros, typed throws, performance, and testing. Use when writing Swift 6 code, debugging concurrency issues, optimizing iOS performance, migrating to strict concurrency, or asking 'how do I use actors', 'Swift 6 strict mode', 'Sendable protocol', 'MainActor', 'async/await patterns', 'iOS best practices', 'Swift 6 migration'.
metadata:
  swift: "6.0"
  xcode: "16+"
  platforms: iOS 17+, iPadOS 17+, macOS 14+, watchOS 10+, visionOS 1+
---

# iOS Swift 6 Master

Senior-level quick reference for Swift 6 and iOS development. For detailed explanations, see `references/deep-dive.md`.

## Related Skills

| Skill | When to Use |
|-------|-------------|
| `axiom-swiftui-architecture` | SwiftUI architecture patterns, MVVM, TCA, Coordinators |
| `ios-tuist-architect` | Tuist modular architecture, 5-target structure |
| `crash-safety` | Crash risk audit, force unwraps, error handling |
| `tdd-workflow` | Test-driven development, unit testing |

---

## Swift 6 Quick Decision Trees

### Which Concurrency Pattern?

```
Need shared mutable state?
│
├─ YES → Use Actor
│   └─ UI work? → @MainActor
│   └─ Data layer? → Custom actor
│
└─ NO → Is it async work?
    ├─ YES → async/await
    └─ NO → Regular sync code
```

### Actor vs Class?

```
Is the type shared across concurrency domains?
│
├─ YES → Does it have mutable state?
│   ├─ YES → Actor ✅
│   └─ NO → Sendable struct or class
│
└─ NO → Regular class is fine
```

### Sendable Compliance?

```
Crossing concurrency boundary?
│
├─ Value type (struct/enum)?
│   └─ All properties Sendable? → Automatically Sendable ✅
│
├─ Reference type (class)?
│   ├─ Immutable (let only)? → Mark @unchecked Sendable
│   ├─ Actor? → Already Sendable ✅
│   └─ Mutable? → Convert to actor or use locks
│
└─ Closure?
    └─ Use @Sendable closure
```

---

## Swift 6 Cheatsheet

### async/await Patterns

```swift
// ✅ Basic async function
func fetchData() async throws -> Data {
    let (data, _) = try await URLSession.shared.data(from: url)
    return data
}

// ✅ Parallel execution
async let user = fetchUser()
async let posts = fetchPosts()
let (u, p) = try await (user, posts)

// ✅ Task group for dynamic parallelism
try await withThrowingTaskGroup(of: Image.self) { group in
    for url in urls {
        group.addTask { try await downloadImage(url) }
    }
    for try await image in group {
        images.append(image)
    }
}
```

### Actor Essentials

```swift
// ✅ Custom actor for thread-safe state
actor DataCache {
    private var cache: [String: Data] = [:]
    
    func get(_ key: String) -> Data? {
        cache[key]
    }
    
    func set(_ key: String, data: Data) {
        cache[key] = data
    }
}

// ✅ Using actor from async context
let cache = DataCache()
await cache.set("key", data: myData)
let data = await cache.get("key")

// ✅ nonisolated for sync access (read-only)
actor Settings {
    let appVersion: String = "1.0"  // Immutable
    
    nonisolated var version: String { appVersion }  // No await needed
}
```

### @MainActor Patterns

```swift
// ✅ Entire class on main actor
@MainActor
class ViewModel: ObservableObject {
    @Published var items: [Item] = []
    
    func load() async {
        let fetched = await service.fetch()
        items = fetched  // Safe: already on MainActor
    }
}

// ✅ Single function on main actor
func updateUI() async {
    let data = await fetchData()
    await MainActor.run {
        self.label.text = data.title
    }
}

// ✅ Assume isolated (Swift 6)
@MainActor
func process() {
    // MainActor.assumeIsolated when called from known main context
    MainActor.assumeIsolated {
        updateUI()
    }
}
```

### Sendable & Data Isolation

```swift
// ✅ Sendable struct (automatic)
struct User: Sendable {
    let id: UUID
    let name: String
}

// ✅ Sendable class (immutable)
final class Config: Sendable {
    let apiKey: String
    let baseURL: URL
    
    init(apiKey: String, baseURL: URL) {
        self.apiKey = apiKey
        self.baseURL = baseURL
    }
}

// ✅ @Sendable closure
func execute(_ work: @Sendable @escaping () async -> Void) {
    Task { await work() }
}

// ⚠️ @unchecked Sendable (use carefully)
final class LegacyCache: @unchecked Sendable {
    private let lock = NSLock()
    private var data: [String: Any] = [:]
    
    func get(_ key: String) -> Any? {
        lock.lock()
        defer { lock.unlock() }
        return data[key]
    }
}
```

### Typed Throws (Swift 6)

```swift
// ✅ Typed throws declaration
enum NetworkError: Error {
    case invalidURL
    case timeout
    case serverError(Int)
}

func fetch(url: String) throws(NetworkError) -> Data {
    guard let url = URL(string: url) else {
        throw .invalidURL
    }
    // ...
}

// ✅ Catching typed errors
do {
    let data = try fetch(url: "https://api.example.com")
} catch {
    // error is NetworkError, not any Error
    switch error {
    case .invalidURL: print("Bad URL")
    case .timeout: print("Timeout")
    case .serverError(let code): print("Server error: \(code)")
    }
}
```

### Macros (Swift 5.9+)

```swift
// ✅ Using built-in macros
@Observable  // Generates observation tracking
class Model {
    var name: String = ""
}

#Preview {  // Xcode preview macro
    ContentView()
}

// ✅ Expression macros
let url = #URL("https://api.example.com/users")  // Compile-time validated

// ✅ Debug macros
#warning("TODO: Implement this")
#error("This code path should never execute")
```

---

## iOS Best Practices (Compact)

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Types | UpperCamelCase | `UserProfile`, `NetworkManager` |
| Functions/Variables | lowerCamelCase | `fetchUser()`, `userName` |
| Constants | lowerCamelCase | `let maxRetryCount = 3` |
| Protocols (capability) | -able, -ible | `Sendable`, `Identifiable` |
| Protocols (role) | Noun | `Collection`, `Sequence` |
| Boolean | is/has/should prefix | `isLoading`, `hasError` |

### Performance Checklist

- [ ] **Lazy loading** for expensive resources
- [ ] **MainActor** only for UI updates
- [ ] **Background tasks** for heavy computation
- [ ] **Image caching** and proper sizing
- [ ] **Debounce** rapid user inputs
- [ ] **Pagination** for large data sets
- [ ] **Instruments** profiling before shipping

### Memory Management Rules

```swift
// ✅ Weak self in escaping closures
service.fetch { [weak self] result in
    guard let self else { return }
    self.process(result)
}

// ✅ Unowned when lifetime is guaranteed
class Parent {
    lazy var child = Child(parent: self)
}
class Child {
    unowned let parent: Parent  // Parent always outlives Child
}

// ✅ Capture list for specific values
let id = user.id
service.fetch { [id] result in
    // 'id' is captured by value, not 'user'
}
```

### Error Handling Patterns

```swift
// ✅ Result type for sync errors
func validate(_ input: String) -> Result<ValidInput, ValidationError> {
    guard !input.isEmpty else { return .failure(.empty) }
    return .success(ValidInput(input))
}

// ✅ Throwing for recoverable errors
func load() throws -> Config {
    guard let data = try? Data(contentsOf: configURL) else {
        throw ConfigError.notFound
    }
    return try JSONDecoder().decode(Config.self, from: data)
}

// ✅ Optional for expected absence
func findUser(id: UUID) -> User? {
    users.first { $0.id == id }
}

// ❌ NEVER force unwrap in production
let user = users.first!  // Crash risk!
```

### Testing Quick Patterns

```swift
// ✅ AAA Pattern (Arrange-Act-Assert)
func testUserCreation() {
    // Arrange
    let name = "John"
    
    // Act
    let user = User(name: name)
    
    // Assert
    XCTAssertEqual(user.name, name)
}

// ✅ Async testing
func testAsyncFetch() async throws {
    let service = MockService()
    let result = try await service.fetch()
    XCTAssertFalse(result.isEmpty)
}

// ✅ Protocol-based mocking
protocol UserServiceProtocol {
    func fetch() async throws -> [User]
}

class MockUserService: UserServiceProtocol {
    var mockUsers: [User] = []
    func fetch() async throws -> [User] { mockUsers }
}
```

---

## Strict Concurrency Migration

### Compiler Flags

```swift
// Package.swift
.target(
    name: "MyTarget",
    swiftSettings: [
        .enableExperimentalFeature("StrictConcurrency")
    ]
)

// Or in Xcode: Build Settings → Swift Compiler → Strict Concurrency = Complete
```

### Common Migration Fixes

| Warning | Fix |
|---------|-----|
| `Sendable closure captures non-Sendable` | Add @Sendable or capture Sendable values only |
| `Actor-isolated property accessed from non-isolated` | Add await or make caller async |
| `Main actor-isolated call in non-isolated context` | Add @MainActor or use MainActor.run |
| `Class not Sendable` | Make properties immutable or convert to actor |

### Migration Checklist

1. Enable `StrictConcurrency = Targeted` first
2. Fix warnings incrementally
3. Move to `StrictConcurrency = Complete`
4. Review all `@unchecked Sendable` usages
5. Test thoroughly with TSan (Thread Sanitizer)

---

## Deep Dive

For detailed explanations, advanced patterns, and comprehensive examples, see:

→ **`references/deep-dive.md`**

Topics covered:
- Complete actor internals and reentrancy
- Advanced Task management and cancellation
- AsyncSequence and AsyncStream patterns
- Distributed actors
- Custom property wrappers and result builders
- Performance profiling with Instruments
- Memory debugging techniques
