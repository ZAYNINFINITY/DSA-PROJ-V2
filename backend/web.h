#ifndef WEB_H
#define WEB_H

#include <iostream>
#include <vector>
#include <string>
#include "data_structures.h"
#include "database.h"
using namespace std;

void handleCommand(int argc, char* argv[], Queue& q, Database& db);

#endif
