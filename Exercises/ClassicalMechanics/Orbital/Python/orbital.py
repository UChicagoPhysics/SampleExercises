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
def calculate_forces(positions, masses):
    n = len(positions)
    forces = np.zeros(shape=(n,2))
    for i in range(n):
        for j in range(n):
            if i != j:
                forces[i] += force_gravity(positions[i], positions[j], 
                                           masses[i], masses[j])
    return forces
    
# Update the positions using verlet integration
def update_pos(positions, velocities, masses):
    
    # calculate the total force and accelerations on each body
    forces = calculate_forces(positions, masses)
    accel = np.array([forces[i]/masses[i] for i in range(len(masses))])

    # update the positions using the verlet method
    positions += velocities*dt + .5*accel*dt**2

    # recalculate the accelerations for the new positions
    forces = calculate_forces(positions, masses)
    newaccel = np.array([forces[i]/masses[i] for i in range(len(masses))])

    # use average acceleration to update velocities
    velocities += .5*(newaccel + accel)*dt

    return positions, velocities
    
def main():

    print "Starting calculation."

    # positions is an array of vectors in a 2D plane specifying the
    # positions of [sun, earth, mars, rocket] in m from origin
    positions = np.array([
            [0, 0], 
            [RADIUS_E, 0],
            [RADIUS_M, 0],
            [RADIUS_M + RADIUS_R, 0],
            ])

    # velocities of each body in m/s
    velocities = np.array([
            [0, 0],
            [0, VEL_E],
            [0, VEL_M],
            [0, VEL_M + VEL_R]
            ])
    
    # masses of each body in kg
    masses = np.array([MASS_S, MASS_E, MASS_M, MASS_R])

    for t in range(MAX_T):
        update_pos(positions, velocities, masses)
        print positions[1]
        

# This is Python syntax which tells Python to call the function we
# created, called 'main()', only if this file was run directly, rather
# than with 'import orbital'
if __name__ == "__main__":
    main()

