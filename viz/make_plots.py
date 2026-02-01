#!/usr/bin/env python3
"""
Quick script to build all the plots for CAP5512 HW1.
It reads the processed JSON files (question*-processed.json, q6_run119-processed.json)
and drops the PNGs into viz/.

Run with: python3 viz/make_plots.py
"""
import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "viz"
OUT.mkdir(exist_ok=True)
CI_NOTE = "Bands show mean ±1.96·std across runs (not true 95% CI)."


def load(proc_name):
    path = ROOT / proc_name
    with open(path) as f:
        return json.load(f)


def ribbon_plot(gens, mean, low, high, label, color):
    plt.plot(gens, mean, label=label, color=color, lw=2)
    plt.fill_between(gens, low, high, color=color, alpha=0.2, linewidth=0)


def auto_ylim(values, pad=5, include=None, floor=0):
    flat = list(values)
    if include is not None:
        flat += include
    lo = min(flat)
    hi = max(flat)
    return max(floor, lo - pad), hi + pad


def plot_q1():
    data = load("question1_results-processed.json")
    gens = np.arange(len(data["best"]))
    fig, ax1 = plt.subplots(figsize=(7, 4))
    for key, color in [("best", "tab:blue"), ("average", "tab:orange")]:
        mean = [g["mean"] for g in data[key]]
        low = [g["lower"] for g in data[key]]
        high = [g["upper"] for g in data[key]]
        ax1.plot(gens, mean, label=f"{key} fitness", color=color, lw=2)
        ax1.fill_between(gens, low, high, color=color, alpha=0.2, linewidth=0)
    all_means = [g["mean"] for g in data["best"]] + [g["mean"] for g in data["average"]]
    ylo, yhi = auto_ylim(all_means, pad=5, include=[200])
    ax1.set_ylim(ylo, yhi)
    ax1.set_xlabel("Generation")
    ax1.set_ylabel("Fitness")
    ax1.legend(loc="upper right")
    ax1.set_title("Q1 Baseline (pop=100, cx=0.8, mut=0.005, roulette)")
    ax1.text(0.01, 0.02, CI_NOTE, transform=ax1.transAxes, fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "q1_baseline.png", dpi=200)
    plt.close(fig)


def bar_final_best(label_file_map, title, outfile, ylim=None):
    labels = list(label_file_map.keys())
    means = []
    stds = []
    for f in label_file_map.values():
        d = load(f)["best_overall"]
        means.append(d["mean"])
        stds.append(d["std"])
    plt.figure(figsize=(7, 4))
    x = np.arange(len(labels))
    bars = plt.bar(x, means, yerr=stds, capsize=5, color="tab:blue", alpha=0.8)
    plt.xticks(x, labels, rotation=20)
    plt.ylabel("Mean best fitness (gen 100)")
    if ylim:
        plt.ylim(*ylim)
    else:
        ylo, yhi = auto_ylim(means, pad=5, include=[m + s for m, s in zip(means, stds)])
        plt.ylim(ylo, yhi)
    for rect, m in zip(bars, means):
        plt.text(rect.get_x() + rect.get_width() / 2, rect.get_height() + 0.5, f"{m:.1f}",
                 ha="center", va="bottom", fontsize=9)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(OUT / outfile, dpi=200)
    plt.close()


def q2_lines():
    files = {
        "pop10": "question2_10-processed.json",
        "pop50": "question2_50-processed.json",
        "pop100": "question1_results-processed.json",
        "pop200": "question2_200-processed.json",
    }
    plt.figure(figsize=(7, 4))
    all_vals = []
    for label, path in files.items():
        d = load(path)
        gens = range(len(d["best"]))
        series = [g["mean"] for g in d["best"]]
        all_vals.extend(series)
        plt.plot(gens, series, label=label)
    plt.xlabel("Generation")
    plt.ylabel("Best fitness (mean)")
    plt.title("Q2 Population Size: convergence speed")
    plt.legend()
    ylo, yhi = auto_ylim(all_vals, pad=5, include=[200])
    plt.ylim(ylo, yhi)
    plt.tight_layout()
    plt.savefig(OUT / "q2_population_lines.png", dpi=200)
    plt.close()


def q3_lines():
    files = {
        "0.001": "question3_001-processed.json",
        "0.005 (base)": "question1_results-processed.json",
        "0.01": "question3_01-processed.json",
        "0.05": "question3_05-processed.json",
    }
    plt.figure(figsize=(7, 4))
    all_vals = []
    for label, path in files.items():
        d = load(path)
        gens = range(len(d["best"]))
        series = [g["mean"] for g in d["best"]]
        all_vals.extend(series)
        plt.plot(gens, series, label=label)
    plt.xlabel("Generation")
    plt.ylabel("Best fitness (mean)")
    plt.title("Q3 Mutation Rate: exploration vs disruption")
    plt.legend()
    ylo, yhi = auto_ylim(all_vals, pad=5, include=[200])
    plt.ylim(ylo, yhi)
    plt.tight_layout()
    plt.savefig(OUT / "q3_mutation_lines.png", dpi=200)
    plt.close()


