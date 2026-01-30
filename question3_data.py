from gatestbase import *

print("Q3 mut=0.001:", summarize_experiment(gatest({"mutation_rate": 0.001}, "question3_001.json")))
print("Q3 mut=0.01 :", summarize_experiment(gatest({"mutation_rate": 0.01},  "question3_01.json")))
print("Q3 mut=0.05 :", summarize_experiment(gatest({"mutation_rate": 0.05},  "question3_05.json")))
