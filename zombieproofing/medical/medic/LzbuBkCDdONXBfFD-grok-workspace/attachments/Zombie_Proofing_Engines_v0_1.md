# Zombie Proofing — Engines
## A field guide to restarting civilisation, one suspiciously rusty crankshaft at a time

**Edition 0.1 — source synthesis and safe foundation draft**

> **Mission statement:** preserve enough practical engine knowledge that a future mechanic can move people, pump water, generate electricity, mill grain, power workshops, and avoid being eaten while doing it.

## Read this first: the non-negotiable safety page

An engine is a controlled heat-and-pressure machine. When it stops being controlled, it becomes a metal grenade with opinions.

- Never run petrol, diesel, wood gas, charcoal gas, LPG, or any combustion engine indoors or in an attached garage.
- Carbon monoxide is invisible, tasteless, and odourless. Use a certified CO alarm, but do not treat an alarm as permission to operate a dangerous setup.
- Do not improvise pressure vessels, boilers, compressed-gas receivers, fuel tanks, or high-pressure diesel injection systems. A boiler failure can be fatal. In the UK, pressure systems above the relevant thresholds require appropriate design, inspection, relief devices, and written schemes; HSE says equipment must remain within safe operating limits. [web:17][web:21]
- Do not use a homemade gasifier in a building. Producer gas can contain substantial carbon monoxide and can form explosive mixtures if air leaks in. [file:10]
- Keep ignition sources away from fuel vapour. Petrol vapour travels; it does not politely remain above the puddle.
- Shield rotating machinery. Belts, chains, flywheels, shafts, and fans do not distinguish between zombies and fingers.
- Wear eye, hearing, hand, respiratory, and hot-work protection appropriate to the job.
- The procedures here are educational. Manufacturer service data wins over generic numbers.

HSE advises operating pressure equipment only within its safe limits, maintaining it properly, and using competent people for examination and repair. [web:17]

## How to use this book

This is a **map**, not a licence to build the most dangerous object in the scrapyard. Progress through the tiers:

1. Observe and identify.
2. Learn the energy flow.
3. Service a complete, known engine.
4. Measure before modifying.
5. Build small, low-energy demonstrations.
6. Only then consider advanced fuels, pressure systems, or high-speed machinery.

The source bundle is strongest on four-stroke petrol engines, dormant-engine revival, carburettor cleaning, ethanol adaptation, and biomass gasification. It is not a complete manufacturing textbook for making crankshafts, pressure vessels, turbines, or jet engines from raw ore. Where this guide reaches beyond those materials, it labels the discussion as context rather than a build recipe.

---

# Part I — What is an engine?

An engine converts an input energy source into useful motion. The input may be chemical fuel, steam pressure, compressed air, electricity, falling water, or nuclear heat. The output may be rotation, reciprocation, or thrust.

A petrol engine burns fuel **inside** its cylinders. A steam engine burns fuel in a separate furnace and uses heat to make steam. A jet engine accelerates air and combustion products rearwards to produce thrust. An electric motor converts electromagnetic forces directly into rotation.

The universal pattern is:

```text
energy source → working fluid or electromagnetic field → force → motion → useful load
```

A machine is not useful merely because it runs. It must run safely, reject waste heat, survive loads, and deliver power through a controllable interface.

## The four-stroke engine in one diagram

```text
                 cylinder head
          intake valve   exhaust valve
               ↓              ↑
        ┌─────────────────────────┐
        │     combustion space    │
        │       ┌────────┐        │
        │       │ piston │        │
        │       └───┬────┘        │
        └───────────┼─────────────┘
                    │ connecting rod
                    │
              ──────┴────── crankpin
             /              \
        main journal      crank throw
                    crankshaft
```

### The cycle

| Stroke | Piston | Valves | What happens |
|---|---:|---|---|
| Intake | TDC → BDC | Intake open | Air or air–fuel charge enters |
| Compression | BDC → TDC | Both closed | Charge pressure and temperature rise |
| Power | TDC → BDC | Both closed | Spark or compression ignition releases heat; gas expands |
| Exhaust | BDC → TDC | Exhaust open | Spent gas leaves |

