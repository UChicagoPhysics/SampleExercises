// Martian Invasion

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define DIM 2
#define N_BODY 4

#define MAX_T    2.43e7
#define dt       3.6e3    // time step of 1 hour
#define MAX_STEP (int)(MAX_T/dt)
#define G        6.67e-11 // Gravitational constant [N m^2/kg^2]
#define PI 3.14159265359

#define DIAM_E   1.273e7  // Diameter of the earth
#define RADIUS_E 1.521e11 // Earth to sun           [meters]
#define RADIUS_M 2.296e11 // mars to sun            [meters]
#define RADIUS_R 9.281e6  // Mars to rocket orbit   [meters]

#define MASS_S   1.989e30 // Mass of the Sun        [kg]
#define MASS_E   5.972e24 // Mass of Earth          [kg]
#define MASS_M   6.417e23 // Mass of Mars           [kg]
#define MASS_R   1.072e6  // Mass of rocket         [kg]

#define VEL_E    2.98e4   // Velocity of Earth      [m/s]
#define VEL_M    2.41e4   // Velocity of Mars       [m/s]
#define VEL_R    2.14e3   // Velocity of rocket     [m/s]

const double R1 = RADIUS_M-RADIUS_R;


double norm(double r[DIM])
{
    double sqnorm = 0;
    for (int i = 0; i < DIM; i++)
	sqnorm += r[i]*r[i];
    return sqrt(sqnorm);
}

// Calculates the force of gravity given displacement vectors r1 & r1
// and scalar masses m1, m2
void force_gravity(double r1[DIM], double r2[DIM], 
		   double m1, double m2, double F[DIM])
{
    double r[DIM];
    for (int i = 0; i < DIM; i++)
	r[i] = r1[i] - r2[i];
    for (int i = 0; i < DIM; i++)
	F[i] += - G*m1*m2*pow(norm(r), -1)*r[i];
    return;
}

// Sum the forces on each body in the current system
void calculate_forces(double positions[N_BODY][DIM], 
		      double masses[N_BODY], 
		      double forces[N_BODY][DIM])
{
    
    // for each body, add the gravitational force to each other body
    for (int i = 0; i < N_BODY; i++){
        for (int j = 0; j < N_BODY; j++){

            // make sure we are not calculating the gravity to itself
            if (i != j){
		// add the force of gravity to the array of forces
		force_gravity(positions[i], positions[j], 
			      masses[i], masses[j], forces[i]);

	    }
	}
    }

    return;
}

    
// Update the positions using velocity Verlet integration
void update_pos(double positions[N_BODY][DIM], 
		double velocities[N_BODY][DIM], 
		double masses[N_BODY])
{

    // calculate the total force and accelerations on each body
    double forces[N_BODY][DIM], new_forces[N_BODY][DIM];
    double accel[N_BODY][DIM], new_accel[N_BODY][DIM];

    for (int i = 0; i < N_BODY; i++){
	for (int j = 0; j < DIM; j++){
	    forces[i][j] = 0;
	    accel[i][j] = 0;
	    new_forces[i][j] = 0;
	    new_accel[i][j] = 0;
	}
    }

    calculate_forces(positions, masses, forces);

    // update the positions using the verlet method
    for (int i = 0; i < N_BODY; i++){
	for (int j = 0; j < DIM; j++){
	    accel[i][j] = forces[i][j]/masses[i];
	    positions[i][j] += velocities[i][j]*dt + .5*accel[i][j]*dt*dt;
	}
    }
    
    // recalculate the accelerations for the new positions
    calculate_forces(positions, masses, new_forces);

    // use average acceleration to update velocities
    for (int i = 0; i < N_BODY; i++){
	for (int j = 0; j < DIM; j++){
	    new_accel[i][j] = forces[i][j]/masses[i];
	    velocities[i][j] += .5*(new_accel[i][j] + accel[i][j])*dt;
	}
    }

    return;
}

void calculate_trajectory(double V_Y, 
			  double V_Y2, 
			  double THETA, 
			  double ADJUSTMENT)
{
    V_Y += ADJUSTMENT;

    // positions is an array of vectors in a 2D plane specifying the
    // positions of [sun, earth, mars, rocket] in m from origin

    double positions[N_BODY][DIM], velocities[N_BODY][DIM];

    /* Sun */
    positions[0][0] = 0.0;
    positions[0][1] = 0.0;
    velocities[0][0] = 0.0;
    velocities[0][1] = 0.0;


    /* Earth */
    positions[1][0] = RADIUS_E*cos(THETA);
    positions[1][1] = -RADIUS_E*sin(THETA);
    velocities[1][0] = VEL_E*sin(THETA);
    velocities[1][1] = VEL_E*cos(THETA);

    /* Mars */
    positions[2][0] = RADIUS_M;
    positions[2][1] = 0;
    velocities[2][0] = 0;
    velocities[2][1] = VEL_M;

    /* Rocket */
    positions[3][0] = R1;
    positions[3][1] = 0;
    velocities[3][0] = 0;
    velocities[3][1] = VEL_M - VEL_R;

    printf("Applying primary Hohmann boost.\n");
    velocities[3][1] += V_Y;
    
    // masses of each body in kg
    double masses[] = {MASS_S, MASS_E, MASS_M, MASS_R};
    
    int BOOSTED = 0;

    printf("Calculating trajectory.\n");

    for (int i = 0; i < MAX_STEP; i++){

	double ROCKET_Y = positions[3][1];

        update_pos(positions, velocities, masses);
        
	double disp_to_earth[DIM];
	for (int i = 0; i < DIM; i++)
	    disp_to_earth[i] = positions[1][i] - positions[3][i];

	printf("%.2e\t%.2e\n", disp_to_earth[0], disp_to_earth[1]);
        if (norm(disp_to_earth) < DIAM_E/2){
            printf("LANDED\n");
	    return;
	}

        if (ROCKET_Y > 0 && positions[3][1] < 0 && !BOOSTED){
            BOOSTED = 1;
            printf("Applying secondary Hohmann boost.\n");
            velocities[3][1] -= V_Y2;
	}
    }

    return;

}


// This is the function that gets called when we run the program    
int main(int argc, char *argv[])
{
    printf("Starting calculation.\n");

    /* Use analytical solution to find Hohmann velocity difference */
    double V_Y = sqrt(G*MASS_S/R1)*(sqrt(2*RADIUS_E/(RADIUS_E+R1))-1);

    // correction for numerical error of integration techinique
    V_Y *= .97;

    // Secondary Hohmann boost
    double V_Y2 = sqrt(G*MASS_S/RADIUS_E)*(1-sqrt(2*R1/(RADIUS_E+R1)));

    // Parameters for gravity well adjustment
    double ADJUSTMENT = 8.10493e2;

    // Relative orbital angle between Mars and Earth
    double THETA      = PI*.45;

    // Calculate the trajectories
    calculate_trajectory(V_Y, V_Y2, THETA, ADJUSTMENT);

}
