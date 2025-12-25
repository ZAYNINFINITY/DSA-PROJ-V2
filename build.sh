#!/bin/bash
echo "Building Hospital Queue System for Railway deployment..."

# Install g++ if not available (Railway might have it, but ensure)
if ! command -v g++ &> /dev/null; then
    echo "Installing g++..."
    apt-get update && apt-get install -y g++
fi

# Compile C++ backend for Linux
echo "Compiling C++ backend..."
cd backend
g++ main.cpp data_structures.cpp database.cpp web.cpp -o ds -lsqlite3 -std=c++11
if [ $? -ne 0 ]; then
    echo "ERROR: C++ compilation failed!"
    exit 1
fi
echo "C++ compilation successful!"

# Make executable
chmod +x ds
echo "Build complete!"
