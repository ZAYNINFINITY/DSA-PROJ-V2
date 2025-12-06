-- Hospital Queue System Database Schema
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    priority INTEGER NOT NULL CHECK(priority IN (1,2,3)),
    status TEXT NOT NULL DEFAULT 'queued' CHECK(status IN ('queued', 'served')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    served_at DATETIME
);

-- Index for faster queries
CREATE INDEX IF NOT EXISTS idx_status ON patients(status);
CREATE INDEX IF NOT EXISTS idx_priority ON patients(priority);
