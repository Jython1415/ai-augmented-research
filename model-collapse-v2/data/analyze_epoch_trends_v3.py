#!/usr/bin/env python3
"""
Epoch trend analysis with V3 data structure.
"""

import sqlite3
from pathlib import Path
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['font.size'] = 10

db_path = Path(__file__).parent / "posts.db"
figures_path = Path(__file__).parent.parent / "figures"
figures_path.mkdir(exist_ok=True)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 80)
print("EPOCH TREND ANALYSIS (V3)")
print("=" * 80)

# ============================================================================
# PASS 1 DATA
# ============================================================================

cursor.execute("""
    SELECT cu.epoch, cp1.claim_strength, cp1.paper_fidelity, cp1.field_accuracy
    FROM coding_pass1 cp1
    JOIN citation_units cu ON cp1.citation_unit_id = cu.id
    WHERE cu.epoch IS NOT NULL
    ORDER BY cu.epoch
""")
pass1_data = cursor.fetchall()

pass1_by_epoch = defaultdict(lambda: {"claim_strength": [], "paper_fidelity": [], "field_accuracy": []})

for epoch, claim_strength, paper_fidelity, field_accuracy in pass1_data:
    pass1_by_epoch[epoch]["claim_strength"].append(claim_strength)
    pass1_by_epoch[epoch]["paper_fidelity"].append(paper_fidelity)
    pass1_by_epoch[epoch]["field_accuracy"].append(field_accuracy)

epochs = sorted(pass1_by_epoch.keys())

print(f"\nPass 1 Epochs found: {epochs}")
print(f"Total records: {len(pass1_data)}")

# ============================================================================
# PASS 2 DATA
# ============================================================================

cursor.execute("""
    SELECT cu.epoch, cp2.claim_strength, cp2.paper_fidelity, cp2.field_accuracy
    FROM coding_pass2 cp2
    JOIN citation_units cu ON cp2.citation_unit_id = cu.id
    WHERE cu.epoch IS NOT NULL
    ORDER BY cu.epoch
""")
pass2_data = cursor.fetchall()

pass2_by_epoch = defaultdict(lambda: {"claim_strength": [], "paper_fidelity": [], "field_accuracy": []})

for epoch, claim_strength, paper_fidelity, field_accuracy in pass2_data:
    pass2_by_epoch[epoch]["claim_strength"].append(claim_strength)
    pass2_by_epoch[epoch]["paper_fidelity"].append(paper_fidelity)
    pass2_by_epoch[epoch]["field_accuracy"].append(field_accuracy)

print(f"Pass 2 records: {len(pass2_data)}")

# ============================================================================
# FIGURE 1: Epoch Claim Strength (Pass 1)
# ============================================================================

print("\nGenerating figures...")

claim_strength_order = ["neutral_share", "substantive_mention", "authoritative_claim"]
claim_strength_colors = ["#A8A8A8", "#7BA37B", "#5B6B7D"]

fig, ax = plt.subplots(figsize=(8, 5))

x_pos = np.arange(len(epochs))
width = 0.6

proportions = {cat: [] for cat in claim_strength_order}

for epoch in epochs:
    total = len(pass1_by_epoch[epoch]["claim_strength"])
    for cat in claim_strength_order:
        count = pass1_by_epoch[epoch]["claim_strength"].count(cat)
        proportions[cat].append(count / total if total > 0 else 0)

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
print("  Saved: epoch_claim_strength.png")

# ============================================================================
# FIGURE 2: Epoch Paper Fidelity (Pass 1)
# ============================================================================

paper_fidelity_order = ["accurate", "partially_accurate", "misrepresentation"]
paper_fidelity_colors = ["#6BA58A", "#D4A574", "#C96B6B"]

fig, ax = plt.subplots(figsize=(8, 5))

x_pos = np.arange(len(epochs))

proportions = {cat: [] for cat in paper_fidelity_order}

for epoch in epochs:
    valid_entries = [x for x in pass1_by_epoch[epoch]["paper_fidelity"] if x != "not_applicable"]
    total = len(valid_entries)
    for cat in paper_fidelity_order:
        count = valid_entries.count(cat)
        proportions[cat].append(count / total if total > 0 else 0)

bottom = np.zeros(len(epochs))
for cat, color in zip(paper_fidelity_order, paper_fidelity_colors):
    ax.bar(x_pos, proportions[cat], width, label=cat.replace("_", " ").title(),
           bottom=bottom, color=color)
    bottom += np.array(proportions[cat])

ax.set_xlabel("Epoch", fontsize=11, fontweight="bold")
ax.set_ylabel("Proportion", fontsize=11, fontweight="bold")
ax.set_title("Paper Fidelity Distribution by Epoch (Pass 1, excluding N/A)", fontsize=12, fontweight="bold")
ax.set_xticks(x_pos)
ax.set_xticklabels(epochs)
ax.legend(loc="upper left", framealpha=0.95)
ax.set_ylim([0, 1])
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig(figures_path / "epoch_paper_fidelity.png", dpi=300, bbox_inches="tight")
plt.close()
print("  Saved: epoch_paper_fidelity.png")

# ============================================================================
# FIGURE 3: Epoch Field Accuracy (Pass 1)
# ============================================================================

