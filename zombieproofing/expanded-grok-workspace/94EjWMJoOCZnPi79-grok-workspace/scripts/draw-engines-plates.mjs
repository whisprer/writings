import { chromium } from "playwright";
import fs from "node:fs";
import path from "node:path";

const OUT = "/workspace/public/book/engines/art";
fs.mkdirSync(OUT, { recursive: true });

const P = {
  cream: "#f4ead7",
  sky: "#efe2c8",
  floor: "#d9c7a4",
  olive: "#3e4a32",
  olive2: "#667352",
  olive3: "#2a3224",
  rust: "#c2512a",
  rust2: "#8d3818",
  char: "#241c16",
  amber: "#e2a44a",
  mint: "#c5ddb8",
  mint2: "#8fb888",
  mint3: "#5e8664",
  skin: "#f2c7a2",
  skin2: "#e2aa7c",
  hair: "#8a4328",
  hair2: "#5c2b18",
  jacket: "#6e7c55",
  jacket2: "#556242",
  trouser: "#3d3832",
  boot: "#241c16",
  metal: "#8e9491",
  metal2: "#5e6562",
  rustmetal: "#7a5340",
  paper: "#fbf6ec",
  glass: "#d5ebe8",
};

function grain() {
  return `
  <defs>
    <filter id="g" x="-20%" y="-20%" width="140%" height="140%">
      <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="4" result="n"/>
      <feColorMatrix in="n" type="saturate" values="0" result="m"/>
      <feComponentTransfer in="m" result="a"><feFuncA type="linear" slope="0.055"/></feComponentTransfer>
      <feBlend in="SourceGraphic" in2="a" mode="multiply"/>
    </filter>
    <linearGradient id="wall" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#f6edd9"/>
      <stop offset="100%" stop-color="#e4d2b0"/>
    </linearGradient>
    <radialGradient id="lamp" cx="30%" cy="18%" r="55%">
      <stop offset="0%" stop-color="#fff6df" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#e4d2b0" stop-opacity="0"/>
    </radialGradient>
  </defs>`;
}

