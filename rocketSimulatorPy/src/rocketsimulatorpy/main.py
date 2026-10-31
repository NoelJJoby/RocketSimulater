import time
import datetime
import zmq
from rocketpy import Environment, Flight, Rocket, SolidMotor


def main():
    print("[Sim] Initializing RocketPy environment and physics model...")

    # 1. Environment definition
    env = Environment(
      latitude=32.99, longitude=-106.97, elevation=1400
  )
    
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)

    env.set_date(
        (tomorrow.year, tomorrow.month, tomorrow.day, 12)
    )  # Hour given in UTC time
    env.set_atmospheric_model(type="Forecast", file="GFS")


    # 2. Motor definition
    Pro75M1670_motor = SolidMotor(
    thrust_source="../../Cesaroni_M1670.eng",
    dry_mass=1.815,
    dry_inertia=(0.125, 0.125, 0.002),
    nozzle_radius=33 / 1000,
    grain_number=5,
    grain_density=1815,
    grain_outer_radius=33 / 1000,
    grain_initial_inner_radius=15 / 1000,
    grain_initial_height=120 / 1000,
    grain_separation=5 / 1000,
    grains_center_of_mass_position=0.397,
    center_of_dry_mass_position=0.317,
    nozzle_position=0,
    burn_time=3.9,
    throat_radius=11 / 1000,
    coordinate_system_orientation="nozzle_to_combustion_chamber",
    )

    # 3. Rocket definition
    calisto = Rocket(
        radius=127 / 2000,
        mass=14.426,
        inertia=(6.321, 6.321, 0.034),
        power_off_drag="../../powerOffDragCurve.csv",
        power_on_drag="../../powerOnDragCurve.csv",
        center_of_mass_without_motor=0,
        coordinate_system_orientation="tail_to_nose",
    )
    calisto.add_motor(Pro75M1670_motor, position=-1.255)
    rail_buttons = calisto.set_rail_buttons(
    upper_button_position=0.0818,
    lower_button_position=-0.6182,
    angular_position=45,
)
    nose_cone = calisto.add_nose(
    length=0.55829, kind="von karman", position=1.278
)

    fin_set = calisto.add_trapezoidal_fins(
        n=4,
        root_chord=0.120,
        tip_chord=0.060,
        span=0.110,
        position=-1.04956,
        cant_angle=0.5,
        airfoil=("../../NACA0012-radians.txt","radians"),
    )

    tail = calisto.add_tail(
        top_radius=0.0635, bottom_radius=0.0435, length=0.060, position=-1.194656
    )
    main = calisto.add_parachute(
        name="main",
        cd_s=10.0,
        trigger=800,      # ejection altitude in meters
        sampling_rate=105,
        lag=1,
        noise=(0, 8.3, 0.5),
        radius=1.5,
        height=1.5,
        porosity=0.0432,
    )

    drogue = calisto.add_parachute(
        name="drogue",
        cd_s=1.0,
        trigger="apogee",  # ejection at apogee
        sampling_rate=105,
        lag=1,
        noise=(0, 8.3, 0.5),
        radius=1.5,
        height=1.5,
        porosity=0.0432,
    )

    # 4. Solve trajectory
    print("[Sim] Solving 6-DOF trajectory...")
    test_flight = Flight(
    rocket=calisto, environment=env, rail_length=5.2, inclination=85, heading=0
    )
    print(f"[Sim] Simulation complete. Apogee: {test_flight.apogee:.2f} meters")

    # 5. ZeroMQ Publisher setup
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")
    print("[ZMQ] Broadcasting RocketPy telemetry stream on port 5555...")
    # time.sleep(1)

    # # 6. Real-time streaming loop (50 Hz / dt = 0.02s)
    # dt = 0.02
    # t = 0.0
    # max_time = test_flight.t_final
    # telemetry = {}
    # while t <= max_time:
    #     telemetry = {
    #         "timestamp": t,
    #         "altitude": float(test_flight.z(t)),
    #         "vertical_velocity": float(test_flight.vz(t)),
    #         "acceleration_z": 25.0 if t < Pro75M1670_motor.burn_out_time else -1.5,
    #         "current_stage": 1 if t < Pro75M1670_motor.burn_out_time else 2,
    #     }

    # socket.send_json(telemetry)
    # time.sleep(dt)
    # t += dt

    print("[Sim] Flight profile simulation ended.")
    print("[Sim] Generating flight analysis plots...")
    test_flight.plots.all()  # Opens a window with all trajectory and flight physics plots


if __name__ == "__main__":
  main()