One complete four-stroke cycle takes two crankshaft revolutions, or 720 degrees. Only the power stroke supplies net cylinder work; the flywheel and the other cylinders carry the engine through the remaining strokes. [file:13]

## What the parts do

- **Cylinder:** pressure boundary and sliding guide.
- **Piston:** moving pressure boundary.
- **Piston rings:** seal combustion gases, control oil, and transfer heat to the cylinder.
- **Connecting rod:** transmits force while allowing the piston and crankshaft to follow different paths.
- **Crankshaft:** changes reciprocating motion into rotation.
- **Flywheel:** stores rotational energy and smooths individual power pulses.
- **Camshaft:** opens valves at the correct crank angle.
- **Timing belt or chain:** keeps camshaft and crankshaft synchronised. The cam turns at half crankshaft speed in a conventional four-stroke engine.
- **Spark plug:** creates a timed high-voltage arc in spark-ignition engines.
- **Injector or carburettor:** meters fuel.
- **Oil pump and sump:** reduce friction and carry away heat and wear debris.
- **Cooling system:** moves heat from metal to air or coolant and then to the atmosphere.

---

# Part II — The engine family tree

| Type | Energy conversion | Strengths | Weaknesses | Typical use |
|---|---|---|---|---|
| Steam reciprocating | Fuel heat → steam pressure → piston motion | Multi-fuel, high torque, repairable concepts | Boiler bulk, warm-up, pressure hazard, losses | Historic rail, ships, stationary work |
| Steam turbine | Steam → high-speed rotor | Smooth, powerful at scale | Poor small-scale efficiency, complex blades | Power stations, ships |
| Petrol/Otto | Spark-ignited fuel–air charge → piston rotation | Light, high power-to-weight, easy starting | Knock sensitivity, lower efficiency than diesel | Cars, small generators, tools |
| Diesel | Compressed air heats injected fuel → piston rotation | Efficient, durable, strong low-speed torque | Heavy, injection-system complexity, noise | Trucks, tractors, ships, generators |
| Wankel rotary | Combustion pushes a triangular rotor | Compact, smooth, few reciprocating parts | Seal wear, heat, emissions, fuel consumption | Specialist cars, small aircraft/UAVs |
| Electric motor | Electrical energy → magnetic force → rotation | High efficiency, instant torque, quiet | Needs batteries or grid; storage mass | Vehicles, tools, industrial drives |
| Pneumatic/hydraulic motor | Stored fluid pressure → motion | Safe in some explosive environments; controllable | Requires compressor/pump and reservoir | Automation, mining, tools |
| Gas turbine/jet | Combustion → high-speed gas flow → shaft power or thrust | Excellent power-to-weight at scale and speed | Hot, loud, poor low-speed efficiency, precision manufacture | Aircraft, power generation |
| Water wheel/turbine | Falling or flowing water → rotation | Renewable, continuous where geography permits | Site-dependent, civil works | Mills, hydroelectricity |

An engine can also be classified by output: torque, linear force, shaft power, or thrust. A car engine is not automatically a good generator engine, and a jet engine is an exceptionally bad wheelbarrow motor unless your wheelbarrow is trying to leave Earth.

## A short history

- Hero of Alexandria demonstrated an early steam reaction device before the common industrial era, but it was a demonstration rather than a practical power system.
- Practical steam engines matured through the work of engineers including Newcomen and Watt; steam power drove mines, factories, railways, and ships.
- Early gas engines such as Lenoir’s showed that combustion could happen inside the working cylinder, but efficiency improved dramatically with compression and better timing.
- Nikolaus Otto’s compressed-charge four-stroke engine established the basic cycle that became dominant for petrol engines.
- Rudolf Diesel’s compression-ignition concept produced high efficiency and strong torque, at the cost of heavier components and demanding fuel injection.
- Felix Wankel’s rotary engine replaced pistons and rods with an eccentric triangular rotor.
- Electric motors emerged alongside early electrical generation and became dominant wherever electricity was available.
- Gas turbines and turbojets became practical through improvements in metallurgy, compressors, combustion chambers, and high-speed bearings.

