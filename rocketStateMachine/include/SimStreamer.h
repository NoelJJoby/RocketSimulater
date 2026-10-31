#pragma once
#include "sensor_data.h"
#include <iostream>
#include <string>
#include <zmq.hpp>

class SimStreamer
{
private:
    zmq::context_t context;
    zmq::socket_t subscriber;

public:
    SimStreamer() : context(1), subscriber(context, zmq::socket_type::sub) {}

    bool initialize()
    {
        try
        {
            subscriber.connect("tcp://localhost:5555");
            subscriber.set(zmq::sockopt::subscribe, "");
            std::cout << "[Driver] Initialized ZeroMQ Simulation Subscriber on tcp://localhost:5555\n";
            return true;
        }
        catch (const std::exception &e)
        {
            std::cerr << "[Driver Error] Failed to connect to ZeroMQ: " << e.what() << "\n";
            return false;
        }
    }

    bool read_sensor(SensorFeed &out_feed)
    {
        zmq::message_t update;
        if (subscriber.recv(update, zmq::recv_flags::none))
        {
            out_feed.timestamp += 0.02;
            return true;
        }
        return false;
    }
};
