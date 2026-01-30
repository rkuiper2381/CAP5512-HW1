from gatestbase import *

print("Q2 pop=50  :", summarize_experiment(gatest({"population_size": 50},  "question2_50.json")))
print("Q2 pop=200 :", summarize_experiment(gatest({"population_size": 200}, "question2_200.json")))
print("Q2 pop=10 :", summarize_experiment(gatest({"population_size": 10}, "question2_10.json")))
