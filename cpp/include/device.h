#ifndef DEVICE_H
#define DEVICE_H

#include "rbdimmerESP32.h"
#define PHASE_NUM 0

class Device {
  protected:
    std::string nickname;

    virtual void print(std::ostream& os) const {
      os << "Nickname: " << nickname << std::endl;
    }

  public:
    virtual bool setup() = 0;
    virtual bool setState(const bool newState) const {return false;}
    virtual bool setLevel(const uint8_t level) const {return false;} //runtime polymorphism is not possible due to RTTI disabled on esp32 to save flash
    virtual uint8_t getLevel() const {return 0;}
    virtual ~Device() = default;

    void setNickname(const std::string& newNickname) {nickname = newNickname;}
    std::string getNickname() const {return nickname;}

    friend std::ostream& operator<<(std::ostream& os, const Device& device) {
      device.print(os);
      return os;
    }
};

class Toggleable final : public Device {
  private:
    uint8_t togglePin;

    void print(std::ostream& os) const override {
      Device::print(os);
      os << "Toggle Pin: " << static_cast<int>(togglePin) << std::endl;
      os << "State: " << std::boolalpha << getState() << std::endl;
    }

  public:
    Toggleable(const uint8_t tPin) {
      togglePin = tPin;
      nickname = "";
    }

    Toggleable(const uint8_t tPin, const std::string& nick) {
      togglePin = tPin;
      nickname = nick;
    }

    bool setup() override{
      enablePinAsOutput(togglePin);
      return true;
    }

    bool setState(const bool newState) const override {
      digitalWrite(togglePin, newState);
      return true;
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

  void print(std::ostream& os) const override {
    Device::print(os);
    os << "Zero Cross Pin: " << static_cast<int>(zeroCrossPin) << std::endl;
    os << "Dimmer Pin: " << static_cast<int>(dimmerPin) << std::endl;
    os << "Level: " << static_cast<int>(getLevel()) << std::endl;
  }

  public:
    Dimmable(const uint8_t zcPin, const uint8_t dPin) {
      zeroCrossPin = zcPin;
      dimmerPin = dPin;
      nickname = "";
    }

    Dimmable(const uint8_t zcPin, const uint8_t dPin, const std::string& nick) {
      zeroCrossPin = zcPin;
      dimmerPin = dPin;
      nickname = nick;
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

    bool setState(const bool newState) const override {
        return rbdimmer_set_level(dimmer, newState ? 100 : 0) != RBDIMMER_OK;
      }

    bool setLevel(const uint8_t level) const override {
      if (level < 0 || level > 100)
        return false;

      if (rbdimmer_set_level(dimmer, level) != RBDIMMER_OK)
        return false;

      return true;
    }

    uint8_t getLevel() const override {
      return rbdimmer_get_level(dimmer);
    }
};

#endif //DEVICE_H
