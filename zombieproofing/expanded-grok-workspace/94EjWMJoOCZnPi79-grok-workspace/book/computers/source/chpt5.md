# Zombieproof Computers: How to Keep a Mind When the Grid Is Gone

Chapter 5: Building the CPU Core

Welcome back, brave builder. Now that you’ve mastered the nuts and bolts of memory cells, multiplexers, and data flow control in Chapter 4a, it’s time to step up to the big leagues: assembling these parts into a working CPU core, the nerve center orchestrating every move.

This chapter will guide you step-by-step through designing and wiring your own basic CPU’s brain, grounding every instruction in logic gates, flip-flops, registers, and controlled data routing facilitated by multiplexers—none of the magic happens without these friends.

Understanding the CPU’s Role
Your CPU is the conductor in an orchestra of circuits, maintaining rhythm with a clock and signaling which instruments—registers, memory, ALUs—play at any moment.

It performs a recurring cycle:

Fetch: Grab the instruction from memory, guided by the Program Counter (PC).

Decode: Translate that instruction into control signals that determine what the CPU does next.

Execute: Perform operation in the ALU or data transfer in registers/memory.

Writeback: Save results back to registers or memory.

Update PC: Move to the next instruction.

Bringing Circuits to Life — Step-by-Step
Step 1: Registers — Your CPU’s Quick-Access Memory
Registers capture and hold bits synchronized by the CPU clock:

Build each register from D flip-flops, connected to latch data loaded on clock rising edge.

Add enable (load) signals that control when the register updates, allowing precise data staging.

Use multiplexers to select which data source drives the register inputs.

Step 2: Data Movement — Controlled by Multiplexers
Imagine registers lining the CPU pathway; multiplexers are your circuit's traffic signals directing which register’s data routes where.

A multiplexer logically ANDs input lines with select signals and ORs results to a single output.

Control signals from the control unit decide which register the ALU sees or what the program counter should update to.

Multiplexers let your CPU flexibly route operands and results without physically rewiring circuits.

Step 3: The ALU — The Calculating Muscle
Use the full adders and logic gates you built:

Connect registers’ outputs to ALU inputs to feed numbers for arithmetic and logic operations.

Control lines select operation mode (add, subtract, and, or, xor).

Step 4: The Program Counter — Address Pioneer
The PC is a register with special logic:

Increment logic: Adder increases PC by 1 each cycle.

Load logic: When jump instructions occur, the PC loads a new address.

Controlled by multiplexers to select incremented or jumped address as next PC value.

Step 5: The Control Unit — Mastermind of Signals
This finite state machine interprets instruction bits, generating timed signals to:

Enable or disable register loading.

Select ALU operations.

Control PC increment or jump.

Manage memory read/write cycles.

Timing Is Everything: The Clock and Control Lines
Each register, ALU operation, and data movement happens on precise clock edges. Your clock pulse invades circuits, triggering flip-flops to update, multiplexers to switch paths.

Control signals gate these operations, ensuring only the correct data moves and timing stays synchronized—so no zombie shuffle or electrical chaos.

Practical Build Project: Assemble a 4-Bit CPU Core
Parts needed:

D flip-flop ICs for registers (or transistor equivalents)

Gate ICs/Transistors for multiplexers, logic gates, ALU adders

Breadboard, wires, switch inputs, LEDs for outputs

Oscillator circuit for clock source

Procedure:

Build four 4-bit registers with controlled load signals.

Wire multiplexers to select register outputs for ALU inputs.

Construct the ALU with adders and logic gates — connect to multiplexers' outputs.

Build the program counter with increment and load logic, controlled by multiplexers.

Create a minimalist control unit hardwired for a few basic instructions: load, add, jump, store.

Connect clock to synchronize all components.

Test with step-by-step clock pulses, watching LEDs for register outputs and program counter progress.

This grounding completes your CPU’s brain, built from first principles, ready to be expanded with memory, input/output, and complex instructions. By controlling every gate, flip-flop, multiplexer, and wiring path, you hold the power to resurrect civilization’s digital pulse.
