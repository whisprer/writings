#!/usr/bin/env python3
"""
I/EAS Thesis Figures 1-8 Generation
Dr. L.P. Hillerman & woflfren
2092 CE | Kepler Institute
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Setup output directory
output_dir = Path.cwd() / "ieas_figures"
output_dir.mkdir(exist_ok=True)
print(f"Output directory: {output_dir}")

def fig_1_thrust_curves():
    """Figure 1: Thrust curves for all main thrusters."""
    alt_km = np.array([0, 10, 20, 40, 100])
    thrust_mn = np.array([8.92, 9.67, 10.34, 10.89, 11.05])    # MkII XXL
    thrust_xl = np.array([1.27, 1.31, 1.36, 1.39, 1.42])       # MkII XL

    plt.figure(figsize=(7,5))
    plt.plot(alt_km, thrust_mn, 'b-o', lw=2, label="MkII XXL")
    plt.plot(alt_km, thrust_xl*8, 'g--s', lw=2, label="8x MkII XL (sum)")
    plt.xlabel("Altitude (km)")
    plt.ylabel("Thrust (MN)")
    plt.title("IEAS Main Thruster Curves (Sea Level - Vacuum)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / "fig01_thrust_curves.png", dpi=300, bbox_inches='tight')
    plt.close()

def fig_2_stress_distribution():
    """Figure 2: Stress distribution across structural nodes."""
    # Node labels and stress values (MPa)
    nodes = [
        "Dorsal Thruster Ring", "Ventral Weapons Bay", "Cockpit Zone", "Web Structure"
    ]
    stress = [1247, 892, 634, 412]
    max_stress = 2847  # MPa, ultimate of XS-7
    
    plt.figure(figsize=(7,5))
    bars = plt.bar(nodes, stress, color=['navy','orange','green','grey'], alpha=0.7)
    plt.axhline(max_stress, color='red', lw=2, linestyle='--', label="XS-7 Ultimate")
    plt.ylabel("Peak Stress [MPa]")
    plt.title("IEAS Structural Node Stress under Combat Loads")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "fig02_stress_distribution.png", dpi=300, bbox_inches='tight')
    plt.close()

def fig_3_shield_performance():
    """Figure 3: Shield capacity vs. sustained assault."""
    # Capacitor setups vs. time to depletion
    configs = ["Baseline", "4 Caps", "8 Caps", "8C+12Charger"]
    times = [47.3, 68.2, 91.7, 142.3]
    cap = [127_000, 175_000, 223_000, 223_000]

    plt.figure(figsize=(7,5))
    plt.bar(configs, times, color=['#3380ff','#33c69a','#dda722','#d94c3c'], alpha=0.8)
    plt.ylabel("Time to Depletion (s)")
    plt.title("IEAS Shield Performance (vs. Standardized Threat)")
    for i, c in enumerate(configs):
        plt.text(i, times[i]+2, f"{cap[i]//1000}k SP", ha='center', fontsize=9)
    plt.tight_layout()
    plt.savefig(output_dir / "fig03_shield_performance.png", dpi=300, bbox_inches='tight')
    plt.close()

def fig_4_weapon_systems():
    """Figure 4: IEAS main armament coverage/power."""
    labels = ["Railgun", "Pulse Laser", "Rocket", "Turret"]
    qty = [4,4,4,6]
    dps = [4980,4140,1050,4400]
    fig, ax1 = plt.subplots(figsize=(7,5))
    ax2 = ax1.twinx()
    ax1.bar(labels, qty, color='#3c90ee', alpha=0.7, label="Quantity")
    ax2.plot(labels, dps, 'rs--', label="DPS", lw=2)
    ax1.set_ylabel('Quantity (units)')
    ax2.set_ylabel('Damage (DPS)')
    plt.title('IEAS Main Weapon System Coverage')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(output_dir / "fig04_weapon_systems.png", dpi=300, bbox_inches='tight')
    plt.close()

def fig_5_operational_envelope():
    """Figure 5: Operational envelope (Vacuum, Atmosphere, Underwater)."""
    envs = ["Vacuum", "Atmosphere", "Underwater"]
    vmax = [115, 40, 12]
    amax = [2.6, 2.1, 0.4]
    plt.figure(figsize=(6,6))
    for i, env in enumerate(envs):
        plt.scatter(vmax[i], amax[i], s=250, alpha=0.7, label=env)
    plt.xlabel("Max Velocity (m/s)")
    plt.ylabel("Max Acceleration (G)")
    plt.xlim(0, 130)
    plt.ylim(0, 3)
    plt.legend()
    plt.title("IEAS Operational Performance Envelope")
    plt.tight_layout()
    plt.savefig(output_dir / "fig05_operational_envelope.png", dpi=300, bbox_inches='tight')
    plt.close()

def fig_6_variant_comparison():
    """Figure 6: Key capabilities of IEAS variants."""
    variants = ["Levit8-Aero", "Aardvark", "3lectron"]
    shield = [223_000, 256_000, 190_000]       # est SP
    weapon_types = [4,2,2]
    cpu = [104_000, 73_000, 147_000]
    fig, ax1 = plt.subplots(figsize=(8,5))
    w = 0.25
    idx = np.arange(len(variants))
    ax1.bar(idx-w, shield, width=w, label="Max Shield")
    ax1.bar(idx, weapon_types, width=w, label="Weapon Types")
    ax1.bar(idx+w, cpu, width=w, label="CPU Points")
    ax1.set_xticks(idx)
    ax1.set_xticklabels(variants)
    plt.title("IEAS Variant Comparative Profile")
    plt.ylabel("Capability Value (see legend)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "fig06_variant_comparison.png", dpi=300, bbox_inches='tight')
    plt.close()

def fig_7_cpu_architecture():
    """Figure 7: Block diagram of CPU/control architecture."""
    # Simple architecture diagram (static)
    import matplotlib.patches as mpatches
    fig, ax = plt.subplots(figsize=(10,6))
    ax.axis('off')
    # Boxes
    boxes = [
        ((0.05,0.6,0.25,0.3),'Primary Quantum Core (10M eq)', "#ccecff"),
        ((0.35,0.7,0.25,0.2),'Propulsion/FCS\n24,320 CPU', "#cafac9"),
        ((0.35,0.5,0.25,0.2),'Weapons/Targeting\n31,450 CPU', "#ffd9b3"),
        ((0.65,0.7,0.25,0.2),'Shields/Sensors\n12,780/12,400 CPU', "#ffe7e7"),
        ((0.65,0.5,0.25,0.2),'Life Support/Monitoring\n8,430/4,800 CPU', "#fff7b2"),
    ]
    for rect, label, color in boxes:
        ax.add_patch(mpatches.FancyBboxPatch(
            (rect[0],rect[1]),rect[2],rect[3],boxstyle="round,pad=0.02",fc=color,ec='k',lw=1.5))
        ax.text(
            rect[0]+rect[2]/2, rect[1]+rect[3]/2, label, ha="center", va="center", fontsize=11, weight='bold')
    # Arrows
    arrs = [
        ((0.18,0.6), (0.18,0.5)),
        ((0.18,0.6), (0.76,0.7)),
        ((0.18,0.6), (0.47,0.7)),
        ((0.18,0.6), (0.47,0.5)),
        ((0.47,0.5), (0.47,0.7)),
    ]
    for start,end in arrs:
        ax.annotate('', xy=end, xytext=start,
                    arrowprops=dict(facecolor='grey', shrink=0.05, lw=1.5, width=2, headwidth=9))
    plt.title("IEAS Real-Time CPU/Control Block Architecture", pad=38)
    plt.tight_layout()
    plt.savefig(output_dir / "fig07_cpu_architecture.png", dpi=300, bbox_inches='tight')
    plt.close()

def fig_8_power_distribution():
    """Figure 8: Power network schematic."""
    # Schematic as static diagram
    import matplotlib.patches as mpatches
    fig, ax = plt.subplots(figsize=(10,5))
    ax.axis('off')
    # Nodes
    ax.add_patch(mpatches.Circle((0.18,0.5),0.07,fc="#bff2a8",ec='k',lw=2))
    ax.text(0.18,0.5,"Generator Array\n(57 MW)",ha='center',va='center',fontsize=11)
    for i,(name,x) in enumerate(zip(
        ["Bus A\nPropulsion","Bus B\nWeapons+Shields","Bus C\nCPU/Life"],[0.38,0.58,0.78])):
        ax.add_patch(mpatches.FancyBboxPatch((x,0.60),0.13,0.18,boxstyle="round,pad=0.05",fc="#ccecff",ec='k',lw=1.5))
        ax.text(x+0.065, 0.69, name, ha='center',va='center',fontsize=10)
        ax.annotate('', xy=(x,0.69), xytext=(0.25,0.5),
            arrowprops=dict(facecolor='grey', arrowstyle='->', lw=2, shrinkA=10, shrinkB=3, width=2))
    ax.text(0.65,0.37,"Cross-Ties (3.4 ms auto-switch)",fontsize=10,ha='center')
    plt.title("IEAS Power Distribution Network", pad=26)
    plt.tight_layout()
    plt.savefig(output_dir / "fig08_power_distribution.png", dpi=300, bbox_inches='tight')
    plt.close()

# Generation execution
if __name__ == "__main__":
    print("Generating IEAS Figures 1–8...")

    try: fig_1_thrust_curves(); print("✓ Figure 1 done")
    except Exception as e: print(f"✗ Figure 1 failed: {e}")

    try: fig_2_stress_distribution(); print("✓ Figure 2 done")
    except Exception as e: print(f"✗ Figure 2 failed: {e}")

    try: fig_3_shield_performance(); print("✓ Figure 3 done")
    except Exception as e: print(f"✗ Figure 3 failed: {e}")

    try: fig_4_weapon_systems(); print("✓ Figure 4 done")
    except Exception as e: print(f"✗ Figure 4 failed: {e}")

    try: fig_5_operational_envelope(); print("✓ Figure 5 done")
    except Exception as e: print(f"✗ Figure 5 failed: {e}")

    try: fig_6_variant_comparison(); print("✓ Figure 6 done")
    except Exception as e: print(f"✗ Figure 6 failed: {e}")

    try: fig_7_cpu_architecture(); print("✓ Figure 7 done")
    except Exception as e: print(f"✗ Figure 7 failed: {e}")

    try: fig_8_power_distribution(); print("✓ Figure 8 done")
    except Exception as e: print(f"✗ Figure 8 failed: {e}")

    print(f"\n{'-'*60}")
    print("All 8 figures generated!")
    print(f"Output location: {output_dir}")
    print('-'*60)
    files = list(output_dir.glob("fig0*.png"))
    if files:
        print("Generated files:")
        for f in sorted(files):
            print(f"  - {f.name}")

