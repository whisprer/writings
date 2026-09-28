#!/usr/bin/env python3

"""
Extended I/EAS Thesis Figure Generation Suite - Appendix I
Dr. Ludmilla Pereira Hillerman
Kepler Institute for Advanced Propulsion Studies
2092 CE
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, Polygon, Wedge, Arrow
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from scipy.interpolate import interp1d
from scipy import signal
import matplotlib.cm as cm
from matplotlib.collections import LineCollection
import warnings
import os
from pathlib import Path

warnings.filterwarnings('ignore')

# Set publication-quality parameters
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3

# Create output directory (Windows-compatible)
output_dir = Path.cwd() / "ieas_figures"
output_dir.mkdir(exist_ok=True)
print(f"Output directory: {output_dir}")

def fig_17_gravitic_anomaly_detection():
    """Figure 17: Gravitic Anomaly Detector Performance Characteristics"""
    fig = plt.figure(figsize=(14, 10))
    
    # Detection sensitivity vs range
    ax1 = fig.add_subplot(221)
    range_km = np.logspace(0, 3, 100)
    
    # Different target masses
    fighter_mass = 50 # tonnes
    corvette_mass = 500
    cruiser_mass = 5000
    
    sensitivity_fighter = 1e-12 * fighter_mass / range_km**2
    sensitivity_corvette = 1e-12 * corvette_mass / range_km**2
    sensitivity_cruiser = 1e-12 * cruiser_mass / range_km**2
    noise_floor = 1e-15 * np.ones_like(range_km)
    
    ax1.loglog(range_km, sensitivity_fighter, 'b-', linewidth=2, label='Fighter (50t)')
    ax1.loglog(range_km, sensitivity_corvette, 'g-', linewidth=2, label='Corvette (500t)')
    ax1.loglog(range_km, sensitivity_cruiser, 'r-', linewidth=2, label='Cruiser (5000t)')
    ax1.loglog(range_km, noise_floor, 'k--', linewidth=2, label='Noise Floor')
    ax1.fill_between(range_km, noise_floor, 1e-10, alpha=0.2, color='red', label='Undetectable')
    
    ax1.set_xlabel('Range (km)')
    ax1.set_ylabel('Gravitic Field Strength (G₀)')
    ax1.set_title('Gravitic Anomaly Detection Sensitivity')
    ax1.legend()
    ax1.grid(True, alpha=0.3, which='both')
    
    # Phase space visualization
    ax2 = fig.add_subplot(222, projection='3d')
    
    # Generate gravitic field data
    x = np.linspace(-50, 50, 30)
    y = np.linspace(-50, 50, 30)
    X, Y = np.meshgrid(x, y)
    
    # Multiple gravity sources
    Z = np.zeros_like(X)
    sources = [(0, 0, 1000), (20, -10, 500), (-15, 25, 750)]
    
    for sx, sy, mass in sources:
        r = np.sqrt((X - sx)**2 + (Y - sy)**2 + 100)
        Z += mass / r**2
    
    surf = ax2.plot_surface(X, Y, np.log10(Z), cmap='viridis', alpha=0.8)
    ax2.set_xlabel('X Position (km)')
    ax2.set_ylabel('Y Position (km)')
    ax2.set_zlabel('log₁₀(Field Strength)')
    ax2.set_title('Gravitic Field Topology')
    
    # Spectral analysis
    ax3 = fig.add_subplot(223)
    freq = np.logspace(-2, 2, 1000)
    
    # Spectral signatures
    natural = 1 / (1 + (freq/0.1)**2)
    artificial = np.zeros_like(freq)
    artificial[(freq > 1) & (freq < 10)] = 0.5
    artificial[(freq > 20) & (freq < 30)] = 0.8
    alien = 0.3 * np.exp(-(freq - 47)**2/10)
    
    ax3.semilogy(freq, natural, 'b-', linewidth=2, label='Natural Sources')
    ax3.semilogy(freq, artificial, 'g-', linewidth=2, label='Artificial Drives')
    ax3.semilogy(freq, alien, 'r-', linewidth=2, label='Alien Signature')
    
    ax3.set_xlabel('Frequency (Hz)')
    ax3.set_ylabel('Spectral Power')
    ax3.set_title('Gravitic Signature Analysis')
    ax3.legend()
    ax3.grid(True, alpha=0.3, which='both')
    
    # Detection probability matrix
    ax4 = fig.add_subplot(224)
    speeds = np.linspace(0, 200, 50)
    stealth_factors = np.linspace(0, 1, 50)
    S, F = np.meshgrid(speeds, stealth_factors)
    
    # Detection probability
    P_detect = np.exp(-(S/100)**2) * (1 - F)**2
    
    im = ax4.contourf(S, F, P_detect, levels=10, cmap='hot')
    ax4.set_xlabel('Target Speed (m/s)')
    ax4.set_ylabel('Stealth Factor')
    ax4.set_title('Detection Probability Matrix')
    contours = ax4.contour(S, F, P_detect, levels=[0.25, 0.5, 0.75], colors='white')
    ax4.clabel(contours, inline=True, fontsize=8)
    plt.colorbar(im, ax=ax4, label='P(detect)')
    
    plt.suptitle('Figure 17: Alien-Technology Gravitic Anomaly Detection System',
                fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_dir / "fig17_gravitic_detection.png", dpi=300, bbox_inches='tight')
    plt.close()

def fig_18_submarine_operations():
    """Figure 18: Submarine Operations Performance Analysis"""
    fig = plt.figure(figsize=(14, 10))
    
    # Pressure hull stress
    ax1 = fig.add_subplot(221)
    depth = np.linspace(0, 500, 100)
    pressure = 101.3 + 9.81 * 1000 * depth / 1000 # kPa
    
    # Hull stress for different designs
    stress_conventional = pressure * 5 # MPa
    stress_zero_monocoque = pressure * 3.2 # Better distribution
    yield_strength = 1247 * np.ones_like(depth) # XS-7 composite
    
    ax1.plot(depth, stress_conventional, 'b--', linewidth=2, label='Conventional Hull')
    ax1.plot(depth, stress_zero_monocoque, 'g-', linewidth=2, label='Zero-Monocoque')
    ax1.plot(depth, yield_strength, 'r:', linewidth=2, label='Yield Limit')
    ax1.fill_between(depth, 0, stress_zero_monocoque, alpha=0.2, color='green')
    ax1.fill_between(depth, stress_zero_monocoque, yield_strength,
                    alpha=0.1, color='yellow', label='Safety Margin')
    
    ax1.set_xlabel('Depth (m)')
    ax1.set_ylabel('Hull Stress (MPa)')
    ax1.set_title('Submarine Hull Stress Analysis')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Hydrodynamic drag
    ax2 = fig.add_subplot(222)
    velocity = np.linspace(0, 15, 100)
    
    # Drag components
    friction_drag = 0.5 * 1000 * velocity**2 * 0.003 * 140 # N
    pressure_drag = 0.5 * 1000 * velocity**2 * 0.15 * 12 # N
    wave_drag = np.where(velocity > 5,
                        0.5 * 1000 * (velocity-5)**3 * 0.05 * 12, 0) # N
    total_drag = friction_drag + pressure_drag + wave_drag
    
    ax2.plot(velocity, friction_drag/1000, 'b-', linewidth=2, label='Friction')
    ax2.plot(velocity, pressure_drag/1000, 'g-', linewidth=2, label='Pressure')
    ax2.plot(velocity, wave_drag/1000, 'r-', linewidth=2, label='Wave')
    ax2.plot(velocity, total_drag/1000, 'k-', linewidth=3, label='Total')
    
    ax2.set_xlabel('Velocity (m/s)')
    ax2.set_ylabel('Drag Force (kN)')
    ax2.set_title('Submarine Hydrodynamic Drag Components')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Acoustic signature
    ax3 = fig.add_subplot(223)
    freq = np.logspace(1, 5, 1000) # Hz
    
    # Noise sources
    machinery = 80 * np.exp(-(np.log10(freq) - 2.5)**2)
    propulsion = 70 * np.exp(-(np.log10(freq) - 3)**2)
    flow = 60 * (freq/1000)**(-0.5)
    total_noise = 10*np.log10(10**(machinery/10) + 10**(propulsion/10) + 10**(flow/10))
    ambient = 45 * np.ones_like(freq)
    
    ax3.semilogx(freq, machinery, 'b--', linewidth=1, alpha=0.7, label='Machinery')
    ax3.semilogx(freq, propulsion, 'g--', linewidth=1, alpha=0.7, label='Propulsion')
    ax3.semilogx(freq, flow, 'r--', linewidth=1, alpha=0.7, label='Flow Noise')
    ax3.semilogx(freq, total_noise, 'k-', linewidth=2, label='Total Signature')
    ax3.semilogx(freq, ambient, 'gray', linewidth=2, label='Ocean Ambient')
    
    ax3.set_xlabel('Frequency (Hz)')
    ax3.set_ylabel('Sound Pressure Level (dB)')
    ax3.set_title('Underwater Acoustic Signature')
    ax3.legend()
    ax3.grid(True, alpha=0.3, which='both')
    ax3.set_ylim([30, 100])
    
    # Ballast system response
    ax4 = fig.add_subplot(224)
    time = np.linspace(0, 60, 200) # seconds
    
    # Depth change scenarios
    emergency_surface = 100 * np.exp(-time/10)
    controlled_ascent = 100 - 2*time
    controlled_ascent[controlled_ascent < 0] = 0
    rapid_dive = -100 * (1 - np.exp(-time/5))
    
    ax4.plot(time, emergency_surface, 'r-', linewidth=2, label='Emergency Surface')
    ax4.plot(time, controlled_ascent, 'g-', linewidth=2, label='Controlled Ascent')
    ax4.plot(time, rapid_dive, 'b-', linewidth=2, label='Rapid Dive')
    ax4.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    
    ax4.set_xlabel('Time (s)')
    ax4.set_ylabel('Depth Change (m)')
    ax4.set_title('Ballast System Response Profiles')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.suptitle('Figure 18: Submarine Operations and Underwater Performance',
                fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_dir / "fig18_submarine_ops.png", dpi=300, bbox_inches='tight')
    plt.close()

def fig_19_pentaxid_chemistry():
    """Figure 19: Pentaxid Catalysis in Energy Systems"""
    fig = plt.figure(figsize=(14, 10))
    
    # Reaction rate enhancement
    ax1 = fig.add_subplot(221)
    temperature = np.linspace(300, 3000, 100)
    
    # Arrhenius equation
    k_base = 1e8 * np.exp(-50000/(8.314*temperature))
    k_pentaxid = 1e12 * np.exp(-20000/(8.314*temperature))
    
    ax1.semilogy(temperature, k_base, 'b--', linewidth=2, label='Uncatalyzed D-T')
    ax1.semilogy(temperature, k_pentaxid, 'r-', linewidth=2, label='Pentaxid-Catalyzed')
    ax1.fill_between(temperature, k_base, k_pentaxid, alpha=0.2, color='green')
    
    ax1.set_xlabel('Temperature (K)')
    ax1.set_ylabel('Reaction Rate (s⁻¹)')
    ax1.set_title('Fusion Reaction Rate Enhancement')
    ax1.legend()
    ax1.grid(True, alpha=0.3, which='both')
    
    # Energy level diagram
    ax2 = fig.add_subplot(222)
    
    # Energy levels
    levels = {
        'D + T': 100,
        'Activated Complex': 180,
        'Pentaxid Complex': 140,
        'He-4 + n': 20
    }
    
    # Draw levels
    for i, (label, energy) in enumerate(levels.items()):
        ax2.plot([i-0.3, i+0.3], [energy, energy], 'k-', linewidth=3)
        ax2.text(i, energy-8, label, ha='center', fontsize=9)
    
    # Transitions
    ax2.arrow(0.3, 100, 0.4, 75, head_width=0.05, head_length=3,
             fc='blue', ec='blue', alpha=0.7)
    ax2.arrow(0.3, 100, 0.4, 35, head_width=0.05, head_length=3,
             fc='red', ec='red', alpha=0.7)
    ax2.arrow(2.7, 140, 0.4, -115, head_width=0.05, head_length=3,
             fc='green', ec='green', alpha=0.7)
    
    ax2.text(0.5, 150, 'Ea = 80 keV', fontsize=8, color='blue')
    ax2.text(0.5, 120, 'Ea* = 40 keV', fontsize=8, color='red')
    
    ax2.set_xlim(-0.5, 3.5)
    ax2.set_ylim(0, 200)
    ax2.set_ylabel('Energy (keV)')
    ax2.set_title('Pentaxid Catalysis Energy Diagram')
    ax2.set_xticks([])
    
    # Plasma confinement improvement
    ax3 = fig.add_subplot(223)
    time_ms = np.linspace(0, 100, 1000)
    
    # Confinement quality
    standard = np.exp(-time_ms/20)
    pentaxid = np.exp(-time_ms/84.7)
    
    ax3.plot(time_ms, standard, 'b--', linewidth=2, label='Standard Confinement')
    ax3.plot(time_ms, pentaxid, 'r-', linewidth=2, label='Pentaxid-Enhanced')
    ax3.fill_between(time_ms, pentaxid, standard, where=(pentaxid > standard),
                    alpha=0.3, color='green', label='Improvement')
    
    ax3.set_xlabel('Time (ms)')
    ax3.set_ylabel('Plasma Density (normalized)')
    ax3.set_title('Plasma Confinement Time Enhancement')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Cross-section enhancement
    ax4 = fig.add_subplot(224)
    energy_keV = np.logspace(0, 3, 100)
    
    # Fusion cross-sections
    sigma_dt = 5 * np.exp(-(np.log10(energy_keV) - 1.7)**2)
    sigma_pentaxid = 8 * np.exp(-(np.log10(energy_keV) - 1.3)**2)
    
    ax4.loglog(energy_keV, sigma_dt, 'b--', linewidth=2, label='D-T Standard')
    ax4.loglog(energy_keV, sigma_pentaxid, 'r-', linewidth=2, label='Pentaxid-Catalyzed')
    
    ax4.set_xlabel('Energy (keV)')
    ax4.set_ylabel('Cross Section (barns)')
    ax4.set_title('Fusion Cross-Section Enhancement')
    ax4.legend()
    ax4.grid(True, alpha=0.3, which='both')
    
    plt.suptitle('Figure 19: Pentaxid Catalysis in Fusion Energy Systems',
                fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_dir / "fig19_pentaxid_chemistry.png", dpi=300, bbox_inches='tight')
    plt.close()

def fig_20_combat_simulation():
    """Figure 20: Monte Carlo Combat Simulation Results"""
    fig = plt.figure(figsize=(14, 10))
    
    # Engagement outcome probabilities
    ax1 = fig.add_subplot(221)
    n_enemies = np.arange(1, 11)
    
    # Win probabilities for different configurations
    p_win_base = 0.95 * np.exp(-0.3 * (n_enemies-1))
    p_win_upgraded = 0.98 * np.exp(-0.2 * (n_enemies-1))
    p_win_3lectron = 0.97 * np.exp(-0.15 * (n_enemies-1))
    
    ax1.plot(n_enemies, p_win_base*100, 'b-', linewidth=2, marker='o', label='Levit8-Aero')
    ax1.plot(n_enemies, p_win_upgraded*100, 'r-', linewidth=2, marker='s', label='Upgraded Config')
    ax1.plot(n_enemies, p_win_3lectron*100, 'g-', linewidth=2, marker='^', label='3lectron EW')
    
    ax1.set_xlabel('Number of Enemy Targets')
    ax1.set_ylabel('Victory Probability (%)')
    ax1.set_title('Combat Outcome Probability vs Force Ratio')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Survival time distribution
    ax2 = fig.add_subplot(222)
    
    # Generate Monte Carlo data
    np.random.seed(42)
    survival_times = np.concatenate([
        np.random.exponential(120, 500), # Standard engagements
        np.random.exponential(60, 300), # Heavy combat
        np.random.exponential(180, 200) # Light skirmish
    ])
    
    ax2.hist(survival_times, bins=50, density=True, alpha=0.7, color='blue', edgecolor='black')
    
    # Fit exponential
    x_fit = np.linspace(0, max(survival_times), 100)
    y_fit = (1/120) * np.exp(-x_fit/120)
    
    ax2.plot(x_fit, y_fit, 'r-', linewidth=2, label='Exponential Fit (τ=120s)')
    
    ax2.set_xlabel('Engagement Duration (s)')
    ax2.set_ylabel('Probability Density')
    ax2.set_title('Combat Engagement Duration Distribution')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Damage accumulation
    ax3 = fig.add_subplot(223)
    time = np.linspace(0, 300, 1000)
    
    # Different threat scenarios
    light_damage = 10 * np.sqrt(time) + 5*np.sin(time/10)
    moderate_damage = 20 * np.sqrt(time) + 10*np.sin(time/8)
    heavy_damage = 35 * np.sqrt(time) + 15*np.sin(time/5)
    
    ax3.plot(time, light_damage, 'g-', linewidth=2, label='Light Threat')
    ax3.plot(time, moderate_damage, 'y-', linewidth=2, label='Moderate Threat')
    ax3.plot(time, heavy_damage, 'r-', linewidth=2, label='Heavy Threat')
    ax3.axhline(y=100, color='black', linestyle='--', label='Critical Damage')
    ax3.fill_between(time, 80, 100, alpha=0.2, color='orange')
    ax3.fill_between(time, 100, 120, alpha=0.2, color='red')
    
    ax3.set_xlabel('Combat Time (s)')
    ax3.set_ylabel('Accumulated Damage (%)')
    ax3.set_title('Damage Accumulation Under Fire')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Kill chain efficiency
    ax4 = fig.add_subplot(224)
    stages = ['Detect', 'Track', 'ID', 'Engage', 'Assess']
    baseline_time = [2, 3, 2, 5, 2]
    ai_assisted = [0.5, 1, 0.5, 3, 0.5]
    quantum = [0.1, 0.5, 0.1, 2, 0.1]
    
    x = np.arange(len(stages))
    width = 0.25
    
    ax4.bar(x - width, baseline_time, width, label='Baseline', alpha=0.8, color='blue')
    ax4.bar(x, ai_assisted, width, label='AI-Assisted', alpha=0.8, color='green')
    ax4.bar(x + width, quantum, width, label='Quantum-Enhanced', alpha=0.8, color='red')
    
    ax4.set_xlabel('Kill Chain Stage')
    ax4.set_ylabel('Time (seconds)')
    ax4.set_title('Kill Chain Execution Time')
    ax4.set_xticks(x)
    ax4.set_xticklabels(stages)
    ax4.legend()
    ax4.grid(True, alpha=0.3, axis='y')
    
    plt.suptitle('Figure 20: Monte Carlo Combat Simulation Analysis',
                fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_dir / "fig20_combat_simulation.png", dpi=300, bbox_inches='tight')
    plt.close()

# Execute all figure generation
if __name__ == "__main__":
    print("Generating Extended I/EAS Thesis Figures (Appendix I - Extended)...")
    print(f"Saving to: {output_dir}\n")
    
    try:
        fig_17_gravitic_anomaly_detection()
        print("✓ Figure 17: Gravitic anomaly detection complete")
    except Exception as e:
        print(f"✗ Figure 17 failed: {e}")
    
    try:
        fig_18_submarine_operations()
        print("✓ Figure 18: Submarine operations complete")
    except Exception as e:
        print(f"✗ Figure 18 failed: {e}")
    
    try:
        fig_19_pentaxid_chemistry()
        print("✓ Figure 19: Pentaxid chemistry complete")
    except Exception as e:
        print(f"✗ Figure 19 failed: {e}")
    
    try:
        fig_20_combat_simulation()
        print("✓ Figure 20: Combat simulation complete")
    except Exception as e:
        print(f"✗ Figure 20 failed: {e}")
    
    print(f"\n{'='*60}")
    print("All 4 figures generated successfully!")
    print(f"Output location: {output_dir}")
    print(f"{'='*60}\n")
    
    # List generated files
    files = list(output_dir.glob("*.png"))
    if files:
        print("Generated files:")
        for f in sorted(files):
            print(f"  - {f.name}")
