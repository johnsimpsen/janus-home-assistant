#ifndef JANUS_LEDFUNCTIONS_H
#define JANUS_LEDFUNCTIONS_H

#include <Arduino.h>
#include "gpio.h"

inline int togglePin(uint8_t pin) {
    bool previousState  = GPIO_OUT & (1 << pin);

    if (previousState)
        GPIO_OUT_W1TC |= (1 << pin); //set LOW
    else
        GPIO_OUT_W1TS |= (1 << pin); //set HIGH

    return !previousState; //returns current state
}

#endif //JANUS_LEDFUNCTIONS_H