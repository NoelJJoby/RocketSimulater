#include "state_machine.h"
#include "SimStreamer.h"
#include <memory>
#include <iostream>

int main(int argc, char *argv[])
{
    std::unique_ptr<SimStreamer> sensor_driver = std::make_unique<SimStreamer>();
    ;

    if (!sensor_driver->initialize())
    {
        std::cerr << "[Error] Failed to initialize sensor!\n";
        return -1;
    }

    RocketStateMachine fsw;
    SensorFeed telemetry{};

    // Main Flight Software Execution Loop
    while (sensor_driver->read_sensor(telemetry))
    {
        fsw.update(telemetry);
    }

    return 0;
}
