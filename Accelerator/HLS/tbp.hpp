#include <cstdio>
#include <cinttypes>
#include <math.h>

#include "ap_axi_sdata.h"
#include "hls_stream.h"

#define N 1024

typedef struct _body {
    int id;
    float mass;
    float position[2];
    float velocity[2];
    float acceleration[2];
} body;

const int NUM_BODIES = 128;
const float G = -1;

typedef float DataType;

typedef hls::axis<DataType, 0, 0, 0> packet;
typedef hls::stream<packet> stream;

float squared(float x);
float cubed(float x);
float distance(body& body_0, body& body_1);
float acceleration(float mass_0, body& body_0, body& body_1);
void direction(body& body_0, body& body_1, float out_direction[2]);
void acceleration_step(body& body_0, body system[NUM_BODIES], float out_acceleration[2]);
void velocity_step(float inital_velocity[2], float time_step, float acceleration[2], float out_velocity[2]);
void postion_step(float inital_position[2], float initial_velocity[2], float time_step, float acceleration[2], float out_position[2]);
void step(body& body_0, float initial_position[2], float initial_velocity[2], float initial_acceleration[2], body system[NUM_BODIES], float time_step);
void total_step(body system[NUM_BODIES], float time_step);
template <typename T> void tbp(body system[NUM_BODIES], float time_step);
