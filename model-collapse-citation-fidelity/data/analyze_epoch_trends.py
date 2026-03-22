#!/usr/bin/env python3
"""
/// script
requires-python = ">=3.10"
dependencies = [
    "matplotlib",
    "numpy",
    "seaborn",
    "sqlite3",
]
///
"""

import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from collections import defaultdict

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['font.size'] = 10

# Database path
db_path = Path(__file__).parent / "posts.db"
figures_path = Path(__file__).parent.parent / "figures"
figures_path.mkdir(exist_ok=True)

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# ============================================================================
# PASS 1 DATA - Query citation_units with coding_pass=1
# ============================================================================

# Get all Pass 1 data
cursor.execute("""
    SELECT epoch, claim_strength, paper_fidelity, field_accuracy
    FROM citation_units
    WHERE coding_pass = '1' AND epoch IS NOT NULL
    ORDER BY epoch
""")
pass1_data = cursor.fetchall()

# Organize data by epoch
pass1_by_epoch = defaultdict(lambda: {"claim_strength": [], "paper_fidelity": [], "field_accuracy": []})

for epoch, claim_strength, paper_fidelity, field_accuracy in pass1_data:
    pass1_by_epoch[epoch]["claim_strength"].append(claim_strength)
    pass1_by_epoch[epoch]["paper_fidelity"].append(paper_fidelity)
    pass1_by_epoch[epoch]["field_accuracy"].append(field_accuracy)

epochs = sorted(pass1_by_epoch.keys())

# ============================================================================
# PASS 2 DATA - Get citations with corresponding epoch info
# ============================================================================

cursor.execute("""
    SELECT cu.epoch, cp.claim_strength, cp.paper_fidelity, cp.field_accuracy
    FROM coding_pass2 cp
    JOIN citation_units cu ON cp.citation_unit_id = cu.id
    WHERE cu.epoch IS NOT NULL
    ORDER BY cu.epoch
""")
pass2_data = cursor.fetchall()

# Organize data by epoch
pass2_by_epoch = defaultdict(lambda: {"claim_strength": [], "paper_fidelity": [], "field_accuracy": []})

for epoch, claim_strength, paper_fidelity, field_accuracy in pass2_data:
    pass2_by_epoch[epoch]["claim_strength"].append(claim_strength)
    pass2_by_epoch[epoch]["paper_fidelity"].append(paper_fidelity)
    pass2_by_epoch[epoch]["field_accuracy"].append(field_accuracy)

conn.close()

# ============================================================================
# FIGURE 1: Epoch Claim Strength (Pass 1)
# ============================================================================

claim_strength_order = ["neutral_share", "substantive_mention", "authoritative_claim"]
claim_strength_colors = ["#A8A8A8", "#7BA37B", "#5B6B7D"]

fig, ax = plt.subplots(figsize=(8, 5))

x_pos = np.arange(len(epochs))
width = 0.6

# Calculate proportions for each category
proportions = {cat: [] for cat in claim_strength_order}

for epoch in epochs:
    total = len(pass1_by_epoch[epoch]["claim_strength"])
    for cat in claim_strength_order:
        count = pass1_by_epoch[epoch]["claim_strength"].count(cat)
        proportions[cat].append(count / total if total > 0 else 0)

# Stack bars
bottom = np.zeros(len(epochs))
for cat, color in zip(claim_strength_order, claim_strength_colors):
    ax.bar(x_pos, proportions[cat], width, label=cat.replace("_", " ").title(),
           bottom=bottom, color=color)
    bottom += np.array(proportions[cat])

ax.set_xlabel("Epoch", fontsize=11, fontweight="bold")
ax.set_ylabel("Proportion", fontsize=11, fontweight="bold")
ax.set_title("Claim Strength Distribution by Epoch (Pass 1)", fontsize=12, fontweight="bold")
ax.set_xticks(x_pos)
ax.set_xticklabels(epochs)
ax.legend(loc="upper left", framealpha=0.95)
ax.set_ylim([0, 1])
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig(figures_path / "epoch_claim_strength.png", dpi=300, bbox_inches="tight")
plt.close()

