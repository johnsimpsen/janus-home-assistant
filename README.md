\# Janus Home Assistant



\*The AI-powered home assistant that's the beginning of your convenience.\*



\## Description



\*\*Janus\*\* is an AI-powered home assistant designed to make everyday interactions with your home more convenient. Connect multiple devices and control them all from one place using voice commands and natural language.



\## Features



\- Voice-controlled device management through speech recognition.

\- Natural language command interpretation using Llama 3.2.

\- ESP32 integration for controlling connected devices.

\- Zone-based device organization.

\- Device control through enable, disable, set, and additional commands.



\## Technologies Used



\- \*\*Languages:\*\* Python, C, C++

\- \*\*AI / NLP:\*\* Ollama, Llama 3.2

\- \*\*Speech Recognition:\*\* Vosk

\- \*\*Hardware:\*\* ESP32

\- \*\*Communication:\*\* HTTP REST API



\## Future Improvements



\- Expand support for additional smart home devices.

\- Improve speech recognition accuracy and response time.

\- Add support for more natural language commands.

\- Improve device discovery and zone configuration.

\- Expand home automation capabilities.

\- Implement a Raspberry Pi-based Python controller.



\---



\## Third-Party Credits



\### Speech Recognition



Janus uses \[Vosk](https://alphacephei.com/vosk/) and the `vosk-model-small-en-us-0.15` speech recognition model, included in `python/data`.



\- \*\*Copyright:\*\* 2020 Alpha Cephei Inc.

\- \*\*License:\*\* \[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)



\### Large Language Model



This project uses \[Ollama](https://ollama.com/) to run local large language models for natural language processing.



Janus uses \[Llama 3.2](https://www.llama.com/) by \[Meta](https://about.meta.com/), running locally through Ollama, to power its natural language command interpretation.



Llama 3.2 is licensed under the \[Llama 3.2 Community License](https://dev.meta.ai/llama/llama3\_2/license).



> Llama 3.2 is licensed under the Llama 3.2 Community License, Copyright © Meta Platforms, Inc. All Rights Reserved.



\---



\## Command Description



Janus interprets natural language input and translates it into structured commands.



| Command | Parameters | Description |

|---|---|---|

| `enable <zone-number> <device-number>` | `zone-number`: Target zone. `device-number`: Target device. | Enables the specified device in the specified zone. |

| `disable <zone-number> <device-number>` | `zone-number`: Target zone. `device-number`: Target device. | Disables the specified device in the specified zone. |

| `set <zone-number> <device-number> <level>` | `zone-number`: Target zone. `device-number`: Target device. `level`: Desired device level. | Sets the specified device to the desired level. |



\### Additional Notes



\- `zone-number` identifies the target zone.

\- `device-number` identifies the target device within that zone.

\- `level` specifies the desired setting for a device (e.g., brightness) and must be between `0` and `100`.

\- Use `all` in place of `device-number` to target every device in a zone for `enable` and `disable` commands.

\- More commands will be added in the future.

