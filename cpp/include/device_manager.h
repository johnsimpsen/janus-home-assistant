#ifndef DEVICE_MANAGER_H
#define DEVICE_MANAGER_H

#include "device.h"

class DeviceManager {
    private:
        DeviceManager() = default;
        inline static DeviceManager* instance = nullptr;
        std::unordered_map<uint8_t, Device*> devices = {}; // deviceId : device reference
        uint8_t count = 0;

    public:
        static DeviceManager* getInstance() {
            if (!instance)
                instance = new DeviceManager();

            return instance;
        }

        Device* getDevice(const uint8_t deviceId) const {
            if (!devices.contains(deviceId))
                return nullptr;

            return devices.at(deviceId);
        }

        bool addDevice(Device* device) {
            if (!device)
                return false;

            // Attempt to setup device
            if (!device->setup())
                return false;

            devices.insert({count, device});
            count++;
            return true;
        }

};

#endif //DEVICE_MANAGER_H
