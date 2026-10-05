#include <sstream>

#include "wireless.h"
#include "environment.h"
#include "gpio.h"
#include "device_manager.h"
#include "device.h"

WebServer server(80);

void setup() {
    Serial.begin(115200);

    enablePinAsOutput(BUILTIN_LED);

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
    deviceManager->addDevice(new Toggleable(14, "red"));
    deviceManager->addDevice(new Toggleable(32));
    deviceManager->addDevice(new Dimmable(33, 34, "FirstDimmer"));

    std::ostringstream oss;
    oss << *deviceManager;
    Serial.println(oss.str().c_str());
}


void loop() {
    server.handleClient();
}


