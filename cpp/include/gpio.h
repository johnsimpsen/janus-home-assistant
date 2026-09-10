#ifndef GPIO_H
#define GPIO_H

//Pin memory addresses
#define GPIO_OUT          (*(volatile uint32_t *)0x3FF44004) //For reading GPIO state
#define GPIO_OUT_W1TS     (*(volatile uint32_t *)0x3FF44008) //Write 1 to set gpio pin
#define GPIO_OUT_W1TC     (*(volatile uint32_t *)0x3FF4400C) //Write 1 to clear gpio pin

#define GPIO_ENABLE_W1TS  (*(volatile uint32_t*)0x3FF44024)
#define GPIO_ENABLE_W1TC  (*(volatile uint32_t*)0x3FF44028)

// IO_MUX function selection is bits 12-14
// Bits 12-14 being 010 (function 2) sets a pin to gpio mode
#define IO_MUX_GPIO_BASE  0x3FF49000 //For choosing the functionality of a certain pin
#define IO_MUX_FUNC_SEL_SHIFT 12
#define IO_MUX_FUNC_SEL_MASK  (0x7 << IO_MUX_FUNC_SEL_SHIFT)

//Specific pin definitions
#define BUILTIN_LED_PIN 2

/*
 * Converts pin number to address offset of IO_MUX_GPIO_BASE
 *
 * See page 136 of the ESP32 technical reference manual
 * https://documentation.espressif.com/esp32_technical_reference_manual_en.pdf
*/
inline uint32_t getMuxAddressOffset(uint8_t pin) {
    switch (pin) {
        case 14: //MTMS
            return 0x30;
        case 12: //MTDI
            return 0x34;
        case 13: //MTCK
            return 0x38;
        case 2: //GPIO2
            return 0x40;
        default:
            return 0x00;
    }
}

inline void enablePinAsOutput(uint8_t pin) {
    // Select GPIO function (Function 2)
    volatile uint32_t *currentPinMux =  (volatile uint32_t *) (IO_MUX_GPIO_BASE + getMuxAddressOffset(pin));
    *currentPinMux = (*currentPinMux & ~IO_MUX_FUNC_SEL_MASK) | (2 << IO_MUX_FUNC_SEL_SHIFT);

    // Enable GPIO13's output driver
    GPIO_ENABLE_W1TS = (1 << pin);
}

inline void myDigitalWrite(uint8_t pin, bool value)
{
    if (value)
        GPIO_OUT_W1TS = (1 << pin);
    else
        GPIO_OUT_W1TC = (1 << pin);
}

#endif //GPIO_H
