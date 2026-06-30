"""Sentiment scoring with VADER and TextBlob."""

from __future__ import annotations

import logging

import pandas as pd
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

LOGGER = logging.getLogger(__name__)


def vader_label(compound: float) -> str:
    """Convert VADER compound score to sentiment class."""
    if compound >= 0.05:
        return "Positive"
    if compound <= -0.05:
        return "Negative"
    return "Neutral"


def textblob_label(polarity: float) -> str:
    """Convert TextBlob polarity to sentiment class."""
    if polarity > 0.05:
        return "Positive"
    if polarity < -0.05:
        return "Negative"
    return "Neutral"


def add_vader_sentiment(df: pd.DataFrame, text_column: str = "clean_text") -> pd.DataFrame:
    """Add VADER positive, negative, neutral, compound, and label columns."""
    analyzer = SentimentIntensityAnalyzer()
    df = df.copy()
    scores = df[text_column].fillna("").astype(str).apply(analyzer.polarity_scores)
    df["positive_score"] = scores.apply(lambda item: item["pos"])
    df["negative_score"] = scores.apply(lambda item: item["neg"])
    df["neutral_score"] = scores.apply(lambda item: item["neu"])
    df["compound_score"] = scores.apply(lambda item: item["compound"])
    df["sentiment_label"] = df["compound_score"].apply(vader_label)
    return df


def add_textblob_sentiment(df: pd.DataFrame, text_column: str = "clean_text") -> pd.DataFrame:
    """Add TextBlob polarity, subjectivity, and label columns."""
    df = df.copy()
    blobs = df[text_column].fillna("").astype(str).apply(TextBlob)
    df["textblob_polarity"] = blobs.apply(lambda blob: blob.sentiment.polarity)
    df["textblob_subjectivity"] = blobs.apply(lambda blob: blob.sentiment.subjectivity)
    df["textblob_label"] = df["textblob_polarity"].apply(textblob_label)
    return df


def add_sentiment_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add both VADER and TextBlob sentiment outputs."""
    LOGGER.info("Adding VADER and TextBlob sentiment features")
    return add_textblob_sentiment(add_vader_sentiment(df))

