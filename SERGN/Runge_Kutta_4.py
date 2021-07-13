"""
Skydel Extrapolator for Rinex GLONASS Navigation File - Runge Kutta QT application class.

Created on 14 06 2021

:author: Grace Oulai
:copyright: Skydel © 2021
:Version: 21.6.1
"""

# Import
import math


# Main class
class RungeKutta4:
    """ The Runge-Kutta method finds approximate value of y for a given x. Only first order ordinary differential
        equations can be solved by using the Runge Kutta 4th order method.
        Below is the formula used to compute next value yn+1 from previous value yn.
        The value of n are 0, 1, 2, 3, ….(x – x0)/h. Here h is step height and xn+1 = x0 + h"""

    def __init__(self):
        self.OmegatDot = 7.292115e-5  # [radians/sec] --- Earth rotation angular rate
        self.GM = 398600.4418  # [km^3/s^2] --- Geocentric constant of the Earth’s gravitational field with atmosphere
        self.fMa = 0.35  # [km^3/s^2] = Gravitational constant of atmosphere
        self.Flattening = 1.0 / 298.25784
        self.AE = 6378.136  # [km] --- Semi-major axis of Earth
        self.J_2 = 1082625.75e-9  # Second zonal harmonic of the geopotential
        self.J_4 = -2370.89e-9  # Fourth zonal harmonic of the geopotential
        self.J_6 = 6.08e-9  # Sixth zonal harmonic of the geopotential
        self.J_8 = 1.40e-11  # Eigth zonal harmonic of the geopotential

        self.CodeFreq = 511e3
        self.G1CarrFreq = 1602.00e6
        self.G1CarrChOffset = 562.5e3
        # self.G1CodeLambda     = Bb::GNSS::SpeedOfLight/self.CodeFreq
        # self.G1CarrLambda     = Bb::GNSS::SpeedOfLight/self.G1CarrFreq
        self.G2CarrChOffset = 437.5e3
        self.G2CarrFreq = 1246.00e6
        # self.G2CodeLambda     = Bb::GNSS::SpeedOfLight/self.CodeFreq
        # self.G2CarrLambda     = Bb::GNSS::SpeedOfLight/self.G2CarrFreq

    def check_multi(self, Extrapolation_dir, Position0, Velocity0, Acceleration0):

        """Position0 = [x0, y0, z0]
        # Velocity0 = [vx0, vy0, vz0]
        # Acceleration0 = [ax0, ayy0, az0]"""

        if Extrapolation_dir == "past":
            m = -1
        else:
            m = 1

        for i in range(1, 1800 + 1, 1):
            c = m / 2

            Position = {'x': 0, 'y': 0, 'z': 0}
            next_Position = {'x': 0, 'y': 0, 'z': 0}

            Velocity = {'vx': 0, 'vy': 0, 'vz': 0}
            next_Velocity = {'vx': 0, 'vy': 0, 'vz': 0}

            a = self.get_acceleration_0(Position0, Velocity0, Acceleration0)

            k11 = Velocity0[0]
            k12 = Velocity0[1]
            k13 = Velocity0[2]

            k14 = a[0]
            k15 = a[1]
            k16 = a[2]

            Position['x'] = Position0[0] + c * k11
            Position['y'] = Position0[1] + c * k12
            Position['z'] = Position0[2] + c * k13

            Velocity['x'] = Velocity0[0] + c * k14
            Velocity['y'] = Velocity0[1] + c * k15
            Velocity['z'] = Velocity0[2] + c * k16

            a = self.get_acceleration(Position, Velocity, Acceleration0)
            # Acceleration['x'] = Acceleration0[0] + c * k14
            # Acceleration['y'] = Acceleration[1] + c * k15
            # Acceleration['z'] = Acceleration[2] + c * k16

            k21 = Velocity0[0] + c * k14
            k22 = Velocity0[1] + c * k15
            k23 = Velocity0[2] + c * k16

            k24 = a[0]
            k25 = a[1]
            k26 = a[2]

            Position['x'] = Position0[0] + c * k21
            Position['y'] = Position0[1] + c * k22
            Position['z'] = Position0[2] + c * k23

            Velocity['x'] = Velocity0[0] + c * k24
            Velocity['y'] = Velocity0[1] + c * k25
            Velocity['z'] = Velocity0[2] + c * k26

            a = self.get_acceleration(Position, Velocity, Acceleration0)

            k31 = Velocity0[0] + c * k24
            k32 = Velocity0[1] + c * k25
            k33 = Velocity0[2] + c * k26

            k34 = a[0]
            k35 = a[1]
            k36 = a[2]

            Position['x'] = Position0[0] + c * k31
            Position['y'] = Position0[1] + c * k32
            Position['z'] = Position0[2] + c * k33

            Velocity['x'] = Velocity0[0] + c * k34
            Velocity['y'] = Velocity0[1] + c * k35
            Velocity['z'] = Velocity0[2] + c * k36
            a = self.get_acceleration(Position, Velocity, Acceleration0)

            k41 = Velocity0[0] + m * k34
            k42 = Velocity0[1] + m * k35
            k43 = Velocity0[2] + m * k36

            k44 = a[0]
            k45 = a[1]
            k46 = a[2]

            next_Position['x'] = Position0[0] + m * (k11 + 2.0 * k21 + 2.0 * k31 + k41) / 6.0
            next_Position['y'] = Position0[1] + m * (k12 + 2.0 * k22 + 2.0 * k32 + k42) / 6.0
            next_Position['z'] = Position0[2] + m * (k13 + 2.0 * k23 + 2.0 * k33 + k43) / 6.0

            next_Velocity['vx'] = Velocity0[0] + m * (k14 + 2.0 * k24 + 2.0 * k34 + k44) / 6.0
            next_Velocity['vy'] = Velocity0[1] + m * (k15 + 2.0 * k25 + 2.0 * k35 + k45) / 6.0
            next_Velocity['vz'] = Velocity0[2] + m * (k16 + 2.0 * k26 + 2.0 * k36 + k46) / 6.0

            Position0[0] = next_Position['x']
            Position0[1] = next_Position['y']
            Position0[2] = next_Position['z']

            Velocity0[0] = next_Velocity['vx']
            Velocity0[1] = next_Velocity['vy']
            Velocity0[2] = next_Velocity['vz']

            """Acceleration0[0] = a[0]
            # Acceleration0[1] = a[1]
            # Acceleration0[2] = a[2]"""

        res_Position0 = Position0
        res_Velocity0 = Velocity0
        res_Acceleration0 = Acceleration0
        return res_Position0, res_Velocity0, res_Acceleration0

    def get_acceleration_0(self, Position0, Velocity0, acceleration0):
        a = [0, 0, 0]
        r2 = Position0[0] * Position0[0] + Position0[1] * Position0[1] + Position0[2] * Position0[2]
        r = math.sqrt(r2)
        r3 = r2 * r
        r5 = r2 * r3
        mu_r3 = self.GM / r3
        k = 3.0 / 2.0 * self.J_2 * self.GM * self.AE * self.AE
        k_r5 = k / r5
        z2r2 = 5 * Position0[2] * Position0[2] / r2
        w2 = self.OmegatDot * self.OmegatDot
        a[0] = Position0[0] * (-mu_r3 - k_r5 * (1 - z2r2) + w2) + 2 * self.OmegatDot * Velocity0[1] + acceleration0[0]
        a[1] = Position0[1] * (-mu_r3 - k_r5 * (1 - z2r2) + w2) - 2 * self.OmegatDot * Velocity0[0] + acceleration0[1]
        a[2] = Position0[2] * (-mu_r3 - k_r5 * (3 - z2r2)) + acceleration0[2]
        return a

    def get_acceleration(self, Position, Velocity, acceleration):
        a = [0, 0, 0]
        r2 = Position['x'] * Position['x'] + Position['y'] * Position['y'] + Position['z'] * Position['z']
        r = math.sqrt(r2)
        r3 = r2 * r
        r5 = r2 * r3
        mu_r3 = self.GM / r3
        k = 3.0 / 2.0 * self.J_2 * self.GM * self.AE * self.AE
        k_r5 = k / r5
        z2r2 = 5 * Position['z'] * Position['z'] / r2
        w2 = self.OmegatDot * self.OmegatDot
        a[0] = Position['x'] * (-mu_r3 - k_r5 * (1 - z2r2) + w2) + 2 * self.OmegatDot * Velocity['y'] + acceleration[0]
        a[1] = Position['y'] * (-mu_r3 - k_r5 * (1 - z2r2) + w2) - 2 * self.OmegatDot * Velocity['x'] + acceleration[1]
        a[2] = Position['z'] * (-mu_r3 - k_r5 * (3 - z2r2)) + acceleration[2]
        return a
