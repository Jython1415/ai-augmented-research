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
import numpy as np

# Colorblind-accessible palette
palette = {
    "accurate": "#4477AA",      # blue
    "oversimplified": "#EE6677",  # red
    "wrong": "#228833",         # green
    "unfalsifiable": "#CCBB44"  # yellow
}

# Data from Table 2.5, sorted by accuracy rate (highest to lowest)
sources = [
    ("Other paper\n(n=270)", 76.7, 14.4, 1.1, 7.8),
    ("Nature paper\n(n=132)", 57.6, 36.4, 3.0, 3.0),
    ("Quote post\n(n=55)", 30.9, 40.0, 5.5, 23.6),
    ("News article\n(n=390)", 19.5, 60.8, 2.8, 16.9),
    ("None\n(n=1,934)", 17.5, 47.9, 6.9, 27.7)
]

source_names = [s[0] for s in sources]
accurate = [s[1] for s in sources]
oversimplified = [s[2] for s in sources]
wrong = [s[3] for s in sources]
unfalsifiable = [s[4] for s in sources]

y_pos = np.arange(len(source_names))

fig, ax = plt.subplots(figsize=(11, 6))

# Create horizontal stacked bars
bars1 = ax.barh(y_pos, accurate, label='Accurate',
                color=palette["accurate"], edgecolor='none')
bars2 = ax.barh(y_pos, oversimplified, left=accurate,
                label='Oversimplified', color=palette["oversimplified"], edgecolor='none')

left_wrong = np.array(accurate) + np.array(oversimplified)
bars3 = ax.barh(y_pos, wrong, left=left_wrong,
                label='Wrong', color=palette["wrong"], edgecolor='none')

left_unfalsifiable = left_wrong + np.array(wrong)
bars4 = ax.barh(y_pos, unfalsifiable, left=left_unfalsifiable,
                label='Unfalsifiable', color=palette["unfalsifiable"], edgecolor='none')

# Add percentage labels directly on segments
for i in range(len(source_names)):
    # Accurate
    if accurate[i] > 5:
        ax.text(accurate[i]/2, i, f'{accurate[i]:.1f}%',
               va='center', ha='center', fontsize=9, fontweight='bold', color='white')

    # Oversimplified
    if oversimplified[i] > 5:
        ax.text(accurate[i] + oversimplified[i]/2, i, f'{oversimplified[i]:.1f}%',
               va='center', ha='center', fontsize=9, fontweight='bold', color='white')

    # Wrong (only label if segment is visible)
    if wrong[i] > 3:
        ax.text(left_wrong[i] + wrong[i]/2, i, f'{wrong[i]:.1f}%',
               va='center', ha='center', fontsize=9, fontweight='bold', color='white')

    # Unfalsifiable
    if unfalsifiable[i] > 5:
        ax.text(left_unfalsifiable[i] + unfalsifiable[i]/2, i, f'{unfalsifiable[i]:.1f}%',
               va='center', ha='center', fontsize=9, fontweight='bold', color='white')

ax.set_yticks(y_pos)
ax.set_yticklabels(source_names, fontsize=10)
ax.set_xlabel('Percentage (%)', fontsize=11)
ax.set_title('Accuracy Distribution by Source Type', fontsize=12, fontweight='bold')
ax.set_xlim(0, 105)
ax.grid(axis='x', alpha=0.3, linestyle='-', linewidth=0.5)
ax.set_axisbelow(True)

# Remove spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Place legend below chart to avoid title overlap
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=4,
          frameon=False, fontsize=10)

plt.tight_layout()
plt.savefig('/Users/Joshua/agent/model-collapse-study/paper/figures/fig_accuracy_source.pdf',
            dpi=300, bbox_inches='tight')
print("Saved: fig_accuracy_source.pdf")
