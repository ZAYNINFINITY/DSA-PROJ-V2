#include "web.h"
#include <iostream>
#include <string>
using namespace std;

void handleCommand(int argc, char* argv[], Queue& q, Database& db) {
    if (argc > 1) {
        string cmd = argv[1];
        if (cmd == "add" && argc == 5) {
            string name = argv[2];
            int age = stoi(argv[3]);
            int priority = stoi(argv[4]);
            Patient p = q.enqueue(name, age, priority);
            if (db.insertPatient(p)) {
                cout << "Patient added successfully with ID: " << p.id << endl;
            } else {
                cout << "Error adding patient to database." << endl;
            }
        } else if (cmd == "serve") {
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
            int id = stoi(argv[2]);
            if (db.removeServedPatient(id)) {
                cout << "Patient with ID " << id << " removed from served list." << endl;
            } else {
                cout << "Patient with ID " << id << " not found in served list." << endl;
            }
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
                int age, priority;
                cout << "Enter full name: ";
                getline(cin, name);
                cout << "Enter age: ";
                cin >> age;
                cout << "Enter priority (1=High,2=Medium,3=Low): ";
                cin >> priority;
                cin.ignore();
                Patient p = q.enqueue(name, age, priority);
                if (db.insertPatient(p)) {
                    cout << "Patient added successfully with ID: " << p.id << endl;
                } else {
                    cout << "Error adding patient to database." << endl;
                }
                break;
            }
            case 2: {
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
                break;
            }
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
