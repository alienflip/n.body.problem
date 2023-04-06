#include <iostream>

#include <math.h>

using namespace std;

const int NUM_BODIES = 128;
const float G = -1.0;
const float MAX_VELOCITY = 1;
const float LOWER_BOUNDARY_X = -100;
const float UPPER_BOUNDARY_X = 100;
const float LOWER_BOUNDARY_Y = -100;
const float UPPER_BOUNDARY_Y = 100;

typedef struct _body {
    int id;
    float mass;
    float position[2];
    float velocity[2];
    float acceleration[2];
} body;
        
float squared(float x){
    return x*x;
}

float distance(body& body_0, body& body_1){
    float x = squared(body_0.position[0] - body_1.position[0]);
    float y = squared(body_0.position[1] - body_1.position[1]);
    return (float)sqrt(x + y);
}

float acceleration(float mass_0, body& body_0, body& body_1){
    float distance_ = distance(body_0, body_1);
    float denominator = squared(distance_);
    if(denominator < 0.1){
        return 0.1;
    }
    else {
        return G * mass_0 / denominator;
    }
}

void direction(body& body_0, body& body_1, float out_direction[2]){
    float distance_ = distance(body_0, body_1);
    if(distance_ < 0.1){
        distance_ = 0.1;
    }
    float x = (body_0.position[0] - body_1.position[0]) / distance_;
    float y = (body_0.position[1] - body_1.position[1]) / distance_;
    out_direction[0] = x;
    out_direction[1] = y;
}

void acceleration_step(body& body_0, body* system, float out_acceleration[2]){
    float out_direction[2] = {0.0, 0.0};
    for(int i = 0; i < NUM_BODIES; i++){
        if(system[i].id != body_0.id){
            float accel = acceleration(system[i].mass, body_0, system[i]);
            direction(body_0, system[i], out_direction);
            out_acceleration[0] += out_direction[0] * accel;
            out_acceleration[1] += out_direction[1] * accel;
        }
    }
}

float velocity_condition(float velocity){
    if(velocity < -1 * MAX_VELOCITY){
        return -1 * MAX_VELOCITY;
    }else if(velocity > MAX_VELOCITY){
        return MAX_VELOCITY;
    }else{
        return velocity;
    }
}

void velocity_step(float inital_velocity[2], float acceleration[2], float time_step, float out_velocity[2]){
    float out_velocity_x = inital_velocity[0] + acceleration[0] * time_step;
    float out_velocity_y = inital_velocity[1] + acceleration[1] * time_step;
    out_velocity[0] = velocity_condition(out_velocity_x);
    out_velocity[1] = velocity_condition(out_velocity_y);
}

float position_condition_x(float in_position_x){
    if(in_position_x < LOWER_BOUNDARY_X){
        return UPPER_BOUNDARY_X;
    }
    else if(in_position_x > UPPER_BOUNDARY_X){
        return LOWER_BOUNDARY_X;
    }else{
        return in_position_x;
    }
}

float position_condition_y(float in_position_y){
    if(in_position_y < LOWER_BOUNDARY_Y){
        return UPPER_BOUNDARY_Y;
    }
    else if(in_position_y > UPPER_BOUNDARY_Y){
        return LOWER_BOUNDARY_Y;
    }else{
        return in_position_y;
    }
}

void postion_step(float inital_position[2], float initial_velocity[2], float acceleration[2], float time_step, float out_position[2]){
    float out_position_x = inital_position[0] + initial_velocity[0] * time_step + 0.5 * acceleration[0] * squared(time_step);
    float out_position_y = inital_position[1] + initial_velocity[1] * time_step + 0.5 * acceleration[1] * squared(time_step);
    out_position[0] = position_condition_x(out_position_x);
    out_position[1] = position_condition_y(out_position_y);
}

void step(body& body_0, body* system, float time_step, float out_position[2], float out_velocity[2], float out_acceleration[2]){
    acceleration_step(body_0, system, out_acceleration);
    velocity_step(body_0.velocity, body_0.acceleration, time_step, out_velocity);
    postion_step(body_0.position, body_0.velocity, body_0.acceleration, time_step, out_position);
    body_0.acceleration[0] = out_acceleration[0];
    body_0.acceleration[1] = out_acceleration[1];
    body_0.velocity[0] = out_velocity[0];
    body_0.velocity[1] = out_velocity[1];
    body_0.position[0] = out_position[0];
    body_0.position[1] = out_position[1];
}

void total_step(body* system, float time_step){
    float out_acceleration[2] = {0, 0};
    float out_velocity[2] = {0, 0};
    float out_position[2] = {0, 0};
    for(int i = 0; i < NUM_BODIES; i++){
        step(system[i], system, time_step, out_position, out_velocity, out_acceleration);
        out_acceleration[0] = 0;
        out_acceleration[1] = 0;
        out_velocity[0] = 0;
        out_velocity[1] = 0;
        out_position[0] = 0;
        out_position[1] = 0;
    }
}

int main(){
    float time_step = 0.0;

    body system[NUM_BODIES];
    for(int i = 0; i < NUM_BODIES; i++){
        body new_body;
        float r_0 = (float)(rand() % 100);
        float r_1 = (float)(rand() % 100);
        new_body.id = i;
        new_body.mass = 1.0;
        new_body.position[0] = r_0;
        new_body.position[1] = r_1;
        new_body.velocity[0] = 0.0;
        new_body.velocity[1] = 0.0;
        new_body.acceleration[0] = 0.0;
        new_body.acceleration[1] = 0.0;
        system[i] = new_body;
    }

    for(int i = 0; i < 808; i++){
        std::cout << "Particle positions: ";
        std::cout << " [" << system[0].position[0] << ", " << system[0].position[1] << "]";
        std::cout << " [" << system[1].position[0] << ", " << system[1].position[1] << "]";
        std::cout << " [" << system[2].position[0] << ", " << system[2].position[1] << "]";
        std::cout << " ... " << std::endl;
        total_step(system, time_step);
        time_step += 0.001;
    }
    return 1;
}
