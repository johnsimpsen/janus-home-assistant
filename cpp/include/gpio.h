#ifndef ESP32_TEST_GPIO_H
#define ESP32_TEST_GPIO_H

//Pin memory addresses
#define GPIO_OUT          (*(volatile uint32_t *)0x3FF44004) //For reading GPIO state
#define GPIO_OUT_W1TS     (*(volatile uint32_t *)0x3FF44008) //Write 1 to set gpio pin
#define GPIO_OUT_W1TC     (*(volatile uint32_t *)0x3FF4400C) //Write 1 to clear gpio pin

#define GPIO_ENABLE_W1TS  (*(volatile uint32_t *)0x3FF44024)
//#define GPIO_ENABLE (*(volatile uint32_t *)0x3ff44020)

//Specific pin definitions
#define BUILTIN_LED_PIN 2

#endif //ESP32_TEST_GPIO_H
