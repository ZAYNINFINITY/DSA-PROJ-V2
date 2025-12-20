# 🏥 Hospital Queue Management System (DSA PROJ V2)

A comprehensive full-stack application for managing hospital patient queues with priority-based sorting, real-time updates, and cross-platform support (Web + Android).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-lightgrey.svg)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3.x-green.svg)](https://www.sqlite.org/)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Priority System](#priority-system)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## 🎯 Overview

**Hospital Queue Management System** is a complete solution designed to efficiently manage patient queues in healthcare facilities. The system implements data structures and algorithms concepts (DSA) through a practical application that helps hospital staff prioritize and serve patients based on urgency levels.

### Key Components

- **Backend**: Flask server with SQLite database and C++ data structure operations
- **Web Frontend**: Modern responsive web application with real-time updates
- **Mobile App**: Android application built with Capacitor
- **Chatbot**: Built-in AI assistant for user guidance

## ✨ Features

### Core Functionality

- ✅ **Patient Management**: Add patients with name, age, and priority levels
- ✅ **Priority Queue**: Automatic sorting by priority (Critical → Urgent → Regular)
- ✅ **Real-time Updates**: Queue refreshes every 2 seconds
- ✅ **Search & Filter**: Find patients by name instantly
- ✅ **Export Data**: Download queue data as JSON
- ✅ **Served Patients Tracking**: History of served patients with removal option

### User Experience

- 🎨 **Modern UI**: Beautiful, responsive design with animations
- 📱 **Cross-platform**: Works on web browsers and Android devices
- 🤖 **AI Assistant**: Built-in chatbot for help and guidance
- 🔄 **Auto-refresh**: Real-time synchronization
- 📊 **Statistics**: Live queue and served patient counts
- 🔔 **Notifications**: Toast messages for user feedback

### Technical Features

- 🏗️ **Modular Architecture**: Clean separation of concerns
- 🔧 **Configurable Backend**: Easy server URL configuration
- 💾 **Persistent Storage**: SQLite database for data persistence
- 🚀 **Performance Optimized**: Efficient C++ data structure operations
- 🔒 **Error Handling**: Comprehensive error management and user feedback

## 🏗️ Architecture

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

## 📁 Project Structure

```
DSA-PROJ-V2/
├── README.md                           # Project documentation
├── run_webapp.bat                      # Windows batch script to run web app
├── backend/                            # Flask backend application
│   ├── app_py.py                       # Main Flask application
│   ├── chatbot.py                      # Chatbot implementation
│   ├── data_structures.cpp             # C++ data structure implementations
│   ├── data_structures.h               # C++ header files
│   ├── database.cpp                    # Database operations
│   ├── database.h                      # Database header
│   ├── ds.exe                          # Compiled C++ executable
│   ├── hospital_queue.db               # SQLite database
│   ├── init_db.sql                     # Database schema
│   ├── intents.json                    # Chatbot training data
│   ├── main.cpp                        # C++ main file
│   ├── web.cpp                         # Web-related C++ functions
│   ├── web.h                           # Web header
│   └── *.md                            # Backend documentation
├── frontend/                           # Web frontend
│   ├── static/                         # Static assets (CSS, JS, images)
│   └── templates/
│       └── index.html                  # Main web interface
└── HospitalQueueMobile/                # Mobile application
    ├── android/                        # Android project files
    ├── frontend/                       # Mobile frontend (same as web)
    ├── capacitor.config.json           # Capacitor configuration
    ├── package.json                    # Node.js dependencies
    └── *.md                            # Mobile app documentation
```

## 📋 Prerequisites

### Backend Requirements

- **Python 3.7+** with pip
- **Flask** and required dependencies
- **SQLite3** (usually pre-installed with Python)
- **C++ Compiler** (GCC/MinGW for Windows, g++ for Linux/Mac)

### Frontend Requirements

- **Modern Web Browser** (Chrome, Firefox, Safari, Edge)
- **Internet Connection** for real-time updates

### Mobile Requirements

- **Android Device/Emulator** (API 21+)
- **Node.js 14+** and npm
- **Capacitor CLI**
- **Android Studio** (for APK building)

## 🚀 Installation & Setup

### Backend Setup

1. **Navigate to backend directory:**

   ```bash
   cd backend
   ```

2. **Install Python dependencies:**

   ```bash
   pip install flask flask-cors
   ```

3. **Compile C++ executable:**

   ```bash
   # Windows with MinGW
   g++ -std=c++17 data_structures.cpp database.cpp main.cpp web.cpp -o ds.exe

   # Linux/Mac
   g++ -std=c++17 data_structures.cpp database.cpp main.cpp web.cpp -o ds.exe
   ```

4. **Initialize database:**

   ```bash
   python app_py.py
   ```

   The database will be created automatically on first run.

5. **Start the Flask server:**
   ```bash
   python app_py.py
   ```
   Server will run at `http://localhost:5000`

### Web Application Setup

1. **Open in browser:**

   - Navigate to `frontend/templates/index.html`
   - Or use the batch script: `run_webapp.bat`

2. **Configure backend URL:**
   - Default: `http://localhost:5000`
   - For network access: `http://YOUR_IP:5000`

### Mobile Application Setup

1. **Install dependencies:**

   ```bash
   cd HospitalQueueMobile
   npm install
   ```

2. **Sync with Capacitor:**

   ```bash
   npx cap sync
   ```

3. **Build Android APK:**

   ```bash
   cd android
   ./gradlew assembleDebug
   ```

4. **Install on Android device:**

   - Transfer `app-debug.apk` to your Android device
   - Enable "Install from Unknown Sources" in settings
   - Install and open the app

5. **Configure backend URL in app settings:**
   - Open app → Settings (⚙️)
   - Enter your Flask server URL: `http://YOUR_IP:5000`
   - Test connection and save

## 📖 Usage

### Basic Operations

1. **Add Patient:**

   - Enter patient name, age (1-150), and priority level
   - Click "➕ Add Patient"
   - Patient is automatically sorted into queue

2. **Serve Patient:**

   - Click "✅ Serve Next"
   - Highest priority patient is served and moved to served list

3. **Search Patients:**

   - Type in the search box to filter by name
   - Results update in real-time

4. **Export Data:**

   - Click "💾 Export" to download queue data as JSON

5. **Clear Queue:**
   - Click "🗑️ Clear" to remove all queued patients
   - Confirmation dialog will appear

### Advanced Features

- **Real-time Updates:** Queue refreshes automatically every 2 seconds
- **Chat Assistant:** Click the chat button (💬) for help
- **Settings:** Configure backend server URL
- **Patient Removal:** Remove patients from served list

## 📡 API Documentation

All API endpoints return JSON responses. Base URL is configurable.

### GET `/api/queue`

Fetch current queue and served patients.

```json
{
  "queue": [{ "id": 1, "name": "John Doe", "age": 45, "priority": 1 }],
  "served": [{ "id": 2, "name": "Jane Smith", "age": 30, "priority": 2 }]
}
```

### POST `/api/add`

Add new patient to queue.
**Request Body:**

```json
{
  "name": "John Doe",
  "age": 45,
  "priority": 1
}
```

### POST `/api/serve`

Serve next patient (highest priority).

### POST `/api/sort`

Manually sort queue by priority.

### POST `/api/clear`

Clear all patients from queue.

### POST `/api/remove_served`

Remove patient from served list.
**Request Body:**

```json
{ "id": 123 }
```

### GET `/api/export`

Export complete queue data as JSON.

### POST `/api/chat`

Send message to chatbot assistant.
**Request Body:**

```json
{ "message": "How do I add a patient?" }
```

## 🎯 Priority System

The system uses a 3-level priority queue:

| Priority | Level         | Color     | Description                                   |
| -------- | ------------- | --------- | --------------------------------------------- |
| 1        | High/Critical | 🔴 Red    | Emergency cases requiring immediate attention |
| 2        | Medium/Urgent | 🟠 Orange | Important cases needing prompt care           |
| 3        | Low/Regular   | 🟢 Green  | Standard cases for routine care               |

**Queue Order:** Always sorted by priority (1 → 2 → 3), then by age (descending), then by ID.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Test thoroughly**
5. **Commit your changes:**
   ```bash
   git commit -m 'Add amazing feature'
   ```
6. **Push to the branch:**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### Development Guidelines

- Follow existing code style and structure
- Add comments for complex logic
- Test on both web and mobile platforms
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

**Project Supervisor:** Mr. Obaidullah Miakhail

**Repository:** [ZAYNINFINITY/DSA-PROJ-V2](https://github.com/ZAYNINFINITY/DSA-PROJ-V2)

For questions or suggestions, please open an issue on GitHub.

---

## 🎓 Learning Outcomes

This project demonstrates practical implementation of:

- **Data Structures:** Priority Queues, Linked Lists, Arrays
- **Algorithms:** Sorting, Searching, Queue Operations
- **Full-Stack Development:** Frontend, Backend, Database
- **Cross-Platform Development:** Web and Mobile
- **API Design:** RESTful endpoints
- **Database Management:** SQLite operations
- **UI/UX Design:** Responsive, accessible interfaces

---

_Built with ❤️ for learning Data Structures and Algorithms through real-world application._