print("✓ Generated epoch_claim_strength.png")

# ============================================================================
# FIGURE 2: Epoch Paper Fidelity (Pass 1, excluding not_applicable)
# ============================================================================

paper_fidelity_order = ["accurate", "partially_accurate", "misrepresentation"]
paper_fidelity_colors = ["#6BA58A", "#D4A574", "#C96B6B"]

fig, ax = plt.subplots(figsize=(8, 5))

x_pos = np.arange(len(epochs))

# Calculate proportions excluding not_applicable
proportions = {cat: [] for cat in paper_fidelity_order}

for epoch in epochs:
    valid_entries = [x for x in pass1_by_epoch[epoch]["paper_fidelity"] if x != "not_applicable"]
    total = len(valid_entries)
    for cat in paper_fidelity_order:
        count = valid_entries.count(cat)
        proportions[cat].append(count / total if total > 0 else 0)

# Stack bars
bottom = np.zeros(len(epochs))
for cat, color in zip(paper_fidelity_order, paper_fidelity_colors):
    ax.bar(x_pos, proportions[cat], width, label=cat.replace("_", " ").title(),
           bottom=bottom, color=color)
    bottom += np.array(proportions[cat])

ax.set_xlabel("Epoch", fontsize=11, fontweight="bold")
ax.set_ylabel("Proportion", fontsize=11, fontweight="bold")
ax.set_title("Paper Fidelity Distribution by Epoch (Pass 1)", fontsize=12, fontweight="bold")
ax.set_xticks(x_pos)
ax.set_xticklabels(epochs)
ax.legend(loc="upper left", framealpha=0.95)
ax.set_ylim([0, 1])
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig(figures_path / "epoch_paper_fidelity.png", dpi=300, bbox_inches="tight")
plt.close()

print("✓ Generated epoch_paper_fidelity.png")

# ============================================================================
# FIGURE 3: Epoch Field Accuracy (Pass 1, excluding not_applicable)
# ============================================================================

field_accuracy_order = ["accurate", "partially_accurate", "inaccurate"]
field_accuracy_colors = ["#6BA58A", "#D4A574", "#C96B6B"]

fig, ax = plt.subplots(figsize=(8, 5))

x_pos = np.arange(len(epochs))

# Calculate proportions excluding not_applicable
proportions = {cat: [] for cat in field_accuracy_order}

for epoch in epochs:
    valid_entries = [x for x in pass1_by_epoch[epoch]["field_accuracy"] if x != "not_applicable"]
    total = len(valid_entries)
    for cat in field_accuracy_order:
        count = valid_entries.count(cat)
        proportions[cat].append(count / total if total > 0 else 0)

# Stack bars
bottom = np.zeros(len(epochs))
for cat, color in zip(field_accuracy_order, field_accuracy_colors):
    ax.bar(x_pos, proportions[cat], width, label=cat.replace("_", " ").title(),
           bottom=bottom, color=color)
    bottom += np.array(proportions[cat])

ax.set_xlabel("Epoch", fontsize=11, fontweight="bold")
ax.set_ylabel("Proportion", fontsize=11, fontweight="bold")
ax.set_title("Field Accuracy Distribution by Epoch (Pass 1)", fontsize=12, fontweight="bold")
ax.set_xticks(x_pos)
ax.set_xticklabels(epochs)
ax.legend(loc="upper left", framealpha=0.95)
ax.set_ylim([0, 1])
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig(figures_path / "epoch_field_accuracy.png", dpi=300, bbox_inches="tight")
plt.close()

print("✓ Generated epoch_field_accuracy.png")

# ============================================================================
# FIGURE 4: Two-Pass Comparison
# ============================================================================

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Subplot 1: Claim Strength
ax = axes[0]
x_pos = np.arange(len(epochs))
width = 0.35

pass1_props = []
pass2_props = []