The recurring historical lesson is less “one engine wins” and more “the best engine depends on the fuel, load, scale, maintenance capability, and whether your civilisation has a fuel depot.”

---

# Part III — Physics without the ritual chanting

## Power, torque, and speed

Torque is twisting force. Power is the rate at which work is done.

\[
P = \tau \omega
\]

where power \(P\) is in watts, torque \(\tau\) in newton-metres, and angular speed \(\omega\) in radians per second.

For practical engine calculations:

\[
P_{kW} = \frac{T_{Nm} \times RPM}{9550}
\]

The same torque at twice the speed produces twice the power, but stresses, friction, heat, and failure energy rise sharply with speed. Piston speed is approximately:

\[
v_p = 2 \times stroke \times \frac{RPM}{60}
\]

Large engines use long strokes and heavy parts, so piston speed and inertia discourage extreme RPM. Small engines can use short strokes, light pistons, and high RPM—but their tiny bearings still have to survive the party.

## Compression ratio

\[
r = \frac{V_d + V_c}{V_c}
\]

where \(V_d\) is swept displacement and \(V_c\) is clearance volume.

Higher compression can improve efficiency and power, but raises combustion temperature and knock risk. A fuel’s octane rating describes resistance to knock in spark-ignition engines; it is not an energy-density score.

## Combustion, knock, and pre-ignition

A useful mixture needs fuel, oxygen, sufficient temperature, and enough time. Problems include:

- **Lean mixture:** too much air or too little fuel; can cause overheating, misfire, and damaged exhaust valves.
- **Rich mixture:** too much fuel; wastes fuel, fouls plugs, increases carbon and emissions.
- **Knock/detonation:** part of the unburned charge auto-ignites after the intended flame has begun. Pressure waves hammer the piston and bearings.
- **Pre-ignition:** the charge ignites before the spark because of a hot spot, glowing carbon, or overheated plug. This is even more destructive because combustion starts too early.
- **Valve float:** valve springs cannot control valves at high speed; the engine loses gas exchange and may suffer piston–valve contact.
- **Blow-by:** combustion gas escapes past piston rings into the crankcase.

Do not “solve” knock by simply adding more fuel, more timing, or more compression. Diagnose temperature, mixture, fuel quality, ignition timing, deposits, cooling, and mechanical condition as a system.

## Efficiency

A small conventional petrol engine may convert roughly 25–35% of fuel energy into shaft work under favourable conditions; diesel engines can be more efficient, especially at sustained load. The rest becomes exhaust heat, coolant heat, friction, pumping loss, noise, and accessories. The source bundle uses approximately 30% for typical petrol thermal conversion and 40–45% as a broad diesel benchmark. Treat these as indicative, not universal ratings. [file:2]

Steam systems add furnace, boiler, piping, condensation, and heat-transfer losses. Their advantage is fuel flexibility and scalable stationary operation, not compactness.

---

# Part IV — Fuel and air

## Common fuels

| Fuel | Useful traits | Design problems |
|---|---|---|
| Petrol/gasoline | Volatile, high power density, spark ignition | Vapour fire, storage degradation, knock |
| Diesel | Dense, low volatility, compression ignition | Injection pressure, cold starting, contamination |
| Ethanol | High knock resistance, renewable potential, cleaner combustion in some conditions | Lower volumetric energy, absorbs water, attacks some materials, cold-start difficulty |
| Biodiesel | Can use plant oils or waste oils after proper processing | Viscosity, oxidation, cold flow, deposits, compatibility |
| Wood gas/syngas | Made from biomass; can run adapted spark engines | CO poisoning, tar, ash, moisture, lower power, explosion risk |
| Hydrogen | Very broad flammability range, high flame speed | Leakage, embrittlement, ignition risk, storage complexity |
| Coal/wood | Abundant solid heat source | Ash, smoke, tar, boiler bulk, difficult metering |

Fuel conversion is never “just pour it in.” It changes mixture, timing, temperature, seals, filters, storage, and sometimes compression ratio.

## Ethanol conversion: what the source material says

