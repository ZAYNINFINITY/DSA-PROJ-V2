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
// Priority rule: priority ASC → age DESC → id ASC
//   1) lower priority number = more important
//   2) if equal priority → older age first
//   3) if same age → smaller ID first
Patient Queue::dequeue() {
    if (patients.empty()) {
        Patient empty;
        empty.id = -1;
        empty.name = "";
        empty.age = 0;
        empty.priority = 0;
        return empty;
    }

    size_t bestIndex = 0;

    for (size_t i = 1; i < patients.size(); i++) {
        // Priority check (lower number = higher priority)
        if (patients[i].priority < patients[bestIndex].priority) {
            bestIndex = i;
        }
        // Same priority → older age first (age DESC)
        else if (patients[i].priority == patients[bestIndex].priority &&
                 patients[i].age > patients[bestIndex].age) {
            bestIndex = i;
        }
        // Same priority and age → smaller ID first (id ASC)
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

// Sort function - optimized with std::sort
// Sort order: priority ASC → age DESC → id ASC
void Queue::sortByPriority() {
    std::sort(patients.begin(), patients.end(), [](const Patient& a, const Patient& b) {
        // First: priority (lower number = higher priority)
        if (a.priority != b.priority) {
            return a.priority < b.priority;
        }
        // Second: age (older = higher priority, so DESC)
        if (a.age != b.age) {
            return a.age > b.age;
        }
        // Third: id (lower id = higher priority, so ASC)
        return a.id < b.id;
    });
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
    return static_cast<int>(patients.size());
}
