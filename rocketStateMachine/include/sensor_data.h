#pragma once

struct SensorFeed
{
    double timestamp;
    double altitude;
    double vertical_velocity;
    double acceleration_z;
    int current_stage;
};

enum class RocketState
{
    IDLE,
    POWERED_ASCENT,
    SEPERATION,
    APOGEE,
    DESCENT,
    RECOVERY
};
