#ifndef CONFIG_H
#define CONFIG_H

#include <string>
#include <json.hpp>

using namespace std;
using json = nlohmann::json;

class Config
{
private:
    json config;

public:
    string scheduleAlgorithm;
    int maxTime;
    int processesNumber;
    int timeQuantum;

    Config(string config_dir);
    ~Config();

    json getConfig() const;
};

#endif
