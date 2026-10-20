# Zombieproof Computers: How to Keep a Mind When the Grid Is Gone

Chapter 9: Networking Your Zombieproof Computer

You’ve built a rugged digital fortress—CPU, memory, and peripherals all working in harmony. But in the zombie apocalypse, even the strongest lone survivor benefits from allies, intel networks, and coordinated defense. Networking connects your machines into a resilient tribe, sharing the battle-worn load.

This chapter gives you the science-backed, deep dive into adding networking capabilities. It covers fundamental concepts, practical wiring, protocols, and a survival-ready example of linking multiple zombieproof machines.

Why Network?
Networking lets multiple computers:

Share data and resources, increasing efficiency

Collaborate on tough tasks beyond one CPU’s strength

Exchange real-time info, warnings, and coordinated commands

Form the backbone of rebuilding post-apocalyptic infrastructure

The Physical Layer — Networking Hardware
Wired Connections
Simple serial cables between machines

Ethernet-style twisted pairs (complex but powerful)

USB or similarly structured digital buses

Wireless Options
Radio signals like Wi-Fi or Bluetooth (power-heavy, intricate protocols)

Network Interfaces — Your Machine's Network ID Card
Each device needs a network interface:

Converts internal data to signals for the physical medium

Receives signals, converts back to data

Manages collisions, timing, and error detection

In DIY setups, UART or SPI modules often act as simple interfaces.

Data and Packets: The Language of Networked Machines
Networks communicate by breaking data into packets—discrete units framed with:

Headers: Destination and source addresses, control info

Payload: Actual data content

Error Detection: Checksums or CRCs for detecting corruption

Protocols — Communication Rules
Just like survivors agree on signals (lights, sounds), machines agree on protocols for talking:

Simple serial protocols: RS-232, UART—easy for small-scale connections

TCP/IP: Complex internet backbone protocol

Custom lightweight protocols: Designed for specific machine-to-machine communication

Your zombieproof rigs will likely start with simple serial links expanding to more complex protocols as needed.

Example: Point-to-Point Serial Network
Wiring two zombieproof machines with serial TX/RX lines:

Use UART communication, with matching baud rates and framing

Simple flow control to avoid data loss (wait for ACKs or use buffers)

Software on both ends handles packet formation and interpretation

Survival Project: Building Your Network Interface
Materials:

UART modules or build UART logic from gates

RS-232 level shifters or transistor circuits for signal integrity

Cables and connectors

Basic logic analyzer or LED indicators for debugging

Steps:

Wire serial TX of one CPU to RX of another; cross-connect lines.

Implement baud rate generators for timing the bits.

Develop software to encode messages, add checksums.

Write software to decode and respond to messages.

Debug with LEDs and logic probes; ensure proper data flow.

Networking your zombieproof computer turns isolated survivor devices into a strong, coordinated network. Together, you can outsmart zombies and reboot civilization with real, networked machines communicating reliably over homemade links.
