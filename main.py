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
• Using the data from part 1a, create a plot in which the x-axis indicates the generation and
the y-axis indicates fitness. For each generation, plot
– the average best fitness and its 95% confidence interval, averaged over 50 runs.
– the average average fitness and its 95% confidence interval, averaged over 50 runs.
• Using the data from part 1b, calculate the average best fitness over 50 runs, the standard
deviation of that average, and the 95% confidence interval.
• If you were able to collect data for part 1c, calculate the average generation that an
optimum individual is found over 50 runs, its standard deviation, and its 95% confidence
interval.
For the rest of the assignment, an “experiment” refers to 50 runs with the same parameter
settings
"""


import matplotlib.pyplot as plt
import numpy as np
from deap import base, creator, tools, algorithms


import numpy
import random

population_size=100
#initial_population = Randomly generated
genome_length = 200
#Crossover type One-point
crossover_rate = 0.8
mutation_rate = 0.005
#selection_method = Fitness proportional (Roulette wheel)
number_of_generations = 100
number_of_runs = 50

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
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

stats = tools.Statistics(key=lambda ind: ind.fitness.values)
stats.register("avg", numpy.mean)
stats.register("std", numpy.std)
stats.register("min", numpy.min)
stats.register("max", numpy.max)

for i in range(number_of_runs):
    random.seed(1337 + i)
    numpy.random.seed(1337 + i)
    #initial pop
    pop = toolbox.population(population_size)
    #track the best dude
    hall = tools.HallOfFame(1)
    #now we just run things?
    #mutpb seems to be 1 as mutation always applies with bit flipping at a fixed rate
    pop, logbook = algorithms.eaSimple(pop, toolbox, halloffame=hall, cxpb=crossover_rate, mutpb=1.0, ngen=number_of_generations, stats=stats, verbose=True)
    
    best = logbook.select("max")
    average = logbook.select("avg")
    best_overall = hall[0].fitness.values[0]
    print(best, average, best_overall)
