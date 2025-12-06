#include <iostream>
#include <vector>
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
    vector<Patient> queued = db.getQueuedPatients();
    for (size_t i = 0; i < queued.size(); ++i) {
        Patient p = queued[i];
        q.loadPatient(p.id, p.name, p.age, p.priority);
    }

    // Handle commands
    handleCommand(argc, argv, q, db);

    return 0;
}