Ethanol needs a richer fuel flow because it carries less energy per unit volume than petrol. The supplied guide describes enlarging a carburettor main jet by roughly 20–40%, with an example changing a 0.056-inch jet to about 0.078 inches for a nominal 40% diameter increase. It also describes timing advance toward approximately 22 degrees BTDC and attention to cold-start heating and material compatibility. [file:6]

Treat those numbers as a historical starting point for a specific setup, not a universal recipe. Jet flow depends on area, pressure differential, fuel properties, and the entire carburettor. If converting a real engine:

1. Establish a known baseline on its original fuel.
2. Use replaceable jets rather than drilling irreplaceable parts.
3. Change one variable at a time.
4. Monitor exhaust temperature, plug appearance, oil condition, and load response.
5. Stop at signs of detonation, overheating, lean operation, fuel leakage, or seal damage.

## Wood gas

Gasification is controlled incomplete combustion. A simplified pathway is:

```text
biomass → drying → pyrolysis → oxidation zone → reduction zone
        → hot producer gas → cooling/condensation → cyclone → media filter
        → controlled air mix → engine intake
```

The supplied gasifier material gives a rough producer-gas composition of about 20% hydrogen, 20% carbon monoxide, 50–60% nitrogen, and traces of methane. Its power is lower than petrol operation; the Simple-Fire notes around 30% less power in a comparable engine. [file:9][file:10]

Important principles:

- Fuel must be dry and consistently sized.
- Tar and moisture must be removed before the engine.
- Filters need drainage and inspection.
- The system must be airtight where gas is combustible, but designed with appropriate relief behaviour rather than becoming a sealed bomb.
- A flare test is not a safety certification.
- Use outdoor ventilation, remote operation where possible, and CO monitoring.

The source’s illustrative fire-tube table associates increasing internal diameter with more engine horsepower, from roughly 2 inches for 5 hp to 14 inches for 160 hp. These are empirical guide values, not a design standard. [file:9]

---

# Part V — Reviving a dormant engine

An abandoned engine is not dead; it is a machine that has spent years plotting corrosion.

## The revival sequence

```text
identify → inspect → lubricate → rotate by hand → replace fluids
→ clean fuel system → test electrics → verify timing → test compression
→ first start outdoors → monitor → service again
```

### 1. Identify before touching

Find the engine number, fuel type, firing order, oil grade, timing marks, compression ratio, wiring diagram, and manufacturer limits. Photograph every linkage and hose before disassembly. Label parts. Future-you is not psychic.

### 2. Make it mechanically safe

- Disconnect the battery and remove ignition sources.
- Inspect for nests, seized accessories, cracked castings, corrosion, and liquid in cylinders.
- Remove spark plugs on spark-ignition engines.
- Add a small amount of suitable penetrating or assembly lubricant to cylinders.
- Wait 24–48 hours where appropriate.
- Turn the crankshaft by hand with a suitable socket. Stop at hard resistance; do not convert a stuck piston into a surprise connecting-rod sculpture.

The supplied restoration protocol identifies dry rings, dry bearings, seized valvetrain parts, and incorrect timing as major catastrophic risks. [file:2]

### 3. Replace contaminated fluids

- Drain stale petrol. The source material gives a rough petrol shelf life of three to six months before varnish and oxidation become serious problems.
- Replace engine oil and filter.
- Flush degraded coolant.
- Replace fuel filters and inspect tank sediment.
- Treat old ethanol-blended fuel as especially suspect for moisture and corrosion.

### 4. Clean the carburettor carefully

The supplied cleaning method is a low-caustic hot-water bath for compatible, disassembled parts:

- Photograph settings and count mixture-screw turns before removal.
- Remove jets, float, needle, gaskets, linkages, and parts that should not be heated.
- Use a thermostatically monitored bath around 93°C / 200°F, not an uncontrolled boil.
- Soak for roughly 20–30 minutes in mild detergent/degreaser.
- Scrub with a soft brush.
- Clear calibrated passages with soft nylon line and dry with clean compressed air.
- Do not use abrasive wire tools as files in jets; enlarging a calibrated passage changes fuelling.
- Replace damaged seals and gaskets.

This method removes deposits, not necessarily aluminium staining. [file:3]

### 5. Check the electrical system

