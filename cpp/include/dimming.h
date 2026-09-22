#ifndef DIMMING_H
#define DIMMING_H

#include "rbdimmerESP32.h"

#define ZERO_CROSS_PIN 32
#define DIMMER_PIN 33
#define PHASE_NUM 0

inline rbdimmer_channel_t* dimmer = nullptr;


inline bool setupDimmer() {

    rbdimmer_init();

    // Register the zero-cross detector
    rbdimmer_register_zero_cross(
        ZERO_CROSS_PIN,
        PHASE_NUM,
        0
    );

    // Configure the dimmer
    rbdimmer_config_t config = {
        .gpio_pin = DIMMER_PIN,
        .phase = PHASE_NUM,
        .initial_level = 0,
        .curve_type = RBDIMMER_CURVE_RMS
    };

    rbdimmer_create_channel(&config, &dimmer);

    Serial.println("Dimmer setup");

    return true;


}

inline void setDimmer(int level) {
    rbdimmer_set_level(dimmer, level);
}




#endif //DIMMING_H
