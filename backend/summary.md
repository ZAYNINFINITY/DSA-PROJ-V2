# Hospital Patient Queue System - Complete Project Documentation

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [File Structure & Purpose](#file-structure--purpose)
4. [Backend Workflow](#backend-workflow)
5. [Frontend Explanation](#frontend-explanation)
6. [API Flowchart](#api-flowchart)
7. [Architecture Justification](#architecture-justification)
8. [Queue Logic Details](#queue-logic-details)
9. [Database Schema](#database-schema)
10. [Improvements Made](#improvements-made)

---

## 🎯 Project Overview

### Purpose of the System

The Hospital Patient Queue System is a web-based application designed to manage patient queues in a hospital setting. The system prioritizes patients based on:

- **Priority Level** (1=High/Critical, 2=Medium/Urgent, 3=Low/Regular)
- **Age** (older patients served first when priority is equal)
- **ID** (earlier registrations served first when priority and age are equal)

### High-Level Workflow

```
Frontend (HTML/JS)
    ↓ HTTP Request
Flask Server (Python)
    ↓ Subprocess Call
C++ Executable (ds.exe)
    ↓ Queue Operations
SQLite Database (hospital_queue.db)
    ↓ Data Persistence
    ↑
    ↓ JSON Response
Flask Server
    ↑
Frontend (UI Updates)
```

The system maintains a **hybrid architecture** combining:

- **Python (Flask)** for web server and API routing
- **C++** for efficient queue data structure operations
- **SQLite** for persistent data storage
- **HTML/CSS/JavaScript** for the user interface

---

## 🏗️ System Architecture

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  index.html (User Interface)                         │   │
│  │  - Patient input forms                               │   │
│  │  - Queue visualization                               │   │
│  │  - Real-time updates via JavaScript                  │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTP/JSON
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND LAYER                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  app_py.py (Flask Server)                            │   │
│  │  - REST API endpoints                                │   │
│  │  - Request validation                                │   │
│  │  - Subprocess management                             │   │
│  │  - JSON response formatting                          │   │
│  └──────────────────────────────────────────────────────┘   │
│                            ↕ Subprocess                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  ds.exe (C++ Executable)                             │   │
│  │  ├── main.cpp (Entry point)                          │   │
│  │  ├── web.cpp (Command handler)                       │   │
│  │  ├── data_structures.cpp (Queue logic)               │   │
│  │  └── database.cpp (SQLite operations)                │   │
│  └──────────────────────────────────────────────────────┘   │
│                            ↕ SQL                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  hospital_queue.db (SQLite Database)                 │   │
│  │  - Persistent storage                                │   │
│  │  - Patient records                                   │   │
│  │  - Status tracking                                   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Why This Architecture?

1. **Separation of Concerns**: Each layer has a specific responsibility
2. **Performance**: C++ handles queue operations efficiently
3. **Flexibility**: Flask provides easy API management
4. **Persistence**: SQLite ensures data survives restarts
5. **Maintainability**: Modular design allows independent updates

---

## 📁 File Structure & Purpose

### Backend Files

#### `app_py.py` (Flask Backend + API)

**Purpose**: Main web server that handles HTTP requests and coordinates between frontend and C++ backend.

**Key Responsibilities**:

- Receives HTTP requests from frontend
- Validates input data (name, age, priority)
- Calls C++ executable via subprocess
- Reads data from SQLite database for responses
- Formats JSON responses for frontend
- Manages database connections using context managers
- Handles errors gracefully with proper HTTP status codes

**Key Functions**:

- `call_cpp(*args)`: Executes ds.exe with arguments and captures output
- `read_queue()`: Retrieves queued patients from database
- `read_served()`: Retrieves served patients from database
- Route handlers: `/api/add`, `/api/serve`, `/api/sort`, `/api/clear`, `/api/export`, etc.

**Why Python/Flask?**

- Easy HTTP request handling
- Simple JSON serialization
- Good subprocess support
- Rapid development
- Excellent for web APIs

---

#### `main.cpp` (Entry Point)

**Purpose**: Entry point for the C++ executable. Initializes components and delegates to command handler.

**Key Responsibilities**:

- Creates Database instance
- Creates Queue instance
- Loads existing queued patients from database into memory
- Delegates command processing to `handleCommand()`

**Why Separate Entry Point?**

- Clean separation: initialization vs. logic
- Easy to test individual components
- Follows single responsibility principle

---

#### `data_structures.h` & `data_structures.cpp` (Queue + Patient)

**Purpose**: Defines and implements the core queue data structure and patient entity.

**Key Components**:

1. **Patient Struct**:

   ```cpp
   struct Patient {
       int id;           // Unique identifier
       string name;      // Patient name
       int age;          // Patient age
       int priority;     // 1=High, 2=Medium, 3=Low
   };
   ```

2. **Queue Class**:
   - `enqueue()`: Adds patient to queue
   - `dequeue()`: Removes highest-priority patient
   - `sortByPriority()`: Sorts queue by priority rules
   - `loadPatient()`: Loads patient from database
   - `display()`: Shows current queue
   - `clear()`: Empties queue
   - `isEmpty()`, `size()`: Utility functions

**Why C++ for Queue?**

- **Performance**: C++ provides fast memory operations
- **Control**: Direct memory management for efficiency
- **Data Structures**: Native support for vectors, algorithms
- **Compiled**: Faster execution than interpreted languages

**Why Header Files (.h)?**

- **Declaration vs. Implementation**: Headers declare interfaces, .cpp files implement
- **Modularity**: Other files can include headers without implementation details
- **Compilation**: Faster compilation (only changed .cpp files recompile)
- **Encapsulation**: Clear separation of public interface and private implementation

---

#### `database.h` & `database.cpp` (SQLite Helper)

**Purpose**: Manages all database operations, providing a clean interface for queue operations.

**Key Responsibilities**:

- Database connection management
- Patient insertion with auto-increment ID
- Status updates (queued → served)
- Querying queued and served patients
- Queue clearing
- Removing served patients

**Key Functions**:

- `insertPatient()`: Adds new patient to database
- `updatePatientStatus()`: Marks patient as served
- `getQueuedPatients()`: Retrieves all queued patients (sorted)
- `getServedPatients()`: Retrieves all served patients
- `clearQueue()`: Deletes all queued patients
- `removeServedPatient()`: Deletes a served patient

**Why SQLite?**

- **File-based**: No server setup required
- **ACID Compliance**: Reliable transactions
- **Lightweight**: Minimal overhead
- **Persistent**: Data survives application restarts
- **SQL Support**: Standard query language

**Why Database Module?**

- **Abstraction**: Hides SQLite implementation details
- **Reusability**: Same database code used by all components
- **Maintainability**: Database changes only affect one file
- **Error Handling**: Centralized database error management

---

#### `web.h` & `web.cpp` (Command Handler)

**Purpose**: Handles command-line arguments and interactive menu for the C++ executable.

**Key Responsibilities**:

- Parses command-line arguments
- Routes commands to appropriate queue/database operations
- Provides interactive menu when no arguments provided
- Validates input parameters
- Outputs results to console

**Commands Supported**:

- `add <name> <age> <priority>`: Add patient
- `serve`: Serve next patient
- `sort`: Sort queue
- `display`: Show queue
- `clear`: Clear queue
- `remove_served <id>`: Remove served patient

**Why Separate Command Handler?**

- **Separation**: Command parsing separate from business logic
- **Flexibility**: Easy to add new commands
- **Testing**: Can test commands independently
- **CLI Support**: Allows both API and command-line usage

---

#### `init_db.sql` (Database Schema)

**Purpose**: Defines the database schema for patient storage.

**Schema**:

```sql
CREATE TABLE patients (
    id INTEGER PRIMARY KEY,           -- Auto-increment ID
    name TEXT NOT NULL,               -- Patient name
    age INTEGER NOT NULL,             -- Patient age
    priority INTEGER NOT NULL,        -- 1, 2, or 3
    status TEXT NOT NULL,             -- 'queued' or 'served'
    created_at DATETIME,              -- Registration timestamp
    served_at DATETIME                -- Service timestamp
);
```

**Indexes**: Created on `status` and `priority` for faster queries.

---

### Frontend Files

#### `index.html` (User Interface)

**Purpose**: Provides the web interface for interacting with the queue system.

**Features**:

- Patient input form (name, age, priority)
- Real-time queue display with patient cards
- Served patients list
- Search functionality
- Statistics (queue count, served count)
- Export functionality
- Auto-refresh every 2 seconds

**Technology**: Pure HTML/CSS/JavaScript (no frameworks)

---

## 🔄 Backend Workflow

### 1. Flask Receives Request

```python
@app.route('/api/add', methods=['POST'])
def add_patient():
    # 1. Validate JSON request
    # 2. Extract and validate data (name, age, priority)
    # 3. Call C++ executable
    # 4. Read updated queue from database
    # 5. Return JSON response
```

### 2. Flask Calls C++ Executable

```python
def call_cpp(*args):
    # Uses subprocess.run() to execute ds.exe
    # Passes arguments: ['ds.exe', 'add', 'John', '45', '1']
    # Captures stdout/stderr
    # Returns success/error status
```

### 3. C++ Executable Processing

```
main.cpp:
  1. Initialize Database connection
  2. Initialize Queue
  3. Load existing queued patients from DB into Queue
  4. Call handleCommand() with arguments

web.cpp (handleCommand):
  1. Parse command ('add', 'serve', etc.)
  2. Validate arguments
  3. Call Queue methods (enqueue, dequeue, etc.)
  4. Call Database methods (insertPatient, updateStatus, etc.)
  5. Output result to stdout

data_structures.cpp:
  - Queue operations (enqueue, dequeue, sort)
  - Priority-based sorting logic

database.cpp:
  - SQLite operations
  - INSERT, UPDATE, SELECT, DELETE queries
```

### 4. Database Operations

- **Insert**: New patient added with auto-increment ID
- **Update**: Patient status changed from 'queued' to 'served'
- **Select**: Queries retrieve patients sorted by priority rules
- **Delete**: Queue clearing or served patient removal

### 5. Queue Operations Interact with SQLite

- **On Add**: Patient added to Queue in memory, then inserted into DB
- **On Serve**: Patient dequeued from Queue, then status updated in DB
- **On Load**: Database queried, patients loaded into Queue
- **On Sort**: Queue sorted in memory (DB not updated, but query order matches)

**Why Load from DB?**

- Ensures queue state matches database after restart
- Handles concurrent operations correctly
- Maintains data consistency

---

## 🖥️ Frontend Explanation

### How Frontend Sends API Requests

1. **User Action**: User fills form and clicks "Add Patient"
2. **JavaScript Function**: `addPatient()` is called
3. **Fetch API**: JavaScript uses `fetch()` to send POST request
   ```javascript
   fetch("/api/add", {
     method: "POST",
     headers: { "Content-Type": "application/json" },
     body: JSON.stringify({ name, age, priority }),
   });
   ```
4. **Response Handling**: Promise resolves with JSON response
5. **UI Update**: DOM updated with new queue data

### How Data Flows Back to UI

1. **Flask Response**: Returns JSON like:

   ```json
   {
       "success": true,
       "output": "Patient added successfully...",
       "queue": [
           {"id": 1, "name": "John", "age": 45, "priority": 1},
           ...
       ]
   }
   ```

2. **JavaScript Processing**:

   - Updates `queue` array
   - Calls `renderQueue()` to update DOM
   - Shows toast notification

3. **Auto-Refresh**: Every 2 seconds, `loadQueue()` fetches latest data

4. **Real-time Updates**: UI reflects current database state

---

## 📊 API Flowchart

```
┌─────────────┐
│   Frontend  │
│  (Browser)  │
└──────┬──────┘
       │ HTTP POST /api/add
       │ {name, age, priority}
       ↓
┌─────────────────────────────────────┐
│         Flask Server                │
│  (app_py.py)                        │
│  ┌───────────────────────────────┐  │
│  │ 1. Validate request           │  │
│  │ 2. Extract JSON data          │  │
│  │ 3. Validate age/priority      │  │
│  └───────────────────────────────┘  │
└──────┬──────────────────────────────┘
       │ subprocess.run(['ds.exe', 'add', ...])
       ↓
┌─────────────────────────────────────┐
│      C++ Executable (ds.exe)        │
│  ┌───────────────────────────────┐  │
│  │ main.cpp:                     │  │
│  │ - Initialize Database         │  │
│  │ - Initialize Queue            │  │
│  │ - Load existing patients      │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │ web.cpp:                      │  │
│  │ - Parse 'add' command         │  │
│  │ - Extract name, age, priority │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │ data_structures.cpp:          │  │
│  │ - Queue.enqueue()             │  │
│  │ - Creates Patient object      │  │
│  │ - Adds to vector              │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │ database.cpp:                 │  │
│  │ - Database.insertPatient()    │  │
│  │ - SQL: INSERT INTO patients   │  │
│  │ - Returns auto-generated ID   │  │
│  └───────────────────────────────┘  │
│       │ stdout: "Patient added..."  │
└───────┼─────────────────────────────┘
        │ Return to Flask
        ↓
┌─────────────────────────────────────┐
│         Flask Server                │
│  ┌───────────────────────────────┐  │
│  │ 1. Parse C++ output           │  │
│  │ 2. Read queue from DB         │  │
│  │ 3. Format JSON response       │  │
│  └───────────────────────────────┘  │
└──────┬──────────────────────────────┘
       │ HTTP 200 OK
       │ JSON Response
       ↓
┌─────────────┐
│   Frontend  │
│  (Browser)  │
│  ┌────────┐ │
│  │ Update │ │
│  │   UI   │ │
│  └────────┘ │
└─────────────┘
```

### Detailed Flow for Each Operation

#### Add Patient Flow:

1. Frontend → Flask: POST `/api/add` with JSON
2. Flask → C++: `subprocess.run(['ds.exe', 'add', name, age, priority])`
3. C++ → Queue: `q.enqueue(name, age, priority)` (creates Patient, assigns ID)
4. C++ → Database: `db.insertPatient(p)` (INSERT SQL, gets DB ID)
5. C++ → stdout: "Patient added successfully with ID: X"
6. Flask ← C++: Captures stdout, parses success
7. Flask → Database: `read_queue()` (SELECT SQL, sorted)
8. Flask → Frontend: JSON with success status and updated queue
9. Frontend: Updates UI, shows notification

#### Serve Patient Flow:

1. Frontend → Flask: POST `/api/serve`
2. Flask → C++: `subprocess.run(['ds.exe', 'serve'])`
3. C++ → Queue: `q.dequeue()` (finds highest priority, removes from vector)
4. C++ → Database: `db.updatePatientStatus(id)` (UPDATE SQL, sets status='served')
5. C++ → stdout: "Served patient: Name (ID: X)"
6. Flask ← C++: Captures output
7. Flask → Database: `read_queue()` and `read_served()` (two SELECT queries)
8. Flask → Frontend: JSON with updated queue and served list
9. Frontend: Updates both queue and served sections

---

## 🏛️ Architecture Justification

### Why Separate Header Files (.h) and Implementation Files (.cpp)?

1. **Compilation Efficiency**:

   - Headers contain declarations (interfaces)
   - Implementation files contain definitions (code)
   - Only changed .cpp files need recompilation
   - Multiple files can include same header without code duplication

2. **Encapsulation**:

   - Headers show public interface
   - Implementation details hidden in .cpp
   - Easier to understand what a class does

3. **Modularity**:

   - Clear separation of concerns
   - Easy to swap implementations
   - Better organization

4. **Standard Practice**:
   - C++ convention
   - Industry standard
   - Easier for other developers

### Why Logic is Kept in .cpp Files?

1. **Separation of Interface and Implementation**:

   - Headers declare "what"
   - .cpp files define "how"

2. **Compilation Speed**:

   - Changes to implementation don't require recompiling all files that include the header
   - Only the changed .cpp file needs recompilation

3. **Linking**:
   - Object files (.o) from .cpp files are linked together
   - Headers are just included (text substitution)

### Why main.cpp Only Coordinates?

1. **Single Responsibility**:

   - main.cpp handles initialization and delegation
   - Business logic in other files
   - Easy to understand entry point

2. **Testability**:

   - Can test components independently
   - main.cpp is thin, easy to verify

3. **Maintainability**:
   - Changes to logic don't affect main.cpp
   - Clear flow: main → handler → logic → database

### Why Database and Queue are Modularized?

1. **Separation of Concerns**:

   - Queue handles data structure operations
   - Database handles persistence
   - Clear boundaries

2. **Reusability**:

   - Database class can be used by other components
   - Queue can work with different storage backends

3. **Testability**:

   - Can test queue without database
   - Can test database without queue
   - Mock dependencies easily

4. **Maintainability**:
   - Database changes don't affect queue logic
   - Queue changes don't affect database schema

### Why SQLite Database File Instead of Manual Storage?

1. **ACID Properties**:

   - Atomicity: All or nothing operations
   - Consistency: Data always valid
   - Isolation: Concurrent operations don't interfere
   - Durability: Data survives crashes

2. **Query Capabilities**:

   - SQL provides powerful querying
   - Sorting, filtering, aggregations
   - Indexes for performance

3. **Data Integrity**:

   - Constraints (CHECK, NOT NULL)
   - Foreign keys (if needed)
   - Type safety

4. **Persistence**:

   - Data survives application restarts
   - No need to rebuild queue from scratch
   - Historical data preserved

5. **Concurrency**:

   - SQLite handles concurrent reads
   - Locking mechanisms
   - Safe for multiple processes

6. **Standardization**:
   - SQL is well-known
   - Easy to inspect data
   - Can use SQLite tools

### Why C++ Handles Queue Instead of Python?

1. **Performance**:

   - C++ is compiled, faster execution
   - Direct memory access
   - No interpreter overhead
   - Efficient for data structure operations

2. **Memory Management**:

   - Fine-grained control
   - No garbage collection pauses
   - Predictable performance

3. **Data Structures**:

   - Native support for vectors, algorithms
   - std::sort is highly optimized
   - Efficient pointer operations

4. **Suitability**:

   - Queue operations are compute-intensive
   - C++ excels at algorithms
   - Better for large datasets

5. **Learning Value**:
   - Demonstrates multi-language architecture
   - Shows when to use each language
   - Real-world pattern (Python for web, C++ for compute)

---

## 🎯 Queue Logic Details

### Priority Rules (Consistent Throughout System)

The queue uses a **three-tier sorting system**:

1. **Priority (ASC)**: Lower number = higher priority

   - Priority 1 (High/Critical) served first
   - Priority 2 (Medium/Urgent) served second
   - Priority 3 (Low/Regular) served last

2. **Age (DESC)**: When priority is equal, older patients served first

   - Age 80 served before Age 30
   - Age 50 served before Age 25

3. **ID (ASC)**: When priority and age are equal, lower ID served first
   - ID 1 served before ID 5
   - ID 10 served before ID 15

### Implementation in Code

#### C++ Queue Sort (data_structures.cpp):

```cpp
std::sort(patients.begin(), patients.end(), [](const Patient& a, const Patient& b) {
    // 1. Priority ASC
    if (a.priority != b.priority) {
        return a.priority < b.priority;
    }
    // 2. Age DESC
    if (a.age != b.age) {
        return a.age > b.age;
    }
    // 3. ID ASC
    return a.id < b.id;
});
```

#### Database Query (database.cpp):

```sql
SELECT id, name, age, priority
FROM patients
WHERE status = 'queued'
ORDER BY priority ASC, age DESC, id ASC
```

#### Python Query (app_py.py):

```python
cursor.execute(
    "SELECT id, name, age, priority FROM patients WHERE status = 'queued' "
    "ORDER BY priority ASC, age DESC, id ASC"
)
```

**All three places use the same logic for consistency!**

### Dequeue Algorithm

The `dequeue()` function finds the best patient without sorting the entire queue:

1. Start with first patient as "best"
2. Compare each remaining patient:
   - If priority is lower → new best
   - If priority equal and age higher → new best
   - If priority and age equal and ID lower → new best
3. Remove and return best patient

**Why not sort first?**

- More efficient: O(n) vs O(n log n)
- Only need to find one patient
- Sorting entire queue unnecessary

---

## 💾 Database Schema

### Patients Table

```sql
CREATE TABLE patients (
    id INTEGER PRIMARY KEY,              -- Auto-increment, unique identifier
    name TEXT NOT NULL,                  -- Patient's full name
    age INTEGER NOT NULL,                -- Patient's age (1-150)
    priority INTEGER NOT NULL            -- Priority level (1, 2, or 3)
        CHECK(priority IN (1,2,3)),
    status TEXT NOT NULL                 -- Current status
        DEFAULT 'queued'
        CHECK(status IN ('queued', 'served')),
    created_at DATETIME                  -- Registration timestamp
        DEFAULT CURRENT_TIMESTAMP,
    served_at DATETIME                   -- Service timestamp (NULL if queued)
);
```

### Indexes

```sql
CREATE INDEX idx_status ON patients(status);      -- Fast status filtering
CREATE INDEX idx_priority ON patients(priority);  -- Fast priority sorting
```

### Why These Fields?

- **id**: Unique identifier, auto-incremented
- **name**: Patient identification
- **age**: Used in priority sorting
- **priority**: Primary sorting criterion
- **status**: Distinguishes queued vs served
- **created_at**: Timestamp for registration order
- **served_at**: Timestamp for service tracking

---

## ✨ Improvements Made

### 1. Code Quality Improvements

#### app_py.py:

- ✅ Added context manager for database connections (prevents leaks)
- ✅ Improved error handling with try-except blocks
- ✅ Added input validation (age range, priority values)
- ✅ Consistent JSON responses with success/error fields
- ✅ Added timeout for subprocess calls (prevents hanging)
- ✅ Better error messages for debugging
- ✅ Used list comprehensions for cleaner code

#### data_structures.cpp:

- ✅ Replaced bubble sort with `std::sort` (O(n log n) vs O(n²))
- ✅ Used lambda function for cleaner comparison logic
- ✅ Fixed type safety (size_t for indices)
- ✅ Improved empty patient initialization
- ✅ Added explicit casting for size() return

#### database.cpp:

- ✅ Added null pointer checks for database connection
- ✅ Improved error messages with context
- ✅ Used nullptr instead of 0/NULL
- ✅ Added error handling for all SQL operations
- ✅ Fixed memory safety (null checks for text columns)
- ✅ Consistent error reporting

#### web.cpp:

- ✅ Removed code duplication (extracted helper functions)
- ✅ Added input validation for command-line arguments
- ✅ Improved error handling with try-catch
- ✅ Better user feedback for invalid input
- ✅ Cleaner code structure

#### main.cpp:

- ✅ Fixed indentation
- ✅ Cleaner includes

### 2. Logic Consistency

- ✅ **Fixed sorting consistency**: All three places (C++ sort, DB query, Python query) now use: `priority ASC, age DESC, id ASC`
- ✅ **Database query updated**: Changed from `created_at ASC` to `id ASC` for consistency
- ✅ **Queue logic verified**: Dequeue and sort use same priority rules

### 3. Safety Improvements

- ✅ **Database connection management**: Context managers prevent leaks
- ✅ **Null pointer checks**: All database operations check for null
- ✅ **Input validation**: Age, priority, and name validated
- ✅ **Error handling**: All operations have proper error handling
- ✅ **Type safety**: Fixed size_t/int mismatches

### 4. Performance Improvements

- ✅ **Optimized sorting**: std::sort instead of bubble sort
- ✅ **Efficient queries**: Indexes on status and priority
- ✅ **Connection pooling**: Context managers reuse connections efficiently

### 5. Maintainability

- ✅ **Code organization**: Clear separation of concerns
- ✅ **Consistent naming**: All functions follow naming conventions
- ✅ **Documentation**: Comments explain complex logic
- ✅ **Error messages**: Clear, actionable error messages

---

## 🔐 Authentication Consideration

**Decision: Authentication NOT Added**

After analyzing the codebase, adding authentication (login/register) would require:

- New database table (users)
- Session management or JWT tokens
- Protected routes middleware
- Password hashing
- Login/logout endpoints
- Frontend login UI
- Session state management

This would significantly increase complexity and is not necessary for the core queue management functionality. The system is designed for internal hospital use where authentication can be handled at the network/infrastructure level if needed.

**Recommendation**: If authentication is needed later, it should be added as a separate module without disrupting the existing architecture.

---

## 📝 API Endpoints Summary

| Endpoint             | Method | Purpose                    | Request Body            | Response                     |
| -------------------- | ------ | -------------------------- | ----------------------- | ---------------------------- |
| `/`                  | GET    | Serve frontend             | None                    | HTML page                    |
| `/api/queue`         | GET    | Get current queue          | None                    | `{queue: [], served: []}`    |
| `/api/add`           | POST   | Add patient                | `{name, age, priority}` | `{success, queue}`           |
| `/api/serve`         | POST   | Serve next patient         | None                    | `{success, queue, served}`   |
| `/api/sort`          | POST   | Sort queue                 | None                    | `{success, queue}`           |
| `/api/clear`         | POST   | Clear queue                | None                    | `{success, queue, served}`   |
| `/api/export`        | GET    | Export all data            | None                    | `{patients, timestamp, ...}` |
| `/api/display`       | GET    | Display queue (C++ output) | None                    | `{success, output}`          |
| `/api/remove_served` | POST   | Remove served patient      | `{id}`                  | `{success, served}`          |

---

## 🚀 Running the System

### Prerequisites

- Python 3.x with Flask and flask-cors
- C++ compiler (g++ or MSVC)
- SQLite3 library

### Compilation

```bash
cd backend
g++ main.cpp web.cpp data_structures.cpp database.cpp -o ds.exe -lsqlite3
```

### Running

```bash
cd backend
python app_py.py
```

### Access

Open browser to: `http://localhost:5000`

---

## 📚 Conclusion

This Hospital Patient Queue System demonstrates a well-architected hybrid application combining:

- **Python** for web server flexibility
- **C++** for performance-critical queue operations
- **SQLite** for reliable data persistence
- **Modern web technologies** for user interface

The architecture is:

- ✅ **Modular**: Clear separation of concerns
- ✅ **Maintainable**: Easy to understand and modify
- ✅ **Performant**: Efficient algorithms and data structures
- ✅ **Reliable**: Proper error handling and data persistence
- ✅ **Scalable**: Can handle growing patient queues

The system successfully manages patient queues with priority-based sorting, ensuring critical patients are served first while maintaining fairness through age and registration order.

---

**Document Version**: 1.0  
**Last Updated**: 2024  
**Project**: Hospital Patient Queue System (DSA-PROJ-V2)
