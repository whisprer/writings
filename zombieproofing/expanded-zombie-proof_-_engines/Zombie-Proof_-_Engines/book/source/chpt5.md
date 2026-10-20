# Chapter 5: Radio Protocols & Data — Speaking Zombie Fluently

## Introduction: The Language of Radio Signals

Once you understand how radio waves travel and how antennas broadcast those waves, it's crucial to know how information is encoded and decoded. Radio protocols are the grammar and vocabulary of wireless communication — without them, your radio is just static.

---

## Common Radio Protocols for Survivors

- **Morse Code**  
  Old but gold. A series of short and long signals (dots and dashes) used as a simple digital alphabet.

- **AM/FM**  
  Analog modulation; AM varies amplitude, FM frequency. Widely used for broadcasting voice and music.

- **Frequency Shift Keying (FSK)**  
  Digital method switching between frequencies to represent binary data.

- **Phase Shift Keying (PSK)**  
  Digital phase changes of the carrier wave. PSK31 is famous among radio hackers.

- **Packet Radio**  
  Transmits data in small packets with headers, checksums, and error-correction.

- **Wi-Fi & Bluetooth**  
  Higher-frequency protocols for local area networking and device communication.

- **LoRa / LoRaWAN**  
  Long-range, low-power digital modulation for IoT and survival sensor nets.

---

## Protocol Layers Simplified

- Physical Layer: How signals are sent (AM/FM, FSK, etc.)
- Data Link Layer: Packet framing, error detection
- Network Layer: Routing and addressing (mesh, IP)
- Application Layer: Actual message content, commands.

---

## Digital Encoding and Error Correction

- Encoding schemes like Manchester, NRZ for reliable data recovery.
- Error correction: Forward Error Correction (FEC), CRC codes to detect and fix errors.

---

## Open Standards & OSS Radio Protocols

- Popular open-source protocols you can hack on or implement for survival networks.
- Includes APRS, AX.25, POCSAG pager codes, and much more.

---

## Signal Timing & Synchronization

- Clocking signals and synchronization maintain proper message decoding.
- Important in spread-spectrum and frequency hopping protocols to avoid jamming.

---

## Summary Table of Protocols

| Protocol/Modulation | Data Type       | Range           | Power Usage       | Typical Usage                 |
|---------------------|-----------------|-----------------|-------------------|------------------------------|
| Morse (CW)          | Text/Digital    | Long (HF/VHF)   | Very Low          | Emergency and covert comms   |
| AM/FM               | Analog Voice    | Medium          | Medium            | Broadcasting, voice comms    |
| FSK/PSK             | Digital Data    | Variable        | Medium            | Packet radio, data comms     |
| Packet Radio         | Digital Packets | Moderate        | Medium            | Amateur radio networks       |
| Wi-Fi/Bluetooth     | Digital Data    | Short range     | High              | Local comms, IoT devices     |
| LoRa/LoRaWAN         | Digital Data    | Very Long range | Very Low          | Sensor networks, survive net |

---

## Next Up: Building Real-world Projects — Fox Hunting, SDR Hacking, and More

Stay tuned for full projects bridging theory and the real apocalypse game.

