############################################################
# Constants and initial parameters for Martian invasion
############################################################

import numpy as np

MAX_T    = 4.65e7
dt       = 3.6e3
MAX_STEP = int(MAX_T/dt)
G        = 6.67e-11 # Gravitational constant [N m^2/kg^2]

RADIUS_E = 1.521e11 # Earth to sun           [meters]
RADIUS_M = 2.296e11 # mars to sun            [meters]
RADIUS_R = 9.281e6  # Mars to rocket orbit   [meters]

MASS_S   = 1.989e30 # Mass of the Sun        [kg]
MASS_E   = 5.972e24 # Mass of Earth          [kg]
MASS_M   = 6.417e23 # Mass of Mars           [kg]
MASS_R   = 1.072e6  # Mass of rocket         [kg]

VEL_E    = 2.98e4   # Velocity of Earth      [m/s]
VEL_M    = 2.41e4   # Velocity of Mars       [m/s]
VEL_R    = 2.14e3   # Velocity of rocket     [m/s]

# Hohmann boost
V_Y = np.sqrt(G*MASS_S/RADIUS_M)*(np.sqrt(2*RADIUS_E/(RADIUS_E+RADIUS_M))-1)
V_Y += 8.2e2

# correction for numerical error of integration techinique
V_Y *= .94


V_Y2 = np.sqrt(G*MASS_S/RADIUS_E)*(1-np.sqrt(2*RADIUS_M/(RADIUS_E+RADIUS_M)))
V_Y2 += 300
