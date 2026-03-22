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

# Data from Table 2.4
data = np.array([
    [89.9, 7.8, 0.2, 2.1],      # Cites post-2024
    [17.5, 69.4, 6.0, 7.1],     # Only original
    [8.8, 44.2, 7.2, 39.8]      # No citations
])

awareness_labels = [
    "Cites post-2024\n(n=486)",
    "Only original\n(n=870)",
    "No citations\n(n=1,425)"
]

accuracy_labels = ["Accurate", "Oversimplified", "Wrong", "Unfalsifiable"]

fig, ax = plt.subplots(figsize=(9, 5))

# Create heatmap using a sequential colormap
im = ax.imshow(data, cmap='YlOrRd', aspect='auto', vmin=0, vmax=100)

# Set ticks and labels
ax.set_xticks(np.arange(len(accuracy_labels)))
ax.set_yticks(np.arange(len(awareness_labels)))
ax.set_xticklabels(accuracy_labels, fontsize=10)
ax.set_yticklabels(awareness_labels, fontsize=10)

# Rotate x-axis labels to be horizontal (no rotation)
plt.setp(ax.get_xticklabels(), rotation=0, ha="center")

# Add text annotations
for i in range(len(awareness_labels)):
    for j in range(len(accuracy_labels)):
        value = data[i, j]
        # Choose text color based on background intensity
        text_color = 'white' if value > 50 else 'black'
        text = ax.text(j, i, f'{value:.1f}%',
                      ha="center", va="center", color=text_color,
                      fontsize=11, fontweight='bold')

ax.set_title('Accuracy by Literature Awareness', fontsize=12, fontweight='bold')
ax.set_xlabel('Accuracy Category', fontsize=11)
ax.set_ylabel('Literature Awareness', fontsize=11)

# Remove spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

# Add colorbar
cbar = plt.colorbar(im, ax=ax, pad=0.02)
cbar.set_label('Percentage (%)', fontsize=10)

plt.tight_layout()
plt.savefig('/Users/Joshua/agent/model-collapse-study/paper/figures/fig_awareness_accuracy.pdf',
            dpi=300, bbox_inches='tight')
print("Saved: fig_awareness_accuracy.pdf")
