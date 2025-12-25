#!/bin/bash
echo "Building Hospital Queue System..."

# Ensure g++ is installed
if ! command -v g++ &> /dev/null; then
    echo "Installing g++..."
    apt-get update && apt-get install -y g++
fi

cd backend || exit 1

# Detect OS
OS_NAME=$(uname)
if [[ "$OS_NAME" == "Linux" ]]; then
    EXE_NAME="ds"
else
    EXE_NAME="ds.exe"
fi

# Compile
echo "Compiling C++ backend to $EXE_NAME..."
g++ main.cpp data_structures.cpp database.cpp web.cpp -o "$EXE_NAME" -lsqlite3 -std=c++11
if [ $? -ne 0 ]; then
    echo "ERROR: Compilation failed!"
    exit 1
fi

chmod +x "$EXE_NAME"
cd ..
echo "✅ Build complete!"
exit 0