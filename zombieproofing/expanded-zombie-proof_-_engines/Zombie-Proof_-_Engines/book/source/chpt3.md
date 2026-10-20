# Chapter 3: Signal Science — Types, Strength, and Survival

## Overview: Why Signal Matters in Apocalypse Radio

If you want reliable comms, hack the spectrum, or just yak with your crew while zombies roam, understanding signal types, behaviors, and strengths is a must. This chapter unlocks the physics, math, and practicalities of signals—your lifeline in the airwaves.

---

## Signal Types and Modulations

- **Continuous Wave (CW):** Simple on/off pulses, Morse code style, zombie classic.
- **Amplitude Modulation (AM):** Vary signal strength to encode info; simple but noise-prone.
- **Frequency Modulation (FM):** Shift frequency; less noise, better music and voices.
- **Phase Shift Keying (PSK):** Hack-level encoding by changing phase of wave.
- **Frequency Shift Keying (FSK):** Digital style frequency switches.
- **Spread Spectrum:** Secret sauce for jam resistance and secure comms (includes FHSS and DSSS).

---

## Signal Strength & Measuring Power

- Signal power measured in Watts (W) or dBm (decibels referenced to 1 milliwatt).
- \( P(dBm) = 10 \times \log_{10} \left(\frac{P(W)}{1mW}\right) \).
- Field strength (Volts per meter, \(V/m\)) tells actual wave voltage in air.
- Free space path loss (FSPL) law describes how signal weakens with distance \(d\):
  
  \[
  FSPL(dB) = 20 \log_{10}(d) + 20 \log_{10}(f) + 20 \log_{10} \left(\frac{4\pi}{c}\right)
  \]

- Practical survival tip: antenna gain can boost received signal strength by degrees.

---

## Signal-to-Noise Ratio (SNR)

- How clean your signal is vs background noise.
- High SNR = clear messages; low SNR = zombie static and confusion.
- Techniques to improve SNR:
  - Use directional antennas.
  - Increase transmitter power or receiver sensitivity.
  - Use digital protocols with error correction.

---

## Doppler Effect in Radio

- Moving zombies and vehicles change perceived frequency.
- Important for fast-moving drones or when tracking survivors.
- Formula for shifted frequency:
  
  \[
  f' = f \times \frac{c + v_r}{c + v_s}
  \]

  where \(v_r\) and \(v_s\) are velocities of receiver and source.

---

## Advanced Signal Handling

- Filtering: Removing unwanted frequencies/noise.
- Mixing and Heterodyning: Creating new frequencies by combining signals.
- IQ Modulation: Complex amplitude and phase control for SDR and advanced radios.

---

## Signal Types Summary Table

| Signal Type        | Characteristics                  | Usage                  | Apocalypse Utility                 |
|--------------------|---------------------------------|------------------------|----------------------------------|
| CW (Morse Code)    | Simple on/off                   | Basic text messaging   | Stealth comms with minimal power |
| AM                 | Strength varies, noisier        | AM radio, simple voice | Low-tech, widely understood      |
| FM                 | Frequency varies, noise-resistant| Radio broadcasting     | Clearer voice, music transmission|
| PSK, FSK           | Digital phase/freq modulation   | Data comms, hacking    | Secure, efficient data transfer  |
| Spread Spectrum    | Hopping/fading frequencies      | Military, secure radio | Resistant to jamming, secure ops |

---

## Next Up: Antennas and Direction - How to Catch Those Signals Like a Pro

Stay tuned for full antenna designs, direction-finding tricks, and signal-strength formulae with hands-on projects up next!

---
