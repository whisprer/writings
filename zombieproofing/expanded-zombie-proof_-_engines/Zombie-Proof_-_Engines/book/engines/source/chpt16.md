Chapter 16: Seven Projects, Ranked by Whether You Get to Tell Them

The projects are in order of how likely you are to finish the story in person. None of them requires a flywheel at head height. If a project starts to require one, you have left the chapter.

## Project 1: The cycle, drawn and not burned

A small program can show crank angle, piston position, and which stroke you are in. It contains no opportunity for a flywheel to emigrate.

```python
import math
import matplotlib.pyplot as plt

stroke = 0.086  # metres
rod = 0.143
angles = list(range(0, 721))

def piston_down(theta):
    r = stroke / 2
    return (
        r * (1 - math.cos(theta))
        + rod
        - math.sqrt(rod**2 - (r * math.sin(theta)) ** 2)
    )

def phase(theta_deg):
    a = theta_deg % 720
    if a < 180:
        return "intake"
    if a < 360:
        return "compression"
    if a < 540:
        return "power"
    return "exhaust"

theta = [math.radians(a) for a in angles]
pos = [piston_down(t) * 1000 for t in theta]
colours = {
    "intake": "tab:blue",
    "compression": "tab:orange",
    "power": "tab:red",
    "exhaust": "tab:green",
}

plt.figure(figsize=(12, 4))
for i in range(len(angles) - 1):
    plt.plot(
        angles[i : i + 2],
        pos[i : i + 2],
        color=colours[phase(angles[i])],
        linewidth=3,
    )
plt.xlabel("Crank angle (degrees)")
plt.ylabel("Piston distance below top dead centre (mm)")
plt.title("One four-stroke cycle")
plt.tight_layout()
plt.show()
```

Crank angle zero is top dead centre. The curve is the whole sermon: two turns, one push, three strokes carried by the flywheel you wisely did not bolt to the desk.

## Project 2: A sum you can do in your head, almost

```python
def power_kw(torque_nm, rpm):
    return torque_nm * rpm / 9550

for rpm in (800, 1500, 3000, 6000):
    print(rpm, round(power_kw(100, rpm), 2), "kW at 100 Nm")
```

A hundred newton-metres at eight hundred revolutions is not the same animal as a hundred newton-metres at six thousand. The second one is faster and hotter and more interested in breaking something. Write both numbers down before you boast.

## Project 3: A fault tree that is only a notebook

```text
symptom → measurement → one hypothesis → one change → measure again
```

Do not change five things and declare victory on the grounds of vibes. Vibes are how the original fault hides behind the new one.

## Project 4: A cutaway that does not run

Cardboard, foam, a bit of clear plastic, or a donated engine that will never be asked to fire. Mark top and bottom dead centre. Mark the four strokes. Add coloured arrows for air, fuel, oil, coolant, and exhaust. If a child, or a tired adult, can point at the power stroke without your help, the model has earned its keep.

## Project 5: A belt, guarded, and slow

A hand crank or a low-voltage motor. A speed ratio you can measure. Every pinch point behind a guard before the first turn. If you cannot put the guard on, you do not have a project. You have a dare, and this book does not sign dares.

## Project 6: Someone else's steam

A certified low-pressure model, used exactly as it was supplied. No homemade boiler. No sealed tube. No pressure cooker with a dream. No bottle. No vessel that "held" yesterday. If the kit is incomplete, the project is incomplete, and you stop.

## Project 7: A gasifier that is only a sum

Do not start with a live producer-gas rig. Model the flow, the moisture, the filtering, and the power you will not get, on paper or in code. If a real system ever enters your life, it should be a design that a competent person has reviewed, run outdoors, watched with a carbon-monoxide alarm, built with real relief behaviour, and supervised by someone who can tell you to shut it down. Until that person exists, the model on the page is the whole project.

The plate shows the notebook curve, the cardboard lump, and the hand crank. The students are welcome. The flame is not.