The “spark” branch of diagnosis includes:

- battery state and clean terminals;
- starter engagement and current draw;
- ignition-coil resistance against the engine’s specification;
- plug condition and gap;
- continuity and insulation of high-tension leads;
- distributor, rotor, cap, points, or electronic trigger;
- proper engine ground paths.

A spark must be tested safely away from fuel vapour, using the correct tester and procedure. Do not hold a plug lead in your hand to “see if it sparks.” That is not diagnostics; that is volunteering for a nervous-system reboot.

### 6. Confirm air, compression, and timing

An engine that cranks but does not run needs the classic three checks:

```text
fuel/air mixture + compression + correctly timed ignition
```

Inspect intake hoses, manifold gaskets, PCV hoses, and throttle bodies for leaks. Use a proper smoke test rather than spraying flammable substances around a hot engine. Perform a compression test if the engine’s condition permits. Align crankshaft and camshaft marks at the correct number-one TDC position. Interference engines can bend valves if timing is wrong. [file:13][file:14]

### 7. First start

- Start outdoors, clear of people, fuel stores, and combustible vegetation.
- Use fresh, correct fuel.
- Confirm oil pressure as soon as the engine runs.
- Watch for leaks, abnormal noise, runaway speed, smoke, overheating, and exhaust direction.
- Blue smoke suggests oil; white smoke can indicate coolant or condensation; black smoke often indicates over-fuelling, but diagnosis must consider the engine type and conditions.
- Do not immediately load an engine that has just survived resurrection.
- Change oil and filter again after the initial run-in interval if contamination was expected.

For engines dormant for decades, the supplied protocol recommends teardown rather than assuming a key-start will be successful. [file:2]

---

# Part VI — Maintenance field cards

| Interval | Petrol/diesel engine | Steam/boiler system | Electric motor |
|---|---|---|---|
| Before use | Leaks, oil, coolant, belts, guards, fuel, battery | Water level, relief devices, gauges, leaks, burner, feedwater | Cables, insulation, cooling, bearings, guards |
| Daily/each run | Temperature, oil pressure, exhaust, vibration, unusual noise | Pressure, water chemistry, flame, blowdown, leaks | Current, temperature, vibration, smell |
| Periodic | Filters, plugs/injectors, valve clearance, timing belt/chain | Inspection, scale removal, relief-device testing by competent person | Bearing lubrication, insulation tests, alignment |
| Storage | Stabilise or drain fuel; oil protection; dry intake/exhaust; rotate as appropriate | Drain/protect against corrosion; inspect before firing | Keep dry; prevent condensation; exercise bearings |
| After contamination | Flush fuel/oil/coolant systems | Isolate, depressurise, inspect | Isolate electrically; clean and test insulation |

Never defeat a relief valve, governor, overspeed trip, thermal cut-out, or interlock. The device is not “getting in the way”; it is the one component that has read the incident report.

---

# Part VII — Steam, electricity, and working fluid systems

## Steam

Steam is an external-combustion system:

```text
fuel + air → furnace heat → boiler water → steam pressure
→ piston or turbine → condenser/exhaust → feedwater return
```

The boiler is the critical hazard. Homemade pressure vessels are not a beginner project. The UK pressure-systems guidance stresses suitable construction, limiting devices, pressure gauges, relief valves, inspection, and competent operation. [web:24][web:28][web:31]

For safe learning, use:

- low-pressure educational models designed and certified for the purpose;
- open, non-pressurised solar or water-heating demonstrations;
- commercially manufactured boilers with documented operating limits;
- simulations of Rankine-cycle efficiency rather than improvised boilers.

## Electricity and ignition

A basic spark-ignition chain is:

```text
battery/alternator → switch/control → ignition coil primary
→ magnetic field collapse → high voltage secondary
→ plug gap → spark → combustion
```

An alternator is itself an engine accessory: mechanical rotation creates changing magnetic flux, inducing electrical current. It needs regulation to avoid overcharging the battery and damaging loads.

A safe low-energy project is to model this chain with a current-limited bench supply, an ignition module designed for education, and a commercial spark tester. Do not build high-voltage ignition circuits on a breadboard or near fuel.

