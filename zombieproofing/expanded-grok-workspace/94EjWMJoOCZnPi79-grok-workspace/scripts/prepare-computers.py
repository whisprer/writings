"""Turn the Computers draft pile into one chapter file per subject."""

import re
from pathlib import Path

RAW = Path("/tmp/computers")
OUT = Path("/workspace/book/computers/source")

# Fullest pass of each subject. Near-duplicates and the unwritten outline stay out.
PICKS = [
    (1, "What Even Is a Computer", "chpt19.md"),
    (2, "From Scavenged Bits to Building Blocks", "chpt2-1.md"),
    (3, "Digital Logic from the Ground Up", "chpt3.md"),
    (4, "The Building Blocks Beneath the Brain", "chpt4a.md"),
    (5, "Building the CPU Core", "chpt5-mkiii.md"),
    (6, "Memory Integration", "chpt10.md"),
    (7, "Peripherals and Serial Communication", "chpt8.md"),
    (8, "Simple Operating Systems", "chpt11.md"),
    (9, "Networking Your Zombieproof Computer", "chpt16.md"),
    (10, "A Hands-On Blueprint", "chpt20.md"),
    (11, "Debugging and Optimizing", "chpt23.md"),
    (12, "Powering Your Zombieproof Computer", "chpt24.md"),
    (13, "Cooling and Enclosure", "chpt29.md"),
    (14, "Expanding and Securing the Network", "chpt33.md"),
    (15, "Writing Resilient Survival Code", "chpt36.md"),
    (16, "A Bootloader and a Shell", "chpt38.md"),
    (17, "Memory Management and Direct Memory Access", "chpt40.md"),
]


def strip_old_title(text: str) -> str:
    lines = text.replace("\r\n", "\n").split("\n")
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and re.match(r"^(?:chapter|hapter)\b", lines[0].strip(), re.I):
        lines.pop(0)
    return "\n".join(lines).strip()


def sweep(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = re.sub(r"Congratulations,?\s*woflfren\s*!", "At this stage", text, flags=re.I)
    text = re.sub(r",?\s*woflfren\b!?", "", text, flags=re.I)
    text = re.sub(
        r"Based on the mouse-project materials you provided, here’s a breakdown:",
        "Here is a practical breakdown:",
        text,
    )
    text = re.sub(r"\s*Next up, cooling and enclosure techniques for physical survival\.", "", text)
    text = re.sub(r"\n+Ready to move towards[\s\S]*\Z", "\n", text)
    text = re.sub(r"\n+Next up[\s\S]*\Z", "\n", text)
    text = re.sub(r"\n+Next steps\?[\s\S]*\Z", "\n", text)
    text = re.sub(r"\n+Next comes the fun part[\s\S]*\Z", "\n", text)
    text = re.sub(r"\n+Onward[\s\S]*\Z", "\n", text)
    text = re.sub(r"Let’s plan that in the next chapter\.", "", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def fix_math(name: str, text: str) -> str:
    def put(pattern: str, repl: str, src: str) -> str:
        return re.sub(pattern, lambda _m: repl, src)

    if name == "chpt3.md":
        text = put(
            r"Half adder adds two single bits\s+A\s+A and\s+B\s+B, outputs a sum and a carry bit\.",
            "A half adder adds two single bits, \\(A\\) and \\(B\\), and outputs a sum and a carry.",
            text,
        )
        text = put(
            r"Sum is like XOR:\s*S\s*=\s*A\s*⊕\s*B\s*S=A⊕B",
            "The sum is the XOR: \\(S = A \\oplus B\\).",
            text,
        )
        text = put(
            r"Carry is AND:\s*C\s*=\s*A\s*⋅\s*B\s*C=A⋅B",
            "The carry is the AND: \\(C = A \\cdot B\\).",
            text,
        )
        text = put(
            r"Full adder takes in\s+A\s+A,\s+B\s+B, and a carry-in\s+C\s+i\s+n\s+C\s+in\s+\.",
            "A full adder takes in \\(A\\), \\(B\\), and a carry-in \\(C_{in}\\).",
            text,
        )
        text = put(
            r"Outputs sum\s+S\s+S and carry-out\s+C\s+o\s+u\s+t\s+C\s+out\s+\.",
            "It outputs a sum \\(S\\) and a carry-out \\(C_{out}\\).",
            text,
        )
        text = put(
            r"Logical formulas:\s*S\s*=\s*A\s*⊕\s*B\s*⊕\s*C\s*i\s*n\s*S=A⊕B⊕C\s*in\s*,\s*"
            r"C\s*o\s*u\s*t\s*=\s*\(\s*A\s*⋅\s*B\s*\)\s*\+\s*\(\s*C\s*i\s*n\s*⋅\s*\(\s*A\s*⊕\s*B\s*\)\s*\)\s*"
            r"C\s*out\s*=\(A⋅B\)\+\(C\s*in\s*⋅\(A⊕B\)\)\.",
            "The formulas are \\(S = A \\oplus B \\oplus C_{in}\\) and "
            "\\(C_{out} = (A \\cdot B) + (C_{in} \\cdot (A \\oplus B))\\).",
            text,
        )
    if name == "chpt10.md":
        text = put(
            r"N\s*N address lines give\s*2\s*N\s*2\s*N\s*unique addresses\.",
            "\\(N\\) address lines give \\(2^{N}\\) unique addresses.",
            text,
        )
    return text


def fence_code(text: str) -> str:
    """The code scrap arrived as a chat paste with bare language tags."""
    if "ldi sp, STACK_TOP" not in text and "void shell_loop" not in text:
        return text
    text = re.sub(r"^(text|c)\s*$", "", text, flags=re.M)

    def grab(src: str, start_pat: str, end_pat: str, lang: str) -> str:
        m = re.search(start_pat + r"[\s\S]*?" + end_pat, src)
        if not m:
            return src
        body = m.group(0).strip("\n")
        return src[: m.start()] + f"\n```{lang}\n{body}\n```\n" + src[m.end() :]

    text = grab(text, r"; Initialize stack", r"jmp main_entry", "text")
    text = grab(text, r"void shell_loop\(\)", r"\n\}", "c")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for n, title, src_name in PICKS:
        raw = (RAW / src_name).read_text()
        if src_name == "chpt38.md":
            body = raw.strip()
        else:
            body = strip_old_title(raw)
        body = fence_code(fix_math(src_name, sweep(body)))
        doc = (
            "# Zombieproof Computers: How to Keep a Mind When the Grid Is Gone\n\n"
            f"Chapter {n}: {title}\n\n"
            f"{body.strip()}\n"
        )
        (OUT / f"chpt{n}.md").write_text(doc)
        print(f"chpt{n}.md  {src_name}  {len(doc)} chars")


if __name__ == "__main__":
    main()
