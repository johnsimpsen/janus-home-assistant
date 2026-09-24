#ifndef DEVICE_H
#define DEVICE_H

#include "rbdimmerESP32.h"
#define PHASE_NUM 0

class Device {
  public:
    virtual bool setup() = 0;
    virtual ~Device() = default;

};

class Toggleable final : public Device {
  private:
    uint8_t togglePin;
    std::string nickname;


  public:
    Toggleable(const uint8_t tPin, const std::string& n) {
      togglePin = tPin;
      nickname = n;
    }

    bool setup() override{
      enablePinAsOutput(togglePin);
      return true;
    }

    void setState(const bool newState) const {
      digitalWrite(togglePin, newState);
    }

    bool getState() const {
      return readPinValue(togglePin);
    }
};

class Dimmable final : public Device {
  private:
    rbdimmer_channel_t* dimmer = nullptr;
    uint8_t zeroCrossPin;
    uint8_t dimmerPin;


  public:
    Dimmable(const uint8_t zcPin, const uint8_t dPin) {
      zeroCrossPin = zcPin;
      dimmerPin = dPin;
    }

    bool setup() override {
      rbdimmer_init();

      // Register the zero-cross detector
      rbdimmer_register_zero_cross(
          zeroCrossPin,
          PHASE_NUM,
          0
      );

      // Configure the dimmer
      rbdimmer_config_t config = {
        .gpio_pin = zeroCrossPin,
        .phase = PHASE_NUM,
        .initial_level = 0,
        .curve_type = RBDIMMER_CURVE_RMS
      };

      if (rbdimmer_create_channel(&config, &dimmer) != RBDIMMER_OK)
        return false;

      return true;
    }

    bool setLevel(const uint8_t level) const {
      if (level < 0 || level > 100)
        return false;

      if (rbdimmer_set_level(dimmer, level) != RBDIMMER_OK)
        return false;

      return true;
    }
};

#endif //DEVICE_H
