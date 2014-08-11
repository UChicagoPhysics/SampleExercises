############################################################
# Double Pendulum Parameter file
############################################################

import numpy as np

g = 9.8                  # m/s

l1       = 1.2           # m
l2       = .7            #m

theta1_0 = np.pi/4
theta2_0 = np.pi

m1       = .10           # kg
m2       = .05           # kg

dt       = 1e-3
max_t    = 5.0

nsteps   = int(max_t/dt) # number of steps

print "nsteps:", nsteps

