<picture>
  <source media="(max-width: 900px) and (prefers-reduced-motion: reduce) and (prefers-color-scheme: dark)" srcset="assets/brand/hero-mobile-static-dark.svg">
  <source media="(max-width: 900px) and (prefers-reduced-motion: reduce) and (prefers-color-scheme: light)" srcset="assets/brand/hero-mobile-static-light.svg">
  <source media="(max-width: 900px) and (prefers-color-scheme: dark)" srcset="assets/brand/hero-mobile-dark.svg">
  <source media="(max-width: 900px) and (prefers-color-scheme: light)" srcset="assets/brand/hero-mobile-light.svg">
  <source media="(prefers-reduced-motion: reduce) and (prefers-color-scheme: dark)" srcset="assets/brand/hero-static.svg">
  <source media="(prefers-reduced-motion: reduce) and (prefers-color-scheme: light)" srcset="assets/brand/hero-static-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/brand/hero-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/brand/hero-light.svg">
  <img src="assets/brand/hero-static.svg" alt="Elias Cheng — embedded software engineer; testable cores and hardware-aware design" width="100%">
</picture>

Open a project to inspect its implementation, host tests and target limits.

## Selected engineering

### [Python Host Application](https://github.com/REliasCheng/Python-Host-Application-Lab)

<picture>
  <source media="(max-width: 900px) and (prefers-color-scheme: dark)" srcset="assets/cards/featured-python-mobile-dark.svg">
  <source media="(max-width: 900px) and (prefers-color-scheme: light)" srcset="assets/cards/featured-python-mobile-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/evidence/python-host-mock-gui-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="assets/evidence/python-host-mock-gui-light.png">
  <img src="assets/evidence/python-host-mock-gui-dark.png" alt="Real Qt window with MOCK0 connected, showing a status command and MOCK ACK response" width="100%">
</picture>

This real Qt window uses an in-memory serial backend, not a connected device. The serial interface keeps connection and error paths testable without hardware; real-device communication is unverified.

