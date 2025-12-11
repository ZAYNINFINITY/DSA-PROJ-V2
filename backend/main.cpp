#include <iostream>
#include <vector>
#include <cstdlib>
#include <stdexcept>
#include "data_structures.h"
#include "database.h"
#include "web.h"
using namespace std;

int main(int argc, char* argv[]) {
    // Initialize database
    Database db("hospital_queue.db", "init_db.sql");

    // Initialize queue
    Queue q;

    // Load existing queued patients from database into queue
    try {
        vector<Patient> queued = db.getQueuedPatients();
        for (size_t i = 0; i < queued.size(); ++i) {
            const Patient& p = queued[i];
            q.loadPatient(p.id, p.name, p.age, p.priority);
        }
    } catch (const exception& e) {
        cerr << "Error loading patients from database: " << e.what() << endl;
        return 1;
    } catch (...) {
        cerr << "Unknown error loading patients from database" << endl;
        return 1;
    }

    // Handle commands
    handleCommand(argc, argv, q, db);

    return 0;
}
