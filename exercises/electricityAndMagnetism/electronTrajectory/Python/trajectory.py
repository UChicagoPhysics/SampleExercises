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

# Creates a matplotlib plot and plots a list of trajectories labeled
# by a list of masses.
# called by      : main()
# arguments      :
# - trajectories : an array of trajectories
# - masses       : a list of masses
# = returns      : None
def plot_trajectory(trajectories, masses):

    # settings for plotting
    print "Plotting."
    IMAGE_PATH = "trajectory.png"

    # create a plot
    plt = pyplot.figure(figsize=(15, 10), dpi=80, facecolor='w')
    ax = pyplot.axes()

    # set the title and axis labels
    ax.set_xlabel("X [meters]") 
    ax.set_ylabel("Y [meters]")
    ax.set_title("Electron Trajectories")

    # for each trajectory in our array of trajectories, add a plot
    for i in range(len(trajectories)):
        trajectory = trajectories[i]
        ax.plot(trajectory[:,0], trajectory[:,1], "-", 
                alpha=.7, linewidth=3, label="M = %.2e kg" % masses[i])
        
    # Define the plot limits
    pyplot.xlim(0, BOX_X)
    pyplot.ylim(.4*BOX_Y, BOX_Y)

    # Draw a legend and save our plot
    print "Saving plot to %s." % IMAGE_PATH
    ax.legend(loc="lower right", fancybox=True, shadow=True)
    plt.savefig(IMAGE_PATH, bbox_inches='tight')

    return None

# calculates the magnetic force on the particle and moves it
# accordingly
# called by  : calculate_trajectory()
# arguments  :  
# - position : 3D numpy array (r_x,r_y,r_z) in meters
# - velocity : 3D numpy array (v_x,v_y,v_z) in m/s
# - mass     : scalar float in kg
# - B        : magnetic field strength, scalar float in Tesla
# = returns  : the updated position and velocity (3D vectors)
def update_pos(position, velocity, mass, B):

    # calculate the total force and accelerations on each body using
    # numpy's vector cross product
    field = [0, 0, B]
    force = q*np.cross(velocity, field)
    
    accel = force/mass

    # update the positions and velocity
    position += velocity*dt + .5*accel*dt**2
    velocity += accel*dt

    return position, velocity

# Calculates the trajectory of the particle 
# called by  : main()
# arguments  :
# - position : 3D vector (r_x,r_y,r_z) in meters
# - velocity : 3D vector (v_x,v_y,v_z) in m/s
# - mass     : scalar float in kg
# - B        : magnetic field strength, scalar float in Tesla
# = returns  : a numpy array of 3D vectors (np.arrays)
def calculate_trajectory(position, velocity, mass, B):

    print "Calculating trajectory: %.2e kg" % mass

    # Start a list to append the positions to as we move the particle
    trajectory = [np.array(position)]

    # While the particle is inside the wall, update its position
    while position[1] < BOX_Y:
        position, velocity = update_pos(position, velocity, mass, B)
        trajectory.append(np.array(position))

    return np.array(trajectory)

# main is the function that gets called when we run the program.
# Loops over multiples of electron mass, calculates trajectories, and
# plots them.
def main():

    print "Starting calculation."

    # Magnetic field strength [Telsa]
    B = -1.0e-3 

    # Create lists to append a trajectory for each mass, 
    # and a list for masses
    trajectories = []
    masses = []

    # Loop over masses from 1 to 6 times electron mass
    for i in range(1,7):
        # Initial velocity and positionfor particle
        position = np.array([0, .5*BOX_Y, 0])
        velocity = np.array([.5*C, 0, 0])
        mass = i*MASS_E

        # calculate the list of positions the particle travels through
        trajectory = calculate_trajectory(position, velocity, mass, B)

        # add the mass and trajectory to our lists
        masses.append(mass)
        trajectories.append(np.array(trajectory))

    trajectories = np.array(trajectories)

    # Plotting each trajectory
    plot_trajectory(trajectories, masses)

# This is Python syntax which tells Python to call the function we
# created, called 'main()', only if this file was run directly, rather
# than with 'import orbital'
if __name__ == "__main__":
    main()

