#include "state_machine.h"
#include <iostream>

RocketStateMachine::RocketStateMachine() : rocket_state(RocketState::IDLE) {}

void RocketStateMachine::update(const SensorFeed &sensorTelemetry)
{
    switch (rocket_state)
    {
    case RocketState::IDLE:
        if (sensorTelemetry.acceleration_z > 15.0)
        {
            rocket_state = RocketState::POWERED_ASCENT;
            std::cout << "[FSW] Liftoff! Entering POWERED_ASCENT.\n";
        }
        break;

    case RocketState::POWERED_ASCENT:
        if (sensorTelemetry.vertical_velocity < 0.0 && sensorTelemetry.current_stage == 1)
        {
            rocket_state = RocketState::SEPERATION;
            std::cout << "[FSW] Burnout detected. Initiating SEPERATION.\n";
        }
        break;

    case RocketState::SEPERATION:
        rocket_state = RocketState::APOGEE;
        std::cout << "[FSW] Stage separation complete. Entering APOGEE.\n";
        break;

    case RocketState::APOGEE:
        if (sensorTelemetry.vertical_velocity < 0.0)
        {
            rocket_state = RocketState::DESCENT;
            std::cout << "[FSW] Apogee reached. Deploying recovery systems.\n";
        }
        break;

    case RocketState::DESCENT:
        if (sensorTelemetry.vertical_velocity == 0.0)
        {
            rocket_state = RocketState::RECOVERY;
            std::cout << "[FSW] Descent Finished. Rocket Landed. Waiting for RECOVERY.\n";
        }
        break;

    case RocketState::RECOVERY:
        break;
    }
}

RocketState RocketStateMachine::getState() const
{
    return rocket_state;
}
