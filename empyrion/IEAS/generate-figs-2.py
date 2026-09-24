#!/usr/bin/env python3
"""
I/EAS Thesis Figures 9-16: Extended System Analysis
Advanced Visualization Suite (FIXED VERSION)
Dr. L.P. Hillerman & woflfren | 2092 CE
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Wedge, Polygon, Arrow, FancyArrowPatch
from matplotlib.collections import LineCollection, PatchCollection
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import numpy as np
from pathlib import Path
import matplotlib.gridspec as gridspec

# Setup
output_dir = Path.cwd() / "ieas_figures"
output_dir.mkdir(exist_ok=True)

# High-quality rendering
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['lines.linewidth'] = 1.8
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.25
plt.rcParams['axes.facecolor'] = '#f8f8f8'

print("="*70)
print("GENERATING ADVANCED I/EAS THESIS FIGURES 9-16 (FIXED)")
print("="*70)

# ============================================================================
# FIGURE 9: Thermal Management & Heat Rejection System
# ============================================================================
def fig_09_thermal_management():
    fig = plt.figure(figsize=(15, 10))
    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

    ax1 = fig.add_subplot(gs[0, 0])
    time = np.linspace(0, 300, 500)
    combat_heat = 45 * (1 - np.exp(-time/80)) + 8*np.sin(time/15)**2
    cruise_heat = 8 + 2*np.sin(time/30)
    emergency_heat = 120 * (1 - np.exp(-time/40))

    ax1.fill_between(time, 0, combat_heat, alpha=0.4, color='red', label='Combat Profile')
    ax1.plot(time, combat_heat, 'r-', lw=2)
    ax1.plot(time, cruise_heat, 'b--', lw=2, label='Cruise')
    ax1.plot(time, emergency_heat, 'orange', lw=2.5, label='Emergency Boost')
    ax1.axhline(90, color='darkred', linestyle=':', lw=2, label='Critical Temp')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Heat Output (MW)')
    ax1.set_title('A) Thermal Load Profiles')
    ax1.legend(loc='upper left', fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim([0, 130])

    ax2 = fig.add_subplot(gs[0, 1], projection='3d')
    temp_c = np.linspace(-180, 1650, 40)
    rad_area = np.linspace(2, 24, 40)
    T, A = np.meshgrid(temp_c, rad_area)
    Efficiency = (100 * (1 - np.exp(-A/6))) * np.exp(-(T-900)**2/500000)
    surf = ax2.plot_surface(T, A, Efficiency, cmap='hot', alpha=0.8, edgecolor='none')
    ax2.set_xlabel('Hull Temp (C)')
    ax2.set_ylabel('Radiator Area (m2)')
    ax2.set_zlabel('Efficiency (%)')
    ax2.set_title('B) Radiator Performance Surface')

    ax3 = fig.add_subplot(gs[1, 0])
    mission_hours = np.linspace(0, 8, 200)
    main_rad = 500 * (1 - np.exp(-mission_hours/4))
    reserve_cap = 300 * (1 - 0.5*mission_hours/8)
    cryo_backup = 200 * np.exp(-mission_hours/2)
    total = main_rad + reserve_cap + cryo_backup

    ax3.fill_between(mission_hours, 0, main_rad, alpha=0.5, label='Primary Radiator', color='#ff6b6b')
    ax3.fill_between(mission_hours, main_rad, main_rad+reserve_cap, alpha=0.5, label='Reserve Capacity', color='#ffa500')
    ax3.fill_between(mission_hours, main_rad+reserve_cap, total, alpha=0.5, label='Cryo Backup', color='#4dabf7')
    ax3.plot(mission_hours, total, 'k-', lw=2.5, label='Total Available')
    ax3.set_xlabel('Mission Duration (hours)')
    ax3.set_ylabel('Heat Dissipation Capacity (MW)')
    ax3.set_title('C) Cumulative Heat Management')
    ax3.legend(loc='lower right', fontsize=9)
    ax3.grid(True, alpha=0.3)

    ax4 = fig.add_subplot(gs[1, 1])
    regions = ['Port Engines', 'Starboard Engines', 'Weapon Bays', 'Cockpit', 'Aux Systems', 'Hull']
    temps = [1200, 1180, 950, 380, 520, 420]
    colors_temp = cm.hot(np.linspace(0.2, 0.9, len(temps)))
    bars = ax4.barh(regions, temps, color=colors_temp, edgecolor='black', lw=1.5)
    ax4.axvline(1000, color='red', linestyle='--', lw=2, label='Safety Limit')
    ax4.set_xlabel('Temperature (K)')
    ax4.set_title('D) Regional Thermal Distribution')
    ax4.legend(loc='lower right')
    ax4.set_xlim([0, 1400])

    plt.suptitle('Figure 9: Advanced Thermal Management & Heat Rejection Systems', 
                 fontsize=14, fontweight='bold', y=0.995)
    plt.savefig(output_dir / "fig09_thermal_management.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Figure 9: Thermal Management")

# ============================================================================
# FIGURE 10: Gravitic Sensor Array & Anomaly Detection
# ============================================================================
def fig_10_gravitic_sensors():
    fig = plt.figure(figsize=(15, 11))
    gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.35, wspace=0.3)

    ax1 = fig.add_subplot(gs[0, :])
    mass_tons = np.array([10, 50, 100, 500, 1000, 5000, 10000])
    range_km = 2.1 * np.sqrt(mass_tons)

    ax1.scatter(mass_tons, range_km, s=200, alpha=0.7, c=mass_tons, cmap='viridis', edgecolors='black', lw=1.5)
    ax1.plot(mass_tons, range_km, 'k--', lw=2, alpha=0.5)
    for m, r in zip(mass_tons, range_km):
        ax1.annotate(str(int(m))+'t', xy=(m,r), xytext=(5,5), textcoords='offset points', fontsize=9)

    ax1.set_xscale('log')
    ax1.set_xlabel('Target Mass (tonnes) [log scale]')
    ax1.set_ylabel('Maximum Detection Range (km)')
    ax1.set_title('A) Gravitic Sensor Detection Envelope vs. Target Mass')
    ax1.grid(True, alpha=0.3, which='both')

    ax2 = fig.add_subplot(gs[1, 0])
    freq = np.logspace(-1, 3, 500)
    sensor_resp = 1 / (1 + (freq/47)**2)

    ax2.semilogx(freq, sensor_resp, 'b-', lw=2.5, label='Sensor Response')
    ax2.fill_between(freq, 0, sensor_resp, alpha=0.3, color='blue')
    ax2.axvline(47, color='red', linestyle='--', lw=2, label='Peak Sensitivity')
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Normalized Response')
    ax2.set_title('B) Gravitic Signature Frequency Response')
    ax2.legend()
    ax2.grid(True, alpha=0.3, which='both')
    ax2.set_ylim([0, 1.1])

    ax3 = fig.add_subplot(gs[1, 1], projection='3d')
    x = np.linspace(-80, 80, 50)
    y = np.linspace(-80, 80, 50)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X, dtype=float)
    sources = [(-30, 30, 8000), (40, -20, 12000), (0, 0, 5000)]
    for sx, sy, mass in sources:
        r = np.sqrt((X-sx)**2 + (Y-sy)**2 + 1)
        Z += mass / (r**2)

    surf = ax3.plot_surface(X, Y, np.log10(Z+1), cmap='plasma', alpha=0.85, edgecolor='none')
    ax3.set_xlabel('X (km)')
    ax3.set_ylabel('Y (km)')
    ax3.set_zlabel('log10(Field)')
    ax3.set_title('C) Multi-Source Gravitic Field Topology')

    ax4 = fig.add_subplot(gs[2, :])
    t_track = np.linspace(0, 120, 500)
    target_range = 2400 - 12*t_track + 0.05*t_track**2
    target_range[target_range < 100] = 100
    noise = 30 * np.sin(t_track/8) + np.random.normal(0, 15, len(t_track))
    measured = target_range + noise

    ax4.plot(t_track, target_range, 'g-', lw=3, label='True Range', alpha=0.8)
    ax4.scatter(t_track, measured, s=20, alpha=0.5, c='red', label='Noisy Measurement')
    ax4.fill_between(t_track, target_range-50, target_range+50, alpha=0.2, color='green', label='Confidence Interval')

    ax4.set_xlabel('Tracking Time (s)')
    ax4.set_ylabel('Target Range (km)')
    ax4.set_title('D) Real-Time Target Tracking (Alien Corvette Approach Simulation)')
    ax4.legend(loc='upper right')
    ax4.grid(True, alpha=0.3)
    ax4.set_ylim([0, 2500])

    plt.suptitle('Figure 10: Gravitic Sensor Array & Anomaly Detection System', 
                 fontsize=14, fontweight='bold', y=0.998)
    plt.savefig(output_dir / "fig10_gravitic_sensors.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Figure 10: Gravitic Sensors")

# ============================================================================
# FIGURE 11: Quantum Computing & Real-Time Processing Architecture
# ============================================================================
def fig_11_quantum_computing():
    fig = plt.figure(figsize=(16, 10))
    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

    ax1 = fig.add_subplot(gs[0, 0])
    time = np.linspace(0, 600, 1000)
    propulsion = 24320 * (0.3 + 0.7*np.abs(np.sin(time/60)))
    weapons = 31450 * (0.2 + 0.8*np.random.exponential(1, len(time))/3)
    shields = 12780 * (0.4 + 0.6*np.abs(np.cos(time/45)))
    sensors = 18940 * (0.6 + 0.4*np.sin(time/90))
    other = 16377 * 0.5

    ax1.fill_between(time, 0, propulsion, alpha=0.6, label='Propulsion', color='#3498db')
    ax1.fill_between(time, propulsion, propulsion+weapons, alpha=0.6, label='Weapons', color='#e74c3c')
    ax1.fill_between(time, propulsion+weapons, propulsion+weapons+shields, alpha=0.6, label='Shields', color='#f39c12')
    ax1.fill_between(time, propulsion+weapons+shields, propulsion+weapons+shields+sensors, alpha=0.6, label='Sensors', color='#2ecc71')
    ax1.fill_between(time, propulsion+weapons+shields+sensors, propulsion+weapons+shields+sensors+other, alpha=0.6, label='Other', color='#9b59b6')

    ax1.axhline(103847, color='red', linestyle='--', lw=2.5, label='Max Capacity')
    ax1.set_xlabel('Mission Time (s)')
    ax1.set_ylabel('CPU Points Allocated')
    ax1.set_title('A) Real-Time CPU Load Distribution')
    ax1.legend(loc='upper left', fontsize=8, ncol=3)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim([0, 115000])

    ax2 = fig.add_subplot(gs[0, 1])
    tau_vals = np.linspace(0, 2000, 500)
    ec_surface17 = np.exp(-tau_vals/847)
    ec_surface19 = np.exp(-tau_vals/1200)
    ec_surface21 = np.exp(-tau_vals/1800)
    uncorrected = np.exp(-tau_vals/47)

    ax2.semilogy(tau_vals, uncorrected, 'r--', lw=2, label='Uncorrected', alpha=0.7)
    ax2.semilogy(tau_vals, ec_surface17, 'b-', lw=2.5, label='Surface-17 Code (tau=847us)')
    ax2.semilogy(tau_vals, ec_surface19, 'g-', lw=2.5, label='Surface-19 Code')
    ax2.semilogy(tau_vals, ec_surface21, 'orange', lw=2.5, label='Surface-21 Code')

    ax2.axvline(847, color='blue', linestyle=':', alpha=0.5)
    ax2.fill_between(tau_vals[tau_vals<=847], 1e-10, 1, alpha=0.1, color='blue', label='IEAS Operating Window')

    ax2.set_xlabel('Time (us)')
    ax2.set_ylabel('Fidelity (log scale)')
    ax2.set_title('B) Quantum Error Correction Dynamics')
    ax2.legend(loc='upper right', fontsize=8)
    ax2.grid(True, alpha=0.3, which='both')

    ax3 = fig.add_subplot(gs[1, 0])
    levels = ['Reflex', 'Tactical', 'Strategic', 'Mission']
    latency_us = [1, 10, 100, 1000]
    throughput = [1.2e7, 1.2e6, 1.2e5, 1.2e4]
    colors_level = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db']

    for i, (level, lat, thr, col) in enumerate(zip(levels, latency_us, throughput, colors_level)):
        circle = Circle((i+1, np.log10(thr)), radius=np.sqrt(lat)/8, color=col, alpha=0.7, edgecolor='black', lw=2)
        ax3.add_patch(circle)
        ax3.text(i+1, np.log10(thr), str(lat)+'us', ha='center', va='center', fontsize=9, weight='bold')

    ax3.set_xticks(range(1, 5))
    ax3.set_xticklabels(levels, fontsize=9)
    ax3.set_ylabel('Throughput (ops/s) [log scale]')
    ax3.set_title('C) Real-Time Processing Hierarchy')
    ax3.set_ylim([3.5, 7.5])
    ax3.grid(True, alpha=0.3, axis='y')
    ax3.set_xlim([0.5, 4.5])

    ax4 = fig.add_subplot(gs[1, 1])
    scenarios = ['Routine\nCruise', 'Light\nCombat', 'Heavy\nEngage', 'Emergency\nEvade']
    hit_rate = [92, 78, 64, 45]
    prediction_acc = [89, 75, 58, 38]

    x_pos = np.arange(len(scenarios))
    width = 0.35

    bars1 = ax4.bar(x_pos - width/2, hit_rate, width, label='Cache Hit Rate', color='#2ecc71', edgecolor='black', lw=1.5)
    bars2 = ax4.bar(x_pos + width/2, prediction_acc, width, label='Prediction Accuracy', color='#3498db', edgecolor='black', lw=1.5)

    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 1,
                    str(int(height))+'%', ha='center', va='bottom', fontsize=9, weight='bold')

    ax4.set_ylabel('Percentage (%)')
    ax4.set_title('D) Quantum Processor Efficiency Under Load')
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(scenarios)
    ax4.set_ylim([0, 105])
    ax4.legend(loc='upper right')
    ax4.grid(True, alpha=0.3, axis='y')

    plt.suptitle('Figure 11: Quantum Computing & Real-Time Processing Architecture', 
                 fontsize=14, fontweight='bold', y=0.998)
    plt.savefig(output_dir / "fig11_quantum_computing.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Figure 11: Quantum Computing")

print("\nGenerating all remaining figures...\n")

# Execute all
try:
    fig_09_thermal_management()
    fig_10_gravitic_sensors()
    fig_11_quantum_computing()
    print("\n" + "="*70)
    print("✅ FIGURES 9-11 SUCCESSFULLY GENERATED (NO SYNTAX ERRORS)")
    print("="*70)
    print("\nOutput directory: " + str(output_dir))

except Exception as e:
    print(f"\n✗ ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
