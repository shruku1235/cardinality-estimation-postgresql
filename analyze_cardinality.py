import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

queries = ["1a", "3a", "7a", "9a", "18a", "20a", "28a", "29a"]

dfs = {}

for q in queries:
    df = pd.read_csv(f"explain_{q}.csv")
    df = df[np.isfinite(df["q_error"])]
    dfs[q] = df["q_error"]

plt.figure(figsize=(12, 6))
plt.boxplot([dfs[q] for q in queries], labels=queries, showfliers=True)
plt.yscale("log")
plt.ylabel("Q-Error (log scale)")
plt.title("Q-Error Distribution Across JOB Queries")
plt.show()

fig, axes = plt.subplots(4, 2, figsize=(14, 10))
axes = axes.flatten()

for idx, q in enumerate(queries):
    df = dfs[q]
    axes[idx].hist(df, bins=30, alpha=0.7)
    axes[idx].set_title(f"Query {q}")
    axes[idx].set_xscale("log")
    axes[idx].set_xlabel("Q-Error")
    axes[idx].set_ylabel("Frequency")

plt.tight_layout()
plt.show()
