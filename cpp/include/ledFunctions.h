#ifndef ESP32_TEST_LEDFUNCTIONS_H
#define ESP32_TEST_LEDFUNCTIONS_H

#include <Arduino.h>
#include "gpio.h"

int togglePin(uint32_t PIN) {
    bool previousState  = GPIO_OUT & (1 << PIN);

    if (previousState)
        GPIO_OUT_W1TC |= (1 << PIN); //set LOW
    else
        GPIO_OUT_W1TS |= (1 << PIN); //set HIGH

    return !previousState; //returns current state
}

#endif //ESP32_TEST_LEDFUNCTIONS_H