field_accuracy_order = ["accurate", "partially_accurate", "inaccurate"]
field_accuracy_colors = ["#6BA58A", "#D4A574", "#C96B6B"]

fig, ax = plt.subplots(figsize=(8, 5))

x_pos = np.arange(len(epochs))

proportions = {cat: [] for cat in field_accuracy_order}

for epoch in epochs:
    valid_entries = [x for x in pass1_by_epoch[epoch]["field_accuracy"] if x != "not_applicable"]
    total = len(valid_entries)
    for cat in field_accuracy_order:
        count = valid_entries.count(cat)
        proportions[cat].append(count / total if total > 0 else 0)

bottom = np.zeros(len(epochs))
for cat, color in zip(field_accuracy_order, field_accuracy_colors):
    ax.bar(x_pos, proportions[cat], width, label=cat.replace("_", " ").title(),
           bottom=bottom, color=color)
    bottom += np.array(proportions[cat])

ax.set_xlabel("Epoch", fontsize=11, fontweight="bold")
ax.set_ylabel("Proportion", fontsize=11, fontweight="bold")
ax.set_title("Field Accuracy Distribution by Epoch (Pass 1, excluding N/A)", fontsize=12, fontweight="bold")
ax.set_xticks(x_pos)
ax.set_xticklabels(epochs)
ax.legend(loc="upper left", framealpha=0.95)
ax.set_ylim([0, 1])
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig(figures_path / "epoch_field_accuracy.png", dpi=300, bbox_inches="tight")
plt.close()
print("  Saved: epoch_field_accuracy.png")

# ============================================================================
# FIGURE 4: Two-Pass Comparison by Epoch
# ============================================================================

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Subplot 1: Claim Strength - Authoritative
ax = axes[0]
x_pos = np.arange(len(epochs))
width = 0.35

pass1_props = []
pass2_props = []

for epoch in epochs:
    total1 = len(pass1_by_epoch[epoch]["claim_strength"])
    count1 = pass1_by_epoch[epoch]["claim_strength"].count("authoritative_claim")
    pass1_props.append(count1 / total1 if total1 > 0 else 0)

    total2 = len(pass2_by_epoch[epoch]["claim_strength"])
    count2 = pass2_by_epoch[epoch]["claim_strength"].count("authoritative_claim")
    pass2_props.append(count2 / total2 if total2 > 0 else 0)

ax.bar(x_pos - width/2, pass1_props, width, label="Pass 1", color="#7BA37B", alpha=0.8)
ax.bar(x_pos + width/2, pass2_props, width, label="Pass 2", color="#5B6B7D", alpha=0.8)

ax.set_xlabel("Epoch", fontsize=10, fontweight="bold")
ax.set_ylabel("Proportion (Authoritative)", fontsize=10, fontweight="bold")
ax.set_title("Claim Strength: Authoritative", fontsize=11, fontweight="bold")
ax.set_xticks(x_pos)
ax.set_xticklabels(epochs)
ax.legend(framealpha=0.95)
ax.grid(axis="y", alpha=0.3)

# Subplot 2: Paper Fidelity - Accurate
ax = axes[1]
pass1_props = []
pass2_props = []

for epoch in epochs:
    valid1 = [x for x in pass1_by_epoch[epoch]["paper_fidelity"] if x != "not_applicable"]
    total1 = len(valid1)
    count1 = valid1.count("accurate")
    pass1_props.append(count1 / total1 if total1 > 0 else 0)

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

# Subplot 3: Field Accuracy - Accurate
ax = axes[2]
pass1_props = []
pass2_props = []

for epoch in epochs:
    valid1 = [x for x in pass1_by_epoch[epoch]["field_accuracy"] if x != "not_applicable"]
    total1 = len(valid1)
    count1 = valid1.count("accurate")
    pass1_props.append(count1 / total1 if total1 > 0 else 0)

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
plt.savefig(figures_path / "twopass_comparison_by_epoch.png", dpi=300, bbox_inches="tight")
plt.close()
print("  Saved: twopass_comparison_by_epoch.png")

# ============================================================================
# SUMMARY STATISTICS
# ============================================================================

print("\n" + "=" * 80)
print("EPOCH TREND SUMMARY")
print("=" * 80)

print("\nPass 1 - Accurate Paper Fidelity % by Epoch (excluding N/A):")
for epoch in epochs:
    valid = [x for x in pass1_by_epoch[epoch]["paper_fidelity"] if x != "not_applicable"]
    if valid:
        accurate_pct = 100 * valid.count("accurate") / len(valid)
        print(f"  Epoch {epoch}: {accurate_pct:.1f}% ({valid.count('accurate')}/{len(valid)})")

print("\nPass 1 - Accurate Field Accuracy % by Epoch (excluding N/A):")
for epoch in epochs:
    valid = [x for x in pass1_by_epoch[epoch]["field_accuracy"] if x != "not_applicable"]
    if valid:
        accurate_pct = 100 * valid.count("accurate") / len(valid)
        print(f"  Epoch {epoch}: {accurate_pct:.1f}% ({valid.count('accurate')}/{len(valid)})")

print("\n" + "=" * 80)

conn.close()
