"""Feature engineering for tweet-level analytics."""

from __future__ import annotations

import pandas as pd


def add_text_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create tweet length, word count, character count, hashtag, and mention features."""
    df = df.copy()
    df["tweet_length"] = df["raw_tweet_text"].fillna("").astype(str).str.len()
    df["word_count"] = df["clean_text"].fillna("").astype(str).str.split().str.len()
    df["character_count"] = df["clean_text"].fillna("").astype(str).str.len()
    df["hashtag_count"] = df["hashtags"].apply(len)
    df["mention_count"] = df["mentions"].apply(len)
    return df


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create day, month, hour, week, and weekend dimensions."""
    df = df.copy()
    dates = pd.to_datetime(df["tweet_date"], errors="coerce", utc=True)
    df["day"] = dates.dt.date
    df["month"] = dates.dt.to_period("M").astype(str)
    df["hour"] = dates.dt.hour
    df["week"] = dates.dt.isocalendar().week.astype("Int64")
    df["weekend_flag"] = dates.dt.dayofweek.isin([5, 6])
    return df


def add_all_features(df: pd.DataFrame) -> pd.DataFrame:
    """Apply all feature engineering steps."""
    return add_time_features(add_text_features(df))

