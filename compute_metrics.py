import pandas as pd
import numpy as np

queries = ["1a", "3a", "7a", "9a", "18a", "20a", "28a", "29a"]

table_sizes = {
    "title": 2528312,
    "movie_info": 14835720,
    "cast_info": 36244344,
    "movie_keyword": 4523930,
    "info_type": 112,
    "keyword": 134170,
    "kind_type": 7,
    "movie_info_idx": 460012,
    "complete_cast": 135086,
    "comp_cast_type": 4
}

def count_joins(sql_file):
    """Count joins by scanning SQL."""
    try:
        text = open(sql_file).read().lower()
        return text.count(" join ") + text.count(",")
    except:
        return None

def compute_metrics():
    rows = []

    for q in queries:
        df = pd.read_csv(f"explain_{q}.csv")
        df = df[np.isfinite(df["q_error"])]

        mean_q = df["q_error"].mean()
        median_q = df["q_error"].median()
        max_q = df["q_error"].max()

        over_10 = (df["q_error"] > 10).sum()
        over_100 = (df["q_error"] > 100).sum()
        over_1000 = (df["q_error"] > 1000).sum()

        join_count = count_joins(f"{q}.sql")

        sql_text = open(f"{q}.sql").read().lower()
        referenced = [table_sizes[t] for t in table_sizes if t in sql_text]
        total_table_size = sum(referenced)

        rows.append({
            "query": q,
            "mean_q_error": mean_q,
            "median_q_error": median_q,
            "max_q_error": max_q,
            "num_nodes_q>10": over_10,
            "num_nodes_q>100": over_100,
            "num_nodes_q>1000": over_1000,
            "join_count": join_count,
            "total_table_size": total_table_size
        })

    df = pd.DataFrame(rows)
    df.to_csv("job_query_metrics.csv", index=False)
    print(df)

    print("\nCorrelation: joins ↔ median q-error:")
    print(df["join_count"].corr(df["median_q_error"]))

    print("\nCorrelation: table size ↔ median q-error:")
    print(df["total_table_size"].corr(df["median_q_error"]))


if __name__ == "__main__":
    compute_metrics()
