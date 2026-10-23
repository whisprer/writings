# Zombieproof Computers: How to Keep a Mind When the Grid Is Gone

Chapter 7: Peripherals and Serial Communication

The brains inside your zombieproof computer crack problems and spit out solutions, but it doesn’t know a thing about the zombies, your hands, or the world outside unless you give it senses and limbs. Those come via peripherals: keyboards, mice, monitors, speakers—all the gadgets that let you feed data in and get results back out.

This chapter equips you with a down-and-dirty, no-nonsense look at peripherals, their communication protocols, and practical projects like building a working mouse interface from scratch.

The Basics of Peripherals: Input and Output Explained
Input Devices
At their core, input devices convert physical user actions into electrical signals your computer can understand.

Keyboards: Pressing a key sends a scan code to the CPU, often over serial or parallel interfaces.

Mice: Capture motion and button presses, encoding them as digital pulses.

Switches and sensors: Simple inputs that toggle bits ‘on’ or ‘off’.

Output Devices
Output devices translate your computer's digital signals into the physical or graphical world.

LEDs: Simple binary indicators, on and off controlled by bits.

Displays: From simple 7-segment LEDs to complex pixel arrays, they transform data into visuals.

Speakers: Convert digital audio data into sound waves.

Serial Communication: The Lifeline Protocol for Peripherals
Serial data transfer sends information one bit at a time over a wire or pair of wires—a bit like sending Morse code. It is the backbone for many peripherals because it simplifies wiring and is bandwidth-efficient for user input devices.

Key Serial Protocols
UART (Universal Asynchronous Receiver/Transmitter): Asynchronous serial communication used by many simple devices.

SPI (Serial Peripheral Interface): A synchronous protocol for short-distance, fast communication, e.g., sensors.

I2C (Inter-Integrated Circuit): Multiple devices sharing two wires, each with a unique address.

How Serial Communication Works Practically
Data bits are clocked out one by one.

Start and stop bits frame each byte.

Parity bits can check data integrity.

Both devices must agree on baud rate (bits per second).

Building a Zombieproof Mouse — From Parts to Protocol
Here is a practical breakdown:

How a Mouse Works Mechanically
Motion detection: Optical sensors track surface movement, turning it into x/y data increments. Mechanical mice use roller balls with encoders.

Button switches: Simple contacts that close circuits when clicked.

How a Mouse Communicates
Mouse data packets are serially sent to the computer.

Standard protocols like PS/2 or USB structure these packets with defined bytes for movement and button states.

Serial nature allows simple two-wire connections and relatively low hardware complexity.

Building Your Own Mouse
Use optical or mechanical sensors scavenged from old devices.

Implement a simple microcontroller or logic circuit to buffer movement data and button presses.

Encode data packets according to a serial protocol.

Transmit via UART or similar serial line to your homemade CPU.

Practical Survival Project: Serial Mouse Interface
Parts

Optical sensor assembly or rotary encoders

Push-button switches

Logic gates or simple microcontroller for encoding

UART compatible output stage

Breadboard, wiring, power

Steps

Assemble sensors to detect motion increments, convert analog signals to pulses.

Attach buttons as digital switches with debouncing circuits.

Create simple state machine or logic circuit to format and serialize data packets.

Connect to CPU serial input port, verifying data integrity and timing.

Develop CPU-side code or hardware interpreters to translate mouse packets into cursor movements or commands.

Other Important Peripherals: Keyboards and Displays
Keyboards scan key matrices, sending codes serially to the computer; usually use protocols similar to mice.

Displays need framebuffer storage and protocol to update pixels or segments; simple LED arrays can be driven directly by CPU via multiplexers.

Consider how interrupt-driven input can optimize responsiveness.

Bringing peripherals online with serial communication protocols is the key to making your homemade computer a practical, interactive survivor ready for the end times.
