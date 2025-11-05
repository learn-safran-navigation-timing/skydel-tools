# This Python script illustrates how to display Heading values.

# Before running this script, make sure Skydel is runnin and the splash screen is closed.

import time
import skydelsdx
from skydelsdx.commands import *
from skydelsdx.units import toDegree, toRadian
import numpy as np


# Collect Skydel Antenna Offsets and return a list
def lever_arm_vector(VehicleAntennaOffset):
    return np.array(
        [
            VehicleAntennaOffset.x(),
            VehicleAntennaOffset.y(),
            VehicleAntennaOffset.z(),
        ]
    )


# Return a 3D Rotation Matrix from Yaw,Pitch,Roll data
def rotation_matrix_ypr(yaw, pitch, roll):
    cy, sy = np.cos(yaw), np.sin(yaw)
    cp, sp = np.cos(pitch), np.sin(pitch)
    cr, sr = np.cos(roll), np.sin(roll)
    # Skydel rotation : yaw (Z), pitch (Y), roll (X)
    Rz = np.array([[cy, -sy, 0], [sy, cy, 0], [0, 0, 1]])
    Ry = np.array([[cp, 0, sp], [0, 1, 0], [-sp, 0, cp]])
    Rx = np.array([[1, 0, 0], [0, cr, -sr], [0, sr, cr]])
    return Rz @ Ry @ Rx


# Connect both instances
sim_ant1 = skydelsdx.RemoteSimulator()
sim_ant2 = skydelsdx.RemoteSimulator()
sim_ant1.connect("localhost", 0)
sim_ant2.connect("localhost", 1)

# Collect Antenna Offsets
offset_ant1 = lever_arm_vector(sim_ant1.call(GetVehicleAntennaOffset()))
offset_ant2 = lever_arm_vector(sim_ant2.call(GetVehicleAntennaOffset()))

# You must call beginVehicleInfo before getting vehicle informations
sim_ant1.beginVehicleInfo()

# Define orientation of the heading vector
vector_orientation_bool = input(
    "Is the heading vector orientation from Instance2(tail) to Instance1(front) ? (True/False)\n"
)
if vector_orientation_bool == "False":
    vector_orientation = -1
else:
    vector_orientation = 1


# Check if instance 1 is Main to start the simulation. Else start simulation with instance 2.
if sim_ant1.call(GetMainInstanceStatus()).isMainInstance():
    sim_ant1.start()
    sim_ant2.disconnect()
else:
    sim_ant2.start()
    sim_ant1.disconnect()

# This callback function gives position and attitude of the body.
info_vehicle = sim_ant1.lastVehicleInfo()

try:
    while True:
        info_vehicle = sim_ant1.lastVehicleInfo()

        # info_vehicle gives position/orientation of the vehicle body center. We determine the heading orientation of the two antenna vector
        yaw, pitch, roll = (
            toRadian(info_vehicle.attitude.yawDeg()),
            toRadian(info_vehicle.attitude.pitchDeg()),
            toRadian(info_vehicle.attitude.rollDeg()),
        )
        R = rotation_matrix_ypr(yaw, pitch, roll)
        ant1 = R @ offset_ant1
        ant2 = R @ offset_ant2

        delta_Y = (ant1[1] - ant2[1]) * vector_orientation
        delta_X = (ant1[0] - ant2[0]) * vector_orientation

        print(
            "------------------------------------------------------------------"
        )
      
        print("Time (ms): %d" % info_vehicle.elapsedTime)
        heading_value = (toDegree(np.arctan2(delta_Y, delta_X)) + 360) % 360
        print("Heading (degree): %.2f" % heading_value)
        time.sleep(1)
except KeyboardInterrupt:
    print("\nSimulation Stopped")
finally:
    sim_ant1.stop()
    sim_ant1.endVehicleInfo()

    sim_ant1.disconnect()
