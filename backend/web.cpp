#include "web.h"
#include <iostream>
#include <string>
#include <sstream>
using namespace std;

// Helper function to add a patient
static void addPatientToQueue(Queue& q, Database& db, const string& name, int age, int priority) {
    Patient p = q.enqueue(name, age, priority);
    if (db.insertPatient(p)) {
        cout << "Patient added successfully with ID: " << p.id << endl;
    } else {
        cout << "Error adding patient to database." << endl;
    }
}

// Helper function to serve a patient
static void serveNextPatient(Queue& q, Database& db) {
    Patient p = q.dequeue();
    if (p.id != -1) {
        if (db.updatePatientStatus(p.id)) {
            cout << "Served patient: " << p.name << " (ID: " << p.id << ")" << endl;
        } else {
            cout << "Error updating patient status in database." << endl;
        }
    } else {
        cout << "No patients in queue." << endl;
    }
}

// Helper function to remove served patient
static void removeServedPatientById(Database& db, int id) {
    if (db.removeServedPatient(id)) {
        cout << "Patient with ID " << id << " removed from served list." << endl;
    } else {
        cout << "Patient with ID " << id << " not found in served list." << endl;
    }
}

void handleCommand(int argc, char* argv[], Queue& q, Database& db) {
    if (argc > 1) {
        string cmd = argv[1];
        
        if (cmd == "add" && argc == 5) {
            string name = argv[2];
            int age = 0;
            int priority = 0;
            try {
                age = stoi(argv[3]);
                priority = stoi(argv[4]);
                if (priority < 1 || priority > 3) {
                    cout << "Error: Priority must be 1, 2, or 3." << endl;
                    return;
                }
                if (age < 1 || age > 150) {
                    cout << "Error: Age must be between 1 and 150." << endl;
                    return;
                }
                addPatientToQueue(q, db, name, age, priority);
            } catch (const exception& e) {
                cout << "Error: Invalid age or priority value." << endl;
            }
        } else if (cmd == "serve") {
            serveNextPatient(q, db);
        } else if (cmd == "sort") {
            q.sortByPriority();
            cout << "Queue sorted by priority." << endl;
        } else if (cmd == "display") {
            q.display();
        } else if (cmd == "clear") {
            q.clear();
            db.clearQueue();
            cout << "Queue cleared." << endl;
        } else if (cmd == "remove_served" && argc == 3) {
            try {
                int id = stoi(argv[2]);
                removeServedPatientById(db, id);
            } catch (const exception& e) {
                cout << "Error: Invalid patient ID." << endl;
            }
        } else {
            cout << "Unknown command or invalid arguments." << endl;
            cout << "Usage: ds.exe <command> [args]" << endl;
            cout << "Commands: add <name> <age> <priority>, serve, sort, display, clear, remove_served <id>" << endl;
        }
        return;
    }

    // Interactive menu if no args
    int ch;
    do {
        cout << "\n--- Patient Queue Menu ---\n";
        cout << "1. Add Patient\n2. Serve Patient\n3. Sort by Priority\n4. Display\n5. Clear Queue\n6. Exit\n";
        cout << "Enter choice: ";
        cin >> ch;
        cin.ignore(); // consume newline

        switch (ch) {
            case 1: {
                string name;
                int age = 0, priority = 0;
                cout << "Enter full name: ";
                getline(cin, name);
                if (name.empty()) {
                    cout << "Error: Name cannot be empty." << endl;
                    break;
                }
                cout << "Enter age: ";
                if (!(cin >> age) || age < 1 || age > 150) {
                    cout << "Error: Invalid age (must be 1-150)." << endl;
                    cin.clear();
                    cin.ignore(10000, '\n');
                    break;
                }
                cout << "Enter priority (1=High,2=Medium,3=Low): ";
                if (!(cin >> priority) || priority < 1 || priority > 3) {
                    cout << "Error: Invalid priority (must be 1, 2, or 3)." << endl;
                    cin.clear();
                    cin.ignore(10000, '\n');
                    break;
                }
                cin.ignore();
                addPatientToQueue(q, db, name, age, priority);
                break;
            }
            case 2:
                serveNextPatient(q, db);
                break;
            case 3:
                q.sortByPriority();
                cout << "Queue sorted by priority." << endl;
                break;
            case 4:
                q.display();
                break;
            case 5:
                q.clear();
                db.clearQueue();
                cout << "Queue cleared." << endl;
                break;
            case 6:
                cout << "Goodbye!\n";
                break;
            default:
                cout << "Invalid choice!\n";
        }
    } while (ch != 6);
}