function stage(w, h, inner) {
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">
${grain()}
<g filter="url(#g)">
<rect width="${w}" height="${h}" fill="url(#wall)"/>
<rect width="${w}" height="${h}" fill="url(#lamp)"/>
${inner}
</g>
</svg>`;
}

function ground(w, h, y) {
  return `<ellipse cx="${w / 2}" cy="${y}" rx="${w * 0.46}" ry="28" fill="#cbb892" opacity="0.55"/>`;
}

function daisy(x, y, s = 1) {
  const petals = Array.from({ length: 8 }, (_, i) => {
    const a = (i / 8) * Math.PI * 2;
    return `<ellipse cx="${Math.cos(a) * 7 * s}" cy="${Math.sin(a) * 7 * s}" rx="${4.2 * s}" ry="${2.2 * s}" transform="rotate(${(a * 180) / Math.PI})" fill="#f7f3e8"/>`;
  }).join("");
  return `<g transform="translate(${x} ${y})">${petals}<circle r="${3.3 * s}" fill="${P.amber}"/></g>`;
}

function survivor(x, y, sc = 1, pose = {}) {
  const arm = pose.arm || "down";
  const flip = pose.flip ? -1 : 1;
  const expr = pose.expr || "smile";
  let arms = "";
  if (arm === "down") {
    arms = `
      <path d="M-22 -90 C-40 -84 -46 -118 -34 -128" fill="none" stroke="${P.jacket2}" stroke-width="16" stroke-linecap="round"/>
      <ellipse cx="-34" cy="-132" rx="9" ry="8" fill="${P.skin}"/>
      <path d="M22 -90 C40 -84 48 -118 36 -128" fill="none" stroke="${P.jacket}" stroke-width="16" stroke-linecap="round"/>
      <ellipse cx="36" cy="-132" rx="9" ry="8" fill="${P.skin}"/>`;
  } else if (arm === "stop") {
    arms = `
      <path d="M-22 -90 C-40 -86 -44 -120 -32 -130" fill="none" stroke="${P.jacket2}" stroke-width="16" stroke-linecap="round"/>
      <ellipse cx="-32" cy="-134" rx="9" ry="8" fill="${P.skin}"/>
      <path d="M18 -96 C28 -130 22 -162 8 -176" fill="none" stroke="${P.jacket}" stroke-width="16" stroke-linecap="round"/>
      <ellipse cx="4" cy="-184" rx="11" ry="10" fill="${P.skin}"/>`;
  } else if (arm === "lean") {
    arms = `
      <path d="M-22 -90 C-36 -88 -34 -122 -22 -128" fill="none" stroke="${P.jacket2}" stroke-width="16" stroke-linecap="round"/>
      <ellipse cx="-20" cy="-132" rx="9" ry="8" fill="${P.skin}"/>
      <path d="M20 -88 C55 -92 90 -104 108 -108" fill="none" stroke="${P.jacket}" stroke-width="16" stroke-linecap="round"/>
      <ellipse cx="114" cy="-108" rx="10" ry="8" fill="${P.skin}"/>`;
  } else if (arm === "point") {
    arms = `
      <path d="M-22 -90 C-40 -84 -42 -120 -30 -128" fill="none" stroke="${P.jacket2}" stroke-width="16" stroke-linecap="round"/>
      <ellipse cx="-30" cy="-132" rx="9" ry="8" fill="${P.skin}"/>
      <path d="M22 -90 C52 -86 78 -90 104 -86" fill="none" stroke="${P.jacket}" stroke-width="16" stroke-linecap="round"/>
      <ellipse cx="110" cy="-86" rx="9" ry="8" fill="${P.skin}"/>`;
  } else if (arm === "photo") {
    arms = `
      <path d="M-8 -92 C0 -88 8 -100 4 -112" fill="none" stroke="${P.jacket}" stroke-width="16" stroke-linecap="round"/>
      <rect x="-12" y="-128" width="28" height="18" rx="3" fill="${P.char}"/>
      <circle cx="2" cy="-119" r="5" fill="${P.glass}"/>
      <path d="M-24 -90 C-42 -96 -44 -122 -32 -128" fill="none" stroke="${P.jacket2}" stroke-width="14" stroke-linecap="round"/>
      <ellipse cx="-32" cy="-132" rx="8" ry="7" fill="${P.skin}"/>`;
  } else if (arm === "catch") {
    arms = `
      <path d="M18 -92 C48 -80 74 -64 96 -52" fill="none" stroke="${P.jacket}" stroke-width="16" stroke-linecap="round"/>
      <ellipse cx="102" cy="-50" rx="10" ry="8" fill="${P.skin}"/>
      <path d="M-22 -90 C-40 -86 -42 -120 -30 -128" fill="none" stroke="${P.jacket2}" stroke-width="16" stroke-linecap="round"/>
      <ellipse cx="-30" cy="-132" rx="9" ry="8" fill="${P.skin}"/>`;
  }
  const mouth =
    expr === "focus"
      ? `<path d="M-6 -148 Q0 -146 7 -148" stroke="${P.rust2}" fill="none" stroke-width="1.6" stroke-linecap="round"/>`
      : `<path d="M-7 -150 Q1 -143 8 -150" stroke="${P.rust2}" fill="none" stroke-width="1.7" stroke-linecap="round"/>`;
  return `<g transform="translate(${x} ${y}) scale(${flip * sc} ${sc})">
    <ellipse cx="0" cy="6" rx="36" ry="8" fill="#c3ad88" opacity="0.7"/>
    <path d="M-16 -8 L-18 -52 L-6 -52 L-4 -8 Z" fill="${P.trouser}"/>
    <path d="M6 -8 L8 -52 L20 -52 L22 -8 Z" fill="${P.trouser}"/>
    <ellipse cx="-16" cy="-4" rx="12" ry="7" fill="${P.boot}"/>
    <ellipse cx="18" cy="-4" rx="12" ry="7" fill="${P.boot}"/>
    <path d="M-34 -56 C-38 -110 -20 -128 0 -126 C22 -128 40 -108 36 -56 C22 -44 -22 -44 -34 -56 Z" fill="${P.jacket}"/>
    <path d="M-8 -120 L0 -78 L8 -120 Z" fill="${P.jacket2}"/>
    <path d="M-16 -112 Q0 -100 16 -112 L12 -96 Q0 -88 -12 -96 Z" fill="${P.skin2}"/>
    ${arms}
    <ellipse cx="0" cy="-158" rx="26" ry="28" fill="${P.skin}"/>
    <path d="M-24 -160 C-30 -198 -8 -214 2 -210 C20 -216 32 -190 24 -158 C18 -176 4 -184 -8 -178 C-18 -184 -22 -170 -24 -160 Z" fill="${P.hair}"/>
    <path d="M18 -186 C28 -176 26 -158 16 -156" fill="${P.hair2}"/>
    <circle cx="-10" cy="-158" r="8" fill="none" stroke="${P.char}" stroke-width="1.7"/>
    <circle cx="10" cy="-158" r="8" fill="none" stroke="${P.char}" stroke-width="1.7"/>
    <path d="M-2 -158 H2" stroke="${P.char}" stroke-width="1.5"/>
    <circle cx="-10" cy="-158" r="2.2" fill="${P.char}"/>
    <circle cx="10" cy="-158" r="2.2" fill="${P.char}"/>
    <path d="M-1 -152 Q2 -148 5 -152" stroke="${P.skin2}" fill="none" stroke-width="1.4"/>
    ${mouth}
  </g>`;
}

function zombie(x, y, sc = 1, pose = {}) {
  const flip = pose.flip ? -1 : 1;
  const kind = pose.kind || "stand";
  let extra = "";
  if (kind === "dizzy") {
    extra = `<path d="M-18 -210 C-6 -226 10 -214 4 -200" fill="none" stroke="${P.amber}" stroke-width="3" stroke-linecap="round"/>
      <path d="M8 -214 C18 -228 32 -214 22 -202" fill="none" stroke="${P.amber}" stroke-width="3" stroke-linecap="round"/>`;
  }
  if (kind === "sleep") {
    return `<g transform="translate(${x} ${y}) scale(${flip * sc} ${sc})">
      <ellipse cx="20" cy="0" rx="70" ry="16" fill="#c3ad88" opacity="0.65"/>
      <ellipse cx="10" cy="-28" rx="62" ry="26" fill="${P.mint2}"/>
      <ellipse cx="46" cy="-36" rx="28" ry="24" fill="${P.mint}"/>
      <path d="M62 -48 Q78 -30 60 -22" fill="${P.mint3}"/>
      <path d="M36 -40 Q40 -36 46 -40" stroke="${P.mint3}" fill="none" stroke-width="1.5"/>
      <path d="M50 -38 Q54 -34 58 -38" stroke="${P.mint3}" fill="none" stroke-width="1.5"/>
      <path d="M42 -30 Q50 -26 58 -30" stroke="${P.rust2}" fill="none" stroke-width="1.4"/>
      <ellipse cx="-20" cy="-16" rx="10" ry="7" fill="${P.mint3}"/>
    </g>`;
  }
  const armL =
    kind === "reach"
      ? `<path d="M18 -90 C46 -70 72 -48 92 -36" fill="none" stroke="${P.mint2}" stroke-width="14" stroke-linecap="round"/><ellipse cx="98" cy="-32" rx="9" ry="8" fill="${P.mint}"/>`
      : kind === "wrongwrench"
        ? `<path d="M16 -92 C34 -80 40 -108 32 -118" fill="none" stroke="${P.mint2}" stroke-width="14" stroke-linecap="round"/><ellipse cx="30" cy="-124" rx="8" ry="7" fill="${P.mint}"/><rect x="22" y="-150" width="8" height="30" rx="2" fill="${P.metal2}" transform="rotate(25 26 -135)"/>`
        : `<path d="M-20 -90 C-38 -78 -40 -114 -28 -124" fill="none" stroke="${P.mint3}" stroke-width="14" stroke-linecap="round"/><ellipse cx="-28" cy="-128" rx="8" ry="7" fill="${P.mint}"/>`;
  const armR =
    kind === "wrongwrench" || kind === "reach"
      ? `<path d="M-20 -90 C-36 -80 -34 -116 -24 -124" fill="none" stroke="${P.mint3}" stroke-width="14" stroke-linecap="round"/><ellipse cx="-24" cy="-128" rx="8" ry="7" fill="${P.mint}"/>`
      : `<path d="M18 -90 C36 -78 42 -114 30 -124" fill="none" stroke="${P.mint2}" stroke-width="14" stroke-linecap="round"/><ellipse cx="32" cy="-128" rx="8" ry="7" fill="${P.mint}"/>`;
  const eyes =
    kind === "woozy"
      ? `<ellipse cx="-9" cy="-156" rx="6" ry="3" fill="#f4faf2"/><ellipse cx="10" cy="-154" rx="6" ry="3" fill="#f4faf2"/>
         <circle cx="-8" cy="-155" r="1.6" fill="${P.char}"/><circle cx="12" cy="-153" r="1.6" fill="${P.char}"/>`
      : kind === "peek"
        ? `<ellipse cx="-9" cy="-156" rx="6.5" ry="6" fill="#f7fbf6"/><ellipse cx="10" cy="-156" rx="6.5" ry="6" fill="#f7fbf6"/>
           <circle cx="-8" cy="-156" r="2.4" fill="${P.char}"/><circle cx="12" cy="-156" r="2.4" fill="${P.char}"/>`
        : `<path d="M-16 -158 Q-9 -152 -2 -158" fill="#f7fbf6"/><path d="M4 -158 Q11 -152 18 -158" fill="#f7fbf6"/>
           <circle cx="-9" cy="-155" r="2" fill="${P.char}"/><circle cx="11" cy="-155" r="2" fill="${P.char}"/>
           <path d="M-16 -160 Q-9 -166 -2 -160" fill="${P.mint}"/><path d="M4 -160 Q11 -166 18 -160" fill="${P.mint}"/>`;
  return `<g transform="translate(${x} ${y}) scale(${flip * sc} ${sc})">
    <ellipse cx="0" cy="4" rx="34" ry="8" fill="#c3ad88" opacity="0.65"/>
    <path d="M-14 -6 L-16 -48 L-4 -48 L-2 -6 Z" fill="${P.mint3}"/>
    <path d="M6 -6 L8 -48 L20 -48 L22 -6 Z" fill="${P.mint3}"/>
    <ellipse cx="-14" cy="-2" rx="11" ry="6" fill="${P.olive3}"/>
    <ellipse cx="16" cy="-2" rx="11" ry="6" fill="${P.olive3}"/>
    <ellipse cx="2" cy="-78" rx="32" ry="36" fill="${P.mint2}"/>
    ${armL}${armR}
    <ellipse cx="2" cy="-150" rx="30" ry="28" fill="${P.mint}"/>
    <path d="M-20 -166 C-16 -196 24 -198 26 -164 C16 -180 0 -184 -10 -176 C-18 -182 -22 -172 -20 -166" fill="${P.mint3}" opacity="0.85"/>
    ${eyes}
    <path d="M-6 -140 Q2 -134 10 -140" stroke="${P.mint3}" fill="none" stroke-width="1.6" stroke-linecap="round"/>
    ${extra}
  </g>`;
}

function engine(x, y, sc = 1, opt = {}) {
  const rusty = opt.rusty ? P.rustmetal : P.metal2;
  const block = opt.rusty ? "#6a4636" : "#4e5552";
  return `<g transform="translate(${x} ${y}) scale(${sc})">
    <ellipse cx="0" cy="8" rx="70" ry="10" fill="#c3ad88" opacity="0.6"/>
    <rect x="-54" y="-36" width="108" height="40" rx="6" fill="${block}"/>
    <rect x="-40" y="-70" width="52" height="38" rx="5" fill="${rusty}"/>
    <rect x="-30" y="-92" width="32" height="26" rx="4" fill="${P.char}"/>
    <circle cx="58" cy="-16" r="28" fill="${P.olive3}"/>
    <circle cx="58" cy="-16" r="18" fill="${P.metal}"/>
    <circle cx="58" cy="-16" r="5" fill="${P.char}"/>
    <rect x="46" y="-20" width="40" height="8" rx="3" fill="${P.char}" transform="rotate(-28 66 -16)"/>
    <path d="M-8 -92 C-8 -110 10 -114 12 -96" fill="none" stroke="${P.metal}" stroke-width="6" stroke-linecap="round"/>
    ${opt.daisy ? daisy( -14, -98, 1.1) : ""}
    ${opt.crank ? `<path d="M-70 -8 H-96" stroke="${P.char}" stroke-width="6" stroke-linecap="round"/><circle cx="-100" cy="-8" r="7" fill="${P.rust}"/>` : ""}
  </g>`;
}

function bench(x, y, w = 280) {
  return `<g>
    <rect x="${x}" y="${y}" width="${w}" height="16" rx="3" fill="#8a6244"/>
    <rect x="${x + 18}" y="${y + 16}" width="12" height="46" fill="#6d4c34"/>
    <rect x="${x + w - 30}" y="${y + 16}" width="12" height="46" fill="#6d4c34"/>
  </g>`;
}

function windowFrame(x, y, w, h) {
  return `<g>
    <rect x="${x}" y="${y}" width="${w}" height="${h}" rx="4" fill="#c9d7ea"/>
    <path d="M${x} ${y + h * 0.55} Q${x + w * 0.3} ${y + h * 0.2} ${x + w} ${y + h * 0.35} L${x + w} ${y + h} L${x} ${y + h} Z" fill="#b7c6b0" opacity="0.85"/>
    <rect x="${x}" y="${y}" width="${w}" height="${h}" fill="none" stroke="#6d4c34" stroke-width="10"/>
    <path d="M${x + w / 2} ${y} V${y + h}" stroke="#6d4c34" stroke-width="6"/>
    <path d="M${x} ${y + h / 2} H${x + w}" stroke="#6d4c34" stroke-width="6"/>
  </g>`;
}

function jerry(x, y, c) {
  return `<g transform="translate(${x} ${y})">
    <rect x="-16" y="-40" width="32" height="44" rx="4" fill="${c}"/>
    <rect x="-8" y="-48" width="16" height="10" rx="2" fill="${P.char}"/>
    <path d="M-10 -28 H10" stroke="#f4ead7" stroke-width="3" opacity="0.0"/>
  </g>`;
}

const scenes = {
  cover: {
    w: 1000,
    h: 1500,
    svg: () =>
      stage(
        1000,
        1500,
        `
      <rect x="0" y="980" width="1000" height="520" fill="#d7c4a4"/>
      ${windowFrame(620, 180, 300, 360)}
      ${zombie(700, 560, 0.72, { kind: "peek" })}
      ${zombie(820, 590, 0.62, { kind: "peek", flip: 1 })}
      ${zombie(760, 640, 0.55, { kind: "stand" })}
      ${bench(180, 980, 520)}
      ${engine(430, 980, 1.35, { daisy: true, crank: true })}
      ${survivor(250, 1040, 1.15, { arm: "lean" })}
      <rect x="80" y="1180" width="70" height="90" rx="6" fill="${P.olive3}"/>
      <circle cx="115" cy="1210" r="10" fill="${P.amber}"/>
      <path d="M150 150 Q180 80 240 120" stroke="${P.amber}" stroke-width="8" fill="none" opacity="0.35"/>
      `,
      ),
  },
  frontis: {
    w: 1000,
    h: 1330,
    svg: () =>
      stage(
        1000,
        1330,
        `
      <rect y="900" width="1000" height="430" fill="#e4d3b4"/>
      ${bench(220, 860, 560)}
      ${engine(520, 860, 1.5, { daisy: true })}
      ${zombie(430, 860, 1.35, { kind: "sleep" })}
      <ellipse cx="300" cy="820" rx="26" ry="16" fill="${P.rust}"/>
      <rect x="286" y="760" width="10" height="60" rx="3" fill="${P.metal2}"/>
      <circle cx="250" cy="800" r="16" fill="none" stroke="${P.char}" stroke-width="3"/>
      <circle cx="282" cy="800" r="16" fill="none" stroke="${P.char}" stroke-width="3"/>
      <path d="M266 800 H266" stroke="${P.char}" stroke-width="3"/>
      `,
      ),
  },
};

function plate(name, w, h, body) {
  scenes[name] = { w, h, svg: () => stage(w, h, body) };
}

const W = 1500;
const H = 1000;

plate(
  "ch01",
  W,
  H,
  `
  <rect y="640" width="1500" height="360" fill="#dcc9a8"/>
  <rect x="0" y="0" width="460" height="1000" fill="#c9b48e"/>
  <path d="M460 0 L700 80 L700 1000 L460 1000 Z" fill="#efe6d2"/>
  ${engine(1040, 760, 1.15)}
  <rect x="960" y="700" width="200" height="70" rx="8" fill="${P.olive3}"/>
  <circle cx="1120" cy="690" r="16" fill="${P.amber}"/>
  <rect x="180" y="220" width="54" height="70" rx="8" fill="#e2b63a"/>
  <circle cx="207" cy="250" r="8" fill="${P.rust}"/>
  ${survivor(820, 820, 1.35, { arm: "stop" })}
  ${zombie(1180, 860, 1.15, { kind: "reach" })}
  `,
);

plate(
  "ch02",
  W,
  H,
  `
  <rect y="700" width="1500" height="300" fill="#dcc9a8"/>
  ${bench(180, 640, 700)}
  <rect x="240" y="560" width="160" height="90" rx="4" fill="${P.paper}" transform="rotate(-8 320 600)"/>
  <path d="M270 590 Q340 560 390 600" fill="none" stroke="${P.olive2}" stroke-width="3"/>
  ${engine(560, 640, 0.55, { daisy: false })}
  <rect x="700" y="560" width="36" height="22" rx="3" fill="#c4a574"/>
  <rect x="720" y="538" width="36" height="22" rx="3" fill="#b8431f"/>
  <rect x="740" y="516" width="36" height="22" rx="3" fill="${P.olive2}"/>
  ${survivor(360, 820, 1.25, { arm: "point" })}
  <rect x="1080" y="180" width="280" height="200" rx="6" fill="#2c3324"/>
  ${zombie(1160, 560, 0.7, { kind: "peek" })}
  ${zombie(1280, 590, 0.62, { kind: "peek" })}
  `,
);

plate(
  "ch03",
  W,
  H,
  `
  <rect y="690" width="1500" height="310" fill="#dcc9a8"/>
  ${bench(360, 640, 520)}
  ${engine(620, 640, 1.4, { daisy: true })}
  <path d="M470 520 C420 470 400 430 430 400" fill="none" stroke="#9ec4d4" stroke-width="10" stroke-linecap="round" opacity="0.8"/>
  <path d="M760 500 C830 450 860 400 840 360" fill="none" stroke="#e2a44a" stroke-width="10" stroke-linecap="round" opacity="0.75"/>
  ${survivor(280, 830, 1.3, { arm: "point" })}
  ${zombie(1040, 860, 1.2, { kind: "wrongwrench" })}
  `,
);

plate(
  "ch04",
  W,
  H,
  `
  <rect y="700" width="1500" height="300" fill="#dcc9a8"/>
  ${bench(280, 620, 620)}
  <rect x="400" y="360" width="150" height="250" rx="16" fill="#d5ebe8" opacity="0.85"/>
  <rect x="430" y="390" width="90" height="150" rx="8" fill="#c9d7ea" stroke="${P.char}" stroke-width="4"/>
  <rect x="448" y="470" width="54" height="48" rx="6" fill="${P.rust}"/>
  <rect x="470" y="518" width="10" height="70" fill="${P.char}"/>
  <circle cx="475" cy="600" r="22" fill="${P.olive3}"/>
  <circle cx="250" cy="420" r="18" fill="#6ea0c8"/>
  <circle cx="250" cy="480" r="18" fill="#e09a45"/>
  <circle cx="250" cy="540" r="18" fill="#c2512a"/>
  <circle cx="250" cy="600" r="18" fill="#6f8f62"/>
  ${survivor(860, 820, 1.2, { arm: "point" })}
  ${zombie(1120, 860, 1.15, { kind: "stand" })}
  `,
);

plate(
  "ch05",
  W,
  H,
  `
  <rect y="620" width="1500" height="380" fill="#b7c6a4"/>
  <ellipse cx="200" cy="250" rx="160" ry="40" fill="#fff6df" opacity="0.7"/>
  ${engine(160, 640, 0.7)}
  <ellipse cx="150" cy="500" rx="26" ry="18" fill="${P.metal}"/>
  <rect x="138" y="470" width="24" height="30" rx="4" fill="${P.char}"/>
  <rect x="380" y="560" width="150" height="50" rx="8" fill="${P.rust2}"/>
  <circle cx="410" cy="640" r="22" fill="${P.char}"/>
  <circle cx="500" cy="640" r="22" fill="${P.char}"/>
  <ellipse cx="700" cy="600" rx="40" ry="24" fill="${P.paper}"/>
  <path d="M740 590 Q780 540 760 600" fill="${P.paper}"/>
  ${daisy(760, 560, 1.3)}
  <rect x="900" y="580" width="70" height="50" rx="8" fill="${P.metal2}"/>
  <circle cx="935" cy="600" r="12" fill="${P.amber}"/>
  ${daisy(960, 560, 1)}
  ${survivor(1080, 780, 1.15, { arm: "point" })}
  ${zombie(180, 860, 0.85, { kind: "sit" })}
  ${zombie(420, 900, 0.8)}
  `,
);

plate(
  "ch06",
  W,
  H,
  `
  <rect y="680" width="1500" height="320" fill="#dcc9a8"/>
  ${bench(200, 640, 480)}
  <circle cx="420" cy="600" r="70" fill="${P.olive3}"/>
  <circle cx="420" cy="600" r="42" fill="${P.metal}"/>
  <circle cx="420" cy="600" r="10" fill="${P.char}"/>
  <rect x="250" y="560" width="90" height="14" rx="4" fill="${P.rust}" transform="rotate(-20 300 567)"/>
  ${survivor(240, 820, 1.25, { arm: "point" })}
  ${zombie(980, 860, 1.3, { kind: "dizzy" })}
  <rect x="1120" y="240" width="240" height="180" rx="6" fill="#2a3224"/>
  `,
);

plate(
  "ch07",
  W,
  H,
  `
  <rect y="660" width="1500" height="340" fill="#c9b48a"/>
  ${jerry(220, 700, P.rust)}
  ${jerry(280, 710, P.olive2)}
  ${jerry(340, 690, P.amber)}
  <path d="M300 640 C360 600 420 620 480 560" fill="none" stroke="#e7d7a8" stroke-width="14" stroke-linecap="round" opacity="0.8"/>
  ${survivor(620, 820, 1.3, { arm: "catch" })}
  ${zombie(980, 840, 1.2, { kind: "reach" })}
  <rect x="1040" y="640" width="8" height="40" fill="#e8d7b0" transform="rotate(20 1044 660)"/>
  <circle cx="1052" cy="630" r="6" fill="${P.amber}"/>
  `,
);

plate(
  "ch08",
  W,
  H,
  `
  <rect y="690" width="1500" height="310" fill="#dcc9a8"/>
  ${bench(240, 620, 700)}
  <path d="M360 560 Q420 500 500 560 Q440 600 360 560" fill="${P.metal}"/>
  <circle cx="430" cy="545" r="8" fill="${P.char}"/>
  <circle cx="620" cy="590" r="10" fill="${P.amber}"/>
  <circle cx="660" cy="590" r="14" fill="${P.rust}"/>
  <path d="M700 520 L760 470" stroke="${P.metal2}" stroke-width="6"/>
  <path d="M700 540 L770 560" stroke="${P.metal2}" stroke-width="6"/>
  ${survivor(300, 840, 1.2, { arm: "point", expr: "focus" })}
  ${zombie(1100, 860, 1.15)}
  <circle cx="1180" cy="700" r="16" fill="#6a3a78"/>
  <circle cx="1210" cy="720" r="14" fill="#7d4a86"/>
  <path d="M1160 690 Q1140 660 1170 650" stroke="${P.mint3}" fill="none" stroke-width="3"/>
  `,
);

plate(
  "ch09",
  W,
  H,
  `
  <rect y="640" width="1500" height="360" fill="#b7c6a4"/>
  <rect x="180" y="520" width="70" height="140" rx="8" fill="${P.rustmetal}"/>
  <rect x="270" y="560" width="90" height="100" rx="8" fill="${P.metal2}"/>
  <rect x="390" y="500" width="110" height="150" rx="10" fill="${P.olive2}"/>
  <path d="M210 500 C210 440 240 420 250 460" fill="none" stroke="${P.amber}" stroke-width="8" stroke-linecap="round"/>
  <path d="M520 560 C620 500 700 540 760 480" fill="none" stroke="#f4f7f2" stroke-width="16" opacity="0.55" stroke-linecap="round"/>
  ${survivor(560, 820, 1.15, { arm: "stop" })}
  ${zombie(1040, 860, 1.05, { kind: "woozy" })}
  ${zombie(1220, 880, 0.95, { kind: "woozy", flip: 1 })}
  `,
);

plate(
  "ch10",
  W,
  H,
  `
  <rect width="1500" height="1000" fill="#e7dcc4"/>
  <rect y="700" width="1500" height="300" fill="#cbb892"/>
  ${engine(640, 720, 1.45, { rusty: true })}
  <ellipse cx="520" cy="690" rx="16" ry="10" fill="#8d6a52"/>
  <circle cx="512" cy="684" r="6" fill="#f2c7a2"/>
  <circle cx="528" cy="684" r="6" fill="#f2c7a2"/>
  <path d="M536 690 Q560 700 548 680" stroke="#8d6a52" fill="none" stroke-width="2"/>
  ${survivor(300, 840, 1.25, { arm: "photo" })}
  ${zombie(1120, 820, 1.1, { kind: "sleep" })}
  <path d="M1080 640 Q1120 600 1160 680" fill="none" stroke="#f7f3e8" stroke-width="2" opacity="0.8"/>
  `,
);

plate(
  "ch11",
  W,
  H,
  `
  <rect y="660" width="1500" height="340" fill="#c9d3b4"/>
  <ellipse cx="400" cy="180" rx="200" ry="50" fill="#fff8e8" opacity="0.8"/>
  ${engine(520, 700, 1.3, { crank: true })}
  <path d="M700 560 C820 520 900 560 980 500" fill="none" stroke="#cfc6b8" stroke-width="12" stroke-linecap="round" opacity="0.7"/>
  ${survivor(300, 840, 1.25, { arm: "lean", expr: "focus" })}
  ${zombie(1080, 860, 1.15)}
  <ellipse cx="1040" cy="700" rx="22" ry="12" fill="${P.olive2}"/>
  <ellipse cx="1160" cy="690" rx="22" ry="12" fill="${P.olive2}"/>
  `,
);

plate(
  "ch12",
  W,
  H,
  `
  <rect y="680" width="1500" height="320" fill="#dcc9a8"/>
  ${bench(200, 640, 900)}
  <rect x="260" y="500" width="90" height="120" rx="4" fill="${P.paper}"/>
  <path d="M280 540 H330 M280 560 H320 M280 580 H334" stroke="${P.olive2}" stroke-width="3"/>
  <circle cx="520" cy="560" r="26" fill="${P.metal}"/>
  <path d="M520 534 V548" stroke="${P.char}" stroke-width="4"/>
  <path d="M500 520 Q520 500 540 520 L532 534 H508 Z" fill="${P.amber}"/>
  <rect x="640" y="560" width="70" height="18" rx="3" fill="${P.rust}"/>
  <rect x="760" y="540" width="50" height="70" rx="4" fill="${P.paper}" transform="rotate(180 785 575)"/>
  ${survivor(1040, 840, 1.2, { arm: "point" })}
  ${zombie(360, 900, 0.9, { kind: "stand" })}
  `,
);

plate(
  "ch13",
  W,
  H,
  `
  <rect y="690" width="1500" height="310" fill="#dcc9a8"/>
  ${bench(180, 640, 480)}
  <rect x="300" y="560" width="80" height="36" rx="6" fill="${P.metal}"/>
  <circle cx="300" cy="578" r="16" fill="${P.olive3}"/>
  <rect x="360" y="500" width="28" height="40" rx="4" fill="${P.char}"/>
  <ellipse cx="374" cy="492" rx="16" ry="8" fill="${P.metal2}"/>
  <rect x="980" y="280" width="280" height="20" fill="#8a6244"/>
  <rect x="1040" y="300" width="90" height="70" rx="8" fill="${P.paper}"/>
  <rect x="1060" y="250" width="50" height="50" rx="6" fill="${P.metal2}"/>
  <circle cx="1085" cy="250" r="16" fill="${P.char}" opacity="0.25"/>
  ${survivor(640, 840, 1.25, { arm: "stop" })}
  ${zombie(1180, 860, 1.05, { kind: "woozy" })}
  `,
);

plate(
  "ch14",
  W,
  H,
  `
  <rect y="680" width="1500" height="320" fill="#dcc9a8"/>
  ${bench(200, 660, 780)}
  <circle cx="340" cy="620" r="40" fill="${P.olive3}"/>
  <circle cx="620" cy="600" r="70" fill="${P.char}"/>
  <circle cx="620" cy="600" r="48" fill="${P.metal}"/>
  <path d="M360 590 Q480 520 600 560" fill="none" stroke="${P.rust}" stroke-width="8"/>
  <path d="M300 560 H700 V500 H300 Z" fill="${P.olive2}" opacity="0.85"/>
  ${survivor(860, 860, 1.15, { arm: "down" })}
  ${zombie(520, 900, 1, { kind: "reach" })}
  `,
);

plate(
  "ch15",
  W,
  H,
  `
  <rect y="640" width="1500" height="360" fill="#e6d5b6"/>
  <rect x="160" y="300" width="900" height="22" fill="#8a6244"/>
  <rect x="220" y="360" width="120" height="80" rx="6" fill="${P.olive3}"/>
  <ellipse cx="430" cy="420" rx="50" ry="30" fill="${P.metal}"/>
  <path d="M470 400 Q520 360 490 430" fill="${P.metal2}"/>
  <polygon points="620,340 700,390 650,470 560,430" fill="${P.rust}"/>
  ${survivor(980, 820, 1.2, { arm: "stop" })}
  ${zombie(700, 860, 1.1, { kind: "reach" })}
  `,
);

plate(
  "ch16",
  W,
  H,
  `
  <rect y="690" width="1500" height="310" fill="#dcc9a8"/>
  ${bench(160, 640, 980)}
  <rect x="220" y="500" width="150" height="120" rx="4" fill="${P.paper}"/>
  <path d="M240 580 C270 540 300 600 340 540" fill="none" stroke="${P.rust}" stroke-width="4"/>
  <rect x="460" y="520" width="100" height="110" rx="6" fill="#e7d3b0" stroke="${P.char}" stroke-width="3"/>
  <rect x="490" y="548" width="40" height="28" fill="${P.rust}"/>
  <circle cx="760" cy="600" r="28" fill="${P.olive3}"/>
  <path d="M700 600 H760" stroke="${P.char}" stroke-width="6"/>
  ${survivor(1040, 840, 1.15, { arm: "point" })}
  ${zombie(360, 900, 0.85, { kind: "peek" })}
  ${zombie(560, 920, 0.75)}
  `,
);

plate(
  "ch17",
  W,
  H,
  `
  <rect width="1500" height="520" fill="#f6e2b8"/>
  <circle cx="1180" cy="180" r="70" fill="#fff1cf"/>
  <rect y="560" width="1500" height="440" fill="#c3b48a"/>
  ${bench(160, 620, 420)}
  ${engine(340, 620, 1)}
  <rect x="620" y="560" width="40" height="90" rx="6" fill="${P.metal2}"/>
  <ellipse cx="640" cy="550" rx="28" ry="12" fill="${P.glass}"/>
  ${survivor(820, 820, 1.2, { arm: "point", expr: "smile" })}
  ${zombie(1080, 860, 1.05)}
  <rect x="1120" y="760" width="8" height="90" fill="#8a6244"/>
  <path d="M1100 770 H1180" stroke="${P.mint2}" stroke-width="8"/>
  ${daisy(400, 500, 1.2)}
  `,
);

// fix zombie sit - kind sit falls through to stand which is ok

async function main() {
  const browser = await chromium.launch({ args: ["--no-sandbox"] });
  const page = await browser.newPage();
  for (const [name, scene] of Object.entries(scenes)) {
    const html = `<!doctype html><html><body style="margin:0;background:${P.cream}">${scene.svg()}</body></html>`;
    await page.setViewportSize({ width: scene.w, height: scene.h });
    await page.setContent(html, { waitUntil: "load" });
    const file = path.join(OUT, `${name}.jpg`);
    await page.screenshot({ path: file, type: "jpeg", quality: 82, clip: { x: 0, y: 0, width: scene.w, height: scene.h } });
    console.log(name, fs.statSync(file).size);
  }
  await browser.close();
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
