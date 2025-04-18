#ifndef PROCESS_H
#define PROCESS_H

#include <string>
#include <Config.h>
using namespace std;

struct Process
{
    int id;
    double arrival;
    double burst;
    int priority;
};

struct ProcessesQueue
{
    Process processes[100];
};

class ProcessGenerator
{
private:
    const Config &config;

public:
    ProcessGenerator(const Config &config);
    ~ProcessGenerator();

    ProcessesQueue generateRandomProcesses(int num);
    ProcessesQueue generateRandomProcessesByTime(int time);

    int generateID();
};

#endif
