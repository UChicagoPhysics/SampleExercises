############################################################
# Double Pendulum
############################################################

# Import numpy for numerical calculations, vectors, etc.
from numpy import array, zeros, cos, sin, pi
from numpy.linalg import norm as norm
from scipy.integrate import ode

from params import *
import plotting

"""Evolves the a double pendulum system given initial parameters
definied in ````params.py```` module
"""

def dtheta1(theta1, theta2, p1, p2):
    """the time derivative of ``theta1``

    :param theta1: float
    :param theta2: float
    :param p1: float
    :param p2: float
    :returns: float, the time derivative of theta1

    """
    num = l2*p1 - l1*p2*cos(theta1 - theta2)
    den = l1*l1*l2*(m1 + m2*sin(theta1 - theta2)**2)
    return num/den

def dtheta2(theta1, theta2, p1, p2):
    """the time derivative of ``theta2``

    :param theta1: float
    :param theta2: float
    :param p1: float
    :param p2: float
    :returns: float, the time derivative of theta2

    """
    num = l1*(m1+m2)*p2 - l2*m2*p1*cos(theta1-theta2)
    den = l1*l2*l2*m2*(m1+ m2*sin(theta1-theta2)**2)
    return num/den

def dp1(theta1, theta2, p1, p2, c1, c2):
    """the time derivative of ``p1``

    :param theta1: float
    :param theta2: float
    :param p1: float
    :param p2: float
    :returns: float, the time derivative of p1

    """
    return -(m1+m2)*g*l1*sin(theta1) - c1 + c2

def dp2(theta1, theta2, p1, p2, c1, c2):
    """the time derivative of ``p2``

    :param theta1: float
    :param theta2: float
    :param p1: float
    :param p2: float
    :returns: float, the time derivative of p2

    """
    return -m2*g*l2*sin(theta2) + c1 - c2

def C1(theta1, theta2, p1, p2):
    """helper function to calculate a constant ``C_1``

    :param theta1: float
    :param theta2: float
    :param p1: float
    :param p2: float
    :returns: float, constant used in calculating Hamilton's equation

    """
    num = p1*p2*sin(theta1 - theta2)
    den = l1*l2*(m1 + m2*sin(theta1 - theta2)**2)
    return num/den

def C2(theta1, theta2, p1, p2):
    """helper function to calculate a constant ``C_2``

    :param theta1: float
    :param theta2: float
    :param p1: float
    :param p2: float
    :returns: float, constant used in calculating Hamilton's equation

    """
    num = l2*l2*m2*p1*p2 + l1*(m1 + m2)*p2**2 - l1*l2*m2*p1*p2*cos(theta1-theta2)
    den = 2*l1*l1*l2*l2*(m1 + m2*sin(theta1-theta2)**2)**2*sin(2*(theta1-theta2))
    return num/den

def deriv(t, y):
    """calculated the derivative of ``theta1, theta2, p1, p2``

    :param theta1: float
    :param theta2: float
    :param p1: float
    :param p2: float
    :returns: numpy array, time derivative of parameters

    """
    theta1, theta2, p1, p2 = y[0], y[1], y[2], y[3]

    _c1 = C1(theta1, theta2, p1, p2)
    _c2 = C2(theta1, theta2, p1, p2)

    _dtheta1 = dtheta1(theta1, theta2, p1, p2)
    _dtheta2 = dtheta2(theta1, theta2, p1, p2)
    
    _dp1 = dp1(theta1, theta2, p1, p2, _c1, _c2)
    _dp2 = dp2(theta1, theta2, p1, p2, _c1, _c2)

    return array([_dtheta1, _dtheta2, _dp1, _dp2])

def euler(theta1, theta2, p1, p2):
    """use a naive euler integration schemed to make a single step in
    the pendulum's motion

    :param theta1: float
    :param theta2: float
    :param p1: float
    :param p2: float
    :returns: tuple of updated parameters

    """

    _y = deriv(0, [theta1, theta2, p1, p2])
    _dtheta1, _dtheta2, _dp1, _dp2 = _y[0], _y[1], _y[2], _y[3]

    theta1 += _dtheta1*dt
    theta2 += _dtheta2*dt

    p1 += _dp1*dt
    p2 += _dp2*dt
    
    return theta1, theta2, p1, p2


def velocity_verlet(theta1, theta2, p1, p2):
    """**TODO** use a velocity verlet integration schemed to make a single step in
    the pendulum's motion

    :param theta1: float
    :param theta2: float
    :param p1: float
    :param p2: float
    :returns: tuple of parameters

    """

        
    return theta1, theta2, p1, p2


def calculate_paths(method = "euler"):
    """use a default or specified method of integration to solve the
    pendulum's motion

    :param method: optional, string.  specify the integration method to use

    """
    
    theta1 = theta1_0
    theta2 = theta2_0
    p1, p2 = 0.0, 0

    paths = []
    if method == "euler":
        for i in range(nsteps):
            theta1, theta2, p1, p2 = euler(theta1, theta2, p1, p2)
            r1 = array([l1*sin(theta1), -l1*cos(theta1)])
            r2 = r1 + array([l2*sin(theta2), -l2*cos(theta2)])
            paths.append([r1, r2])


    elif method == "scipy":
        yint = [theta1, theta2, p1, p2]
        # r = ode(deriv).set_integrator('zvode', method='bdf')
        r = ode(deriv).set_integrator('vode', method='bdf')
        r.set_initial_value(yint, 0)
        
        paths = []
        while r.successful() and r.t < max_t:
            r.integrate(r.t+dt)
            theta1, theta2 = r.y[0], r.y[1]
            r1 = array([l1*sin(theta1), -l1*cos(theta1)])
            r2 = r1 + array([l2*sin(theta2), -l2*cos(theta2)])
            paths.append([r1, r2])

    return array(paths)

# This is the function that gets called when we run the program    
def main():

    print "Starting calculation."

    # Calculate the trajectories
    # paths = calculate_paths("scipy")
    paths = calculate_paths()
    # print paths

    # Plotting
    plotting.plot_paths(paths)

    # animation
    # plotting.animate_paths(paths, dt)

# This is Python syntax which tells Python to call the function we
# created, called 'main()', only if this file was run directly, rather
# than with 'import orbital'
if __name__ == "__main__":
    main()

