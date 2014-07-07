#include <stdio.h>

// Constants
const double C      = 2.998e8;        // Speed of light [m/s]
const double MASS_E = 9.10938e-31;    // Mass of electron [kg]
const double q      = 1.60217657e-19; // Charge of electron [coulombs]

// simulation domain parameters
const double BOX_X = 2.0;
const double BOX_Y = 1.0;
const double BOX_Z = 1.0;

// timestep
const double dt = 1e-10;

// the dimensionality of the simulation
const int DIM = 3;

void cross(double a[DIM], double b[DIM], double res[DIM])
{
    res[0] = a[1]*b[2] - a[2]*b[1];
    res[1] = a[2]*b[0] - a[0]*b[2];
    res[2] = a[0]*b[1] - a[1]*b[0];
    return;
}

// calculates the magnetic force on the particle and moves it
// accordingly
// called by  : calculate_trajectory()
// arguments  :  
// - position : 3D numpy array (r_x,r_y,r_z) in meters
// - velocity : 3D numpy array (v_x,v_y,v_z) in m/s
// - mass     : scalar double in kg
// - B        : magnetic field strength, scalar double in Tesla
// = returns  : nothing, the position and velocity arrays are updated in placegg
void update_pos(double position[DIM], double velocity[DIM], double mass, double B)
{
    // calculate the total force and accelerations on each body using
    // numpy's vector cross product
    double field[] = {0, 0, B};
    double force[] = {0, 0, 0};

    // Calculate the force as a cross product using function defined above
    cross(velocity, field, force);

    fprintf(stderr, "%.2e\n", .5*force[1]/mass*dt*dt);
    
    // update the positions and velocity
    for (int i = 0; i < DIM; i++){
	double accel = force[i]/mass;
	position[i] += velocity[i]*dt + .5*accel*dt*dt;
	velocity[i] += accel*dt;
    }

    // returns nothing because we updated the position and velocity
    // arrays that were passed to us
    return;
}


// Calculates the trajectory of the particle 
// called by  : main()
// arguments  :
// - position : 3D vector (r_x,r_y,r_z) in meters
// - velocity : 3D vector (v_x,v_y,v_z) in m/s
// - mass     : scalar double in kg
// - B        : magnetic field strength, scalar double in Tesla
// = returns  : a numpy array of 3D vectors (np.arrays)
void calculate_trajectory(FILE *output_file, double mass, double B){

    fprintf(stdout, "Calculating trajectory: %.2e kg\n", mass);

    double position[] = {0, .5*BOX_Y, 0};
    double velocity[] = {.5*C, 0, 0};
    
    // While the particle is inside the wall, update its position
    while (position[1] < BOX_Y){
        update_pos(position, velocity, mass, B);
	for (int i = 0; i < DIM; i++)
	    fprintf(output_file, "%f\t", position[i]);
	for (int i = 0; i < DIM; i++)
	    fprintf(output_file, "%f\t", velocity[i]);
	fprintf(output_file, "\n");
    }

    return;
}


int main()
{
    FILE *output_file = fopen("data.tsv", "w");
    
    calculate_trajectory(stdout, MASS_E, -1.0e-3);

    fclose(output_file);

    return 0;
}

