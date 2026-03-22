#!/usr/bin/env python3
"""
/// script
requires-python = ">=3.9"
dependencies = [
    "matplotlib>=3.5.0",
    "numpy>=1.20.0",
]
///
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
import numpy as np

# Colorblind-accessible palette
palette = {
    "line": "#4477AA",      # blue
    "fill": "#66CCEE",      # cyan
    "event1": "#EE6677",    # red
    "event2": "#228833"     # green
}

# Data from Appendix A2
months_str = [
    "2023-05", "2023-06", "2023-07", "2023-08", "2023-09", "2023-10", "2023-11", "2023-12",
    "2024-01", "2024-02", "2024-03", "2024-04", "2024-05", "2024-06", "2024-07", "2024-08",
    "2024-09", "2024-10", "2024-11", "2024-12", "2025-01", "2025-02", "2025-03", "2025-04",
    "2025-05", "2025-06", "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12",
    "2026-01", "2026-02", "2026-03"
]

volumes = [
    2, 18, 22, 23, 9, 15, 19, 23, 27, 40, 32, 54, 23, 29, 81, 80,
    65, 52, 86, 148, 182, 88, 98, 111, 270, 268, 131, 97, 92, 92, 94, 101,
    154, 152, 57
]

# Convert months to datetime for plotting
dates = [datetime.strptime(m, "%Y-%m") for m in months_str]
x_numeric = np.arange(len(dates))

fig, ax = plt.subplots(figsize=(14, 6))

# Add epoch background shading
# E1: pre-Jul 2024 (indices 0-13)
# E2: Jul-Sep 2024 (indices 14-16)
# E3: Oct 2024-Feb 2025 (indices 17-20)
# E4: Mar 2025+ (indices 21+)

epoch_colors = ["#F0F0F0", "#E8E8E8", "#F0F0F0", "#E8E8E8"]
epoch_boundaries = [
    (0, 13, "E1: Pre-Nature pub"),
    (14, 16, "E2: Jul-Sep 2024"),
    (17, 20, "E3: Oct 2024-Feb 2025"),
    (21, len(dates)-1, "E4: Post-Schaeffer")
]

for idx, (start, end, label) in enumerate(epoch_boundaries):
    ax.axvspan(start - 0.5, end + 0.5, alpha=0.15, color=epoch_colors[idx], zorder=0)

# Plot line and fill
ax.plot(x_numeric, volumes, color=palette["line"], linewidth=2.5, zorder=3, label="Post Volume")
ax.fill_between(x_numeric, volumes, alpha=0.3, color=palette["fill"], zorder=2)

# Add vertical lines for key events
# Nature pub at Jul 2024 (index 14)
ax.axvline(x=14, color=palette["event1"], linestyle='--', linewidth=1.5, alpha=0.7, zorder=2)
ax.text(14, max(volumes)*0.95, "Nature pub\n(Jul 2024)",
        fontsize=9, ha='center', va='top', color=palette["event1"], fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=palette["event1"], alpha=0.8))

# Schaeffer et al. at Mar 2025 (index 22)
ax.axvline(x=22, color=palette["event2"], linestyle='--', linewidth=1.5, alpha=0.7, zorder=2)
ax.text(22, max(volumes)*0.85, "Schaeffer et al.\n(Mar 2025)",
        fontsize=9, ha='center', va='top', color=palette["event2"], fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=palette["event2"], alpha=0.8))

# Format x-axis to show months
tick_positions = list(range(0, len(dates), 3))  # Every 3 months
tick_labels = [months_str[i] for i in tick_positions]
ax.set_xticks(tick_positions)
ax.set_xticklabels(tick_labels, rotation=45, ha='right', fontsize=9)

# Labels and title
ax.set_ylabel('Number of Posts', fontsize=11)
ax.set_xlabel('Month', fontsize=11)
ax.set_title('Monthly Relevant Post Volume', fontsize=12, fontweight='bold')

# Grid
ax.grid(axis='y', alpha=0.3, linestyle='-', linewidth=0.5)
ax.set_axisbelow(True)

# Remove spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Set y-axis to start at 0
ax.set_ylim(bottom=0)

plt.tight_layout()
plt.savefig('/Users/Joshua/agent/model-collapse-study/paper/figures/fig_monthly_volume.pdf',
            dpi=300, bbox_inches='tight')
print("Saved: fig_monthly_volume.pdf")
