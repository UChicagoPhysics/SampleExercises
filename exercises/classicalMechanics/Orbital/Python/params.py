############################################################
# Constants and initial parameters for Martian invasion
############################################################

import numpy as np

MAX_T    = 2.43e7
# MAX_T    = 3.0e7
dt       = 3.6e3    # time step of 1 hour
MAX_STEP = int(MAX_T/dt)
G        = 6.67e-11 # Gravitational constant [N m^2/kg^2]

DIAM_E   = 1.273e7  # Diameter of the earth
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

R1 = RADIUS_M-RADIUS_R

# Hohmann boost
V_Y = np.sqrt(G*MASS_S/R1)*(np.sqrt(2*RADIUS_E/(RADIUS_E+R1))-1)

# correction for numerical error of integration techinique
V_Y *= .97

# Secondary Hohmann boost
V_Y2 = np.sqrt(G*MASS_S/RADIUS_E)*(1-np.sqrt(2*R1/(RADIUS_E+R1)))
