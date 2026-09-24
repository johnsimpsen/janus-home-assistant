#include "wireless.h"
#include "environment.h"
#include "gpio.h"
#include "device_manager.h"
#include "device.h"

WebServer server(80);

void setup() {
    Serial.begin(115200);

    enablePinAsOutput(BUILTIN_LED);
    enablePinAsOutput(12);
    enablePinAsOutput(13);
    enablePinAsOutput(14);

    NetworkCredentials credentials;

    //Get Network Credentials
    bool hasNetworkCredentials = readNetworkCredentials(credentials);
    if (!hasNetworkCredentials) return;

    //Connect to Wi-Fi
    bool wifiConnected = connectToWifi(credentials.WIFI_SSID, credentials.WIFI_PASSWORD);
    if (!wifiConnected) return;

    startServer();

    Device* dimmer1 = new Dimmable(32, 33);
    dimmer1->setup();
}


void loop() {
    server.handleClient();
}