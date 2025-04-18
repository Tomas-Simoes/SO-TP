#include "ProcessGenerator.h"

ProcessGenerator::ProcessGenerator(const Config &config)
    : config(config)
{
}

ProcessGenerator::~ProcessGenerator()
{
}

// Generates processes by number of processes
ProcessesQueue ProcessGenerator::generateRandomProcesses(int numProcesses)
{
    ProcessesQueue newQueue;

    for (int i = 0; i < numProcesses; i++)
    {
    }
}

// Generates processes by time
ProcessesQueue ProcessGenerator::generateRandomProcessesByTime(int time)
{
    ProcessesQueue newQueue;

    for (int i = 0; i < config.maxTime; i++)
    {
    }
}

int ProcessGenerator::generateID()
{
}