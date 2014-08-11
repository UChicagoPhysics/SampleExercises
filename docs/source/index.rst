.. UChicago Physics Sample Exercises documentation master file, created by
   sphinx-quickstart on Tue Jul 22 21:25:14 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

UChicago Physics Sample Exercises's documentation
=============================================================

:mod:`Orbital` -- Launching a rocket from Mars to Earth
-------------------------------------------------------

This problem asks the student to launch a rocket from the orbit of
Mars on a course for intercept with Earth.  

Build/Run
+++++++++
.. code-block:: bash

    $ python orbital.py

Sample Parameter file
+++++++++++++++++++++

.. literalinclude:: exercises/classicalMechanics/Orbital/Python/params.py
    :language: python

Output
++++++

.. literalinclude:: exercises/classicalMechanics/Orbital/Python/sample_output.txt
    :linenos:

.. image:: exercises/classicalMechanics/Orbital/Python/radii.png

Plots
++++++

.. image:: exercises/classicalMechanics/Orbital/Python/trajectories.png


Methods
+++++++

.. automodule:: orbital
   :members:


:mod:`doublePendulum` -- Solving the Classical Double Pendulum
--------------------------------------------------------------

Solve the classical double pendulum problem.  This problem is
appropriate for an intermediate mechanics course teach Lagrangian and
Hamiltonian Dynamics.  

Build/Run
+++++++++
.. code-block:: bash

    $ python doublePendulum.py

Sample Parameter file
+++++++++++++++++++++

.. literalinclude:: exercises/classicalMechanics/doublePendulum/Python/params.py
    :language: python

Output
++++++

.. literalinclude:: exercises/classicalMechanics/doublePendulum/Python/sample_output.txt
    :linenos:

Plots
++++++

.. image:: exercises/classicalMechanics/doublePendulum/Python/pendulum.png


Methods
+++++++

.. automodule:: doublePendulum
   :members:

.. automodule:: plotting
   :members:

:mod:`electronTrajectory` -- Comparing Trajectory of Charged Particles in a Magnetic Field
------------------------------------------------------------------------------------------

Calculate the trajectory of charged particles with different masses in
an external magnetic field.

Build/Run
+++++++++
.. code-block:: bash

    $ python electronTrajectory.py

Output
++++++

.. literalinclude:: exercises/electricityAndMagnetism/electronTrajectory/Python/sample_output.txt
    :linenos:

Plots
++++++

.. image:: exercises/electricityAndMagnetism/electronTrajectory/Python/trajectory.png


Methods
+++++++

cd.. automodule:: electronTrajectory
   :members:


