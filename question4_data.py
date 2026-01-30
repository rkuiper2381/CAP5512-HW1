from gatestbase import *

print("Q4 cx=0.4 :", summarize_experiment(gatest({"crossover_rate": 0.4}, "question4_cx04.json")))
print("Q4 cx=1.0 :", summarize_experiment(gatest({"crossover_rate": 1.0}, "question4_cx10.json")))
print("Q4 cx=0.9 :", summarize_experiment(gatest({"crossover_rate": 0.9}, "question4_cx09.json")))
