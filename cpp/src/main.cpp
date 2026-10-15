#include "wireless.h"
#include "environment.h"
#include "gpio.h"

WebServer server(80);

void setup() {
    Serial.begin(115200);
    enablePinAsOutput(BUILTIN_LED);

    //Get Network Credentials
    NetworkCredentials credentials;
    if (!readNetworkCredentials(credentials))
        return;

    //Connect to Wi-Fi
    if (!connectToWifi(credentials.WIFI_SSID, credentials.WIFI_PASSWORD))
        return;

    //Start Server
    startServer();

}


void loop() {
    server.handleClient();
}


