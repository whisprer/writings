# WoflCorp I/EAS-3lectron Specification Sheet

**Designation:** I/EAS-3lectron [SV]  
**Creator:** Leagounan  
**Vessel ID:** 1003  
**Type:** Small Vessel - Insert/Extract Assault Shuttle (3lectron variant)

---

## 1. Basic Information & Classification

| Parameter | Value |
|-----------|-------|
| **Official Name** | WoflCorp I/EAS-3lectron |
| **Ship Type** | Small Vessel (SV) |
| **Size Class** | 1 |
| **Unlock Level** | 20 |
| **Faction** | Private |
| **Creator/Author** | Leagounan |
| **Vessel ID** | 1003 |
| **Production Time** | 1 hour 43 minutes (103 minutes) |

---

## 2. Physical Specifications & Structural Data

### Dimensional Profile

| Metric | Value |
|--------|-------|
| **Length × Width × Height** | 13.5m × 10.5m × 6.5m |
| **Total Mass** | 87.5 tonnes |
| **Block Count** | 300 blocks |
| **Triangle Count** | 2,827 triangles |
| **Device Count** | 105 devices (109,968 total device instances) |
| **Light Sources** | 1 light emitter |

### Hull Composition & Materials

The vessel's structure is built primarily from advanced composite materials:

| Material | Individual Blocks | Total Instances |
|----------|------------------|-----------------|
| **Hardened Steel Blocks S** | 151 | 755 |
| **Modular Wings** | 15 | 156 |
| **Truss Blocks S** | 39 | 39 |
| **Carbon Composite Blocks S** | 3 | 3 |
| **Steel Blocks S** | 2 | 2 |
| **TOTAL** | **210** | **955** |

The dominance of hardened steel blocks (79.3% of individual blocks) provides excellent structural integrity and combat durability for a small assault platform.

---

## 3. Propulsion Systems

### Thruster Configuration

The I/EAS-3lectron features an advanced vectored thrust system with 12 total thrusters distributed across multiple axes:

#### Primary Thrusters

| Thruster Type | Quantity | Displacement | Configuration | Thrust Output |
|---------------|----------|--------------|---------------|---------------|
| **Thruster Jet II XL** | 8 | 3×10×3 | Primary banks | 54,000 DPS |
| **Thruster Jet II XXL** | 4 | 3×13×3 | Auxiliary boost | 35,480 DPS |

#### Directional Distribution

- **Back/Front Thrusters:** 2 pairs (primary translation)
- **Top/Down Thrusters:** 2 pairs (vertical control)
- **Left/Right Thrusters:** 0 (no lateral-only thrusters; achieved via vectoring)

**Total Combined Thrust:** 89,480 DPS equivalent

### Rotational Performance & Acceleration

#### Angular Velocities

| Axis | Maximum Speed | Speed Differential |
|------|---------------|-------------------|
| **Yaw** | ±234–219 deg/s | -15 deg/s asymmetry |
| **Pitch** | ±255–259 deg/s | +4 deg/s reverse bias |
| **Roll** | ±241–195 deg/s | -46 deg/s asymmetry |

#### Angular Accelerations

| Axis | Acceleration Magnitude | Direction |
|------|------------------------|-----------|
| **Yaw** | 607.3 deg/s² | Negative (deceleration dominance) |
| **Pitch** | 762.5 deg/s² | Negative (strong pitch control) |
| **Roll** | 519.2 deg/s² | Negative (moderate roll braking) |

### Torque Vectoring System

The vessel employs differential thrust vectoring for exceptional maneuverability:

#### Roll (X-axis) Torque

| Direction | Torque Output |
|-----------|---------------|
| **Positive (Right Roll)** | 423 MNm |
| **Negative (Left Roll)** | 31.8 MNm |
| **Asymmetry Ratio** | 13.3:1 (right-biased) |

#### Yaw (Z-axis) Torque

| Direction | Torque Output |
|-----------|---------------|
| **Positive (Clockwise)** | 54.8 MNm |
| **Negative (Counter-clockwise)** | 50.2 MNm |
| **Balance Ratio** | 1.09:1 (near-balanced) |