## Electric drive

Electric motors reverse the generator relationship. Current through windings creates magnetic fields; interaction with permanent magnets or another field produces torque. Motor speed depends on applied voltage, load, winding design, controller strategy, and back-EMF. A battery-electric drivetrain usually contains:

```text
battery → fuse/contactors → inverter/controller → motor → reduction gear
         ↘ battery-management system ↗
```

Electric drive can be extremely efficient and controllable, but batteries require careful charging, thermal management, isolation, and fire planning.

---

# Part VIII — Power transmission and locomotion

The engine rarely drives the final load directly.

```text
engine → clutch/coupling → gearbox or reduction drive
→ differential/final drive → axle/wheel
```

- **Gearbox:** trades speed for torque. Low gear multiplies torque and reduces output speed; high gear does the opposite.
- **Clutch:** allows an engine to run while the load is stationary and smooths engagement.
- **Differential:** lets driven wheels rotate at different speeds in a turn.
- **Belt drive:** cheap and forgiving, but can slip and needs guarding.
- **Chain drive:** positive engagement, but requires lubrication and alignment.
- **Direct drive:** efficient and mechanically simple, but demands a suitable engine speed and load.
- **Generator coupling:** match engine speed to alternator requirements, use a governor, and protect against overspeed.

For rail and road travel, energy must be budgeted for rolling resistance, aerodynamic drag, gradients, payload, acceleration, and weather. A low-speed diesel may be excellent at pulling a heavy train and terrible at making a lightweight vehicle feel lively. A high-speed petrol engine may be the reverse.

---

# Part IX — Advanced engines, briefly and honestly

## Diesel

A diesel compresses air until it is hot, then injects fuel. There is no premixed spark-ignition charge in the basic cycle. High compression and high injection pressures demand strong pistons, rods, bearings, and a very clean fuel system. Diesel engines tend to be heavier and slower than petrol engines but deliver strong low-speed torque and better sustained-load efficiency.

## Atkinson and Miller cycles

Valve timing can make the effective compression stroke shorter than the expansion stroke. This improves efficiency at the expense of specific power, making the approach attractive in hybrids where an electric motor can provide transient acceleration.

## Turbochargers and superchargers

- A **turbocharger** uses exhaust energy to drive a compressor.
- A **supercharger** is mechanically driven by the engine.
- An intercooler reduces charge temperature and increases density.

More oxygen permits more fuel, but also increases cylinder pressure, heat, knock risk, and mechanical loading. Boost is not free horsepower; it is a loan from the parts department.

## Variable valve timing

Variable cam timing changes when valves open and close to improve low-speed torque, high-speed breathing, emissions, or efficiency. Variable lift and multi-stage systems push this further. Timing errors in interference engines can cause piston–valve contact.

## Wankel rotary

A roughly triangular rotor turns eccentrically in a housing. It offers compactness and smoothness but depends heavily on apex and side seals, has unusual chamber geometry, and presents heat and emissions challenges.

## Gas turbines, afterburners, ramjets, and scramjets

These systems belong in the advanced theory tier:

```text
air intake → compressor or ram compression → combustor
→ turbine/nozzle → shaft power or thrust
```

A turbojet makes thrust by accelerating mass rearwards. A turboprop extracts much of the gas energy into a propeller. A ramjet has no compressor; forward speed compresses the air. A scramjet keeps supersonic airflow through the combustor and operates only in specialised high-speed regimes. These are not sensible home workshop builds: rotating parts, hot sections, fuel systems, acoustics, and failure energies are severe.

The FAA notes that turbine engines must remain within limiting temperatures, rotational speeds, and—where applicable—torque. [web:20]

---

# Part X — Projects, ranked by survivability

## Project 1: Four-stroke cycle simulator

Use Python to visualise crank angle, piston position, and valve states. This is safe, useful, and contains zero opportunities for a flywheel to escape.

