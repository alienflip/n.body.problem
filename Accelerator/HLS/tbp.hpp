#include <cstdio>
#include <cinttypes>
#include <math.h>

#include "ap_axi_sdata.h"
#include "hls_stream.h"

#define N 1024

struct body {
    int id;
    float mass;
    float position[2];
    float velocity[2];
    float acceleration[2];
};

const int NUM_BODIES = 128;
const float G = -1;
const float time_step = 0.001;

typedef float DataType;

typedef hls::axis<DataType, 0, 0, 0> packet;
typedef hls::stream<packet> stream;

float squared(float x);
float cubed(float x);
float distance(struct body body_0, struct body body_1);
float acceleration(float mass_0, struct body body_0, struct body body_1);
void direction(struct body body_0, struct body body_1, float out_direction[2]);
void acceleration_step(struct body body, struct body system[NUM_BODIES], float out_acceleration[2]);
void velocity_step(float inital_velocity[2], float time_step, float acceleration[2], float out_velocity[2]);
void postion_step(float inital_position[2], float initial_velocity[2], float time_step, float acceleration[2], float out_position[2]);
void step(struct body body, float initial_position[2], float initial_velocity[2], float initial_acceleration[2], struct body system[NUM_BODIES]);
void total_step(struct body system[NUM_BODIES]);
template <typename T> void tbp(struct body system[NUM_BODIES]);
