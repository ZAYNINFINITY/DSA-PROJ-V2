#ifndef DATABASE_H
#define DATABASE_H

#include <iostream>
#include <vector>
#include <string>
#include <sqlite3.h>
#include "data_structures.h"
using namespace std;

class Database {
private:
    sqlite3* db;
    string db_file;
    string init_file;

    void initDatabase();

public:
    Database(string db_path, string init_path);
    ~Database();
    bool insertPatient(Patient& p);      // Patient passed by reference
    bool updatePatientStatus(int id);
    vector<Patient> getQueuedPatients();
    vector<Patient> getServedPatients();
    void clearQueue();
    bool removeServedPatient(int id);
};

#endif
