#include <Arduino.h>
#include "wireless.h"
#include <environment.h>
#include "gpio.h"

WebServer server(80);

void setup() {
    Serial.begin(115200);

    pinMode(12, OUTPUT);
    pinMode(13, OUTPUT);
    pinMode(14, OUTPUT);
    pinMode(BUILTIN_LED_PIN, OUTPUT);

    NetworkCredentials credentials;

    //Get Network Credentials
    bool hasNetworkCredentials = readNetworkCredentials(credentials);
    if (!hasNetworkCredentials) return;

    //Connect to WiFi
    bool wifiConnected = connectToWifi(credentials.WIFI_SSID, credentials.WIFI_PASSWORD);
    if (!wifiConnected) return;

    //Start Server and define api endpoints
    startServer();
    GPIO_OUT_W1TS |= (1 << BUILTIN_LED_PIN);
}


void loop() {
    server.handleClient();
}