############################################################
# Martian Invasion
############################################################

# Import matplotlib library for plotting
import matplotlib
matplotlib.use('Agg') # this is a hack to keep matplotlib
                      # non-interactive/keep python from complaining
                      # if you're using an ssh connection
import matplotlib.pyplot as pyplot

# Import numpy for numerical calculations, vectors, etc.
import numpy as np
from numpy.linalg import norm as norm

# Import our parameter file, the '*' says take everything in that
# file, and make it available for use in this file
from params import *

# Calculates the force of gravity given displacement vectors r1 & r1
# and scalar masses m1, m2
def force_gravity(r1, r2, m1, m2):
    
    # numpy can subtract arrays like vectors
    r = r1 - r2
    F = - G*m1*m2*norm(r)**(-3.)*r
    return F

# Sum the forces on each body in the current system
def calculate_forces(positions, masses):
    
    # set n to be the number of bodies to consider
    n = len(positions)
    
    # create an array of 2D vectors of length n
    forces = np.zeros(shape=(n,2))

    # for each body, add the gravitational force to each other body
    for i in range(n):
        for j in range(n):
            # make sure we are not calculating the gravity to itself
            if i != j:
                forces[i] += force_gravity(positions[i], positions[j], 
                                           masses[i], masses[j])
    return forces
    
# Update the positions using velocity Verlet integration
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

# This is the function that gets called when we run the program    
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

    trajectories = []
    print "Calculating trajectory."
    for t in range(MAX_T):
        # we append 'np.array(positions)' to the list so we make a
        # COPY of the position array if we just appended 'positions'
        # then we would only append a reference to the array, whose
        # values would be updated each iteration!
        trajectories.append(np.array(positions))
        positions, velocities = update_pos(positions, velocities, masses)

    # turn our python list into a numpy array
    trajectories = np.array(trajectories)

    # settings for plotting
    IMAGE_PATH = "trajectories.png"
    TITLE = "Rocket Projectile"
    YAXIS = "Y"
    XAXIS = "X"

    # Plot the trajectories
    print "Plotting."
    plt = pyplot.figure(figsize=(15, 10), dpi=80, facecolor='w')
    ax = pyplot.axes()
    ax.set_xlabel(XAXIS) 
    ax.set_ylabel(YAXIS)
    ax.set_title(TITLE)

    ax.plot(trajectories[:,0][:, 0], trajectories[:,0][:, 1], 
            "o-", alpha=.7, linewidth=3, label="Sun")
    ax.plot(trajectories[:,1][:, 0], trajectories[:,1][:, 1], 
            "-", alpha=.7, linewidth=3, label="Earth")
    ax.plot(trajectories[:,2][:, 0], trajectories[:,2][:, 1], 
            "-", alpha=.7, linewidth=3, label="Mars")
    ax.plot(trajectories[:,3][:, 0], trajectories[:,3][:, 1], 
            "-", alpha=.7, linewidth=3, label="Rocket")

    pyplot.xlim(-3e11, 3e11)
    pyplot.ylim(-3e11, 3e11)

    ax.legend(bbox_to_anchor=(1., 1.), loc="best", 
              ncol=1, fancybox=True, shadow=True)

    # Save our plot
    print "Saving plot to %s." % IMAGE_PATH
    plt.savefig(IMAGE_PATH, bbox_inches='tight')

# This is Python syntax which tells Python to call the function we
# created, called 'main()', only if this file was run directly, rather
# than with 'import orbital'
if __name__ == "__main__":
    main()

