#!/usr/bin/env bash
set -e

echo "======================================"
echo "Building Hospital Queue System (Railway)"
echo "======================================"

# Ensure we are in repo root
ROOT_DIR="$(pwd)"
echo "Working directory: $ROOT_DIR"

# Check backend directory
if [ ! -d "backend" ]; then
    echo "ERROR: backend directory not found!"
    exit 1
fi

# Ensure g++ exists (Railway usually has it)
if ! command -v g++ >/dev/null 2>&1; then
    echo "g++ not found. Installing..."
    apt-get update
    apt-get install -y g++
fi

echo "g++ version:"
g++ --version

# Compile C++ backend
echo "Compiling C++ backend..."
cd backend

g++ main.cpp data_structures.cpp database.cpp web.cpp \
    -o ds \
    -std=c++11 \
    -lsqlite3

echo "C++ compilation successful!"

# Ensure executable permission
chmod +x ds

echo "Executable created at: backend/ds"
echo "======================================"
echo "Build completed successfully"
echo "======================================"