#### Pitch (Y-axis) Torque

| Direction | Torque Output |
|-----------|---------------|
| **Positive (Up Pitch)** | 33.5 MNm |
| **Negative (Down Pitch)** | 34.3 MNm |
| **Balance Ratio** | 0.98:1 (highly balanced) |

---

## 4. Flight Dynamics & Aeronautical Performance

### Linear Acceleration Profile

| Vector | Acceleration | Force Generated |
|--------|--------------|-----------------|
| **Roll** | 349 m/s² | 30.6 MN |
| **Pitch** | 301 m/s² | 26.3 MN |
| **Yaw** | 252 m/s² | 22.1 MN |

**Acceleration Hierarchy:** Roll ≥ Pitch > Yaw (XYZ priority)

### Lift & Drag Characteristics

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Minimum Liftoff Thrust** | 525 kN | Required for atmospheric operations |
| **Drag Factor** | 18.9 t | Atmospheric resistance at speed |
| **Lift Factor** | 166.0 t | Sustained lift capability |
| **Maximum Velocity** | 70.0 m/s | Top speed in standard atmosphere |
| **Cargo Lift Capacity** | 5.01 kt | Maximum loadable cargo mass |
| **Remaining Thrust Margin** | 30.1 MN | Safety margin above lift requirements |

---

## 5. Weapons Systems

### Primary Armament

The I/EAS-3lectron carries a mixed weapons suite optimized for rapid assault tactics:

#### Turret-Mounted Systems

| Weapon | Quantity | Configuration | Damage/DPS | Unlock Level | Notes |
|--------|----------|----------------|-----------|--------------|-------|
| **Rail Gun** | 2 | Twin turrets | 4,980 DPS | — | High-penetration kinetic |
| **Minigun Turret** | 4 | Quad mounts | 4,400 DPS | — | Rapid-fire ballistic |
| **Pulse Laser** | 2 | Twin energy | 4,140 DPS | — | Directed energy weapon |
| **Rocket Launcher** | 1 | Single hard-point | 1,050 DPS | — | Explosive ordnance |

**Total Integrated Firepower:** 14,570 DPS (sustained combined arms)

### Ammunition & Energy Loadout

#### Kinetic Ammunition

| Ammunition Type | Quantity | Status | Notes |
|-----------------|----------|--------|-------|
| **LS Charge SV/HV** | 20,000 rounds | Loaded | Rail gun compatible |
| **Railgun Bullet** | 20,000 rounds | Loaded | Primary kinetic |
| **15mm Bullet** | 24,000 rounds | Loaded | Minigun feed stock |
| **130mm MSL** | 8,000 rounds | Loaded | Missile ordinance |

**Total Ammunition Mass:** ~240 units (combined ballistic load)

#### Energy Reserves

- **Fuel Capacity:** 98% (optimal operational window)
- **Pentaxid Reserves:** 6000% (over-charged state indicator)

---

## 6. Power Systems & Energy Management

### Power Generation & Distribution

| Parameter | Value | Status |
|-----------|-------|--------|
| **Total Power Capacity** | 349 PU (Power Units) | Rated maximum |
| **Generator Count** | 21 units | Distributed network |
| **Generator Efficiency** | 3,927 total output | Cumulative generation |
| **Current Output** | 36.2 kPU | Real-time generation |
| **Current Consumption** | 0.3 kPU | Active systems draw |
| **Power Remaining** | 16.50 kPU | Available reserve |
| **Efficiency Level** | 100% (OFF) | Disabled/not optimized |

**Power Margin:** ~16.2 kPU headroom for combat systems activation

### CPU Processing Tiers

The vessel utilizes a multi-tiered CPU architecture for distributed computing:

#### CPU Tier Distribution

| Tier | Quantity | CPU Cost | Total Cost | Classification |
|------|----------|----------|-----------|-----------------|
| **Tier 1** | 1 | — | — | Basic processing |
| **Tier 2** | 1 | — | — | Secondary system |
| **Tier 3** | 1 | 40,000 | 40,000 | Advanced logic |
| **Tier 4** | 4 | 15,000 | 60,000 | Combat processing |

