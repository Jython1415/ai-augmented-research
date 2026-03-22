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

# Data from Appendix A1
epochs = ["E1\n(n=336)", "E2\n(n=226)", "E3\n(n=554)", "E4\n(n=1,665)"]
accurate = [21.7, 34.1, 26.7, 25.0]
oversimplified = [47.0, 48.2, 42.6, 46.2]
wrong = [5.7, 2.2, 4.7, 6.3]
unfalsifiable = [25.6, 15.5, 26.0, 22.5]

x = np.arange(len(epochs))
width = 0.2

fig, ax = plt.subplots(figsize=(10, 6))

# Create bars
bars1 = ax.bar(x - 1.5*width, accurate, width, label="Accurate",
               color=palette["accurate"], edgecolor="none")
bars2 = ax.bar(x - 0.5*width, oversimplified, width, label="Oversimplified",
               color=palette["oversimplified"], edgecolor="none")
bars3 = ax.bar(x + 0.5*width, wrong, width, label="Wrong",
               color=palette["wrong"], edgecolor="none")
bars4 = ax.bar(x + 1.5*width, unfalsifiable, width, label="Unfalsifiable",
               color=palette["unfalsifiable"], edgecolor="none")

# Add percentage labels directly on bars
for bars in [bars1, bars2, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        if height > 2:  # Only label if bar is tall enough to be readable
            ax.text(bar.get_x() + bar.get_width()/2., height/2.,
                   f'{height:.1f}%',
                   ha='center', va='center', fontsize=9, fontweight='bold',
                   color='white')

ax.set_ylabel('Percentage (%)', fontsize=11)
ax.set_xlabel('Knowledge Epoch', fontsize=11)
ax.set_title('Accuracy Distribution by Knowledge Epoch', fontsize=12, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(epochs, fontsize=10)
ax.set_ylim(0, 55)
ax.grid(axis='y', alpha=0.3, linestyle='-', linewidth=0.5)
ax.set_axisbelow(True)

# Remove top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Add legend below chart for clarity
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=4,
          frameon=False, fontsize=10)

plt.tight_layout()
plt.savefig('/Users/Joshua/agent/model-collapse-study/paper/figures/fig_accuracy_epoch.pdf',
            dpi=300, bbox_inches='tight')
print("Saved: fig_accuracy_epoch.pdf")