for epoch in epochs:
    # Pass 1
    total1 = len(pass1_by_epoch[epoch]["claim_strength"])
    count1 = pass1_by_epoch[epoch]["claim_strength"].count("authoritative_claim")
    pass1_props.append(count1 / total1 if total1 > 0 else 0)

    # Pass 2
    total2 = len(pass2_by_epoch[epoch]["claim_strength"])
    count2 = pass2_by_epoch[epoch]["claim_strength"].count("authoritative_claim")
    pass2_props.append(count2 / total2 if total2 > 0 else 0)

ax.bar(x_pos - width/2, pass1_props, width, label="Pass 1", color="#7BA37B", alpha=0.8)
ax.bar(x_pos + width/2, pass2_props, width, label="Pass 2", color="#5B6B7D", alpha=0.8)

ax.set_xlabel("Epoch", fontsize=10, fontweight="bold")
ax.set_ylabel("Proportion (Authoritative)", fontsize=10, fontweight="bold")
ax.set_title("Claim Strength: Authoritative Claim", fontsize=11, fontweight="bold")
ax.set_xticks(x_pos)
ax.set_xticklabels(epochs)
ax.legend(framealpha=0.95)
ax.grid(axis="y", alpha=0.3)

# Subplot 2: Paper Fidelity
ax = axes[1]
pass1_props = []
pass2_props = []

for epoch in epochs:
    # Pass 1
    valid1 = [x for x in pass1_by_epoch[epoch]["paper_fidelity"] if x != "not_applicable"]
    total1 = len(valid1)
    count1 = valid1.count("accurate")
    pass1_props.append(count1 / total1 if total1 > 0 else 0)

    # Pass 2
    valid2 = [x for x in pass2_by_epoch[epoch]["paper_fidelity"] if x != "not_applicable"]
    total2 = len(valid2)
    count2 = valid2.count("accurate")
    pass2_props.append(count2 / total2 if total2 > 0 else 0)

ax.bar(x_pos - width/2, pass1_props, width, label="Pass 1", color="#6BA58A", alpha=0.8)
ax.bar(x_pos + width/2, pass2_props, width, label="Pass 2", color="#C96B6B", alpha=0.8)

ax.set_xlabel("Epoch", fontsize=10, fontweight="bold")
ax.set_ylabel("Proportion (Accurate)", fontsize=10, fontweight="bold")
ax.set_title("Paper Fidelity: Accurate", fontsize=11, fontweight="bold")
ax.set_xticks(x_pos)
ax.set_xticklabels(epochs)
ax.legend(framealpha=0.95)
ax.grid(axis="y", alpha=0.3)

# Subplot 3: Field Accuracy
ax = axes[2]
pass1_props = []
pass2_props = []

for epoch in epochs:
    # Pass 1
    valid1 = [x for x in pass1_by_epoch[epoch]["field_accuracy"] if x != "not_applicable"]
    total1 = len(valid1)
    count1 = valid1.count("accurate")
    pass1_props.append(count1 / total1 if total1 > 0 else 0)

    # Pass 2
    valid2 = [x for x in pass2_by_epoch[epoch]["field_accuracy"] if x != "not_applicable"]
    total2 = len(valid2)
    count2 = valid2.count("accurate")
    pass2_props.append(count2 / total2 if total2 > 0 else 0)

ax.bar(x_pos - width/2, pass1_props, width, label="Pass 1", color="#6BA58A", alpha=0.8)
ax.bar(x_pos + width/2, pass2_props, width, label="Pass 2", color="#C96B6B", alpha=0.8)

ax.set_xlabel("Epoch", fontsize=10, fontweight="bold")
ax.set_ylabel("Proportion (Accurate)", fontsize=10, fontweight="bold")
ax.set_title("Field Accuracy: Accurate", fontsize=11, fontweight="bold")
ax.set_xticks(x_pos)
ax.set_xticklabels(epochs)
ax.legend(framealpha=0.95)
ax.grid(axis="y", alpha=0.3)

plt.suptitle("Pass 1 vs Pass 2 Comparison by Epoch", fontsize=13, fontweight="bold", y=1.00)
plt.tight_layout()
plt.savefig(figures_path / "twopass_comparison.png", dpi=300, bbox_inches="tight")
plt.close()

print("✓ Generated twopass_comparison.png")

print(f"\n✓ All figures saved to {figures_path}")
