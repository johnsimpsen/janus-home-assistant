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

    //Start Server
    startServer();

    //Setup Device Manager
    DeviceManager* deviceManager = DeviceManager::getInstance();
    deviceManager->addDevice(new Toggleable(12));
    deviceManager->addDevice(new Toggleable(13));
    deviceManager->addDevice(new Toggleable(14));
    deviceManager->addDevice(new Dimmable(32, 33));
    Serial.println(deviceManager->getCount());
}


void loop() {
    server.handleClient();
}


