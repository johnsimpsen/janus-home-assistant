#ifndef ENVIRONMENT_H
#define ENVIRONMENT_H

#include <LittleFS.h>

struct NetworkCredentials {
    String WIFI_SSID;
    String WIFI_PASSWORD;
};

//Read Network Credentials from .env using LittleFS
inline bool readNetworkCredentials(NetworkCredentials& credentials) {
    if (!LittleFS.begin(true)) {
        Serial.println("LittleFS failed");
        return false;
    }

    File file = LittleFS.open("/.env", "r");

    if (!file) {
        Serial.println("Failed to open .env");
        return false;
    }

    //Parse file
    while (file.available()) {
        String line = file.readStringUntil('\n');
        line.trim();

        if (line.startsWith("WIFI_SSID=")) {
            credentials.WIFI_SSID = line.substring(10);
        }
        else if (line.startsWith("WIFI_PASSWORD=")) {
            credentials.WIFI_PASSWORD = line.substring(14);
        }
    }

    file.close();

    return true;
}

#endif //ENVIRONMENT_H
