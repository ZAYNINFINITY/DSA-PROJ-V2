#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sqlite3.h>
#include "database.h"

Database::Database(string db_path, string init_path) : db_file(db_path), init_file(init_path) {
    // Open database
    if (sqlite3_open(db_file.c_str(), &db)) {
        cerr << "Can't open database: " << sqlite3_errmsg(db) << endl;
        db = nullptr;
        return;
    }
    initDatabase();
}

Database::~Database() {
    if (db) sqlite3_close(db);
}

void Database::initDatabase() {
    char* errMsg = 0;
    string sql;

    // Read and execute schema
    ifstream schemaFile(init_file);
    if (schemaFile.is_open()) {
        string line;
        while (getline(schemaFile, line)) {
            if (!line.empty() && line.substr(0, 2) != "--") {
                sql += line + "\n";
            }
        }
        schemaFile.close();
    }

    if (!sql.empty()) {
        if (sqlite3_exec(db, sql.c_str(), 0, 0, &errMsg) != SQLITE_OK) {
            cerr << "SQL error: " << errMsg << endl;
            sqlite3_free(errMsg);
        }
    }
}

// Insert a new patient into the database (auto-increment ID)
bool Database::insertPatient(Patient& p) {
    string sql = "INSERT INTO patients (name, age, priority, status) VALUES (?, ?, ?, 'queued')";
    sqlite3_stmt* stmt;

    if (sqlite3_prepare_v2(db, sql.c_str(), -1, &stmt, 0) != SQLITE_OK) {
        cerr << "Failed to prepare statement: " << sqlite3_errmsg(db) << endl;
        return false;
    }

    sqlite3_bind_text(stmt, 1, p.name.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_int(stmt, 2, p.age);
    sqlite3_bind_int(stmt, 3, p.priority);

    bool success = (sqlite3_step(stmt) == SQLITE_DONE);
    if (success) {
        p.id = static_cast<int>(sqlite3_last_insert_rowid(db));
    } else {
        cerr << "Failed to insert patient: " << sqlite3_errmsg(db) << endl;
    }

    sqlite3_finalize(stmt);
    return success;
}

// Update patient status to served
bool Database::updatePatientStatus(int id) {
    string sql = "UPDATE patients SET status = 'served', served_at = CURRENT_TIMESTAMP WHERE id = ?";
    sqlite3_stmt* stmt;

    if (sqlite3_prepare_v2(db, sql.c_str(), -1, &stmt, 0) != SQLITE_OK) return false;

    sqlite3_bind_int(stmt, 1, id);
    bool success = (sqlite3_step(stmt) == SQLITE_DONE);

    sqlite3_finalize(stmt);
    return success;
}

// Get all queued patients
vector<Patient> Database::getQueuedPatients() {
    vector<Patient> patients;
    string sql = "SELECT id, name, age, priority FROM patients WHERE status = 'queued' ORDER BY priority ASC, age DESC, created_at ASC";
    sqlite3_stmt* stmt;

    if (sqlite3_prepare_v2(db, sql.c_str(), -1, &stmt, 0) != SQLITE_OK) return patients;

    while (sqlite3_step(stmt) == SQLITE_ROW) {
        Patient p;
        p.id = sqlite3_column_int(stmt, 0);
        p.name = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
        p.age = sqlite3_column_int(stmt, 2);
        p.priority = sqlite3_column_int(stmt, 3);
        patients.push_back(p);
    }
    sqlite3_finalize(stmt);
    return patients;
}

// Get all served patients
vector<Patient> Database::getServedPatients() {
    vector<Patient> patients;
    string sql = "SELECT id, name, age, priority FROM patients WHERE status = 'served' ORDER BY served_at DESC";
    sqlite3_stmt* stmt;

    if (sqlite3_prepare_v2(db, sql.c_str(), -1, &stmt, 0) != SQLITE_OK) return patients;

    while (sqlite3_step(stmt) == SQLITE_ROW) {
        Patient p;
        p.id = sqlite3_column_int(stmt, 0);
        p.name = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
        p.age = sqlite3_column_int(stmt, 2);
        p.priority = sqlite3_column_int(stmt, 3);
        patients.push_back(p);
    }
    sqlite3_finalize(stmt);
    return patients;
}

// Clear the queue (delete queued patients)
void Database::clearQueue() {
    string sql = "DELETE FROM patients WHERE status = 'queued'";
    sqlite3_exec(db, sql.c_str(), 0, 0, 0);
}

// Remove a served patient
bool Database::removeServedPatient(int id) {
    string sql = "DELETE FROM patients WHERE id = ? AND status = 'served'";
    sqlite3_stmt* stmt;

    if (sqlite3_prepare_v2(db, sql.c_str(), -1, &stmt, 0) != SQLITE_OK) return false;

    sqlite3_bind_int(stmt, 1, id);
    bool success = (sqlite3_step(stmt) == SQLITE_DONE);

    sqlite3_finalize(stmt);
    return success;
}