def q4_lines():
    files = {
        "cx0.4": "question4_cx04-processed.json",
        "cx0.8": "question1_results-processed.json",
        "cx0.9": "question4_cx09-processed.json",
        "cx1.0": "question4_cx10-processed.json",
    }
    plt.figure(figsize=(7, 4))
    all_vals = []
    for label, path in files.items():
        d = load(path)
        gens = range(len(d["best"]))
        series = [g["mean"] for g in d["best"]]
        all_vals.extend(series)
        plt.plot(gens, series, label=label)
    plt.xlabel("Generation")
    plt.ylabel("Best fitness (mean)")
    plt.title("Q4 Crossover Rate: recombination strength")
    plt.legend()
    ylo, yhi = auto_ylim(all_vals, pad=5, include=[200])
    plt.ylim(ylo, yhi)
    plt.tight_layout()
    plt.savefig(OUT / "q4_crossover_lines.png", dpi=200)
    plt.close()


def plot_q2():
    bar_final_best({
        "pop 10": "question2_10-processed.json",
        "pop 50": "question2_50-processed.json",
        "pop 100": "question1_results-processed.json",
        "pop 200": "question2_200-processed.json",
    }, "Q2 Population Size Effect", "q2_population_bar.png", ylim=(110, 150))
    q2_lines()


def plot_q3():
    bar_final_best({
        "0.001": "question3_001-processed.json",
        "0.005 (base)": "question1_results-processed.json",
        "0.01": "question3_01-processed.json",
        "0.05": "question3_05-processed.json",
    }, "Q3 Mutation Rate Effect", "q3_mutation_bar.png", ylim=(125, 145))
    q3_lines()


def plot_q4():
    bar_final_best({
        "0.4": "question4_cx04-processed.json",
        "0.8 (base)": "question1_results-processed.json",
        "0.9": "question4_cx09-processed.json",
        "1.0": "question4_cx10-processed.json",
    }, "Q4 Crossover Rate Effect", "q4_crossover_bar.png", ylim=(130, 145))
    q4_lines()


def plot_q5():
    files = {
        "roulette": "question5_roulette-processed.json",
        "tournament": "question5_tournament-processed.json",
        "rank": "question5_rank-processed.json",
        "random": "question5_random-processed.json",
    }
    plt.figure(figsize=(7, 4))
    colors = {
        "roulette": "tab:blue",
        "tournament": "tab:green",
        "rank": "tab:purple",
        "random": "tab:red",
    }
    all_vals = []
    for name, path in files.items():
        d = load(path)
        gens = np.arange(len(d["best"]))
        mean = [g["mean"] for g in d["best"]]
        all_vals.extend(mean)
        plt.plot(gens, mean, label=name, color=colors.get(name))
        opt = d.get("optimum")
        if opt:
            plt.axvline(opt.get("mean", None), color=colors.get(name), ls="--", alpha=0.4)
    plt.axhline(200, color="k", ls="--", lw=1, label="optimum")
    plt.xlabel("Generation")
    plt.ylabel("Best fitness (mean over runs)")
    plt.title("Q5 Selection Methods")
    plt.legend()
    ylo, yhi = auto_ylim(all_vals, pad=5, include=[200])
    plt.ylim(ylo, yhi)
    plt.tight_layout()
    plt.savefig(OUT / "q5_selection_lines.png", dpi=200)
    plt.close()


def plot_q6():
    d = load("q6_run119-processed.json")
    gens = np.arange(len(d["best"]))
    mean = [g["mean"] for g in d["best"]]
    low = [g["lower"] for g in d["best"]]
    high = [g["upper"] for g in d["best"]]
    plt.figure(figsize=(7, 4))
    ribbon_plot(gens, mean, low, high, "best fitness", "tab:green")
    plt.axhline(200, color="k", ls="--", lw=1, label="optimum")
    opt = d.get("optimum")
    if opt:
        plt.axvline(opt.get("mean", None), color="tab:green", ls=":", alpha=0.6, label="mean hit gen")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.title("Q6 Best config: pop=400, mut=0.002, cx=1.0, tournament")
    plt.legend()
    ylo, yhi = auto_ylim(mean + low + high, pad=5, include=[200])
    plt.ylim(ylo, yhi)
    plt.text(0.01, 0.02, CI_NOTE, transform=plt.gca().transAxes, fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT / "q6_best_config.png", dpi=200)
    plt.close()


def main():
    plot_q1()
    plot_q2()
    plot_q3()
    plot_q4()
    plot_q5()
    plot_q6()
    print("Plots written to", OUT)


if __name__ == "__main__":
    main()
