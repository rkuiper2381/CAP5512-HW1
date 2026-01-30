from gatestbase import *
import itertools
import os

def score(summary):
    avg_hit  = summary["avg_gen_optimum_reached"]
    return  avg_hit



grid = {
    "population_size":  [50, 100, 200, 400],
    "mutation_rate":    [0.002, 0.005, 0.01],
    "crossover_rate":   [0.6, 0.8, 0.9, 1.0],
    "selection_method": ["roulette", "rank", "tournament"]
}

TEST_RUNS = 50


# this should give us all variants
configs = []
for pop, mut, cx, sel in itertools.product(
        grid["population_size"],
        grid["mutation_rate"],
        grid["crossover_rate"],
        grid["selection_method"],
):
    cfg = {
        "population_size":  pop,
        "mutation_rate":    mut,
        "crossover_rate":   cx,
        "selection_method": sel,
    }

    configs.append(cfg)
    
def run_cached(cfg, runs, seed_base, outfile):
    if os.path.exists(outfile):
        with open(outfile, "r") as f:
            exp = json.load(f)
    else:
        exp = gatest(
            {**cfg, "number_of_runs": runs, "seed_base": seed_base},
            outfile
        )
    return exp
   
results = []
for i, cfg in enumerate(configs):
    print(i, len(configs))
    out_file = "q6_run%d.json"%i

    exp  = run_cached(cfg, TEST_RUNS, 1337, out_file)
    
    summ = summarize_experiment(exp)
    summ["score"] = score(summ)

    results.append((cfg, summ, out_file))


results.sort(key=lambda x: x[1]["score"] if x[1]["score"] is not None else float("inf"))

for cfg, summ, out in results[:5]:
    print("score =", round(summ["score"], 3), cfg, out)
    print("  ", summ)
    print("")

