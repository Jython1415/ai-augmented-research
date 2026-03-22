#!/usr/bin/env python3
"""
/// script
requires-python = ">=3.10"
dependencies = [
    "matplotlib",
    "numpy",
]
///
"""

import sqlite3
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

DB_PATH = "/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/data/posts.db"
OUTPUT_DIR = "/Users/Joshua/agent/ai-augmented-research/model-collapse-v2/paper/"

DISTORTION_TAGS = [
    "certainty_inflation",
    "scope_inflation",
    "temporal_overclaim",
    "causal_conflation",
    "mechanism_omission",
    "mitigation_blindness",
    "definitional_conflation",
    "sensationalism",
]

# Use a clean style
matplotlib.style.use('default')
plt.rcParams['font.size'] = 10
plt.rcParams['axes.edgecolor'] = 'black'
plt.rcParams['axes.linewidth'] = 1
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'


def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_all_coding_data():
    """Fetch all coding_v4 records with citation unit info."""
    conn = connect_db()
    query = """
    SELECT
        cv.id,
        cv.citation_unit_id,
        cv.claim_strength,
        cv.certainty_inflation,
        cv.scope_inflation,
        cv.temporal_overclaim,
        cv.causal_conflation,
        cv.mechanism_omission,
        cv.mitigation_blindness,
        cv.definitional_conflation,
        cv.sensationalism,
        cv.epoch,
        cu.citation_type
    FROM coding_v4 cv
    JOIN citation_units cu ON cv.citation_unit_id = cu.id
    ORDER BY cv.epoch, cv.citation_unit_id
    """
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows


def compute_distortion_tags(row):
    """Extract distortion tags from a row as a list."""
    tags = []
    for tag in DISTORTION_TAGS:
        if row[tag] == 1:
            tags.append(tag)
    return tags


def prepare_epoch_data(rows):
    """Organize rows by epoch."""
    epoch_data = defaultdict(list)
    for row in rows:
        if row["epoch"]:
            epoch_data[row["epoch"]].append(row)
    return epoch_data


def fig1_tags_by_epoch(rows):
    """Generate stacked bar chart of distortion tags by epoch."""
    epoch_data = prepare_epoch_data(rows)
    epochs = sorted(epoch_data.keys())

    # Collect tag counts by epoch
    tag_counts_by_epoch = {}
    for epoch in epochs:
        epoch_rows = epoch_data[epoch]
        epoch_substantive = [r for r in epoch_rows if r["claim_strength"] == "substantive_mention"]
        tag_counts = defaultdict(int)
        for row in epoch_substantive:
            tags = compute_distortion_tags(row)
            for tag in tags:
                tag_counts[tag] += 1
        tag_counts_by_epoch[epoch] = tag_counts

    # Prepare data for stacked bar
    tag_data = {tag: [] for tag in DISTORTION_TAGS}
    for epoch in epochs:
        counts = tag_counts_by_epoch[epoch]
        for tag in DISTORTION_TAGS:
            tag_data[tag].append(counts.get(tag, 0))

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    x = np.arange(len(epochs))
    width = 0.6
    bottom = np.zeros(len(epochs))

    colors = plt.cm.tab10(np.linspace(0, 1, len(DISTORTION_TAGS)))

    for i, tag in enumerate(DISTORTION_TAGS):
        ax.bar(x, tag_data[tag], width, label=tag.replace('_', ' ').title(),
               bottom=bottom, color=colors[i], edgecolor='white', linewidth=0.5)
        bottom += np.array(tag_data[tag])

    ax.set_xlabel('Epoch', fontsize=11, fontweight='bold')
    ax.set_ylabel('Count', fontsize=11, fontweight='bold')
    ax.set_title('Distortion Tag Frequency by Epoch\n(Substantive Posts Only)',
                 fontsize=12, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels([f'Epoch {e}' for e in epochs])
    ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=9, frameon=True)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    plt.tight_layout()
    fig.savefig(f'{OUTPUT_DIR}v4_tags_by_epoch.png', dpi=300, bbox_inches='tight')
    print("Saved: v4_tags_by_epoch.png")
    plt.close()


def fig2_cooccurrence_heatmap(rows):
    """Generate heatmap of tag co-occurrence."""
    substantive_rows = [r for r in rows if r["claim_strength"] == "substantive_mention"]

    # Build co-occurrence matrix
    cooccurrence = np.zeros((len(DISTORTION_TAGS), len(DISTORTION_TAGS)))
    tag_to_idx = {tag: i for i, tag in enumerate(DISTORTION_TAGS)}

    for row in substantive_rows:
        tags = compute_distortion_tags(row)
        for tag1 in tags:
            for tag2 in tags:
                i, j = tag_to_idx[tag1], tag_to_idx[tag2]
                cooccurrence[i, j] += 1

    # Create heatmap
    fig, ax = plt.subplots(figsize=(10, 9))

    im = ax.imshow(cooccurrence, cmap='YlOrRd', aspect='auto')

    # Set ticks and labels
    tag_labels = [t.replace('_', '\n') for t in DISTORTION_TAGS]
    ax.set_xticks(np.arange(len(DISTORTION_TAGS)))
    ax.set_yticks(np.arange(len(DISTORTION_TAGS)))
    ax.set_xticklabels(tag_labels, fontsize=8, rotation=45, ha='right')
    ax.set_yticklabels(tag_labels, fontsize=8)

    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Co-occurrence Count', fontsize=10, fontweight='bold')

    ax.set_title('Tag Co-occurrence Matrix\n(Substantive Posts Only)',
                 fontsize=12, fontweight='bold', pad=15)

    # Add text annotations
    for i in range(len(DISTORTION_TAGS)):
        for j in range(len(DISTORTION_TAGS)):
            if cooccurrence[i, j] > 0:
                text = ax.text(j, i, int(cooccurrence[i, j]),
                              ha="center", va="center", color="black", fontsize=8, fontweight='bold')

    plt.tight_layout()
    fig.savefig(f'{OUTPUT_DIR}v4_cooccurrence.png', dpi=300, bbox_inches='tight')
    print("Saved: v4_cooccurrence.png")
    plt.close()


