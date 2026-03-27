#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sqlite3.h>
#include "database.h"

Database::Database(string db_path, string init_path) : db_file(db_path), init_file(init_path), db(nullptr) {
    // Open database
    int rc = sqlite3_open(db_file.c_str(), &db);
    if (rc != SQLITE_OK) {
        cerr << "ERROR: Can't open database: " << sqlite3_errmsg(db) << endl;
        sqlite3_close(db);
        db = nullptr;
        return;
    }
    initDatabase();
}

Database::~Database() {
    if (db) {
        sqlite3_close(db);
        db = nullptr;
    }
}

void Database::initDatabase() {
    if (!db) {
        cerr << "ERROR: Database not initialized" << endl;
        return;
    }

    char* errMsg = nullptr;
    string sql;

    // Read and execute schema
    ifstream schemaFile(init_file);
    if (!schemaFile.is_open()) {
        cerr << "WARNING: Could not open schema file: " << init_file << endl;
        return;
    }

    string line;
    while (getline(schemaFile, line)) {
        // Skip empty lines and comments
        string trimmed = line;
        trimmed.erase(0, trimmed.find_first_not_of(" \t"));
        if (!trimmed.empty() && trimmed.substr(0, 2) != "--") {
            sql += line + "\n";
        }
    }
    schemaFile.close();

    if (!sql.empty()) {
        int rc = sqlite3_exec(db, sql.c_str(), nullptr, nullptr, &errMsg);
        if (rc != SQLITE_OK) {
            cerr << "ERROR: SQL execution failed: " << (errMsg ? errMsg : "Unknown error") << endl;
            if (errMsg) {
                sqlite3_free(errMsg);
            }
        }
    }
}
    
// Insert a new patient into the database (auto-increment ID)
bool Database::insertPatient(Patient& p) {
    if (!db) {
        cerr << "ERROR: Database not initialized" << endl;
        return false;
    }

    string sql = "INSERT INTO patients (name, age, priority, status) VALUES (?, ?, ?, 'queued')";
    sqlite3_stmt* stmt = nullptr;

    if (sqlite3_prepare_v2(db, sql.c_str(), -1, &stmt, nullptr) != SQLITE_OK) {
        cerr << "ERROR: Failed to prepare statement: " << sqlite3_errmsg(db) << endl;
        return false;
    }

    sqlite3_bind_text(stmt, 1, p.name.c_str(), -1, SQLITE_STATIC);
    sqlite3_bind_int(stmt, 2, p.age);
    sqlite3_bind_int(stmt, 3, p.priority);

    int rc = sqlite3_step(stmt);
    bool success = (rc == SQLITE_DONE);
    
    if (success) {
        p.id = static_cast<int>(sqlite3_last_insert_rowid(db));
    } else {
        cerr << "ERROR: Failed to insert patient: " << sqlite3_errmsg(db) << endl;
    }

    sqlite3_finalize(stmt);
    return success;
}

// Update patient status to served
bool Database::updatePatientStatus(int id) {
    if (!db) {
        cerr << "ERROR: Database not initialized" << endl;
        return false;
    }

    string sql = "UPDATE patients SET status = 'served', served_at = CURRENT_TIMESTAMP WHERE id = ?";
    sqlite3_stmt* stmt = nullptr;

    if (sqlite3_prepare_v2(db, sql.c_str(), -1, &stmt, nullptr) != SQLITE_OK) {
        cerr << "ERROR: Failed to prepare update statement: " << sqlite3_errmsg(db) << endl;
        return false;
    }

    sqlite3_bind_int(stmt, 1, id);
    int rc = sqlite3_step(stmt);
    bool success = (rc == SQLITE_DONE);

    if (!success && rc != SQLITE_DONE) {
        cerr << "ERROR: Failed to update patient status: " << sqlite3_errmsg(db) << endl;
    }

    sqlite3_finalize(stmt);
    return success;
}

// Get all queued patients - sorted by priority ASC, age DESC, id ASC
vector<Patient> Database::getQueuedPatients() {
    vector<Patient> patients;
    if (!db) {
        cerr << "ERROR: Database not initialized" << endl;
        return patients;
    }

    string sql = "SELECT id, name, age, priority FROM patients WHERE status = 'queued' "
                 "ORDER BY priority ASC, age DESC, id ASC";
    sqlite3_stmt* stmt = nullptr;

    if (sqlite3_prepare_v2(db, sql.c_str(), -1, &stmt, nullptr) != SQLITE_OK) {
        cerr << "ERROR: Failed to prepare query: " << sqlite3_errmsg(db) << endl;
        return patients;
    }

    while (sqlite3_step(stmt) == SQLITE_ROW) {
        Patient p;
        p.id = sqlite3_column_int(stmt, 0);
        const unsigned char* name_text = sqlite3_column_text(stmt, 1);
        p.name = name_text ? reinterpret_cast<const char*>(name_text) : "";
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
    if (!db) {
        cerr << "ERROR: Database not initialized" << endl;
        return patients;
    }

    string sql = "SELECT id, name, age, priority FROM patients WHERE status = 'served' "
                 "ORDER BY served_at DESC";
    sqlite3_stmt* stmt = nullptr;

    if (sqlite3_prepare_v2(db, sql.c_str(), -1, &stmt, nullptr) != SQLITE_OK) {
        cerr << "ERROR: Failed to prepare query: " << sqlite3_errmsg(db) << endl;
        return patients;
    }

    while (sqlite3_step(stmt) == SQLITE_ROW) {
        Patient p;
        p.id = sqlite3_column_int(stmt, 0);
        const unsigned char* name_text = sqlite3_column_text(stmt, 1);
        p.name = name_text ? reinterpret_cast<const char*>(name_text) : "";
        p.age = sqlite3_column_int(stmt, 2);
        p.priority = sqlite3_column_int(stmt, 3);
        patients.push_back(p);
    }
    sqlite3_finalize(stmt);
    return patients;
}


// Clear the queue (delete queued patients)
void Database::clearQueue() {
    if (!db) {
        cerr << "ERROR: Database not initialized" << endl;
        return;
    }

    string sql = "DELETE FROM patients WHERE status = 'queued'";
    char* errMsg = nullptr;
    int rc = sqlite3_exec(db, sql.c_str(), nullptr, nullptr, &errMsg);
    
    if (rc != SQLITE_OK) {
        cerr << "ERROR: Failed to clear queue: " << (errMsg ? errMsg : "Unknown error") << endl;
        if (errMsg) {
            sqlite3_free(errMsg);
        }
    }
}

// Remove a served patient
bool Database::removeServedPatient(int id) {
    if (!db) {
        cerr << "ERROR: Database not initialized" << endl;
        return false;
    }

    string sql = "DELETE FROM patients WHERE id = ? AND status = 'served'";
    sqlite3_stmt* stmt = nullptr;

    if (sqlite3_prepare_v2(db, sql.c_str(), -1, &stmt, nullptr) != SQLITE_OK) {
        cerr << "ERROR: Failed to prepare delete statement: " << sqlite3_errmsg(db) << endl;
        return false;
    }

    sqlite3_bind_int(stmt, 1, id);
    int rc = sqlite3_step(stmt);
    bool success = (rc == SQLITE_DONE);

    if (!success && rc != SQLITE_DONE) {
        cerr << "ERROR: Failed to remove served patient: " << sqlite3_errmsg(db) << endl;
    }

    sqlite3_finalize(stmt);
    return success;
}
