#!/bin/bash
echo "Building Hospital Queue System for Railway deployment..."

# Ensure g++ is installed
if ! command -v g++ &> /dev/null; then
    echo "Installing g++..."
    apt-get update && apt-get install -y g++
fi

# Compile C++ backend
cd backend || exit 1
echo "Compiling C++ backend..."
g++ main.cpp data_structures.cpp database.cpp web.cpp -o ds -lsqlite3 -std=c++11
if [ $? -ne 0 ]; then
    echo "ERROR: C++ compilation failed!"
    exit 1
fi

# Make executable
chmod +x ds
cd ..
echo "✅ Build complete!"
