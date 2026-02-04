# iOS Swift 6 Deep Dive

Detailed explanations and advanced patterns for Swift 6 and iOS development.

---

## Table of Contents

1. [Swift 6 Concurrency Deep Dive](#swift-6-concurrency-deep-dive)
2. [Actor Internals](#actor-internals)
3. [Task Management](#task-management)
4. [AsyncSequence & AsyncStream](#asyncsequence--asyncstream)
5. [Advanced Sendable Patterns](#advanced-sendable-patterns)
6. [Property Wrappers](#property-wrappers)
7. [Result Builders](#result-builders)
8. [Performance Optimization](#performance-optimization)
9. [Memory Management Deep Dive](#memory-management-deep-dive)
10. [Testing Strategies](#testing-strategies)

---

## Swift 6 Concurrency Deep Dive

### Understanding Structured Concurrency

Swift's structured concurrency ensures that child tasks cannot outlive parent tasks, preventing resource leaks and dangling operations.

```swift
// ✅ Structured: Child tasks bound to parent scope
func processImages(_ urls: [URL]) async throws -> [Image] {
    try await withThrowingTaskGroup(of: Image.self) { group in
        for url in urls {
            group.addTask {
                try await downloadImage(url)
            }
        }
        
        var images: [Image] = []
        for try await image in group {
            images.append(image)
        }
        return images
    }
    // All child tasks guaranteed to complete here
}

// ✅ Unstructured: Use when task lifetime differs from scope
func startBackgroundSync() {
    Task.detached(priority: .background) {
        await syncWithServer()
    }
    // Task continues after function returns
}
```

### Task Priority and Inheritance

```swift
// Task inherits priority from context
Task {  // Inherits current priority
    await doWork()
}

Task(priority: .high) {  // Explicit priority
    await urgentWork()
}

Task.detached(priority: .background) {  // No inheritance
    await backgroundWork()
}

// Priority escalation happens automatically
// If high-priority task awaits low-priority task, the low-priority gets escalated
```

### Cancellation Handling

```swift
func fetchWithCancellation() async throws -> Data {
    // Check cancellation before expensive work
    try Task.checkCancellation()
    
    // Cooperative cancellation in loops
    for url in urls {
        guard !Task.isCancelled else {
            throw CancellationError()
        }
        await process(url)
    }
    
    // withTaskCancellationHandler for cleanup
    return try await withTaskCancellationHandler {
        try await longRunningFetch()
    } onCancel: {
        // Called immediately when task is cancelled
        connection.cancel()
    }
}

// Cancelling tasks
let task = Task {
    await longWork()
}
task.cancel()  // Requests cancellation (cooperative)
```

---

## Actor Internals

### Actor Reentrancy

Actors are reentrant: when an actor awaits, other calls can execute. This can cause state changes between awaits.

```swift
actor BankAccount {
    var balance: Int = 100
    
    // ⚠️ Reentrancy issue
    func transferIfSufficient(amount: Int, to other: BankAccount) async {
        guard balance >= amount else { return }
        
        // ⚠️ balance could change here while awaiting!
        await other.deposit(amount)
        
        // This might overdraw if another transfer happened during await
        balance -= amount
    }
    
    // ✅ Fix: Capture state before await
    func safeTransfer(amount: Int, to other: BankAccount) async -> Bool {
        guard balance >= amount else { return false }
        
        // Deduct first (synchronous)
        balance -= amount
        
        // Then deposit (async, safe now)
        await other.deposit(amount)
        return true
    }
    
    func deposit(_ amount: Int) {
        balance += amount
    }
}
```

### GlobalActor Pattern

```swift
// Define a global actor
@globalActor
actor DatabaseActor {
    static let shared = DatabaseActor()
}

// Use it to isolate database operations
@DatabaseActor
class DatabaseManager {
    private var connection: Connection?
    
    func query(_ sql: String) async -> [Row] {
        // All calls serialized on DatabaseActor
    }
}

// Functions can be isolated to global actors
@DatabaseActor
func performDatabaseWork() async {
    // Runs on DatabaseActor
}
```

### Actor-Isolated Properties

```swift
actor Counter {
    var count = 0
    
    // Synchronous access within actor
    func increment() {
        count += 1  // No await needed
    }
    
    // nonisolated for thread-safe read-only access
    nonisolated let id = UUID()  // Immutable, safe to read from anywhere
    
    // Computed property accessing isolated state
    var doubleCount: Int {
        count * 2  // Within actor, synchronous
    }
}

// External access requires await
let counter = Counter()
await counter.increment()
let value = await counter.count
let id = counter.id  // No await (nonisolated)
```

---

## Task Management

### Task Local Values

```swift
enum RequestContext {
    @TaskLocal static var requestID: String?
    @TaskLocal static var user: User?
}

func handleRequest() async {
    await RequestContext.$requestID.withValue("req-123") {
        await processRequest()
    }
}

func processRequest() async {
    // Access task local anywhere in the call chain
    if let id = RequestContext.requestID {
        logger.log("Processing \(id)")
    }
}
```

### Task Groups with Results

```swift
// Collecting all results
func fetchAllUsers(ids: [UUID]) async throws -> [User] {
    try await withThrowingTaskGroup(of: User.self) { group in
        for id in ids {
            group.addTask {
                try await fetchUser(id: id)
            }
        }
        return try await group.reduce(into: []) { $0.append($1) }
    }
}

// First successful result
func fetchFromAnyMirror(mirrors: [URL]) async -> Data? {
    await withTaskGroup(of: Data?.self) { group in
        for mirror in mirrors {
            group.addTask {
                try? await fetch(from: mirror)
            }
        }
        
        for await result in group {
            if let data = result {
                group.cancelAll()  // Cancel remaining
                return data
            }
        }
        return nil
    }
}
```

---

## AsyncSequence & AsyncStream

### Custom AsyncSequence

```swift
struct Counter: AsyncSequence {
    typealias Element = Int
    let limit: Int
    
    struct AsyncIterator: AsyncIteratorProtocol {
        var current = 0
        let limit: Int
        
        mutating func next() async -> Int? {
            guard current < limit else { return nil }
            defer { current += 1 }
            return current
        }
    }
    
    func makeAsyncIterator() -> AsyncIterator {
        AsyncIterator(limit: limit)
    }
}

// Usage
for await number in Counter(limit: 10) {
    print(number)
}
```

### AsyncStream for Bridging

```swift
// Bridging callback-based APIs
func locationUpdates() -> AsyncStream<CLLocation> {
    AsyncStream { continuation in
        let manager = CLLocationManager()
        let delegate = LocationDelegate { location in
            continuation.yield(location)
        }
        manager.delegate = delegate
        manager.startUpdatingLocation()
        
        continuation.onTermination = { _ in
            manager.stopUpdatingLocation()
        }
    }
}

// Buffering stream
func notifications(named name: Notification.Name) -> AsyncStream<Notification> {
    AsyncStream(bufferingPolicy: .bufferingNewest(5)) { continuation in
        let observer = NotificationCenter.default.addObserver(
            forName: name,
            object: nil,
            queue: nil
        ) { notification in
            continuation.yield(notification)
        }
        
        continuation.onTermination = { _ in
            NotificationCenter.default.removeObserver(observer)
        }
    }
}
```

### AsyncThrowingStream

```swift
func fetchPages() -> AsyncThrowingStream<Page, Error> {
    AsyncThrowingStream { continuation in
        Task {
            var nextURL: URL? = initialURL
            
            while let url = nextURL {
                do {
                    let page = try await fetch(url)
                    continuation.yield(page)
                    nextURL = page.nextPageURL
                } catch {
                    continuation.finish(throwing: error)
                    return
                }
            }
            continuation.finish()
        }
    }
}
```

---

## Advanced Sendable Patterns

### Sendable Closures in Practice

```swift
// ✅ @Sendable closure captures must be Sendable
func process(with handler: @Sendable @escaping () -> Void) {
    Task {
        handler()
    }
}

// ✅ Capturing Sendable values
let id = UUID()  // UUID is Sendable
process { 
    print(id)  // OK
}

// ❌ Non-Sendable capture error
class NonSendable {
    var value = 0
}
let obj = NonSendable()
process {
    print(obj.value)  // Error: capturing non-Sendable
}
```

### Making Legacy Code Sendable

```swift
// Using locks for thread safety
final class ThreadSafeCache<Key: Hashable & Sendable, Value: Sendable>: @unchecked Sendable {
    private var storage: [Key: Value] = [:]
    private let lock = NSLock()
    
    subscript(key: Key) -> Value? {
        get {
            lock.lock()
            defer { lock.unlock() }
            return storage[key]
        }
        set {
            lock.lock()
            defer { lock.unlock() }
            storage[key] = newValue
        }
    }
}

// Using dispatch queue isolation
final class QueueIsolated<Value>: @unchecked Sendable {
    private var _value: Value
    private let queue = DispatchQueue(label: "isolation")
    
    init(_ value: Value) {
        _value = value
    }
    
    var value: Value {
        queue.sync { _value }
    }
    
    func mutate(_ transform: (inout Value) -> Void) {
        queue.sync { transform(&_value) }
    }
}
```

---

## Property Wrappers

### Custom Property Wrappers

```swift
// Clamping values to a range
@propertyWrapper
struct Clamped<Value: Comparable> {
    private var value: Value
    private let range: ClosedRange<Value>
    
    var wrappedValue: Value {
        get { value }
        set { value = min(max(newValue, range.lowerBound), range.upperBound) }
    }
    
    init(wrappedValue: Value, _ range: ClosedRange<Value>) {
        self.range = range
        self.value = min(max(wrappedValue, range.lowerBound), range.upperBound)
    }
}

// Usage
struct Volume {
    @Clamped(0...100) var level: Int = 50
}

var volume = Volume()
volume.level = 150  // Clamped to 100
```

### Property Wrapper with Projection

```swift
@propertyWrapper
struct Validated<Value> {
    private var value: Value
    private(set) var isValid: Bool = false
    private let validator: (Value) -> Bool
    
    var wrappedValue: Value {
        get { value }
        set {
            value = newValue
            isValid = validator(newValue)
        }
    }
    
    var projectedValue: Bool { isValid }
    
    init(wrappedValue: Value, validator: @escaping (Value) -> Bool) {
        self.value = wrappedValue
        self.validator = validator
        self.isValid = validator(wrappedValue)
    }
}

// Usage
struct Form {
    @Validated(validator: { $0.contains("@") })
    var email: String = ""
}

var form = Form()
form.email = "test@example.com"
print(form.$email)  // true (projectedValue)
```

---

## Result Builders

### Custom Result Builder

```swift
@resultBuilder
struct ArrayBuilder<Element> {
    static func buildBlock(_ components: Element...) -> [Element] {
        components
    }
    
    static func buildOptional(_ component: [Element]?) -> [Element] {
        component ?? []
    }
    
    static func buildEither(first component: [Element]) -> [Element] {
        component
    }
    
    static func buildEither(second component: [Element]) -> [Element] {
        component
    }
    
    static func buildArray(_ components: [[Element]]) -> [Element] {
        components.flatMap { $0 }
    }
}

// Usage
func makeNumbers(@ArrayBuilder<Int> content: () -> [Int]) -> [Int] {
    content()
}

let numbers = makeNumbers {
    1
    2
    if true { 3 }
    for i in 4...6 { i }
}
// [1, 2, 3, 4, 5, 6]
```

---

## Performance Optimization

### Instruments Profiling Checklist

1. **Time Profiler** — Find CPU hotspots
2. **Allocations** — Track memory growth
3. **Leaks** — Detect retain cycles
4. **System Trace** — Thread blocking and context switches
5. **Network** — Request timing and payload sizes
6. **Core Animation** — Frame drops and GPU usage

### Common Performance Patterns

```swift
// ✅ Lazy initialization
class ViewController {
    lazy var heavyObject = HeavyObject()  // Created only when accessed
}

// ✅ Collection pre-allocation
var items: [Item] = []
items.reserveCapacity(1000)

// ✅ Copy-on-write for value types
struct LargeData {
    private var storage: Storage
    
    private final class Storage {
        var data: [UInt8]
    }
    
    mutating func modify() {
        if !isKnownUniquelyReferenced(&storage) {
            storage = Storage(data: storage.data)
        }
        // Now safe to mutate
    }
}

// ✅ Debouncing rapid inputs
import Combine

class SearchViewModel {
    private var cancellables = Set<AnyCancellable>()
    
    func setup(searchText: Published<String>.Publisher) {
        searchText
            .debounce(for: .milliseconds(300), scheduler: RunLoop.main)
            .removeDuplicates()
            .sink { [weak self] query in
                self?.search(query)
            }
            .store(in: &cancellables)
    }
}
```

---

## Memory Management Deep Dive

### Debugging Retain Cycles

```swift
// Debug helper
class LeakDetector {
    static func track<T: AnyObject>(_ object: T, file: String = #file, line: Int = #line) {
        let description = "\(type(of: object)) at \(file):\(line)"
        weak var weakRef = object
        
        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
            if weakRef != nil {
                print("⚠️ Potential leak: \(description)")
            }
        }
    }
}

// Usage in deinit
deinit {
    print("✅ \(type(of: self)) deallocated")
}
```

### Weak Reference Patterns

```swift
// Weak wrapper for collections
class Weak<T: AnyObject> {
    weak var value: T?
    init(_ value: T) { self.value = value }
}

class Broadcaster {
    private var listeners: [Weak<Listener>] = []
    
    func addListener(_ listener: Listener) {
        listeners.append(Weak(listener))
    }
    
    func broadcast(_ message: String) {
        listeners = listeners.filter { $0.value != nil }
        listeners.forEach { $0.value?.receive(message) }
    }
}
```

---

## Testing Strategies

### Async Testing Patterns

```swift
// Testing async code
func testAsyncOperation() async throws {
    let sut = DataLoader()
    let result = try await sut.load()
    XCTAssertEqual(result.count, 10)
}

// Testing with timeout
func testWithTimeout() async throws {
    let expectation = expectation(description: "completion")
    
    Task {
        try await sut.longOperation()
        expectation.fulfill()
    }
    
    await fulfillment(of: [expectation], timeout: 5.0)
}

// Testing actor state
func testActorState() async {
    let counter = Counter()
    await counter.increment()
    await counter.increment()
    let value = await counter.count
    XCTAssertEqual(value, 2)
}
```

### Dependency Injection for Testing

```swift
// Protocol-based dependencies
protocol NetworkClient: Sendable {
    func fetch(_ url: URL) async throws -> Data
}

class RealClient: NetworkClient {
    func fetch(_ url: URL) async throws -> Data {
        let (data, _) = try await URLSession.shared.data(from: url)
        return data
    }
}

class MockClient: NetworkClient {
    var mockData: Data = Data()
    var mockError: Error?
    
    func fetch(_ url: URL) async throws -> Data {
        if let error = mockError { throw error }
        return mockData
    }
}

// ViewModel with injected dependency
@Observable
class UserViewModel {
    private let client: NetworkClient
    var users: [User] = []
    
    init(client: NetworkClient = RealClient()) {
        self.client = client
    }
    
    func load() async throws {
        let data = try await client.fetch(usersURL)
        users = try JSONDecoder().decode([User].self, from: data)
    }
}

// Test
func testLoadUsers() async throws {
    let mock = MockClient()
    mock.mockData = """
    [{"id": 1, "name": "Test"}]
    """.data(using: .utf8)!
    
    let vm = UserViewModel(client: mock)
    try await vm.load()
    
    XCTAssertEqual(vm.users.count, 1)
    XCTAssertEqual(vm.users.first?.name, "Test")
}
```

---

## Related Skills Reference

- **Architecture Patterns** → `axiom-swiftui-architecture`
- **Modular Structure** → `ios-tuist-architect`
- **Crash Prevention** → `crash-safety`
- **Test-Driven Development** → `tdd-workflow`
