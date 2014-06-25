############################################################
# Martian Invasion
############################################################

# Import 'numpy' for numerical calculations, vectors, etc.
import numpy as np
from numpy.linalg import norm as norm

# Import our parameter file, the '*' says take everything in that
# file, and make it available for use in this file
from params import *

def force_gravity(r1, r2, m1, m2):
    r = r2 - r1
    F = - G*m1*m2*norm(r)**(-3.)*r
    return F
    

# Calculate the forces on the current system
def calculate_forces(positions):
    print "force"
    
# Update the positions using verlet integration
def update_pos(positions, velocities):
    print "verlet"


def main():
    print "Starting calculation."

    # positions is an array of vectors in a 2D plane specifying the
    # positions of [sun, earth, mars, rocket]
    positions = np.array([
            [0, 0], 
            [RADIUS_E, 0],
            [RADIUS_M, 0],
            [RADIUS_M + RADIUS_R, 0],
            ])

    masses = np.array([MASS_S, MASS_E, MASS_M, MASS_R])

    print force_gravity(positions[0], positions[1], 
                        masses[0], masses[1])

# This is Python syntax which tells Python to call the function we
# made called 'main()' only if this file was run directly rather than
# with 'import orbital'
if __name__ == "__main__":
    main()

