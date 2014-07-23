############################################################
# Double Pendulum Plotting
############################################################

# Import matplotlib library for plotting
import matplotlib
matplotlib.use('Agg') # this is a hack to keep matplotlib
                      # non-interactive/keep python from complaining
                      # if you're using an ssh connection
import matplotlib.pyplot as pyplot
from matplotlib import animation
import numpy as np

def plot_paths(paths):

    # settings for plotting
    IMAGE_PATH = "pendulum.png"
    TITLE = "Double Pendulum Evolution"
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

    ax.plot(paths[:, 0, 0], paths[:, 0, 1], "b-", alpha=.7, linewidth=3, label="$m_1$")
    ax.plot(paths[:, 1, 0], paths[:, 1, 1], "g-", alpha=.7, linewidth=3, label="$m_2$")

    # # Objects: draw a dot on the last trajectory point
    ax.plot(paths[-1, 0, 0], paths[-1, 0, 1], "b-")
    ax.plot(paths[-1, 1, 0], paths[-1, 1, 1], "g-")

    # pyplot.axis('equal')
    plt.gca().set_aspect('equal', adjustable='box')

    ax.legend(bbox_to_anchor=(1., 1.), loc="best", 
              ncol=1, fancybox=True, shadow=True)

    # Save our plot
    print "Saving plot to %s." % IMAGE_PATH
    plt.savefig(IMAGE_PATH, bbox_inches='tight')


############################################################
# Animation
############################################################

fig = pyplot.figure()
ax = pyplot.axes(xlim=(-2, 2), ylim=(-2, 2))
line, = ax.plot([], [], lw=4)
dots, = ax.plot([], [], "o", markersize=10)
path, = ax.plot([], [], "-", markersize=10)

plotter_paths = None

def init():
    line.set_data([], [])
    return line

# animation function.  This is called sequentially
def animate(i):

    x = np.array([0]+list(plotter_paths[i,:,0]))
    y = np.array([0]+list(plotter_paths[i,:,1]))

    line.set_data(x, y)
    dots.set_data(x, y)
    path.set_data(plotter_paths[:i,-1,0], plotter_paths[:i,-1,1])

    return line

def animate_paths(paths, dt):
    print "Creating animation."
    global plotter_paths
    rate = 30
    skip = int(1/dt)/rate
    plotter_paths = paths[::skip]
    nframes = len(plotter_paths)

    print "Frame skip: %d\nFrames: %d" % (skip, nframes)

    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=nframes, interval=1, blit=True)

    anim.save('double_pendulum.mp4', fps=rate)