**Total CPU Usage:** 110,922 points  
**Active Tier:** 4 (combat-optimized)  
**CPU Efficiency:** 100% (Currently Disabled)

---

## 7. Environmental & Life Support Systems

### Oxygen Management

| System | Status | Capacity | Notes |
|--------|--------|----------|-------|
| **Primary O₂ Tanks** | 1 unit | 40 units | Main storage |
| **Currently In Tanks** | 1 unit | — | Active supply |
| **Currently In Base** | 0 units | — | Station-stored |
| **Needed to Fill** | 0 units | — | Fully charged |
| **Oxygen Stations** | 0 | — | No additional sources |
| **Ventilators** | 0 | — | No environmental processors |

**Life Support Status:** Minimal (no redundancy, no atmospheric processors)

### Medical & Recreational Systems

| Facility | Quantity | Status | Capacity |
|----------|----------|--------|----------|
| **Medic Stations** | 0 | Not installed | — |
| **Clone Chambers** | 0 | Not installed | — |
| **Life Support Redundancy** | None | — | Catastrophic single-point failure risk |

---

## 8. Storage & Logistics Systems

### Cargo Capacity

| Container Type | Quantity | Capacity per Unit | Total Capacity |
|----------------|----------|------------------|-----------------|
| **Cargo Boxes** | 2 | 30 SU | 60 SU total |
| **Ammo Boxes** | 0 | 30 SU | 0 SU total |
| **Fridges** | 0 | — | — |
| **Food Processors** | 0 | — | — |
| **Constructors** | 0 | — | — |

**Total Cargo Volume:** 60 SU (storage units)

### Fuel Storage

| Tank Type | Quantity | Capacity per Unit | Total Capacity |
|-----------|----------|------------------|-----------------|
| **Fuel Tank** | 10 | 1,500 units | 15,000 units total |
| **Pentaxid Tank** | 1 | 200 units | 200 units total |

**Operational Range:** Extended via distributed fuel storage (10 tanks = operational redundancy)

### Ammunition Storage

| Container | Quantity | Purpose | Notes |
|-----------|----------|---------|-------|
| **Ammo Controller** | 2 | Automated feed | 30 SU capacity each |
| **Integrated Magazines** | — | Weapon-mounted | Distributed across turrets |

---

## 9. Sensor & Detection Systems

### Primary Sensor Suite

#### Detector Unit (LMB Scanning Array)

| Specification | Value | Details |
|---------------|-------|---------|
| **System Type** | LMB (Long-range Mineral & Biological) Scanner | Geological survey |
| **Quantity Installed** | 1 unit | Single primary sensor |
| **Maximum Detection Range** | 14.0 km | Full spectrum capability |
| **Current Effective Range** | 3.5 km | Real-time operational range |
| **Detection Hit Points** | 120 HP | Structural durability |
| **Power Consumption** | 5.00 PU | Energy draw per active scan |
| **CPU Cost** | 50 points | Processing overhead |
| **Scan Resolution** | Type-specific ore deposit identification | Reveals ore type on contact |
| **Ammo Type** | Unlimited (passive energy-based) | Renewable resource scans |

#### Detector Characteristics

- **Mass:** 55.0 kg (lightweight sensor package)
- **Volume:** 31.3 SU (compact integration)
- **Market Value:** 208 PU (average trading price)
- **Unlock Level:** 5 (early-game technology)
- **Unlock Cost:** 7 PU (minimal progression requirement)

### Secondary Sensors

| Sensor Type | Quantity | Function | Status |
|-------------|----------|----------|--------|
| **Radar (Deco)** | 2 units | Tactical display/navigation | Passive |
| **Wireless Connection** | 1 unit | Remote communication | Enabled |
| **Spotlights** | 1 unit | Visual illumination | Offline |

---

## 10. Specialized Equipment & Systems

### Landing & Terrain Interaction

| Equipment | Quantity | Type | Status |
|-----------|----------|------|--------|
| **Retractable Landing Gears** | 3 units | Structural support | Deployable |
| **Configuration** | Tricycle-style | Geometry | Triangle pattern |

