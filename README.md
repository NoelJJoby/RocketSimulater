# Basic Rocket Simulator

Simulates various, custom defined rockets in python via rocketPY
Outputs final graphs of required features.

Alongside a custom C++ state machine which can read in the simulated data and use that as a replacement for real sensor data.
This is to be able to test rocket's flight software through simulations prior to real world testing.

The 2 programs communicate via zeroMQ. In this initial project, this is through TCP but can be altered to use radio or onboard sensors etc.
