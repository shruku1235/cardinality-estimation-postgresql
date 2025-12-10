import json
import csv
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

def walk_plan(node, results):
    est = node.get("Plan Rows", None)
    act = node.get("Actual Rows", None)
    node_type = node.get("Node Type", None)
    relation = node.get("Relation Name", None)

    if est is not None and act is not None:
        if act > 0:
            q_error = max(est / act, act / est)
        else:
            q_error = float("inf")
    else:
        q_error = None

    results.append({
        "node_type": node_type,
        "relation": relation,
        "estimated_rows": est,
        "actual_rows": act,
        "q_error": q_error
    })

    for child in node.get("Plans", []):
        walk_plan(child, results)

def extract_file(json_path):
    with open(json_path, "r") as f:
        plan = json.load(f)

    root = plan[0]["Plan"]
    results = []
    walk_plan(root, results)

    csv_path = json_path.replace(".json", ".csv")

    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "node_type", "relation", "estimated_rows",
            "actual_rows", "q_error"
        ])
        writer.writeheader()
        writer.writerows(results)

    print(f"Saved → {csv_path}")
    return csv_path

def analyze_all():
    json_files = sorted(glob.glob("explain_q*.json"))

    if not json_files:
        print("No explain_q*.json files found in this directory.")
        return

    summary_rows = []
    all_errors = {}

    for jf in json_files:
        csv_path = extract_file(jf)
        df = pd.read_csv(csv_path)

        valid = df[df["q_error"].notna()]

        query_name = os.path.splitext(os.path.basename(jf))[0]

        if len(valid) > 0:
            mean_q = valid["q_error"].mean()
            median_q = valid["q_error"].median()
            max_q = valid["q_error"].max()

            summary_rows.append([query_name, mean_q, median_q, max_q])
            all_errors[query_name] = valid["q_error"].values

    summary_df = pd.DataFrame(summary_rows,
                              columns=["query", "mean_qerror", "median_qerror", "max_qerror"])
    summary_df.to_csv("tpch_summary.csv", index=False)
    print("\nSaved → tpch_summary.csv\n")
    print(summary_df)

    if len(all_errors) > 0:
        plt.figure(figsize=(10, 6))
        plt.boxplot(all_errors.values(), labels=all_errors.keys(), showfliers=False)
        plt.xticks(rotation=45)
        plt.ylabel("Q-error (log scale)")
        plt.yscale("log")
        plt.title("TPC-H Cardinality Estimation Errors Across Queries")
        plt.tight_layout()
        plt.savefig("tpch_boxplot.png", dpi=200)
        print("Saved → tpch_boxplot.png")

if __name__ == "__main__":
    analyze_all()
