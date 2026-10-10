#ifndef GPIO_H
#define GPIO_H

//Lower GPIO Bank
#define GPIO_OUT0          (*(volatile uint32_t *)0x3FF44004) //For reading GPIO state
#define GPIO_OUT0_W1TS     (*(volatile uint32_t *)0x3FF44008) //Write 1 to set gpio pin
#define GPIO_OUT0_W1TC     (*(volatile uint32_t *)0x3FF4400C) //Write 1 to clear gpio pin

#define GPIO_ENABLE0_W1TS  (*(volatile uint32_t*)0x3FF44024)
#define GPIO_ENABLE0_W1TC  (*(volatile uint32_t*)0x3FF44028)


//Upper GPIO Bank
#define GPIO_OUT1          (*(volatile uint32_t *)0x3FF44010)
#define GPIO_OUT1_W1TS     (*(volatile uint32_t *)0x3FF44014)
#define GPIO_OUT1_W1TC     (*(volatile uint32_t *)0x3FF44018)

#define GPIO_ENABLE1_W1TS  (*(volatile uint32_t *)0x3FF4402C)
#define GPIO_ENABLE1_W1TC  (*(volatile uint32_t *)0x3FF44030)

// IO_MUX function selection is bits 12-14
// Bits 12-14 being 010 (function 2) sets a pin to gpio mode
#define IO_MUX_GPIO_BASE 0x3FF49000 //For choosing the functionality of a certain pin
#define IO_MUX_FUNC_SEL_SHIFT 12
#define IO_MUX_FUNC_SEL_MASK  (0x7 << IO_MUX_FUNC_SEL_SHIFT)

//Specific pin definitions
#define BUILTIN_LED 2

/*
 * Converts pin number to address offset of IO_MUX_GPIO_BASE
 *
 * See page 136 of the ESP32 technical reference manual
 * https://documentation.espressif.com/esp32_technical_reference_manual_en.pdf
*/
inline uint32_t getMuxAddressOffset(uint8_t pin) {
    switch (pin) {
        case 2: //GPIO2
            return 0x40;
        case 12: //MTDI
            return 0x34;
        case 13: //MTCK
            return 0x38;
        case 14: //MTMS
            return 0x30;
        case 18: //GPIO18
            return 0x70;
        case 19: //GPIO19
            return 0x74;
        case 32:
            return 0x1C;
        case 33:
            return 0x20;
        default:
            return 0x00;
    }
}

//Mark a pin as a gpio out
inline void enablePinAsOutput(const uint8_t pin) {
    // Select GPIO function (Function 2)
    volatile uint32_t *currentPinMux = (volatile uint32_t *) (IO_MUX_GPIO_BASE + getMuxAddressOffset(pin));
    *currentPinMux = (*currentPinMux & ~IO_MUX_FUNC_SEL_MASK) | (2 << IO_MUX_FUNC_SEL_SHIFT);

    // Enable GPIO13's output driver
    if (pin < 32)
        GPIO_ENABLE0_W1TS = (1U << pin);
    else
        GPIO_ENABLE1_W1TS = (1U << (pin - 32));
}

//Read the value of a pin's state
//Assumes a pin is setup as an output
inline bool readPinValue(const uint8_t pin) {
    if (pin < 32)
        return GPIO_OUT0 & (1U << pin);

    return GPIO_OUT1 & (1U << (pin - 32));
}

//Set a pin to be on or off
inline void digitalWrite(const uint8_t pin, const bool value)
{
    if (pin < 32) {
        if (value)
            GPIO_OUT0_W1TS = (1U << pin);
        else
            GPIO_OUT0_W1TC = (1U << pin);
    } else {
        if (value)
            GPIO_OUT1_W1TS = (1U << (pin - 32));
        else
            GPIO_OUT1_W1TC = (1U << (pin - 32));
    }
}

//Toggle a pin and return it's current state
inline int togglePin(const uint8_t pin) {
    bool previousState  = readPinValue(pin);

    if (previousState)
        digitalWrite(pin, false); //set LOW
    else
        digitalWrite(pin, true); //set HIGH

    return !previousState; //returns current state
}


#endif //GPIO_H
