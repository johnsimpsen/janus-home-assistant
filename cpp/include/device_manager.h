#ifndef DEVICE_MANAGER_H
#define DEVICE_MANAGER_H

#include "device.h"
#include <string>

class DeviceManager {
    private:
        DeviceManager() = default;
        inline static DeviceManager* instance = nullptr;
        std::unordered_map<uint8_t, Device*> devices = {}; // deviceId : device reference
        std::unordered_map<std::string, uint8_t> nicknames = {}; // nickname : deviceId
        uint8_t count = 0;

    public:
        int getCount() {
            return count;
        }

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

        Device* getDevice(const std::string& nickname) const {
            if (!nicknames.contains(nickname))
                return nullptr;

            const uint8_t deviceId = nicknames.at(nickname);
            return getDevice(deviceId);
        }


        bool addDevice(Device* device) {
            if (!device)
                return false;

            // Attempt to setup device
            if (!device->setup())
                return false;

            // Check for valid nickname (a valid nickname is at least one character and contains no spaces)
            std::string nickname = device->getNickname();
            if (nickname.empty() || nickname.find(' ') != std::string::npos) {
                device->setNickname("device" + std::to_string(count));
            }

            nicknames.insert({nickname, count});
            devices.insert({count++, device});
            return true;
        }

        friend std::ostream& operator<<(std::ostream& os, const DeviceManager& manager) {
            for (int i = 0; i < manager.count; i++) {
                os << "Device Id: " << i << std::endl;
                os << *manager.devices.at(i) << std::endl;
            }

            return os;
        }

};

#endif //DEVICE_MANAGER_H
