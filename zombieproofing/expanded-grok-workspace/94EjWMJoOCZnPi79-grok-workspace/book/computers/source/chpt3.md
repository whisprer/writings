# Zombieproof Computers: How to Keep a Mind When the Grid Is Gone

Chapter 3: Digital Logic from the Ground Up

Welcome back, survivor. Now that you’ve learned to carve circuits from scrap and bend electrons to your will, it’s time to learn the language those circuits speak: digital logic. Think of digital logic as the grammar and syntax of computing. If your computer brain is the zombieproof fortress, digital logic lays down the fundamental bricks and mortar of its walls.

Binary: The Computer’s Native Tongue
Everything a computer knows collapses into two states: on or off. We call these states 1 and 0, the binary digits or “bits.” This is like Morse code but electrified, where every pulse or absence of pulse carries meaning.

A bit is the foundation of all information. Group bits together and you can represent numbers, letters, images, sounds, and even ideas.

Logic Gates: The Basic Building Blocks
Logic gates are tiny, electrical decision-makers. Each takes one or more binary inputs and computes a binary output according to a rule.

The Big Six
AND: Outputs 1 if both inputs are 1. Think “both conditions must be true.”

OR: Outputs 1 if either input is 1. “At least one true.”

NOT: Outputs the opposite of input—flip the bit!

NAND: NOT + AND combined; outputs 0 only if both inputs are 1.

NOR: NOT + OR; outputs 1 only if both inputs are 0.

XOR: Outputs 1 if inputs differ; 0 if same. Useful for addition.

Every complex chip, every processor, and even your smartphone’s brain is composed of billions of these simple gates.

Building a Half Adder — Your First Logical Circuit
Remember counting with fingers as a kid? Adding 1 + 1 equals 2, right? But computers calculate bit by bit, so adding 1 + 1 requires carrying over.

A half adder adds two single bits, \(A\) and \(B\), and outputs a sum and a carry.

The sum is the XOR: \(S = A \oplus B\).

The carry is the AND: \(C = A \cdot B\).

Build it from one XOR gate and one AND gate.

You can wire this with salvaged transistors or gate ICs. Testing all four input states (00, 01, 10, 11) proves it adds correctly.

The Full Adder: Accounting for Carry-In
Life’s rarely simple. Sometimes you add with a carry from previous additions.

A full adder takes in \(A\), \(B\), and a carry-in \(C_{in}\).

It outputs a sum \(S\) and a carry-out \(C_{out}\).

The formulas are \(S = A \oplus B \oplus C_{in}\) and \(C_{out} = (A \cdot B) + (C_{in} \cdot (A \oplus B))\).

Build with two half adders and one OR gate.

Link multiple full adders to add multi-bit numbers—a vital function for all your zombieproof computing needs.

Oscillators and Clocks: The Heartbeat of Your Digital World
A clock isn’t a hairy skull ticking—but it’s just as vital. It’s an electronic signal oscillating regularly between high and low voltage, marking beats that synchronize every operation.

How Do You Build a Clock?
Oscillators are circuits that generate repetitive signals: sine waves, triangle waves, but for digital logic, square waves are king because they swing sharply between 0 and 1.

You can build a ring oscillator with an odd number of NOT gates connected in a loop. Each gate’s output flips the input of the next, causing a continuous oscillation.

The frequency depends on gate delays—how long a signal takes to switch.

Why Square Waves?
Square waves switch cleanly between high and low states, allowing digital circuits to latch onto clear logic levels without ambiguity. This sharp transition reduces errors and improves timing precision—a must for your survival-grade gear.

Clock Division
Sometimes you need a slower heartbeat. Flip-flops chained together can divide the frequency of your oscillator by powers of two, giving you adjustable timing.

Survival Project: Build a Half Adder and Clock Circuit
Parts List

Salvaged XOR, AND, NOT gates or transistors with resistors.

Breadboard or simple prototyping surface.

Power source (batteries or power supply).

LED indicators.

Steps

Wire a half adder circuit on your breadboard.

Test sum and carry outputs with all input combinations; watch the LEDs reflect the outputs.

Build a ring oscillator from NOT gates; connect an LED to observe the blinking clock signal.

Add flip-flops to divide clock frequency and observe slower blinking.
