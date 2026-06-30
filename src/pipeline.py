"""End-to-end production pipeline for the ChatGPT Twitter sentiment project."""

from __future__ import annotations

import argparse
import logging

from src.config import CLEANED_DATA_PATH, FEATURED_DATA_PATH, IMAGE_DIR, RAW_DATA_PATH
from src.features import add_all_features
from src.nlp_evaluation import compare_sentiment_models, plot_confusion_matrix
from src.preprocessing import clean_tweets
from src.sentiment import add_sentiment_features
from src.utils import ensure_directories, safe_read_csv, setup_logging
from src.visualization import generate_core_visualizations

LOGGER = logging.getLogger(__name__)


def run_pipeline(raw_path=RAW_DATA_PATH, cleaned_path=CLEANED_DATA_PATH, featured_path=FEATURED_DATA_PATH) -> None:
    """Run cleaning, feature engineering, NLP, evaluation, and visualization generation."""
    setup_logging()
    ensure_directories([cleaned_path.parent, featured_path.parent, IMAGE_DIR / "generated"])

    LOGGER.info("Reading raw data from %s", raw_path)
    raw_df = safe_read_csv(raw_path)

    cleaned_df = clean_tweets(raw_df)
    cleaned_df.to_csv(cleaned_path, index=False)
    LOGGER.info("Saved cleaned data to %s", cleaned_path)

    featured_df = add_sentiment_features(add_all_features(cleaned_df))
    featured_df.to_csv(featured_path, index=False)
    LOGGER.info("Saved featured data to %s", featured_path)

    metrics = compare_sentiment_models(featured_df)
    metrics_path = featured_path.parent / "sentiment_model_comparison.csv"
    metrics.to_csv(metrics_path, index=False)
    plot_confusion_matrix(featured_df, IMAGE_DIR / "generated" / "sentiment_confusion_matrix.png")
    LOGGER.info("Saved model comparison to %s", metrics_path)

    generated = generate_core_visualizations(featured_df, IMAGE_DIR / "generated")
    LOGGER.info("Generated %s visualizations", len(generated))


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run ChatGPT Twitter sentiment analysis pipeline.")
    parser.add_argument("--raw-path", default=str(RAW_DATA_PATH), help="Path to raw Kaggle CSV.")
    parser.add_argument("--cleaned-path", default=str(CLEANED_DATA_PATH), help="Output path for cleaned CSV.")
    parser.add_argument("--featured-path", default=str(FEATURED_DATA_PATH), help="Output path for featured CSV.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_pipeline(args.raw_path, args.cleaned_path, args.featured_path)

