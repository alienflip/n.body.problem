#include <cstdio>
#include <cinttypes>

#include "hls_math.h"
#include "ap_axi_sdata.h"
#include "hls_stream.h"

#define N 1024
#define NUM_BODIES 128

typedef float DataType;

typedef hls::axis<DataType, 0, 0, 0> packet;
typedef hls::stream<packet> stream;

const float G = -1.0;
const int unit_time = 0.01;

typedef struct _body {
    int id;
    float mass;
    float position[2];
    float velocity[2];
    float acceleration[2];
} body;

float squared(float x);
float distance(body& body_0, body& body_1);
float acceleration(float mass_0, body& body_0, body& body_1);
void direction(body& body_0, body& body_1, float out_direction[2]);
void acceleration_step(body& body_0, body* system, float out_acceleration[2]);
void velocity_step(float inital_velocity[2], float acceleration[2], float time_step, float out_velocity[2]);
void postion_step(float inital_position[2], float initial_velocity[2], float acceleration[2], float time_step, float out_position[2]);
void step(body& body_0, body* system, float time_step, float out_position[2], float out_velocity[2], float out_acceleration[2]);
void total_step(body* system, float time_step);