def fig3_distortion_rate_by_epoch(rows):
    """Generate line chart of any distortion rate by epoch."""
    epoch_data = prepare_epoch_data(rows)
    epochs = sorted(epoch_data.keys())

    rates = []
    counts = []
    for epoch in epochs:
        epoch_rows = epoch_data[epoch]
        epoch_substantive = [r for r in epoch_rows if r["claim_strength"] == "substantive_mention"]
        n = len(epoch_substantive)
        with_distortion = sum(1 for r in epoch_substantive if len(compute_distortion_tags(r)) > 0)
        rate = (with_distortion / n * 100) if n > 0 else 0
        rates.append(rate)
        counts.append(n)

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot line with markers
    ax.plot(epochs, rates, marker='o', linewidth=2.5, markersize=8,
            color='#d62728', label='Distortion Rate')

    # Add error bars (optional: based on binomial proportion)
    errors = []
    for rate, n in zip(rates, counts):
        if n > 0:
            p = rate / 100
            se = np.sqrt(p * (1 - p) / n) * 100
            errors.append(se)
        else:
            errors.append(0)
    ax.errorbar(epochs, rates, yerr=errors, fmt='none', capsize=5,
                capthick=2, ecolor='#d62728', alpha=0.6, linewidth=1.5)

    ax.set_xlabel('Epoch', fontsize=11, fontweight='bold')
    ax.set_ylabel('Distortion Rate (%)', fontsize=11, fontweight='bold')
    ax.set_title('Rate of Posts with Any Distortion by Epoch\n(Substantive Posts Only)',
                 fontsize=12, fontweight='bold', pad=15)
    ax.set_xticks(epochs)
    ax.set_xticklabels([f'Epoch {e}' for e in epochs])
    ax.set_ylim(0, 105)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    # Add value labels on points
    for epoch, rate, n in zip(epochs, rates, counts):
        ax.text(epoch, rate + 3, f'{rate:.1f}%\n(n={n})',
               ha='center', fontsize=9, fontweight='bold')

    plt.tight_layout()
    fig.savefig(f'{OUTPUT_DIR}v4_distortion_rate.png', dpi=300, bbox_inches='tight')
    print("Saved: v4_distortion_rate.png")
    plt.close()


def fig4_claim_strength_by_epoch(rows):
    """Generate grouped bar chart of claim strength distribution by epoch."""
    epoch_data = prepare_epoch_data(rows)
    epochs = sorted(epoch_data.keys())

    # Collect claim strengths by epoch
    claim_strengths = ['neutral_share', 'substantive_mention', 'authoritative_claim']
    strength_counts = {cs: [] for cs in claim_strengths}

    for epoch in epochs:
        epoch_rows = epoch_data[epoch]
        counts = Counter(r["claim_strength"] for r in epoch_rows)
        for cs in claim_strengths:
            strength_counts[cs].append(counts.get(cs, 0))

    # Create figure
    fig, ax = plt.subplots(figsize=(11, 6))

    x = np.arange(len(epochs))
    width = 0.25

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    labels = ['Neutral Share', 'Substantive Mention', 'Authoritative Claim']

    for i, (cs, label, color) in enumerate(zip(claim_strengths, labels, colors)):
        offset = width * (i - 1)
        ax.bar(x + offset, strength_counts[cs], width, label=label,
               color=color, edgecolor='black', linewidth=0.5)

    ax.set_xlabel('Epoch', fontsize=11, fontweight='bold')
    ax.set_ylabel('Count', fontsize=11, fontweight='bold')
    ax.set_title('Claim Strength Distribution by Epoch',
                 fontsize=12, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels([f'Epoch {e}' for e in epochs])
    ax.legend(fontsize=10, frameon=True, loc='upper left')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    plt.tight_layout()
    fig.savefig(f'{OUTPUT_DIR}v4_claim_strength_by_epoch.png', dpi=300, bbox_inches='tight')
    print("Saved: v4_claim_strength_by_epoch.png")
    plt.close()


def main():
    rows = get_all_coding_data()
    print(f"Loaded {len(rows)} rows from coding_v4")

    print("\nGenerating figures...")
    fig1_tags_by_epoch(rows)
    fig2_cooccurrence_heatmap(rows)
    fig3_distortion_rate_by_epoch(rows)
    fig4_claim_strength_by_epoch(rows)

    print(f"\nAll figures saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
