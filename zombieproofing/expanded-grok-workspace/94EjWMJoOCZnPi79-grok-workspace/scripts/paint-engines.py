"""One-shot painted plates for Zombieproof Engines. Skips files already saved."""
import base64
import json
import os
import pathlib
import urllib.error
import urllib.request

KEY = os.environ["XAI_API_KEY"]
OUT = pathlib.Path("/workspace/artifacts/engines-paint")
OUT.mkdir(parents=True, exist_ok=True)

STYLE = (
    "Cozy storybook illustration painted in soft gouache, visible brushstrokes, "
    "warm cream paper, muted olive drab, rust, charcoal, amber and mint green. "
    "Not a flat vector, not a diagram, not clipart: a fully painted scene that fills the frame, "
    "characters large and close, rich background. A scruffy survivor with round wire-rim glasses, "
    "reddish-brown hair loosely tied, worn olive canvas jacket. Dopey friendly mint-green cartoon zombies, "
    "round and puzzled, no wounds. Gentle humor. Absolutely no text, no letters, no numbers, no logos, "
    "no signs, no speech bubbles, no watermarks, no gore, no blood. "
)

JOBS = [
    ("cover", "2:3", "A dusk workshop. The survivor leans on a rusty single-cylinder stationary engine bolted to a timber bench. A daisy in the oil filler. A hand crank. A guarded belt to a bicycle wheel. Three dopey zombies peer through a broken window, one holding a wrench backwards."),
    ("frontis", "3:4", "A dopey mint zombie peacefully asleep curled against a small warm stationary engine, an old oil can as a pillow, a daisy in the oil filler. The survivor's round glasses rest on the wooden bench. Soft lamplight."),
    ("ch01", "3:2", "Open garage in daylight. The survivor raises one hand to stop a dopey zombie pulling the start cord of a small generator that is still indoors. A plain yellow alarm box on the wall with no markings at all."),
    ("ch02", "3:2", "The survivor at a timber bench with a folded blank map and a tiny toy engine. Three wooden blocks stacked like steps. Two zombies outside stare at a completely blank chalkboard."),
    ("ch03", "3:2", "A small glowing stationary engine on a bench, painted swirls of cool air in and warm exhaust out, no labels. The survivor explains with open hands. A zombie listens, holding a spanner backwards."),
    ("ch04", "3:2", "A clear cutaway teaching model of one cylinder, piston, rod and crank on a bench. Four soft unlabeled color washes in blue, orange, red and green. The survivor turns a hand crank. A zombie counts on its fingers and gets it wrong."),
    ("ch05", "3:2", "A sunny field parade of small machines: a tiny kettle steam engine, an old friendly tractor, a harmless teapot with a daisy in the spout, a small electric motor with a flower. Zombies picnic. The survivor stands like a proud docent. No weapons."),
    ("ch06", "3:2", "The survivor holds a torque wrench beside a heavy flywheel. A zombie spins too fast with soft dizzy swirls, unhurt. A blank dark board with no writing."),
    ("ch07", "3:2", "Outdoors. Fuel cans in rust, olive and amber. Pale vapour drifting from a puddle. The survivor catches a zombie's wrist before a match can be struck. No explosion, no flame touching fuel."),
    ("ch08", "3:2", "A carburettor on the bench, two spare brass jets, calipers. The survivor compares the jets. A zombie offers a bunch of grapes that was not invited."),
    ("ch09", "3:2", "Outdoors, far from any house. Drums and a small open test flame upwind. The survivor stands upwind. Two woozy zombies downwind look at a pale wisp they cannot quite see. No indoor scene."),
    ("ch10", "3:2", "A rusty dormant engine in a shed. A cute mouse on the block. The survivor photographs the linkages with a small camera. A cobwebbed zombie sleeps in the corner."),
    ("ch11", "3:2", "First start outdoors. Exhaust smoke drifts away from the house. The survivor listens, cautious and pleased. A zombie wears ear defenders on sideways. Daylight, grass."),
    ("ch12", "3:2", "A morning bench of tools, a blank clipboard, and a relief valve wearing a tiny painted crown with no letters. The survivor points at the valve with respect. A zombie holds a blank calendar upside down."),
    ("ch13", "3:2", "A tiny certified model steam engine on a table, shiny and small. On a high shelf an ordinary pressure cooker stays closed and unused. The survivor gestures no. A disappointed zombie."),
    ("ch14", "3:2", "A belt drive and a bicycle wheel, fully guarded by a metal screen. The survivor lowers the guard. A curious zombie reaches and is stopped by the guard. No injury."),
    ("ch15", "3:2", "A museum shelf of small models only: a heavy diesel block, a snail-shell turbo, a triangular rotor. The survivor as docent holds up a gentle no. A zombie wants to touch the turbo."),
    ("ch16", "3:2", "A teaching table: a notebook with one colored wavy curve and no numbers or words, a cardboard engine cutaway, a slow hand-crank belt with a guard. Two zombie students watch. No flame."),
    ("ch17", "3:2", "Dawn workshop restarting a small settlement. A water pump, a small engine with a daisy, hand tools, blank tags. The survivor teaches. One polite zombie holds a broom. Hopeful warm light."),
]


def generate(name, aspect, prompt):
    dest = OUT / f"{name}.jpg"
    if dest.exists() and dest.stat().st_size > 20000:
        print("skip", name, dest.stat().st_size)
        return
    body = json.dumps(
        {
            "model": "grok-imagine-image-2.0",
            "prompt": STYLE + prompt,
            "n": 1,
            "aspect_ratio": aspect,
            "resolution": "1k",
            "quality": "medium",
            "response_format": "b64_json",
        }
    ).encode()
    req = urllib.request.Request(
        "https://api.x.ai/v1/images/generations",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {KEY}",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as res:
            data = json.load(res)
    except urllib.error.HTTPError as err:
        detail = err.read()[:400].decode("utf-8", "replace")
        print("FAIL", name, err.code, detail)
        return
    item = data["data"][0]
    if item.get("b64_json"):
        dest.write_bytes(base64.b64decode(item["b64_json"]))
    else:
        urllib.request.urlretrieve(item["url"], dest)
    print("ok", name, dest.stat().st_size)


def main():
    for name, aspect, prompt in JOBS:
        generate(name, aspect, prompt)


if __name__ == "__main__":
    main()
