############################################################
# Electron trajectory
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

# Global constants
C      = 2.998e8        # Speed of light [m/s]
MASS_E = 9.10938e-31    # Mass of electron [kg]
q      = 1.60217657e-19 # Charge of electron [coulombs]

# simulation domain parameters
BOX_X = 2
BOX_Y = 1
BOX_Z = 1

# timestep
dt = 1e-10

def plot_trajectory(trajectories, masses):

    # settings for plotting
    IMAGE_PATH = "trajectory.png"
    TITLE = "Electron Trajectories"
    YAXIS = "Y"
    XAXIS = "X"

    # Plot the trajectories
    print "Plotting."

    # create a plot
    plt = pyplot.figure(figsize=(15, 10), dpi=80, facecolor='w')
    ax = pyplot.axes()

    # set the title and axis labels
    ax.set_xlabel(XAXIS) 
    ax.set_ylabel(YAXIS)
    ax.set_title(TITLE)

    for i in range(len(trajectories)):
        trajectory = trajectories[i]
        ax.plot(trajectory[:,0], trajectory[:,1], "-", 
                alpha=.7, linewidth=3, label="M = %.2e kg" % masses[i])

    # ax.legend(bbox_to_anchor=(1., 1.), loc="best", 
    #           ncol=1, fancybox=True, shadow=True)
        
    ax.legend(loc="lower right", fancybox=True, shadow=True)

    pyplot.xlim(0, BOX_X)
    pyplot.ylim(0, BOX_Y)

    # Save our plot
    print "Saving plot to %s." % IMAGE_PATH
    plt.savefig(IMAGE_PATH, bbox_inches='tight')


# Update the positions using euler
def update_pos(position, velocity, mass, B):

    # calculate the total force and accelerations on each body
    field = [0, 0, B]
    force = q*np.cross(velocity, field)
    accel = force/mass

    # update the positions using the verlet method
    position += velocity*dt + .5*accel*dt**2
    
    # use average acceleration to update velocities
    velocity += accel*dt

    return position, velocity

def calculate_trajectory(position, velocity, mass, B):

    print "Calculating trajectory."

    trajectory = [np.array(position)]

    while position[1] < BOX_Y:
        position, velocity = update_pos(position, velocity, mass, B)
        trajectory.append(np.array(position))

    return trajectory


# trajectory is the function that gets called when we run the program    
def main():

    print "Starting calculation."

    # Magnetic field strength [Telsa]
    B = -1.0e-3 

    # Calculate the trajectories
    trajectories = []
    masses = []

    for i in range(1,7):
        # Initial velocity and positionfor particle
        position = np.array([0, .5*BOX_Y, 0])
        velocity = np.array([.5*C, 0, 0])
        mass = i*MASS_E

        trajectory = calculate_trajectory(position, velocity, mass, B)
        masses.append(mass)
        trajectories.append(np.array(trajectory))

    trajectories = np.array(trajectories)

    # Plotting
    plot_trajectory(trajectories, masses)

# This is Python syntax which tells Python to call the function we
# created, called 'main()', only if this file was run directly, rather
# than with 'import orbital'
if __name__ == "__main__":
    main()

