import json
import numpy as np

f_name = input()
f_name = f_name[:f_name.index(".json")]

with open((f_name + ".json"), "r", encoding="utf-8") as file:
    experiments = json.load(file)

processed = { "best":[], "average":[] }

for i in range(0, 100):
    gen_list = np.zeros(50)
    for j in range(0, 50):
        gen_list[j] = (experiments[j]["best"][i])

    gen_avg = np.mean(gen_list)
    gen_std = np.std(gen_list, ddof=1)
    gen_lower = gen_avg - 1.96 * gen_std
    gen_upper = gen_avg + 1.96 * gen_std

    processed["best"].append({ "mean":gen_avg, "std":gen_std, "lower":gen_lower, "upper":gen_upper})

for i in range(0, 100):
    gen_list = np.zeros(50)
    for j in range(0, 50):
        gen_list[j] = (experiments[j]["average"][i])

    gen_avg = np.mean(gen_list)
    gen_std = np.std(gen_list, ddof=1)
    gen_lower = gen_avg - 1.96 * gen_std
    gen_upper = gen_avg + 1.96 * gen_std

    processed["average"].append({ "mean":gen_avg, "std":gen_std, "lower":gen_lower, "upper":gen_upper})


best_list = np.zeros(50)
for i in range(0, 50):
    best_list[i] = (experiments[i]["best_overall"])

best_avg = np.mean(best_list)
best_std = np.std(best_list, ddof=1)
best_lower = best_avg - 1.96 * best_std
best_upper = best_avg + 1.96 * best_std

processed["best_overall"] = { "mean":best_avg, "std":best_std, "lower":best_lower, "upper":best_upper}


num_optimums = 0
for i in range(0, 50):
    if not experiments[i]["hit_optimum"] is None:
        num_optimums += 1

if num_optimums > 0:
    optimum_list = np.zeros(num_optimums)
    for i in range(0, 50):
        if not experiments[i]["hit_optimum"] is None:
            num_optimums -= 1
            optimum_list[num_optimums] = (experiments[i]["hit_optimum"])

    optimum_avg = np.mean(optimum_list)
    optimum_std = np.std(optimum_list, ddof=1)
    optimum_lower = optimum_avg - 1.96 * optimum_std
    optimum_upper = optimum_avg + 1.96 * optimum_std

    processed["optimum"] = { "mean":optimum_avg, "std":optimum_std, "lower":optimum_lower, "upper":optimum_upper}


with open((f_name + "-processed.json"), mode="w", encoding="utf-8") as file:
    json.dump(processed, file)
