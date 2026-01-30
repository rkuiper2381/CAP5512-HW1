from gatestbase import *


print("Q5 sel=roulette  :", summarize_experiment(gatest({"selection_method": "roulette"}, "question5_roulette.json")))
print("Q5 sel=tournament:", summarize_experiment(gatest({"selection_method": "tournament", "tournament_size": 3}, "question5_tournament.json")))
print("Q5 sel=rank      :", summarize_experiment(gatest({"selection_method": "rank"}, "question5_rank.json")))
print("Q5 sel=random    :", summarize_experiment(gatest({"selection_method": "random"}, "question5_random.json")))

