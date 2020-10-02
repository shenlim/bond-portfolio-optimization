import pandas as pd
import pulp

df = pd.read_csv("portfolio.csv")
# Assign 1's to weight_multiplier for modeling purposes
df["weight_multiplier"] = 1
df = (df.sort_values("ticker")).reset_index(drop=True)
pd.set_option("display.max_columns", len(df.columns))
print(df.head())

# Define problem
prob = pulp.LpProblem("optimize_ytm", pulp.LpMaximize)
etfs = list(df["ticker"])
funds = 103570.65

# Create dictionaries of variables
weight_multiplier = dict(zip(etfs, df["weight_multiplier"]))
credit_num = dict(zip(etfs, df["credit_num"]))
duration = dict(zip(etfs, df["duration"]))
ytm = dict(zip(etfs, df["ytm"]))
non_benchmark = dict(zip(etfs, df["non_benchmark"]))
sectors = ["govt", "mbs", "corp"]
sectors_dict = {}
for sector in sectors:
    sectors_dict[sector] = dict(zip(etfs, df[sector]))

# Decision variables: weights
etfs_vars = pulp.LpVariable.dicts("ETF", etfs, lowBound=0, upBound=1, cat="Continuous")

# Objective: YTM
prob += pulp.lpSum([ytm[i] * etfs_vars[i] for i in etfs])

# Constraint: SPAXX weight assumed constant, weights must total 100%
prob += pulp.lpSum(weight_multiplier["SPAXX"] * etfs_vars["SPAXX"]) == 1073.22 / funds
prob += pulp.lpSum([weight_multiplier[i] * etfs_vars[i] for i in etfs]) == 1, "weight"

# Constraint: Credit quality +-2 levels
prob += pulp.lpSum([credit_num[i] * etfs_vars[i] for i in etfs]) >=\
        max(1, df[df["ticker"] == "SPAB"]["credit_num"].item() - 2), "credit_num_min"
prob += pulp.lpSum([credit_num[i] * etfs_vars[i] for i in etfs]) <=\
        max(1, df[df["ticker"] == "SPAB"]["credit_num"].item() + 2), "credit_num_max"

# Constraint: Duration +- 20% from benchmark
prob += pulp.lpSum([duration[i] * etfs_vars[i] for i in etfs]) >=\
        df[df["ticker"] == "SPAB"]["duration"] * (1 - 0.2), "duration_min"
prob += pulp.lpSum([duration[i] * etfs_vars[i] for i in etfs]) <=\
        df[df["ticker"] == "SPAB"]["duration"] * (1 + 0.2), "duration_max"

# Constraint: Sectors +- 25% from benchmark
for sector in sectors:
    prob += pulp.lpSum([sectors_dict[sector][i] * etfs_vars[i] for i in etfs]) >=\
            df[df["ticker"] == "SPAB"][sector] * (1 - 0.25), sector + "_min"
    prob += pulp.lpSum([sectors_dict[sector][i] * etfs_vars[i] for i in etfs]) <=\
            df[df["ticker"] == "SPAB"][sector] * (1 + 0.25), sector + "_max"

# Constraint: Non-benchmark (nb) weights not greater than 10%
prob += pulp.lpSum([non_benchmark[i] * etfs_vars[i] for i in etfs]) <= 0.10, "nb_max"

print(prob)
prob.solve()

print("Optimal weights (solution):")
for i in prob.variables():
    print(i.name, "=", "{:.2%}".format(i.varValue))

print("\nOptimal YTM:", "{:.2%}".format(prob.objective.value()))

print("\nOptimal shares:")
for i in df.index:
    print(df["ticker"][i], "=", "{:.0f}".format(prob.variables()[i].varValue * funds / df["price"][i]))
