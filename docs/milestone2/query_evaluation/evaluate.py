# SETUP
import matplotlib.pyplot as plt
from sklearn.metrics import PrecisionRecallDisplay
import numpy as np
import json
import requests
import pandas as pd
import os
import sys

QUERY_NUM = sys.argv[1]
QRELS_FILE = os.path.dirname(__file__) + '/' + QUERY_NUM + '/' + 'qrels.md'
QUERY_URL = os.path.dirname(__file__) + '/' + QUERY_NUM + '/' + 'q.txt'
QUERY_ENHANCED_URL = os.path.dirname(__file__) + '/' + QUERY_NUM + '/' + 'q_e.txt'

# Read the URLs from the files
with open(QUERY_URL, 'r') as query_url_file:
    QUERY_URL = query_url_file.read().strip()

with open(QUERY_ENHANCED_URL, 'r') as query_enhanced_url_file:
    QUERY_ENHANCED_URL = query_enhanced_url_file.read().strip()

relevant = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))

simple_results = requests.get(QUERY_URL).json()['response']['docs']
enhanced_results = requests.get(QUERY_ENHANCED_URL).json()['response']['docs']
# enhanced_results = []

print("Simple Results NUM: ", len(simple_results))
print("Enhanced Results NUM: ", len(enhanced_results))

metrics = {}
metric = lambda f: metrics.setdefault(f.__name__, f)


@metric
def ap(results, relevant):
    """Average Precision"""
    precision_values = []
    relevant_count = 0

    for idx, doc in enumerate(results):
        if doc['id'] in relevant:
            relevant_count += 1
            precision_at_k = relevant_count / (idx + 1)
            precision_values.append(precision_at_k)

    if not precision_values:
        return 0.0

    return sum(precision_values) / len(precision_values)


@metric
def p10(results, relevant, n=10):
    sequence = ''.join(['R' if doc['id'] in relevant else 'N' for doc in results[:n]])
    print(sequence)
    """Precision at N"""
    return len([doc for doc in results[:n] if doc['id'] in relevant]) / n


@metric
def r10(results, relevant, n=10):
    # print(len([doc for doc in results[:n] if doc['id'] in relevant]))
    """Recall at N"""
    return len([doc for doc in results[:n] if doc['id'] in relevant]) / len(relevant)


@metric
def f10(results, relevant, n=10):
    # print(len([doc for doc in results[:n] if doc['id'] in relevant]))
    """F1 Measure at N"""
    recall = r10(results, relevant, n)
    precision = p10(results, relevant, n)

    if (recall + precision) == 0: return 0

    return 2 * (recall * precision) / (recall + precision)


def calculate_metric(key, results, relevant):
    return metrics[key](results, relevant)


# Define metrics to be calculated
evaluation_metrics = {
    'ap': 'Average Precision',
    'p10': 'Precision at 10 (P@10)'
}

simple_metrics = {m: calculate_metric(m, simple_results, relevant) for m in evaluation_metrics}

enhanced_metrics = {m: calculate_metric(m, enhanced_results, relevant) for m in evaluation_metrics}

# Combine metrics for both results
combined_metrics = {
    'Simple Results': simple_metrics,
    'Enhanced Results': enhanced_metrics
}

# Convert metrics to a DataFrame
df = pd.DataFrame([[source, metric, value] for source, metrics_dict in combined_metrics.items()
                   for metric, value in metrics_dict.items()], columns=['Source', 'Metric', 'Value'])

# Export results as LaTeX table
with open(os.path.dirname(__file__) + '/results' + '/' + QUERY_NUM + '.tex', 'w') as tf:
    tf.write(df.to_latex(index=False))


# PRECISION-RECALL CURVE
# Calculate precision and recall values as we move down the ranked list
def graficos(results, tipo):
    precision_values = [
        len([
            doc
            for doc in results[:idx]
            if doc['id'] in relevant
        ]) / idx
        for idx, _ in enumerate(results, start=1)
    ]

    recall_values = [
        len([
            doc for doc in results[:idx]
            if doc['id'] in relevant
        ]) / len(relevant)
        for idx, _ in enumerate(results, start=1)
    ]
    if recall_values[-1] < 1:
        recall_values.append(1)
        precision_values.append(precision_values[-1])

    interpolated_precision_values = []
    for idx, step in enumerate(recall_values):
        interpolated_precision_values.append(max(precision_values[idx:]))
    plt.clf()
    plt.plot(recall_values, interpolated_precision_values, label=tipo)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.legend()
    plt.savefig(str(QUERY_NUM) + '_' + tipo + '.pdf')