### Operational Equipment

| System | Quantity | Function | Notes |
|--------|----------|----------|-------|
| **Warp Drive** | 1 | Faster-than-light transit | Advanced propulsion |
| **CPU Extender T4** | 4 | Processing boost | Combat-optimized |
| **Wireless Connection** | 1 | Communications relay | Network-enabled |
| **Spotlights** | 1 | Illumination | External lighting |

---

## 11. Production Requirements & Manufacturing Data

### Resource Bill of Materials (BOM)

To construct a complete I/EAS-3lectron vessel from raw materials:

#### Metallic Ingots

| Material | Quantity | Purpose | Classification |
|----------|----------|---------|-----------------|
| **Copper Ingot** | 640 units | Electronics & conduction | Primary metal |
| **Cobalt Ingot** | 614 units | Structural hardening | Alloy component |
| **Iron Ingot** | 504 units | General structure | Base material |
| **Titanium Rods** | 354 units | Advanced frames | High-strength |

#### Specialty Materials

| Material | Quantity | Purpose | Classification |
|----------|----------|---------|-----------------|
| **Carbon Substrate** | 616 units | Composite plating | Advanced material |
| **Silicon Ingot** | 493 units | Electronics | Semiconductor |
| **Neodymium Ingot** | 410 units | Magnetic systems | Rare-earth |
| **Erestrum Ingot** | 374 units | Exotic alloys | Specialized |
| **Zascosium Ingot** | 374 units | Advanced tech | Specialized |

#### Optical Components

| Component | Quantity | Purpose | Classification |
|-----------|----------|---------|-----------------|
| **Small Optronic Bridge** | 8 units | Signal routing | Optical network |
| **Small Optronic Matrix** | 4 units | Processing grid | Computational core |

### Production Summary

| Metric | Value |
|--------|-------|
| **Total Material Units** | 5,778 combined resources |
| **Production Time** | 1 hour 43 minutes (103 minutes) |
| **Total Blocks Produced** | 300 blocks |
| **Build Cost (Cumulative)** | Resource-intensive small vessel |

---

## 12. Performance Characteristics Summary

### Combat Readiness Profile

| Category | Rating | Notes |
|----------|--------|-------|
| **Offensive Capability** | High | 14,570 DPS mixed armament |
| **Defensive Capability** | Medium | No shields; armor-dependent |
| **Maneuverability** | Excellent | 255 deg/s pitch maximum |
| **Speed** | Moderate | 70 m/s maximum velocity |
| **Endurance** | High | 10 fuel tanks for extended ops |
| **Loadout Flexibility** | Moderate | Fixed weapon hardpoints |

### Operational Classification

- **Primary Role:** Insert/Extract Assault Shuttle (I/EAS designation)
- **Secondary Role:** Rapid strike craft; geological survey
- **Engagement Profile:** Fast-moving tactical platform
- **Crew Capacity:** Data not specified (likely autonomous/minimal)

---

## 13. System Status & Operational Notes

### Current Vessel State

| System | Status | Alert Level |
|--------|--------|-------------|
| **Propulsion** | Nominal | Green |
| **Power Generation** | Nominal | Green |
| **Weapons Systems** | Armed & Loaded | Green |
| **Life Support** | Minimal | Yellow (no medical/clone backup) |
| **Sensors** | Nominal | Green |
| **Structural Integrity** | Nominal | Green |
| **CPU Efficiency** | Off (100% disabled) | Yellow |
| **Shield Systems** | Offline/Not Present | Red |

### Critical Observations

1. **Shield Status:** No shield generators installed; vessel relies entirely on armor durability
2. **CPU Efficiency:** Disabled despite 100% availability (tactical choice or malfunction)
3. **Life Support:** Minimal redundancy; single O₂ tank with no backup ventilators
4. **Medical Systems:** No medic stations or clone chambers (crew recovery risk)
5. **Ammunition:** Fully loaded across all weapon types (combat-ready state)
6. **Power Headroom:** Significant reserve capacity (16.5+ kPU available)

---

## 14. Dimensional & Geometric Data