```python
import math
import matplotlib.pyplot as plt

stroke = 0.086       # m
rod = 0.143          # m
rpm = 1800
angles = list(range(0, 721))

# Crank angle 0 = TDC; slider-crank piston position from TDC.
def piston_down(theta):
    r = stroke / 2
    return r * (1 - math.cos(theta)) + rod - math.sqrt(rod**2 - (r * math.sin(theta))**2)

def phase(theta):
    a = theta % 720
    if a < 180:
        return "intake"
    if a < 360:
        return "compression"
    if a < 540:
        return "power"
    return "exhaust"

theta = [math.radians(a) for a in angles]
pos = [piston_down(t) * 1000 for t in theta]
colours = {"intake": "tab:blue", "compression": "tab:orange",
           "power": "tab:red", "exhaust": "tab:green"}

plt.figure(figsize=(12, 4))
for i in range(len(angles) - 1):
    plt.plot(angles[i:i+2], pos[i:i+2], color=colours[phase(angles[i])], linewidth=3)
for x, label in [(90, "intake"), (270, "compression"),
                 (450, "power"), (630, "exhaust")]:
    plt.axvline(x, color="0.75", linewidth=0.8)
    plt.text(x + 5, max(pos) * 0.92, label, rotation=90)
plt.xlabel("Crank angle (degrees)")
plt.ylabel("Piston distance below TDC (mm)")
plt.title("One four-stroke cycle: the tiny apocalypse inside the cylinder")
plt.tight_layout()
plt.show()
```

## Project 2: Torque and power calculator

```python
def power_kw(torque_nm, rpm):
    return torque_nm * rpm / 9550

for rpm in (800, 1500, 3000, 6000):
    print(rpm, round(power_kw(100, rpm), 2), "kW at 100 Nm")
```

## Project 3: Engine fault-tree notebook

Record symptoms, measurements, and changes. Do not change five things and then declare victory based on vibes.

```text
symptom → measurement → hypothesis → one change → repeat measurement
```

## Project 4: Cutaway teaching model

Use cardboard, foam, transparent plastic, or a non-running donated engine. Mark TDC, BDC, intake, compression, power, and exhaust. Add coloured arrows for air, fuel, oil, coolant, and exhaust.

## Project 5: Belt-and-pulley transmission

Build only a low-speed, guarded demonstrator using a hand crank or low-voltage motor. Measure speed ratio and torque qualitatively. Guard every pinch point.

## Project 6: Commercial educational steam model

Use a certified low-pressure kit exactly as supplied. Do not substitute a homemade boiler, sealed tube, pressure cooker, bottle, or “it held water yesterday” vessel.

## Project 7: Gasifier theory model

Do not begin with a live producer-gas system. Model mass flow, moisture, filtration, and power derating on paper or in code. If later studying a real system, use a professionally reviewed design, outdoor operation, CO monitoring, relief behaviour, and competent supervision.

---

# Part XI — Troubleshooting: the survivor’s diagnostic tree

## Cranks but does not run

```text
fuel present? ── no → repair supply
      │ yes
correct fuel/air ratio? ── no → clean, meter, inspect leaks
      │ yes
compression? ── no → inspect valves, rings, gasket, timing
      │ yes
spark at correct time? ── no → repair ignition/timing
      │ yes
check flooding, exhaust blockage, sensor/control faults, and safety interlocks
```

## Runs badly

- **Backfire through intake:** ignition timing, lean mixture, valve timing, or valve condition.
- **Black smoke:** over-fuelling, restricted air, injector/carburettor fault.
- **Blue smoke:** oil entering combustion chamber or excessive crankcase oil.
- **White smoke:** coolant, water, or cold condensation; persistent white smoke requires diagnosis.
- **Hunting idle:** vacuum leak, governor problem, mixture instability, or control fault.
- **Overheating:** low coolant, blocked radiator, failed pump, lean mixture, ignition timing, load, or airflow.
- **Knock:** wrong fuel, excessive compression/boost, advanced timing, overheating, deposits, or inadequate octane.
- **Vibration:** misfire, imbalance, loose mount, bent shaft, failed bearing, or unsafe rotating assembly.

## The golden rule

Measurements beat folklore. Compression gauge, tachometer, thermometer, multimeter, current clamp, pressure gauge, leak tester, and a notebook will outperform a heroic amount of random part replacement.

---

