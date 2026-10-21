# Zombieproof Computers: How to Keep a Mind When the Grid Is Gone

Chapter 12: Powering Your Zombieproof Computer

In the apocalypse, your machine’s lifeblood is electricity—without it, no CPU, memory, or peripherals come to life. This chapter covers how to design a robust power supply for your zombieproof computer, handling voltage regulation, power stability, and energy sources that keep your digital fortress running no matter the external chaos.

Power Sources — Picking Your Fuel
Batteries: Portable but limited runtime; choose types with good energy density like Li-ion or NiMH.

Solar panels: Sustainable if you can catch the light; requires batteries or capacitors for buffering.

Generators: Mechanical but noisy and fuel-dependent; good for basecamp setups.

Hand-crank or pedal power: Emergency use for short bursts.

Voltage Regulation
CPUs and logic chips require clean, steady voltages (usually 5V, 3.3V, or 1.8V).

Use linear regulators or switch-mode power supplies (buck converters) for efficient steady outputs.

Add capacitors for smoothing to filter out voltage spikes and noise.

Power Distribution and Protection
Design power buses to distribute voltage and ground properly.

Use fuses or resettable polyfuses to prevent damage from shorts.

Implement decoupling capacitors near ICs for local stability.

Managing Power Efficiency
Minimize consumption by using low-power components.

Use sleep/standby modes in firmware to shut down unused parts.

Turn off clock feeds where possible (clock gating).

Survival Project: Building a Reliable Power Supply Unit
Gather batteries, voltage regulators, capacitors, and wiring.

Assemble a circuit converting battery voltage to stable 5V or 3.3V rails.

Add indicator LEDs to show power status.

Test under load with your assembled boards.

Powering your computer with confidence is the foundation for all other zombieproof designs.
