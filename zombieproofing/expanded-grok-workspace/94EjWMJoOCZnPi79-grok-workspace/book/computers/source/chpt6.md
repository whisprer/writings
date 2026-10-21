# Zombieproof Computers: How to Keep a Mind When the Grid Is Gone

Chapter 6: Memory Integration

Welcome to the most crucial layer of your homemade zombieproof machine: memory. Without memory, your processor is a headless survivor, unable to remember instructions, data, or even which step it’s on. Memory is both the filing cabinet and scratchpad for your digital brain.

This chapter is a deep dive into memory architecture, address decoding, control signals, data buses, and how to hook up your CPU to real memory chips or banks. You’ll learn all the seemingly mystifying details of making memory work seamlessly so your CPU can focus on surviving, computing, and… well, not getting eaten.

Why Memory Integration Matters
Your CPU needs memory for several critical tasks:

Store programs (instructions).

Hold variables and data during operations.

Provide workspace for intermediate calculations.

Without memory, all the logic in the world serves no purpose. The CPU would just stare into empty electrical void.

Memory Types—Basics You Need to Know
RAM (Random Access Memory): Temporary and fast storage, erased when power is off—your prime workspace. Built as arrays of flip-flops or capacitors arranged in grids.

ROM (Read-Only Memory): Permanent storage holding essential firmware or bootstrapping code. Non-volatile, but harder to modify.

Memory-Mapped I/O: Peripherals appear as memory addresses — simplifying CPU access to devices.

Address Spaces and Address Lines
Memory chips are organized in locations accessible by unique addresses. The number of address lines dictates how much memory you can access:

\(N\) address lines give \(2^{N}\) unique addresses.

For example, 8 address lines = 256 addresses; 16 = 65,536.

Your CPU sends address info down the address bus— a set of wires dedicated to carrying address bits.

Decoding Addresses: The Key to Organized Access
With many memory chips and devices, your CPU must ensure only one device answers per address. This calls for decoders or address decoders.

These are logic circuits (made from NAND, NOR gates, or multiplexers) that listen to specific address bits.

When the CPU address matches a chip’s range, the chip decoder outputs an enable signal to activate the chip.

This prevents multiple chips trying to drive the bus at once, which would cause data corruption or electrical damage.

Data Bus and Control Signals — The Communication Layer
The data bus is a multi-wire path carrying actual data to/from memory and CPU.

Control signals include:

Read/Write (R/W): Whether data is being read from or written to memory.

Chip Enable (CE): Permits a specific chip to engage and place data onto the bus.

Output Enable (OE): Makes sure only selected devices drive the bus.

Tristate Buffers — Keeping the Peace on the Bus
When multiple memory chips share a data bus, tristate buffers ensure only one device drives the lines at a time, while others stay ‘off’ electrically.

Practical Integration Walkthrough
CPU puts the target memory address on the address bus.

Address decoder activates the matching chip’s enable signal.

CPU asserts Read or Write.

During Read, the selected chip drives the data bus with requested data.

During Write, the CPU places data on the bus, and the chip saves it.

Timing is critical. Control signals and data must stabilize before reads/writes are acknowledged.

Survival Project: Building a Basic Memory Interface
Materials
RAM IC or homemade flip-flop arrays for memory banks.

NAND gates or decoders for chip select circuitry.

Tristate buffers or logic gates for bus management.

Wires, breadboards, connection tools.

Procedure
Design address decoding for your available RAM banks or modules.

Wire control lines for read and write operational modes.

Connect tristate buffers to ensure clean data bus sharing.

Demonstrate reading and writing sequences with LEDs or logic analyzers.

Program a small loop or test code inside your CPU to read from and write to memory.

Timing, Delays, and Real World Imperfections
Propagation delays mean data doesn’t move instantly; clock synchronization and wait states make sure signals settle.

Power stability and noise immunity are practical concerns—buffer your signals.

Consider handshaking protocols for perfect data transfer with external memory devices.

Memory integration is a mighty challenge and opportunity — the difference between a theoretical CPU and a fully functioning computer that might just reboot civilization.
