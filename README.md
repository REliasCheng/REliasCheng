# Embedded Systems

Anonymous embedded systems learner focusing on hardware foundations, C/C++, MCU development and embedded software. 这里按技术能力组织已经完成的工程与实践记录，从电子电路和数字逻辑延伸到 C/C++、8051 外设和竞赛综合程序。

## 技术方向

| 已有实践 | 对应内容 |
| --- | --- |
| C / C++ | 指针与内存、结构体、模块接口、回调、状态机、类与对象 |
| 8051 / STC MCU | GPIO、Timer、中断、UART、I²C、1-Wire、RTC与显示驱动 |
| 数字逻辑与计算机组成 | 逻辑门、加法器、ALU、寄存器、内存和简化CPU数据通路 |
| 嵌入式软件设计 | 固定缓冲区、命令分发、周期任务、多外设状态与资源安排 |
| 硬件基础 | 电路仿真、原理图分析、BOM和PCB设计流程 |

下一阶段将沿 **STM32 → FreeRTOS → Embedded Linux** 继续学习；这些方向目前作为路线，不列入已完成能力。

## 项目导航

| 能力层 | 代表仓库 | 可查看的技术证据 |
| --- | --- | --- |
| 硬件与计算机底层 | [Embedded-Systems-Foundations](https://github.com/REliasCheng/Embedded-Systems-Foundations) | CircuitJS、Digital、简化 CPU、原理图与 BOM |
| 嵌入式软件基础 | [Embedded-C-Cpp-Learning](https://github.com/REliasCheng/Embedded-C-Cpp-Learning) | 内存、模块接口、命令解析、状态机和主机测试 |
| MCU 与外设驱动 | [stc89c52-learning](https://github.com/REliasCheng/stc89c52-learning) | C51 工程、板级接口、传感器与多外设应用 |
| 综合工程训练 | [BlueBridgeCup-MCU](https://github.com/REliasCheng/BlueBridgeCup-MCU) | CT107D 资源分配、驱动修正和竞赛程序结构 |

## 技术成长路线

```text
Electronic & Digital Foundations
              ↓
       C/C++ Programming
              ↓
    MCU & Peripheral Drivers
              ↓
 Embedded Competition Projects
              ↓
    STM32 / RTOS / Linux
```

## Featured Projects

### [Embedded-Systems-Foundations](https://github.com/REliasCheng/Embedded-Systems-Foundations)

从电子电路、数字逻辑和加法器出发，连接到寄存器、内存、简化CPU、原理图与硬件控制实践。

### [Embedded-C-Cpp-Learning](https://github.com/REliasCheng/Embedded-C-Cpp-Learning)

C/C++、内存管理、模块接口、回调和状态机实践，并包含命令处理框架与轻量任务状态管理两个综合软件项目。

### [stc89c52-learning](https://github.com/REliasCheng/stc89c52-learning)

STC89C52RC的GPIO、显示、按键、定时器、UART、I²C和传感器驱动，以及多外设环境与时钟信息终端。

### [BlueBridgeCup-MCU](https://github.com/REliasCheng/BlueBridgeCup-MCU)

基于CT107D与STC15/IAP15的外设驱动、资源调度、参数保存、多页面控制和蓝桥杯单片机综合训练。

## Representative Work

- [简化CPU自动运行模型](https://github.com/REliasCheng/Embedded-Systems-Foundations/tree/main/projects/03_%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BB%84%E6%88%90%E4%B8%8ECPU)：8位数据通路、4位地址空间、控制字与取指—解码—执行过程。
- [嵌入式命令处理框架](https://github.com/REliasCheng/Embedded-C-Cpp-Learning/tree/main/projects/06_%E7%BB%BC%E5%90%88%E8%BD%AF%E4%BB%B6%E5%AE%9E%E8%B7%B5/%E5%B5%8C%E5%85%A5%E5%BC%8F%E5%91%BD%E4%BB%A4%E5%A4%84%E7%90%86%E6%A1%86%E6%9E%B6)：环形缓冲区、逐字节组帧、命令表、回调和错误返回。
- [STC89C52环境与时钟信息终端](https://github.com/REliasCheng/stc89c52-learning/tree/main/projects/13_%E7%8E%AF%E5%A2%83%E4%B8%8E%E6%97%B6%E9%92%9F%E4%BF%A1%E6%81%AF%E7%BB%88%E7%AB%AF)：RTC、温度、OLED、按键和EEPROM的应用状态与数据流。
- [省赛综合控制训练](https://github.com/REliasCheng/BlueBridgeCup-MCU/tree/main/competition/province/integrated-control)：ADC、温度、按键、显示和输出任务协同。
- [LED模式综合训练](https://github.com/REliasCheng/BlueBridgeCup-MCU/tree/main/competition/national/led-mode-training)：EEPROM参数、ADC亮度、软件PWM、RTC、UART与多模式状态调度。

## Current Focus

- 继续给现有项目补充真实板端照片、串口输出、波形与复测记录。
- 将主机端验证过的缓冲区、状态机和任务接口迁移到MCU项目。
- 进入STM32基础外设与工程环境，再逐步学习FreeRTOS和Embedded Linux。
