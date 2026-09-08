#ifndef JANUS_WIFI_H
#define JANUS_WIFI_H

#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include "ledFunctions.h"

#define WIFI_TIMEOUT 20000

extern WebServer server;

void apiLED();

inline bool connectToWifi(const String& ssid, const String& password) {
    Serial.print("Connecting to WiFi");

    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);

    unsigned long startTime = millis();

    //check if wifi is connected for 20 seconds
    while (WiFi.status() != WL_CONNECTED && millis() - startTime < WIFI_TIMEOUT) {
        Serial.print(".");
        delay(500);
    }

    Serial.println("");

    //wifi connection was unsuccessful
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("WiFi connection failed");
        return false;
    }

    //wifi connection was successful
    Serial.println("WiFi connection successful");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());

    return true;
}

inline void startServer() {
    server.on("/pin", HTTP_GET, apiLED);

    server.begin();
    Serial.println("Server started");
}

inline void apiLED() {
    if (!server.hasArg("gpio")) {
        server.send(400, "text/plain", "Missing gpio parameter");
        return;
    }

    int gpio = server.arg("gpio").toInt();

    std::string ledStatus = std::to_string(togglePin(gpio));
    Serial.println("LED API");
    server.send(200, "text/plain", ledStatus.c_str());
}

#endif //JANUS_WIFI_H