**[View repository →](https://github.com/REliasCheng/Python-Host-Application-Lab)**

[Source](https://github.com/REliasCheng/Python-Host-Application-Lab/blob/main/src/host_app/core/application.py) · [Tests](https://github.com/REliasCheng/Python-Host-Application-Lab/blob/main/tests/test_gui.py) · [CI](https://github.com/REliasCheng/Python-Host-Application-Lab/actions/workflows/test.yml) · [Design](https://github.com/REliasCheng/Python-Host-Application-Lab/blob/main/docs/system-architecture.md)

### [Embedded C/C++ Core](https://github.com/REliasCheng/Embedded-C-Cpp-Learning)

<picture>
  <source media="(max-width: 900px) and (prefers-color-scheme: dark)" srcset="assets/cards/featured-embedded-cpp-mobile-dark.svg">
  <source media="(max-width: 900px) and (prefers-color-scheme: light)" srcset="assets/cards/featured-embedded-cpp-mobile-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/cards/featured-embedded-cpp-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/cards/featured-embedded-cpp-light.svg">
  <img src="assets/cards/featured-embedded-cpp-dark.svg" alt="Host test: undersized command reply leaves the LED state unchanged" width="100%">
</picture>

The handler prepares a response before mutating device state; a valid retry can commit after a short-buffer failure. Command, ring-buffer and task modules have host tests, without an MCU target build.

**[View repository →](https://github.com/REliasCheng/Embedded-C-Cpp-Learning)**

[Source](https://github.com/REliasCheng/Embedded-C-Cpp-Learning/blob/main/projects/06_%E7%BB%BC%E5%90%88%E8%BD%AF%E4%BB%B6%E5%AE%9E%E8%B7%B5/%E5%B5%8C%E5%85%A5%E5%BC%8F%E5%91%BD%E4%BB%A4%E5%A4%84%E7%90%86%E6%A1%86%E6%9E%B6/practice/src/command.c) · [Tests](https://github.com/REliasCheng/Embedded-C-Cpp-Learning/blob/main/projects/06_%E7%BB%BC%E5%90%88%E8%BD%AF%E4%BB%B6%E5%AE%9E%E8%B7%B5/%E5%B5%8C%E5%85%A5%E5%BC%8F%E5%91%BD%E4%BB%A4%E5%A4%84%E7%90%86%E6%A1%86%E6%9E%B6/tests/test_command_framework.c) · [CI](https://github.com/REliasCheng/Embedded-C-Cpp-Learning/actions/workflows/host-tests.yml) · [Design](https://github.com/REliasCheng/Embedded-C-Cpp-Learning/blob/main/docs/%E5%B7%A5%E7%A8%8B%E7%BB%93%E6%9E%84%E8%AE%BE%E8%AE%A1.md)

### [C51 Board Resource Planner](https://github.com/REliasCheng/C51-Board-Lab)

<picture>
  <source media="(max-width: 900px) and (prefers-color-scheme: dark)" srcset="assets/cards/featured-c51-mobile-dark.svg">
  <source media="(max-width: 900px) and (prefers-color-scheme: light)" srcset="assets/cards/featured-c51-mobile-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/cards/featured-c51-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/cards/featured-c51-light.svg">
  <img src="assets/cards/featured-c51-dark.svg" alt="Host test: UART and independent keys share P3.0 and P3.1, so the planner reports a conflict" width="100%">
</picture>

The planner compares declared module resource masks and preserves the existing plan on conflict. GPIO, Timer, UART and I²C mapping and failure paths are host-tested; board wiring and runtime remain unverified.

**[View repository →](https://github.com/REliasCheng/C51-Board-Lab)**

[Source](https://github.com/REliasCheng/C51-Board-Lab/blob/main/projects/06_%E7%BB%BC%E5%90%88%E5%BA%94%E7%94%A8/board-resource-planner/practice/src/board_resources.c) · [Tests](https://github.com/REliasCheng/C51-Board-Lab/blob/main/projects/06_%E7%BB%BC%E5%90%88%E5%BA%94%E7%94%A8/board-resource-planner/tests/test_board_resources.c) · [CI](https://github.com/REliasCheng/C51-Board-Lab/actions/workflows/host-tests.yml) · [Design](https://github.com/REliasCheng/C51-Board-Lab/blob/main/projects/06_%E7%BB%BC%E5%90%88%E5%BA%94%E7%94%A8/board-resource-planner/README.md)

## Verified software engineering

Commit-bound snapshot checked on **2026-10-27**. The linked CI runs passed for the listed projects' audited `main` commits; they are historical evidence, not live status or hardware validation. [Full evidence index](data/engineering-evidence.json).

- **[Firmware Update / OTA](https://github.com/REliasCheng/Embedded-OTA-Update-Lab)** — Portable C update flow with staging, simulated Flash, CRC and journal recovery. Host simulation only; no device update, signatures or A/B rollback. [Source](https://github.com/REliasCheng/Embedded-OTA-Update-Lab/blob/main/src/ota_update.c) · [Tests](https://github.com/REliasCheng/Embedded-OTA-Update-Lab/blob/main/tests/test_ota_update.c) · [Main CI](https://github.com/REliasCheng/Embedded-OTA-Update-Lab/actions/runs/40311425747)
- **[ARM Cortex-M Control](https://github.com/REliasCheng/ARM-Cortex-M-Development-Lab)** — C11 timer-event, sampling and hysteresis core with host compiler and sanitizer tests. No Cortex-M target build or hardware interrupt timing. [Source](https://github.com/REliasCheng/ARM-Cortex-M-Development-Lab/blob/main/src/control_app.c) · [Tests](https://github.com/REliasCheng/ARM-Cortex-M-Development-Lab/blob/main/tests/test_control_app.c) · [Main CI](https://github.com/REliasCheng/ARM-Cortex-M-Development-Lab/actions/runs/40318386452)
- **[FreeRTOS Host Runtime](https://github.com/REliasCheng/FreeRTOS-Embedded-Lab)** — Official FreeRTOS V11.3.2 runs a three-task pipeline on a Host Port. No Cortex-M scheduling or physical ISR evidence. [Source](https://github.com/REliasCheng/FreeRTOS-Embedded-Lab/blob/main/app/rtos_demo.c) · [Tests](https://github.com/REliasCheng/FreeRTOS-Embedded-Lab/blob/main/tests/test_processing.c) · [Main CI](https://github.com/REliasCheng/FreeRTOS-Embedded-Lab/actions/runs/40321931576)
- **[LVGL Host Dashboard](https://github.com/REliasCheng/LVGL-Embedded-GUI-Lab)** — Real LVGL v9.6.0 widgets, SDL2 window and headless framebuffer tests. No MCU display, touch or FreeRTOS target integration. [Source](https://github.com/REliasCheng/LVGL-Embedded-GUI-Lab/blob/main/app/dashboard_ui.c) · [Tests](https://github.com/REliasCheng/LVGL-Embedded-GUI-Lab/blob/main/tests/dashboard_headless.c) · [Main CI](https://github.com/REliasCheng/LVGL-Embedded-GUI-Lab/actions/runs/40327059878)
- **[Wireless / IoT MQTT](https://github.com/REliasCheng/Wireless-IoT-Embedded-Lab)** — C11 client and loopback Mosquitto Broker exercise telemetry, QoS 1 and reconnect. No device Wi-Fi, Aliyun or TLS run. [Source](https://github.com/REliasCheng/Wireless-IoT-Embedded-Lab/blob/main/app/host_mqtt_device.c) · [Tests](https://github.com/REliasCheng/Wireless-IoT-Embedded-Lab/blob/main/tests/mqtt_integration.py) · [Main CI](https://github.com/REliasCheng/Wireless-IoT-Embedded-Lab/actions/runs/40438227834)
- **[ARM Embedded Linux](https://github.com/REliasCheng/ARM-Linux-Embedded-Lab)** — Real Linux PTY I/O, AArch64 userspace cross build and QEMU execution; x86_64 module built without loading. No RK3566 boot or Device Tree validation. [Source](https://github.com/REliasCheng/ARM-Linux-Embedded-Lab/blob/main/src/linux_device_port.c) · [Tests](https://github.com/REliasCheng/ARM-Linux-Embedded-Lab/blob/main/tests/pty_integration.py) · [Main CI](https://github.com/REliasCheng/ARM-Linux-Embedded-Lab/actions/runs/40444152160)
- **[Offline Robotics Control](https://github.com/REliasCheng/Embodied-Robotics-Arm-Lab)** — Synthetic leader–follower controller parses SO-100 YAML, maps six channels and tests Fake Bus fault latching and replay. No third-party LeRobot runtime, motor motion or physical E-stop evidence. [Source](https://github.com/REliasCheng/Embodied-Robotics-Arm-Lab/blob/main/offline_control/controller.py) · [Tests](https://github.com/REliasCheng/Embodied-Robotics-Arm-Lab/blob/main/tests_offline/test_control.py) · [Main CI](https://github.com/REliasCheng/Embodied-Robotics-Arm-Lab/actions/runs/40472442405)

## MCU development

- [STC8 MCU Learning](https://github.com/REliasCheng/STC8-MCU-Learning) — C89 UART RX ring buffer and 8051 adapter; host-tested core, no Keil target or board evidence.
- [STC89C52 Learning](https://github.com/REliasCheng/stc89c52-learning) — RTC, temperature and configuration state behind platform callbacks; host tests, no C51 target or hardware verification.
- [BlueBridgeCup MCU](https://github.com/REliasCheng/BlueBridgeCup-MCU) — CT107D resource, timing and control policies; host tests, no complete target or board validation.

## Foundations

- [Embedded Systems Foundations](https://github.com/REliasCheng/Embedded-Systems-Foundations) — electronics, logic, CPU, MCU and PCB knowledge map; documentation, not runnable firmware.

## Public engineering evidence

<details>
<summary>View dated public metrics and five selected host CI checks</summary>

Statuses are matched to each repository's `main` SHA at the displayed refresh time. `PASS` means host CI only, never target or hardware validation; API failures remain `UNAVAILABLE`.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/REliasCheng/REliasCheng/signalcore-assets/telemetry-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/REliasCheng/REliasCheng/signalcore-assets/telemetry-light.svg">
  <img src="assets/fallback/telemetry-dark.svg" alt="Public GitHub telemetry with dated repository and current-main host CI status" width="100%">
</picture>

[Open full-size dark metrics](https://raw.githubusercontent.com/REliasCheng/REliasCheng/signalcore-assets/telemetry-dark.svg) · [Open full-size light metrics](https://raw.githubusercontent.com/REliasCheng/REliasCheng/signalcore-assets/telemetry-light.svg)

</details>

---

**SIGNALCORE** · [About this portfolio](docs/maintenance.md)

Original profile content follows this repository's [LICENSE](LICENSE). Linked projects, vendor material and dependencies retain their own terms.