# Part XII — Atmosphere, weather, and the outdoors

Engines breathe. Air density changes with altitude, temperature, humidity, and pressure. Less dense air means less oxygen per intake volume and usually less available power unless the engine has a control system or forced induction capable of compensating.

Weather affects:

- cold-start fuel vaporisation;
- battery performance;
- lubrication viscosity;
- cooling-air temperature;
- intake-water ingestion;
- filter loading with dust or ash;
- exhaust dispersion in still air and inversion layers;
- corrosion from salt and humidity;
- traction and rolling resistance.

An inversion can trap exhaust near the ground. A quiet engine is not necessarily a safe engine; carbon monoxide does not care whether the sky looks dramatic.

Lightning and wet conditions increase electrical and fuel-system hazards. Keep generators away from dwellings, windows, vents, and doors. Route exhaust so it cannot be drawn indoors. Store fuel in lawful, approved containers away from ignition and living areas.

---

# Part XIII — The world-restart workshop

If society has fallen over, prioritise machines by capability rather than glamour:

1. Hand tools and measuring tools.
2. Water pumps and filtration.
3. Small repairable engines.
4. Battery charging and low-voltage electrical systems.
5. Generators and belt drives.
6. Milling, sawing, drilling, and agricultural machinery.
7. Transport engines and drivetrain repair.
8. Larger steam, diesel, turbine, and industrial systems.
9. Precision manufacturing, metallurgy, and machine tools.

Preserve:

- service manuals and parts diagrams;
- standard fasteners and seals;
- lubricants and corrosion inhibitors;
- spark plugs, filters, belts, hose, wire, fuses, bearings, and gaskets;
- multimeters, compression testers, torque tools, gauges, thermometers, and tachometers;
- welding, brazing, machining, casting, and heat-treatment knowledge;
- safe fuel storage and water-treatment knowledge;
- notebooks containing every successful measurement and modification.

The engine is only half the civilisation. The other half is the workshop that can measure, repair, align, clean, lubricate, and teach.

---

# Appendix A — Quick reference numbers from the source bundle

| Item | Indicative value | Caveat |
|---|---:|---|
| Typical petrol thermal efficiency cited | ~30% | Depends heavily on load and design |
| Diesel benchmark cited | ~40–45% | Broad theoretical/representative range |
| Petrol shelf life in supplied material | 3–6 months | Storage, formulation, temperature, and container matter |
| Dormant-cylinder lubricant dwell | 24–48 hours | More time may be needed for severe seizure |
| Carburettor hot-water cleaning limit | 93°C / 200°F | Only for compatible parts; use temperature control |
| Carburettor cleaning soak | 20–30 minutes | Inspect materials and gaskets |
| Example ethanol jet enlargement | 20–40% diameter in supplied guide | Historical example; tune by measurement |
| Example ethanol timing | Up to ~22° BTDC in supplied guide | Never copy blindly; detonation and engine design matter |
| Wood-gas engine power | Roughly 30% lower than petrol in supplied material | Gas quality and engine setup dominate |
| Simple-Fire stated range | 2–20 hp | Experimental design, not a certification |

---

# Appendix B — What this edition does not pretend to contain

This foundation draft does not provide a safe from-scratch manufacturing recipe for:

- crankshafts, connecting rods, pistons, rings, or cylinder liners;
- certified boilers or pressure vessels;
- high-pressure diesel injection systems;
- operational jet, ramjet, scramjet, rocket, or afterburner hardware;
- industrial fuel distillation or chemical synthesis;
- military or police weaponisation;
- unreviewed high-voltage systems;
- a universal RPM, temperature, pressure, or torque limit.

Those subjects require material specifications, fatigue analysis, thermal analysis, machining tolerances, inspection, certification, and application-specific data. “The apocalypse made me do it” is not a substitute for a pressure-vessel code.

## Closing principle

Start with a known engine. Make it safe. Make it turn. Make it breathe. Make it lubricate. Make it spark or inject. Make it cool. Then make it work.

Only after that should you ask it to run on the forest, pull a train, charge a settlement, or defeat the undead horde.

**The dead may walk. The engine still needs oil.**
