<p align="center">
  <img src="./assets/images/embedded-systems-hero.svg" alt="Embedded Systems — Hardware, Firmware, Low-level Software" width="100%">
</p>

# Elias Cheng

**Embedded Systems Developer** — MCU firmware, hardware integration, embedded software architecture, and robotics system integration.

## Featured Architecture Labs

These labs highlight system architecture and implementation paths across RTOS, GUI, wireless connectivity, firmware update workflows, and robotic arm integration. Their individual READMEs state the current build, hardware, and runtime evidence boundaries.

| Project | Architecture Focus | Evidence Boundary |
| --- | --- | --- |
| 🔄 [Embedded OTA Update](https://github.com/REliasCheng/Embedded-OTA-Update-Lab) | Bootloader, UART/YMODEM, MQTT transport, Flash layout, CRC | Architecture and source paths documented; build and hardware evidence not provided |
| 🧵 [FreeRTOS Embedded Lab](https://github.com/REliasCheng/FreeRTOS-Embedded-Lab) | Scheduling, IPC, synchronization, ISR-to-task design | Architecture and source paths documented; performance guarantees are not claimed |
| 📡 [Wireless & IoT](https://github.com/REliasCheng/Wireless-IoT-Embedded-Lab) | Native Wi-Fi, lwIP, TCP, MQTT, device integration | Plain TCP 1883 path; TLS and sensor evidence are not claimed |
| 🖥️ [LVGL Embedded GUI](https://github.com/REliasCheng/LVGL-Embedded-GUI-Lab) | Display, input, rendering, events, BSP integration | Interface paths documented; successful rendering and hardware evidence not provided |
| 🦾 [Embodied Robotics Arm](https://github.com/REliasCheng/Embodied-Robotics-Arm-Lab) | Leader–follower control, serial motor interfaces, camera input, LeRobot workflow | Source/configuration and syntax validation available; host functional test, build, hardware, and runtime evidence not provided |

## Current Work

### 💻 [Embedded C/C++](https://github.com/REliasCheng/Embedded-C-Cpp-Learning)

C/C++ software structure with host-tested command processing, task state management, and modular firmware components.

### 🔌 [BlueBridgeCup MCU](https://github.com/REliasCheng/BlueBridgeCup-MCU)

CT107D / 8051 peripheral integration focused on shared resources, timing, communication, and host-tested control policies.

### 🧩 [C51 Board Resource Planner](https://github.com/REliasCheng/C51-Board-Lab)

An 8051 board resource planning tool for mapping peripherals and detecting GPIO, timer, and communication conflicts through host-tested cases.

### 🧠 [STC89C52 Application Architecture](https://github.com/REliasCheng/stc89c52-learning)

STC89C52RC application architecture with a portable core, state-machine control, persistent configuration, and host-tested logic.

### 📐 [Embedded Systems Foundations](https://github.com/REliasCheng/Embedded-Systems-Foundations)

Documentation connecting electronics, digital logic, CPU architecture, PCB workflow, and MCU interface concepts.

## What I Build

- **Embedded C/C++** — Portable application cores, state machines, callback-based modules, and host-tested software boundaries.
- **MCU Firmware** — Peripheral integration, timing, communication, and device control with hardware-aware constraints.
- **Hardware Integration** — Board resource mapping, shared interfaces, and firmware-to-hardware boundaries.

## Technology Path

### Current Evidence

```text
Foundation
├── Electronics / Digital Logic
└── C/C++ / Modular Software / Host Test

MCU Systems
└── 8051 / STC89
```

### Roadmap

```text
MCU Systems
├── STC8
└── ARM Cortex-M

Embedded Software
└── FreeRTOS / Scheduling / IPC / ISR-to-task

Application and System Integration
├── LVGL / Embedded GUI
├── Wireless / IoT
├── Bootloader / OTA
└── Robotics / Robotic Arm Integration

Embedded Linux
└── Boot Flow / Device Tree / Driver Interfaces / Userspace
```

## Technical Roadmap

These repositories track planned learning work and are not presented as completed projects.

- [STC8 MCU](https://github.com/REliasCheng/STC8-MCU-Learning) — enhanced 8051 peripherals and system integration
- [ARM Cortex-M](https://github.com/REliasCheng/ARM-Cortex-M-Development-Lab) — firmware foundations and peripheral drivers
- [FreeRTOS](https://github.com/REliasCheng/FreeRTOS-Embedded-Lab) — scheduling, synchronization, IPC, and ISR-to-task design
- [LVGL / Embedded GUI](https://github.com/REliasCheng/LVGL-Embedded-GUI-Lab) — display, input, and embedded GUI integration
- [Wireless / IoT](https://github.com/REliasCheng/Wireless-IoT-Embedded-Lab) — TCP/IP, MQTT, and device connectivity
- [Bootloader / OTA](https://github.com/REliasCheng/Embedded-OTA-Update-Lab) — firmware update architecture and image lifecycle

## Currently Exploring

### 🐧 [ARM Embedded Linux](https://github.com/REliasCheng/ARM-Linux-Embedded-Lab)

Architecture and source-review lab for the RK3566 ARM64 boot flow, Device Tree, driver interfaces, and userspace boundaries; build, QEMU, hardware, and runtime evidence are not provided.

### 🖥️ [Python Host Application](https://github.com/REliasCheng/Python-Host-Application-Lab)

Documentation and architecture lab for a PyQt5 serial host application, including GUI, application logic, communication flow, and verification boundaries; public runtime and device evidence are not provided.
