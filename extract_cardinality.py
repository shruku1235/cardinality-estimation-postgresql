import json
import sys
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def walk_plan(node, results, parent=None):
    est = node.get("Plan Rows", None)
    act = node.get("Actual Rows", None)
    node_type = node.get("Node Type", None)
    relation = node.get("Relation Name", None)

    if est and act and act > 0:
        q_error = max(est / act, act / est)
    elif est and act == 0:
        q_error = float('inf')
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
        walk_plan(child, results, node)

def extract_from_file(json_path, csv_path):
    with open(json_path, 'r') as f:
        plan = json.load(f)

    root = plan[0]["Plan"]
    results = []
    walk_plan(root, results)

    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "node_type", "relation", "estimated_rows",
            "actual_rows", "q_error"
        ])
        writer.writeheader()
        writer.writerows(results)

    print(f"Saved: {csv_path}")


def analyze_csv_files():

    explain_1a_df = pd.read_csv("explain_1a.csv")
    explain_3a_df = pd.read_csv("explain_3a.csv")
    explain_7a_df = pd.read_csv("explain_7a.csv")
    explain_9a_df = pd.read_csv("explain_9a.csv")
    explain_18a_df = pd.read_csv("explain_18a.csv")
    explain_20a_df = pd.read_csv("explain_20a.csv")
    explain_28a_df = pd.read_csv("explain_28a.csv")
    explain_29a_df = pd.read_csv("explain_29a.csv")


    def calculate_q_error(df):
        return np.maximum(df['estimated_rows'] / df['actual_rows'], df['actual_rows'] / df['estimated_rows'])

    explain_1a_df['q_error'] = calculate_q_error(explain_1a_df)
    explain_3a_df['q_error'] = calculate_q_error(explain_3a_df)
    explain_7a_df['q_error'] = calculate_q_error(explain_7a_df)
    explain_9a_df['q_error'] = calculate_q_error(explain_9a_df)
    explain_18a_df['q_error'] = calculate_q_error(explain_18a_df)
    explain_20a_df['q_error'] = calculate_q_error(explain_20a_df)
    explain_28a_df['q_error'] = calculate_q_error(explain_28a_df)
    explain_29a_df['q_error'] = calculate_q_error(explain_29a_df)

    explain_1a_df = explain_1a_df[np.isfinite(explain_1a_df['q_error'])]
    explain_3a_df = explain_3a_df[np.isfinite(explain_3a_df['q_error'])]
    explain_7a_df = explain_7a_df[np.isfinite(explain_7a_df['q_error'])]
    explain_9a_df = explain_9a_df[np.isfinite(explain_9a_df['q_error'])]
    explain_18a_df = explain_18a_df[np.isfinite(explain_18a_df['q_error'])]
    explain_20a_df = explain_20a_df[np.isfinite(explain_20a_df['q_error'])]
    explain_28a_df = explain_28a_df[np.isfinite(explain_28a_df['q_error'])]
    explain_29a_df = explain_29a_df[np.isfinite(explain_29a_df['q_error'])]


    plt.figure(figsize=(12, 8))

    plt.hist(explain_1a_df['q_error'], bins=30, alpha=0.5, label="1a", range=(0, 100))
    plt.hist(explain_3a_df['q_error'], bins=30, alpha=0.5, label="3a", range=(0, 100))
    plt.hist(explain_7a_df['q_error'], bins=30, alpha=0.5, label="7a", range=(0, 100))
    plt.hist(explain_9a_df['q_error'], bins=30, alpha=0.5, label="9a", range=(0, 100))
    plt.hist(explain_18a_df['q_error'], bins=30, alpha=0.5, label="18a", range=(0, 100))
    plt.hist(explain_20a_df['q_error'], bins=30, alpha=0.5, label="20a", range=(0, 100))
    plt.hist(explain_28a_df['q_error'], bins=30, alpha=0.5, label="28a", range=(0, 100))
    plt.hist(explain_29a_df['q_error'], bins=30, alpha=0.5, label="29a", range=(0, 100))

    plt.xscale('log')

    plt.title('Q-Error Distribution for Different JOB Queries')
    plt.xlabel('Q-Error (Log Scale)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.show()


if __name__ == "__main__":

    extract_from_file("explain_1a.json", "explain_1a.csv")
    extract_from_file("explain_3a.json", "explain_3a.csv")
    extract_from_file("explain_7a.json", "explain_7a.csv")
    extract_from_file("explain_9a.json", "explain_9a.csv")
    extract_from_file("explain_18a.json", "explain_18a.csv")
    extract_from_file("explain_20a.json", "explain_20a.csv")
    extract_from_file("explain_28a.json", "explain_28a.csv")
    extract_from_file("explain_29a.json", "explain_29a.csv")

    analyze_csv_files()
