#ifndef DATA_STRUCTURES_H
#define DATA_STRUCTURES_H

#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
using namespace std;

// Patient structure to hold patient information
struct Patient {
    int id;           // Unique patient ID
    string name;      // Patient's full name
    int age;          // Patient's age in years
    int priority;     // Priority level: 1=High, 2=Medium, 3=Low
};

class Queue {
private:
    vector<Patient> patients;
    int next_id;

public:
    Queue();
    Patient enqueue(string name, int age, int priority);
    void loadPatient(int id, string name, int age, int priority);
    Patient dequeue();
    void sortByPriority();
    void display();
    void clear();
    bool isEmpty();
    int size();
};

#endif
