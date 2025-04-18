#include <iostream>

#include "Config.h"
#include "ProcessGenerator.h"

using namespace std;

int main(int argc, char *argv[])
{
    Config config("./config.json");
    ProcessGenerator processGenerator(config);

    ProcessesQueue processQueue = processGenerator.generateRandomProcesses(config.maxTime);
}