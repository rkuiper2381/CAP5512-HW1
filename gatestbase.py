import json
import random
import multiprocessing

import numpy
from deap import base, creator, tools, algorithms


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

def selRank(population, k):
    ranked = sorted(population, key=lambda ind: ind.fitness.values[0], reverse=True)

    n = len(ranked)
    weights = list(range(n, 0, -1))

    # random.choices does weighted sampling with replacement
    return random.choices(ranked, weights=weights, k=k)

def make_selector(selection_method, tournament_size=None):
    selection_method = selection_method.lower()
    if selection_method == "roulette":
        return tools.selRoulette
    if selection_method == "tournament":
        assert tournament_size != None
        return lambda pop, k: tools.selTournament(pop, k, tournsize=tournament_size)
    if selection_method == "rank":
        return selRank
    if selection_method == "random":
        return tools.selRandom
    raise SystemError("Yeah we messed up")


def build_toolbox(params):
    toolbox = base.Toolbox()

    #we want random binary
    toolbox.register("attr_binary", random.randint, 0, 1)
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr_binary, n=params["genome_length"])

    #now a population
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    #so OneMax, as far as I understand, is just the number of binary 1's present
    def OneMax(x):
        return (sum(x),)
    toolbox.register("evaluate", OneMax)

    #the splitting and joining
    toolbox.register("mate", tools.cxOnePoint)

    #the random flipping (per-bit)
    toolbox.register("mutate", tools.mutFlipBit, indpb=params["mutation_rate"])

    #selection method (roulette/tournament/rank/random)
    selector = make_selector(params["selection_method"], params.get("tournament_size", 3))
    toolbox.register("select", selector)

    return toolbox


#it takes stupid long to run otherwise
def run_one(args):
    i, params = args

    # deterministic seeding per run
    seed = params["seed_base"] + i
    random.seed(seed)
    numpy.random.seed(seed)

    toolbox = build_toolbox(params)

    #initial pop
    pop = toolbox.population(params["population_size"])

    #track the best dude
    hall = tools.HallOfFame(1)

    #we gotta register some statistics to accomplish the goal
    #we mainly need avg + best per generation for question 1a, but keep others if you want later
    stats = tools.Statistics(key=lambda ind: ind.fitness.values[0])
    stats.register("avg", numpy.mean)
    stats.register("max", numpy.max)

    #mutpb seems to be 1 as mutation always applies with bit flipping at a fixed rate
    pop, logbook = algorithms.eaSimple(
        pop, toolbox,
        halloffame=hall,
        cxpb=params["crossover_rate"],
        mutpb=1.0,  # per-bit rate is handled by indpb in mutFlipBit
        ngen=params["number_of_generations"],
        stats=stats,
        verbose=False
    )

    best = logbook.select("max")
    average = logbook.select("avg")

    #best fitness achieved over the course of the entire run
    best_overall = hall[0].fitness.values[0]

    #first generation optimum is found
    hit_optimum = next((g for g, b in enumerate(best) if b >= params["genome_length"]), None)

    # de numpify for json saving
    best = list(map(float, best))
    average = list(map(float, average))
    best_overall = float(best_overall)

    data = {
        "best": best,
        "average": average,
        "best_overall": best_overall,
        "hit_optimum": hit_optimum,
        "seed": seed,
    }
    return data


def gatest(params, save_json_path=None):
    # default params if not provided
    params = dict(params)  # copy
    params.setdefault("population_size", 100)
    params.setdefault("genome_length", 200)
    params.setdefault("crossover_rate", 0.8)
    params.setdefault("mutation_rate", 0.005)
    params.setdefault("selection_method", "roulette")
    params.setdefault("number_of_generations", 100)
    params.setdefault("number_of_runs", 50)
    params.setdefault("seed_base", 1337)
    params.setdefault("tournament_size", 3)

    # run all runs (order preserved)
    jobs = [(i, params) for i in range(params["number_of_runs"])]

    with multiprocessing.Pool() as pool:
        runs = pool.map(run_one, jobs)

    out = runs

    # optional JSON dump
    if save_json_path is not None:
        with open(save_json_path, "w") as f:
            json.dump(out, f)

    return out
    
def summarize_experiment(experiment_result, genome_length = 200):
    runs = experiment_result
    optimum = genome_length

    n_runs = len(runs)

    best_overall_vals = [r["best_overall"] for r in runs]
    avg_best_overall = sum(best_overall_vals) / n_runs if n_runs > 0 else None

    hit_gens = [r["hit_optimum"] for r in runs if r["hit_optimum"] is not None]
    num_hits = len(hit_gens)

    pct_optimum_reached = (100.0 * num_hits / n_runs)
    avg_gen_optimum_reached = (
        sum(hit_gens) / num_hits if num_hits > 0 else None
    )

    per_run_avg_of_avg = []
    for r in runs:
        avg_curve = r["average"]
        if avg_curve:
            per_run_avg_of_avg.append(sum(avg_curve) / len(avg_curve))

    avg_of_all_averages = (
        sum(per_run_avg_of_avg) / len(per_run_avg_of_avg)
        if per_run_avg_of_avg else None
    )

    return {
        "avg_best_overall": avg_best_overall,
        "pct_optimum_reached": pct_optimum_reached,
        "avg_gen_optimum_reached": avg_gen_optimum_reached,
        "avg_of_all_averages": avg_of_all_averages,
        "optimum": optimum,
        "runs": n_runs,
        "runs_reaching_optimum": num_hits,
    }

