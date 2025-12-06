#include "data_structures.h"

// Constructor
Queue::Queue() {
    next_id = 1;
}

// Add a new patient
Patient Queue::enqueue(string name, int age, int priority) {
    Patient p;
    p.id = next_id;
    next_id++;

    p.name = name;
    p.age = age;
    p.priority = priority;

    patients.push_back(p);
    return p;
}

// Load patient from database
void Queue::loadPatient(int id, string name, int age, int priority) {
    Patient p;
    p.id = id;
    p.name = name;
    p.age = age;
    p.priority = priority;

    patients.push_back(p);

    if (id >= next_id) {
        next_id = id + 1;
    }
}

// Remove the highest-priority patient
// Priority rule:
//   1) lower priority number = more important
//   2) if equal priority → older age first
//   3) if same age → smaller ID first
Patient Queue::dequeue() {
    if (patients.empty()) {
        Patient empty;
        empty.id = -1;
        return empty;
    }

    int bestIndex = 0;

    for (int i = 1; i < patients.size(); i++) {

        // Priority check
        if (patients[i].priority < patients[bestIndex].priority) {
            bestIndex = i;
        }
        // Same priority → older age first
        else if (patients[i].priority == patients[bestIndex].priority &&
                 patients[i].age > patients[bestIndex].age) {
            bestIndex = i;
        }
        // Same age → smaller ID
        else if (patients[i].priority == patients[bestIndex].priority &&
                 patients[i].age == patients[bestIndex].age &&
                 patients[i].id < patients[bestIndex].id) {
            bestIndex = i;
        }
    }

    Patient p = patients[bestIndex];
    patients.erase(patients.begin() + bestIndex);

    return p;
}

// Sort function (simple and readable)
void Queue::sortByPriority() {
    // Simple bubble sort for readability
    for (size_t i = 0; i < patients.size(); ++i) {
        for (size_t j = i + 1; j < patients.size(); ++j) {
            bool should_swap = false;
            if (patients[i].priority > patients[j].priority) {
                should_swap = true;
            } else if (patients[i].priority == patients[j].priority) {
                if (patients[i].age < patients[j].age) {
                    should_swap = true;
                } else if (patients[i].age == patients[j].age && patients[i].id > patients[j].id) {
                    should_swap = true;
                }
            }
            if (should_swap) {
                Patient temp = patients[i];
                patients[i] = patients[j];
                patients[j] = temp;
            }
        }
    }
}

// Show queue
void Queue::display() {
    cout << "\nCurrent Queue:\n";
    cout << "ID\tName\tAge\tPriority\n";

    for (size_t i = 0; i < patients.size(); ++i) {
        Patient p = patients[i];
        cout << p.id << "\t" << p.name << "\t" << p.age << "\t" << p.priority << "\n";
    }
}

// Clear queue
void Queue::clear() {
    patients.clear();
}

// Check empty
bool Queue::isEmpty() {
    return patients.empty();
}

// Return size
int Queue::size() {
    return patients.size();
}
