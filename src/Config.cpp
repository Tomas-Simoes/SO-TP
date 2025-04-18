#include "Config.h"
#include <fstream>

Config::Config(string config_dir)
{
    ifstream ifs(config_dir);
    config = json::parse(ifs);

    scheduleAlgorithm = config["scheduleAlgorithm"];

    maxTime = config["maxTime"];
    processesNumber = config["processesNumber"];

    timeQuantum = config["timeQuantum"];
}

Config::~Config() {}

json Config::getConfig() const
{
    return config;
}