### Construction Geometry

| Metric | Value | Analysis |
|--------|-------|----------|
| **Block Count** | 300 | Relatively compact for Class 1 |
| **Device Count** | 105 | Moderate device density |
| **Triangle Polygons** | 2,827 | Visual rendering complexity |
| **Mass Distribution** | 87.5 t | Light for assault shuttle |
| **Footprint** | 13.5m × 10.5m | Reasonable hangar compatibility |
| **Profile Height** | 6.5m | Low silhouette for cover |

### Scale Reference

The I/EAS-3lectron occupies approximately **0.94 m³** of volume (13.5 × 10.5 × 6.5 ÷ 1000), making it a compact, efficient platform despite heavy armament.

---

## 15. Comparative Analysis & Performance Metrics

### Thrust-to-Weight Ratio

\[ \text{T/W Ratio} = \frac{89,480 \text{ DPS}}{87.5 \text{ t}} \approx 1,022 \text{ DPS/tonne} \]

**Interpretation:** Exceptional acceleration capability; designed for rapid tactical maneuvering.

### Power-to-Mass Ratio

\[ \text{P/M} = \frac{36.2 \text{ kPU}}{87.5 \text{ t}} \approx 0.41 \text{ kPU/tonne} \]

**Interpretation:** Efficient power distribution for vessel size.

### Firepower Density

\[ \text{F/M} = \frac{14,570 \text{ DPS}}{87.5 \text{ t}} \approx 166.5 \text{ DPS/tonne} \]

**Interpretation:** High damage output relative to mass; aggressive platform design.

---

## 16. Designation & Etymology

**I/EAS-3lectron Breakdown:**
- **I/** = Insert (tactical deployment)
- **EAS** = Extract/Assault Shuttle (primary mission)
- **-3lectron** = Third-generation electronics suite + "electron" (speed/agility concept)

The "3lectron" variant emphasizes rapid response and precision targeting, distinguishing it from earlier I/EAS iterations.

---

## 17. Technical Specifications Index

### Quick Reference Table

| Specification | Value | Unit |
|---------------|-------|------|
| **Length** | 13.5 | m |
| **Width** | 10.5 | m |
| **Height** | 6.5 | m |
| **Mass** | 87.5 | tonnes |
| **Maximum Velocity** | 70.0 | m/s |
| **Maximum Yaw** | 234 | deg/s |
| **Maximum Pitch** | 255 | deg/s |
| **Maximum Roll** | 241 | deg/s |
| **Total Weapons DPS** | 14,570 | DPS |
| **Generator Output** | 36.2 | kPU |
| **Fuel Capacity** | 15,000 | units |
| **Cargo Capacity** | 60 | SU |
| **Production Time** | 103 | minutes |
| **Unlock Level** | 20 | — |

---

## 18. Final Assessment & Operational Summary

The **WoflCorp I/EAS-3lectron** represents a highly specialized tactical platform optimized for rapid-response assault and extraction operations. Its combination of powerful thrust vectoring, distributed weapon systems, and extended fuel capacity make it ideal for time-sensitive missions requiring high mobility and sustained firepower delivery.

**Strengths:**
- Exceptional rotational performance (255 deg/s pitch)
- Balanced multi-axis thrust (12-thruster configuration)
- Heavy integrated armament (4 weapon types)
- Distributed fuel storage (10 tanks = redundancy)
- Lightweight design (87.5 tonnes)
- Full ammunition loadout

**Limitations:**
- No shield generators (armor-dependent)
- Minimal life support (single O₂ tank)
- No medical/respawn facilities
- CPU efficiency disabled
- Limited cargo capacity (60 SU)
- No secondary sensor suite

**Operational Recommendation:** Best deployed in teams for mutual support; effective against single-target threats and rapid strike scenarios. Avoid prolonged engagements in environments lacking support infrastructure.

---

**Document Generated:** Comprehensive I/EAS-3lectron Specification Sheet  
**Last Updated:** Current operational parameters  
**Data Source:** WoflCorp Control Panel Systems & Blueprint Database  
**Classification:** Technical Specification (Public)