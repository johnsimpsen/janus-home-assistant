#ifndef WIFI_H
#define WIFI_H

#include <WiFi.h>
#include <WebServer.h>
#include "gpio.h"

#define WIFI_TIMEOUT 20000

extern WebServer server;

void toggleLED();
void enableLED();
void disableLED();
void setLevel();

//Connect to the Wi-Fi network
inline bool connectToWifi(const String& ssid, const String& password) {
    Serial.print("Connecting to WiFi");

    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);

    unsigned long startTime = millis();

    //check if Wi-Fi is connected for 20 seconds
    while (WiFi.status() != WL_CONNECTED && millis() - startTime < WIFI_TIMEOUT) {
        Serial.print(".");
        delay(500);
    }

    Serial.println("");

    //Wi-Fi connection was unsuccessful
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("WiFi connection failed");
        return false;
    }

    //Wi-Fi connection was successful
    Serial.println("WiFi connection successful");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());

    return true;
}

//Define all HTTP routes and then start the server
inline void startServer() {
    server.on("/enable", HTTP_GET, enableLED);
    server.on("/disable", HTTP_GET, disableLED);
    server.on("/level", HTTP_GET, setLevel);

    server.begin();

    digitalWrite(BUILTIN_LED, true);
    Serial.println("Server started");
}

#endif //WIFI_H
