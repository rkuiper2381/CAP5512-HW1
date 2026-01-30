"""
4 What to do
Implement a GA to solve the OneMax problem. Set your parameter settings to the following initial
values.
Population size 100
Initial population Randomly generated
Genome length 200 binary bits
Crossover type One-point
Crossover rate 0.8
Mutation rate 0.005
Selection method Fitness proportional (Roulette wheel)
Max number of generations 100
1
1. Because the GA is a pseudorandom algorithm, it is important to run sufficient samples of each
experiment. Typically, you should run a minumum of 50 to 100 runs for each experiment. The
expected behavior of the GA is the average performance, averaged over all 50 to 100 runs.
Anytime you report an average value, you must also give either or both the standard deviation
or 95% confidence interval.
Run your GA with the above parameter settings 50 times. For each run, keep track of the
following:
(a) Record the best fitness and the average population fitness in each generation of the run.
(b) At the end of a run, record the best fitness achieved over the course of the entire run.
(c) If an optimum individual is found, record the first generation in which an optimum
individual is found.
Once you have completed 50 runs, compile the following information. When including plots and
figures in your assignments and presentations, please make sure that all plots and figures are
clearly labelled.
"""


import matplotlib.pyplot as plt
import numpy as np
from deap import base, creator, tools, algorithms

import numpy
import random
import json
import multiprocessing as mp

population_size=100
#initial_population = Randomly generated
genome_length = 200
#Crossover type One-point
crossover_rate = 0.8
mutation_rate = 0.005
#selection_method = Fitness proportional (Roulette wheel)
number_of_generations = 100
number_of_runs = 50

# (guard so reruns don’t crash with “already exists”)
if not hasattr(creator, "FitnessMax"):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
if not hasattr(creator, "Individual"):
    creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
#we want random binary
toolbox.register("attr_binary", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_binary, n=genome_length)

#now a population
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

#so OneMax, as far as I understand, is just the number of binary 1's present, this should be the equivalent of sum but it needs to be a weird pseudo-tuple
def OneMax(x):
    return (sum(x), )
toolbox.register("evaluate", OneMax)

# the splitting and joining
toolbox.register("mate", tools.cxOnePoint)

# the random flipping
toolbox.register("mutate", tools.mutFlipBit, indpb=mutation_rate)
toolbox.register("select", tools.selRoulette)

#we gotta register some statistics to accomplish the goal
#tutorial does it like this

stats = tools.Statistics(key=lambda ind: ind.fitness.values[0])
stats.register("avg", numpy.mean)
stats.register("std", numpy.std)
stats.register("min", numpy.min)
stats.register("max", numpy.max)

# run one experiment run (so we can parallelize it)
def run_one(i):
    random.seed(1337 + i)
    numpy.random.seed(1337 + i)
    #initial pop
    pop = toolbox.population(population_size)
    #track the best dude
    hall = tools.HallOfFame(1)
    #now we just run things?
    #mutpb seems to be 1 as mutation always applies with bit flipping at a fixed rate
    pop, logbook = algorithms.eaSimple(pop, toolbox, halloffame=hall, cxpb=crossover_rate, mutpb=1.0, ngen=number_of_generations, stats=stats, verbose=False)
    
    best = logbook.select("max")
    average = logbook.select("avg")
    best_overall = hall[0].fitness.values[0]

    #de numpify for json saving
    best = list(map(float, best))
    average = list(map(float, average))
    best_overall = float(best_overall)

    hit_optimum = next((g for g, b in enumerate(best) if b >= genome_length), None)
    data = {'best': best, 'average': average, 'best_overall': best_overall, 'hit_optimum': hit_optimum}
    #print(data)
    return data

results = []

if __name__ == "__main__":
    # multiprocessing while keeping output in the same order:
    # Pool.map preserves the order of the inputs, so results[i] is still seed(1337+i)
    with mp.Pool() as pool:
        results = pool.map(run_one, range(number_of_runs))

    # json save the data
    with open("question1_results.json", "w") as f:
        json.dump(results, f)

    print("Saved question1_results.json")

