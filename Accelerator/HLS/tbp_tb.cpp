#include "tbp.hpp"

void sw_tbp(struct body system[NUM_BODIES]) {
    for(int i = 0; i < NUM_BODIES; i++){
        struct body body = system[i];
        step(body, body.velocity, body.position, body.acceleration, system);
    }
}

int main(void) {
	/*initialise*/
    int i, err;

    DataType in[N];
    DataType out_sw[N];
    DataType out_hw[N];

    std::cout << "signal in:" << std::endl;
    for (i = 0; i < N; i++) {
    	in[i] = (float)(i % 2);
        std::cout << in[i] << " ";
    }
    std::cout << std::endl;

    struct body sys_sw[NUM_BODIES];
    struct body sys_hw[NUM_BODIES];
    for(int i = 0; i < N; i++){
        if(i % 8 == 0){
        	int j = (int)(i / 8);
            struct body new_body;
            new_body.id = in[j];
            new_body.mass = in[j + 1];
            new_body.position[0] = in[j + 2];
            new_body.position[1] = in[j + 3];
            new_body.velocity[0] = in[j + 4];
            new_body.velocity[1] = in[j + 5];
            new_body.acceleration[0] = in[j + 6];
            new_body.acceleration[1] = in[j + 7];
            sys_sw[j] = new_body;

            struct body new_body_;
            new_body_.id = in[j];
            new_body_.mass = in[j + 1];
            new_body_.position[0] = in[j + 2];
            new_body_.position[1] = in[j + 3];
            new_body_.velocity[0] = in[j + 4];
            new_body_.velocity[1] = in[j + 5];
            new_body_.acceleration[0] = in[j + 6];
            new_body_.acceleration[1] = in[j + 7];
            sys_hw[j] = new_body_;
        }
    }

    /* software */
    sw_tbp(sys_sw);
    std::cout<<"software kernel complete\n"<<std::endl;
    for(int j = 0; j < NUM_BODIES; j++){
        int i = 8 * j;
        out_sw[i] = sys_sw[j].id;
        out_sw[i + 1] = sys_sw[j].mass;
        out_sw[i + 2] = sys_sw[j].position[0];
        out_sw[i + 3] = sys_sw[j].position[1];
        out_sw[i + 4] = sys_sw[j].velocity[0];
        out_sw[i + 5] = sys_sw[j].velocity[1];
        out_sw[i + 6] = sys_sw[j].acceleration[0];
        out_sw[i + 7] = sys_sw[j].acceleration[1];
    }

    /* hardware */
    tbp<DataType>(sys_hw);
    std::cout<<"hardware kernel complete\n"<<std::endl;
    for(int j = 0; j < NUM_BODIES; j++){
        int i = 8 * j;
        out_hw[i] = sys_hw[j].id;
        out_hw[i + 1] = sys_hw[j].mass;
        out_hw[i + 2] = sys_hw[j].position[0];
        out_hw[i + 3] = sys_hw[j].position[1];
        out_hw[i + 4] = sys_hw[j].velocity[0];
        out_hw[i + 5] = sys_hw[j].velocity[1];
        out_hw[i + 6] = sys_hw[j].acceleration[0];
        out_hw[i + 7] = sys_hw[j].acceleration[1];
    }

    /* comparison */
    err = 1;
    std::cout << "signal out:" << std::endl;
    for(i = 0; i < N; i++){
        if(out_sw[i] != out_hw[i]){
            err = 0;
        }
        std::cout << out_hw[i] << " ";
    }
    std::cout<<std::endl;

    if (err == 1) {
        printf("Test successful!\r\n");
        return 0;
    }
    printf("Test failed\r\n");
    return 1;
}
