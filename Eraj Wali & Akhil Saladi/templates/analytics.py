import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def compute_displacements(data):
    if len(data) < 2:
        return np.array([])
    dx = np.diff([p["x"] for p in data])
    dy = np.diff([p["y"] for p in data])
    return np.hypot(dx, dy)


def compute_speeds(data):
    if len(data) < 2:
        return np.array([])
    if not all("t" in p for p in data):
        return np.array([])

    t = np.array([p["t"] for p in data], dtype=float)
    dt_ms = np.diff(t)
    valid = dt_ms > 0
    if not np.any(valid):
        return np.array([])

    disp = compute_displacements(data)[valid]
    dt_s = dt_ms[valid] / 1000.0
    return disp / dt_s


def summarize(data):
    disp = compute_displacements(data)
    speed = compute_speeds(data)
    return {
        "count": len(data),
        "mean_jitter": float(np.mean(disp)) if len(disp) else 0.0,
        "median_jitter": float(np.median(disp)) if len(disp) else 0.0,
        "p95_jitter": float(np.percentile(disp, 95)) if len(disp) else 0.0,
        "max_jump": float(np.max(disp)) if len(disp) else 0.0,
        "mean_speed": float(np.mean(speed)) if len(speed) else 0.0,
        "p95_speed": float(np.percentile(speed, 95)) if len(speed) else 0.0,
        "disp": disp,
    }


def percent_improvement(before, after):
    if before <= 0:
        return 0.0
    return ((before - after) / before) * 100.0


base_dir = Path(__file__).resolve().parent
raw_path = base_dir / "gaze_raw.json"
smooth_path = base_dir / "gaze_smoothed.json"

raw_data = load_json(raw_path)
smooth_data = load_json(smooth_path)

raw = summarize(raw_data)
smooth = summarize(smooth_data)

mean_improve = percent_improvement(raw["mean_jitter"], smooth["mean_jitter"])
p95_improve = percent_improvement(raw["p95_jitter"], smooth["p95_jitter"])
max_jump_improve = percent_improvement(raw["max_jump"], smooth["max_jump"])

print("=== Gaze Stability Summary ===")
print(f"Samples: raw={raw['count']} | smooth={smooth['count']}")
print(
    f"Mean jitter: {raw['mean_jitter']:.2f}px -> {smooth['mean_jitter']:.2f}px "
    f"({mean_improve:.1f}% lower)"
)
print(
    f"95th jitter: {raw['p95_jitter']:.2f}px -> {smooth['p95_jitter']:.2f}px "
    f"({p95_improve:.1f}% lower)"
)
print(
    f"Max jump: {raw['max_jump']:.2f}px -> {smooth['max_jump']:.2f}px "
    f"({max_jump_improve:.1f}% lower)"
)
if raw["mean_speed"] > 0 or smooth["mean_speed"] > 0:
    print(
        f"Mean speed: {raw['mean_speed']:.1f}px/s -> {smooth['mean_speed']:.1f}px/s"
    )
    print(f"95th speed: {raw['p95_speed']:.1f}px/s -> {smooth['p95_speed']:.1f}px/s")

plt.style.use("seaborn-v0_8-whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(13, 8))
fig.suptitle("Raw vs Smoothed Gaze: Stability Analysis", fontsize=15, fontweight="bold")

# Top-left: key jitter metrics
ax = axes[0, 0]
metric_names = ["Mean jitter", "Median jitter", "95th jitter", "Max jump"]
raw_vals = [raw["mean_jitter"], raw["median_jitter"], raw["p95_jitter"], raw["max_jump"]]
smooth_vals = [
    smooth["mean_jitter"],
    smooth["median_jitter"],
    smooth["p95_jitter"],
    smooth["max_jump"],
]
x = np.arange(len(metric_names))
w = 0.38
ax.bar(x - w / 2, raw_vals, w, label="Raw", color="#d95f02")
ax.bar(x + w / 2, smooth_vals, w, label="Smoothed", color="#1b9e77")
ax.set_xticks(x)
ax.set_xticklabels(metric_names, rotation=12)
ax.set_ylabel("Pixels")
ax.set_title("Jitter Metrics")
ax.legend()

# Top-right: frame-to-frame displacement traces
ax = axes[0, 1]
if len(raw["disp"]):
    ax.plot(raw["disp"], label="Raw", color="#d95f02", alpha=0.65, linewidth=1.0)
if len(smooth["disp"]):
    ax.plot(
        smooth["disp"],
        label="Smoothed",
        color="#1b9e77",
        alpha=0.8,
        linewidth=1.2,
    )
ax.set_title("Frame-to-Frame Displacement Over Time")
ax.set_xlabel("Frame Index")
ax.set_ylabel("Pixels")
ax.legend()

# Bottom-left: displacement distribution
ax = axes[1, 0]
if len(raw["disp"]) and len(smooth["disp"]):
    upper = np.percentile(np.concatenate([raw["disp"], smooth["disp"]]), 99)
    bins = np.linspace(0, max(upper, 1), 35)
    ax.hist(raw["disp"], bins=bins, alpha=0.5, label="Raw", color="#d95f02", density=True)
    ax.hist(
        smooth["disp"],
        bins=bins,
        alpha=0.6,
        label="Smoothed",
        color="#1b9e77",
        density=True,
    )
ax.set_title("Displacement Distribution (Up to 99th Percentile)")
ax.set_xlabel("Pixels")
ax.set_ylabel("Density")
ax.legend()

# Bottom-right: summary card
ax = axes[1, 1]
ax.axis("off")
summary_text = (
    "Insights\n"
    f"- Mean jitter reduced by {mean_improve:.1f}%\n"
    f"- 95th percentile jitter reduced by {p95_improve:.1f}%\n"
    f"- Largest jump reduced by {max_jump_improve:.1f}%\n"
    f"- Raw samples: {raw['count']:,}\n"
    f"- Smoothed samples: {smooth['count']:,}"
)
ax.text(
    0.02,
    0.95,
    summary_text,
    va="top",
    fontsize=11,
    bbox=dict(boxstyle="round,pad=0.55", facecolor="#f7f7f7", edgecolor="#bdbdbd"),
)

plt.tight_layout()
plt.show()
