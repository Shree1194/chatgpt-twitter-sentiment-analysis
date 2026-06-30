"""NLP model comparison utilities."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, precision_recall_fscore_support


def compare_sentiment_models(
    df: pd.DataFrame,
    baseline_column: str = "sentiment_label",
    challenger_column: str = "textblob_label",
) -> pd.DataFrame:
    """Compare TextBlob against VADER as a practical weak-label baseline."""
    valid = df[[baseline_column, challenger_column]].dropna()
    labels = ["Negative", "Neutral", "Positive"]
    precision, recall, f1, _ = precision_recall_fscore_support(
        valid[baseline_column],
        valid[challenger_column],
        labels=labels,
        average="weighted",
        zero_division=0,
    )
    return pd.DataFrame(
        [
            {
                "baseline": baseline_column,
                "challenger": challenger_column,
                "accuracy": accuracy_score(valid[baseline_column], valid[challenger_column]),
                "precision": precision,
                "recall": recall,
                "f1_score": f1,
            }
        ]
    )


def classification_report_frame(
    df: pd.DataFrame,
    baseline_column: str = "sentiment_label",
    challenger_column: str = "textblob_label",
) -> pd.DataFrame:
    """Return a class-level classification report."""
    report = classification_report(
        df[baseline_column],
        df[challenger_column],
        output_dict=True,
        zero_division=0,
    )
    return pd.DataFrame(report).transpose()


def plot_confusion_matrix(
    df: pd.DataFrame,
    output_path: Path,
    baseline_column: str = "sentiment_label",
    challenger_column: str = "textblob_label",
) -> None:
    """Save a confusion matrix chart comparing TextBlob and VADER labels."""
    labels = ["Negative", "Neutral", "Positive"]
    matrix = confusion_matrix(df[baseline_column], df[challenger_column], labels=labels)
    plt.figure(figsize=(8, 6))
    sns.heatmap(matrix, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels)
    plt.title("TextBlob vs VADER Sentiment Confusion Matrix")
    plt.xlabel("TextBlob Label")
    plt.ylabel("VADER Label")
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=180)
    plt.close()

