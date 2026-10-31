#pragma once
#include "sensor_data.h"

class RocketStateMachine
{
private:
    RocketState rocket_state;

public:
    RocketStateMachine();
    void update(const SensorFeed &sensorTelemetry);
    RocketState getState() const;
};
