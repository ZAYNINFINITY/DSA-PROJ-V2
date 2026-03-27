# 🏥 Hospital Queue Management System - Complete Project Explanation

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [How It Works](#how-it-works)
4. [Workflow](#workflow)
5. [Features](#features)
6. [Technical Components](#technical-components)
7. [Setup & Usage](#setup--usage)
8. [API Endpoints](#api-endpoints)

---

## 🎯 Project Overview

**Hospital Queue Management System** is a full-stack application designed to efficiently manage patient queues in a hospital setting. The system helps hospital staff:

- Add patients to a queue with priority levels
- Serve patients in priority order
- Track served patients
- Manage and organize the queue efficiently

### Key Highlights

- ✅ **Mobile App** (Android) built with Capacitor
- ✅ **Web App** (Browser-based)
- ✅ **Backend** (Flask + SQLite + C++ executable)
- ✅ **Real-time Updates** (Auto-refresh every 2 seconds)
- ✅ **Help Assistant Chatbot** (Built-in guidance)

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                        │
│  ┌──────────────┐         ┌──────────────┐             │
│  │  Mobile App  │         │   Web App    │             │
│  │  (Capacitor) │         │  (Browser)   │             │
│  └──────┬───────┘         └──────┬───────┘             │
│         │                        │                      │
│         └────────────┬───────────┘                      │
│                      │                                   │
│         ┌────────────▼───────────┐                      │
│         │   Frontend Files       │                      │
│         │  - index.html          │                      │
│         │  - styles.css          │                      │
│         │  - config.js           │                      │
│         │  - chatbot.js          │                      │
│         └────────────┬───────────┘                      │
└──────────────────────┼──────────────────────────────────┘
                       │
                       │ HTTP Requests (REST API)
                       │
┌──────────────────────▼──────────────────────────────────┐
│                  BACKEND LAYER                          │
│  ┌──────────────────────────────────────────────┐      │
│  │         Flask Server (Python)                │      │
│  │  - Handles HTTP requests                     │      │
│  │  - Manages API endpoints                     │      │
│  │  - Processes queue operations                 │      │
│  └──────────────┬───────────────────────────────┘      │
│                 │                                       │
│         ┌───────▼────────┐      ┌──────────────┐       │
│         │   SQLite DB    │      │   ds.exe     │       │
│         │  (Patient Data)│      │  (C++ Exec) │       │
│         └────────────────┘      └──────────────┘       │
└─────────────────────────────────────────────────────────┘
```

### Component Breakdown

1. **Frontend (Mobile/Web)**

   - Single codebase works for both mobile and web
   - Uses HTML, CSS, JavaScript
   - Capacitor wraps it for mobile

2. **Backend (Flask Server)**

   - Python Flask framework
   - RESTful API endpoints
   - Connects to SQLite database
   - Calls C++ executable for queue operations

3. **Database (SQLite)**

   - Stores patient information
   - Queue data
   - Served patients history

4. **C++ Executable (ds.exe)**
   - Core queue logic
   - Priority-based sorting
   - Data structure operations

---

## ⚙️ How It Works

### 1. **User Interface Flow**

```
User Opens App
    ↓
App Loads → Fetches Queue Data from Backend
    ↓
Displays Current Queue + Served Patients
    ↓
User Can:
    • Add Patient
    • Serve Patient
    • Sort Queue
    • Search Queue
    • Clear Queue
    • Export Data
    • Configure Settings
    • Get Help (Chatbot)
```

### 2. **Data Flow**

```
Frontend Action (e.g., Add Patient)
    ↓
JavaScript sends HTTP POST request
    ↓
Flask Backend receives request
    ↓
Backend calls C++ executable (ds.exe)
    ↓
C++ processes queue operation
    ↓
Updates SQLite database
    ↓
Backend returns JSON response
    ↓
Frontend updates UI automatically
```

### 3. **Priority System**

The queue uses a **priority-based system**:

- **Priority 1 (High/Critical)** 🔴

  - Urgent cases requiring immediate attention
  - Red border in UI
  - Served first

- **Priority 2 (Medium/Urgent)** 🟠

  - Important but not critical
  - Orange border in UI
  - Served second

- **Priority 3 (Low/Regular)** 🟢
  - Standard cases
  - Green border in UI
  - Served last

**Queue Order**: Always sorted by priority (1 → 2 → 3)

---

## 🔄 Workflow

### **Adding a Patient**

1. User enters:

   - Patient Name
   - Age (1-150)
   - Priority Level (High/Medium/Low)

2. Clicks "➕ Add Patient"

3. System:
   - Validates input
   - Sends data to backend
   - Backend adds to queue
   - Queue auto-sorts by priority
   - UI updates immediately

### **Serving a Patient**

1. User clicks "👨‍⚕️ Serve Next Patient"

2. System:
   - Finds highest priority patient
   - Marks as served
   - Moves to "Served Patients" section
   - Removes from active queue
   - Updates UI

### **Queue Management**

- **Auto-refresh**: Queue updates every 2 seconds
- **Search**: Filter patients by name in real-time
- **Sort**: Manual re-sort button available
- **Clear**: Remove all queued patients (with confirmation)

### **Settings & Configuration**

1. Click "⚙️ Settings"
2. Enter backend server URL (e.g., `http://192.168.1.50:5000`)
3. Test connection
4. Save settings
5. App reloads with new configuration

---

## ✨ Features

### **Core Features**

1. **Patient Management**

   - Add patients with name, age, priority
   - View current queue
   - Track served patients
   - Remove served patients

2. **Queue Operations**

   - Automatic priority-based sorting
   - Manual sort option
   - Search/filter functionality
   - Clear queue option

3. **Data Management**

   - Export queue data as JSON
   - Real-time updates
   - Persistent storage (SQLite)

4. **User Experience**

   - Beautiful, modern UI
   - Color-coded priority indicators
   - Responsive design (mobile & web)
   - Toast notifications
   - Connection status indicator

5. **Help System**
   - Built-in chatbot assistant
   - Answers common questions
   - Quick suggestion buttons
   - Feature explanations

### **Technical Features**

- **Cross-platform**: Works on Android and Web browsers
- **Configurable Backend**: Easy to change server URL
- **Offline Detection**: Shows connection status
- **Error Handling**: User-friendly error messages
- **Network Security**: Configured for HTTP/HTTPS

---

## 🔧 Technical Components

### **Frontend Files**

#### `index.html`

- Main application interface
- HTML structure
- JavaScript functions for API calls
- Modal dialogs (Settings, Chatbot)
- Event handlers

#### `styles.css`

- Complete styling
- Responsive design
- Color schemes
- Animations and transitions
- Mobile optimizations

#### `config.js`

- API base URL management
- localStorage for settings persistence
- URL configuration functions
- Default values

#### `chatbot.js`

- Rule-based chatbot logic
- Pattern matching
- Response generation
- Help suggestions

### **Backend Integration**

#### API Configuration

- Uses `config.js` for base URL
- All API calls use `getApiUrl()` function
- Supports dynamic URL changes
- Works with localhost (web) and network IP (mobile)

#### Network Setup

- Android: Network security config allows HTTP
- Capacitor: Configured for HTTP scheme
- Manifest: Internet permission enabled

### **Mobile App (Capacitor)**

- **Platform**: Android
- **Framework**: Capacitor
- **Build**: Gradle
- **Output**: APK file

---

## 🚀 Setup & Usage

### **For Mobile App**

1. **Build APK**

   ```bash
   npx cap sync
   cd android
   ./gradlew assembleDebug
   ```

2. **Install APK**

   - Transfer `app-debug.apk` to Android device
   - Enable "Install from Unknown Sources"
   - Install and open app

3. **Configure Backend**
   - Open app → Settings
   - Enter Flask server URL: `http://YOUR_IP:5000`
   - Test connection
   - Save

### **For Web App**

1. **Open in Browser**

   - Navigate to `frontend/public/index.html`
   - Or serve via web server

2. **Configure Backend**
   - Click Settings
   - Enter backend URL (usually `http://localhost:5000`)
   - Save

### **Backend Requirements**

- Flask server running
- Accessible on network (for mobile)
- Port 5000 open
- SQLite database initialized
- C++ executable (ds.exe) available

---

## 📡 API Endpoints

All endpoints use the base URL configured in settings.

### **GET `/api/queue`**

- **Purpose**: Fetch current queue and served patients
- **Response**: JSON with `queue` and `served` arrays
- **Usage**: Auto-called every 2 seconds

### **POST `/api/add`**

- **Purpose**: Add new patient to queue
- **Body**: `{ name, age, priority }`
- **Response**: `{ success: true/false, error?: string }`

### **POST `/api/serve`**

- **Purpose**: Serve next patient (highest priority)
- **Response**: `{ success: true/false, error?: string }`

### **POST `/api/sort`**

- **Purpose**: Manually sort queue by priority
- **Response**: `{ success: true/false }`

### **POST `/api/clear`**

- **Purpose**: Clear all patients from queue
- **Response**: `{ success: true/false }`

### **POST `/api/remove_served`**

- **Purpose**: Remove patient from served list
- **Body**: `{ id: number }`
- **Response**: `{ success: true/false }`

### **GET `/api/export`**

- **Purpose**: Export queue data
- **Response**: JSON with all queue data

---

## 🔐 Security & Configuration

### **Network Security**

- Android allows HTTP for local networks
- Network security config file created
- Cleartext traffic enabled for development

### **API Configuration**

- Base URL stored in localStorage
- Can be changed via Settings UI
- Default: `http://192.168.1.100:5000`
- Supports both HTTP and HTTPS

### **Data Storage**

- Frontend: localStorage for settings
- Backend: SQLite database for patient data
- No sensitive data stored in frontend

---

## 📱 Mobile vs Web Differences

| Feature          | Mobile App                     | Web App                 |
| ---------------- | ------------------------------ | ----------------------- |
| **Backend URL**  | Network IP (e.g., 192.168.x.y) | localhost or network IP |
| **Installation** | APK file                       | Direct browser access   |
| **Platform**     | Android only                   | Any browser             |
| **Network**      | Requires network access        | Can use localhost       |
| **UI**           | Same interface                 | Same interface          |

---

## 🎓 Key Concepts Explained

### **Why Capacitor?**

- Capacitor wraps web code into native mobile app
- Single codebase for web and mobile
- No need to rewrite code for different platforms

### **Why Priority Queue?**

- Ensures critical patients are served first
- Automatic sorting maintains order
- Visual indicators help staff identify urgency

### **Why Auto-refresh?**

- Keeps queue synchronized across multiple devices
- Real-time updates without manual refresh
- Better user experience

### **Why Chatbot?**

- Helps new users learn the system
- Reduces support burden
- Provides instant help

---

## 📊 Data Flow Example

**Scenario: Adding a Critical Patient**

```
1. User fills form:
   Name: "John Doe"
   Age: 45
   Priority: High (1)

2. Clicks "Add Patient"

3. Frontend sends:
   POST http://192.168.1.50:5000/api/add
   Body: { name: "John Doe", age: 45, priority: 1 }

4. Backend receives request

5. Backend calls ds.exe with patient data

6. C++ executable:
   - Adds patient to priority queue
   - Sorts by priority
   - Updates database

7. Backend returns:
   { success: true }

8. Frontend:
   - Shows success toast
   - Refreshes queue display
   - Patient appears at top (Priority 1)

9. Auto-refresh continues every 2 seconds
```

---

## 🛠️ Development Workflow

### **Making Changes**

1. **Edit Frontend Files**

   - Modify `frontend/public/*` files
   - Test in browser first

2. **Sync to Mobile**

   ```bash
   npx cap sync
   ```

3. **Rebuild APK**

   ```bash
   cd android
   ./gradlew assembleDebug
   ```

4. **Test**
   - Install new APK
   - Verify changes work

### **File Structure**

```
HospitalQueueMobile/
├── frontend/
│   └── public/
│       ├── index.html      (Main UI)
│       ├── styles.css      (Styling)
│       ├── config.js       (API config)
│       └── chatbot.js      (Chatbot logic)
├── android/                (Android project)
├── capacitor.config.json    (Capacitor config)
└── package.json            (Dependencies)
```

---

## ✅ Summary

**Hospital Queue Management System** is a complete solution for managing patient queues:

- ✅ **Easy to Use**: Simple interface, clear actions
- ✅ **Efficient**: Priority-based queue, auto-sorting
- ✅ **Flexible**: Works on mobile and web
- ✅ **Helpful**: Built-in chatbot assistant
- ✅ **Reliable**: Real-time updates, error handling
- ✅ **Configurable**: Easy backend URL setup

The system ensures critical patients are served first while providing a smooth experience for hospital staff managing queues.

---

## 📝 Quick Reference

**Common Tasks:**

- Add Patient → Fill form → Click Add
- Serve Patient → Click Serve Next
- Search → Type in search box
- Settings → Click Settings → Enter URL → Save
- Help → Click Help Assistant → Ask questions

**Important URLs:**

- Mobile: Use network IP (e.g., `http://192.168.1.50:5000`)
- Web: Use localhost (e.g., `http://localhost:5000`)

**Priority Levels:**

- 1 = High (Critical) 🔴
- 2 = Medium (Urgent) 🟠
- 3 = Low (Regular) 🟢

---

_This document provides a complete overview of the Hospital Queue Management System. For technical details, refer to the code comments and API documentation._
