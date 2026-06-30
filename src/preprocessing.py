"""Professional tweet cleaning and normalization pipeline."""

from __future__ import annotations

import html
import logging
import re
from collections.abc import Iterable

import emoji
import nltk
import pandas as pd
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from src.config import (
    COUNTRY_COLUMNS,
    COUNTRY_REPLACEMENTS,
    DATE_COLUMNS,
    LANGUAGE_ALLOWLIST,
    LANGUAGE_COLUMNS,
    TEXT_COLUMNS,
    USER_COLUMNS,
    VERIFIED_COLUMNS,
)
from src.utils import first_existing_column

LOGGER = logging.getLogger(__name__)

URL_PATTERN = re.compile(r"https?://\S+|www\.\S+")
USERNAME_PATTERN = re.compile(r"@\w+")
HASHTAG_PATTERN = re.compile(r"#(\w+)")
HTML_PATTERN = re.compile(r"<.*?>")
NON_ALPHA_PATTERN = re.compile(r"[^a-zA-Z\s]")
WHITESPACE_PATTERN = re.compile(r"\s+")


def download_nltk_assets() -> None:
    """Download required NLTK assets if missing."""
    for package in ["punkt", "stopwords", "wordnet", "omw-1.4"]:
        nltk.download(package, quiet=True)


def extract_hashtags(text: str) -> list[str]:
    """Extract hashtags without the leading hash sign."""
    return [tag.lower() for tag in HASHTAG_PATTERN.findall(str(text))]


def extract_mentions(text: str) -> list[str]:
    """Extract mentioned accounts without the leading @ sign."""
    return [mention[1:].lower() for mention in USERNAME_PATTERN.findall(str(text))]


def remove_noise(text: str) -> str:
    """Remove URLs, HTML, emojis, usernames, hashtags, and non-letter noise."""
    text = html.unescape(str(text))
    text = BeautifulSoup(text, "html.parser").get_text(" ")
    text = URL_PATTERN.sub(" ", text)
    text = USERNAME_PATTERN.sub(" ", text)
    text = HASHTAG_PATTERN.sub(r"\1", text)
    text = emoji.replace_emoji(text, replace=" ")
    text = HTML_PATTERN.sub(" ", text)
    text = NON_ALPHA_PATTERN.sub(" ", text)
    return WHITESPACE_PATTERN.sub(" ", text).strip().lower()


def tokenize_and_lemmatize(text: str, stop_words: set[str], lemmatizer: WordNetLemmatizer) -> list[str]:
    """Tokenize, remove stopwords, and lemmatize a cleaned tweet."""
    tokens = word_tokenize(text)
    return [
        lemmatizer.lemmatize(token)
        for token in tokens
        if token.isalpha() and token not in stop_words and len(token) > 1
    ]


def normalize_country(value: object) -> str:
    """Normalize country names and common abbreviations."""
    if pd.isna(value) or str(value).strip() == "":
        return "Unknown"
    cleaned = WHITESPACE_PATTERN.sub(" ", str(value).strip())
    return COUNTRY_REPLACEMENTS.get(cleaned.lower(), cleaned.title())


def normalize_verified(value: object) -> bool:
    """Normalize verified account flags from booleans, strings, and integers."""
    if pd.isna(value):
        return False
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "y", "verified"}


def _copy_or_default(df: pd.DataFrame, source: str | None, target: str, default: object) -> None:
    if source is None:
        df[target] = default
    else:
        df[target] = df[source]


def standardize_schema(df: pd.DataFrame) -> pd.DataFrame:
    """Map common Kaggle export column names into a stable analytical schema."""
    df = df.copy()
    _copy_or_default(df, first_existing_column(df, TEXT_COLUMNS), "tweet_text", "")
    _copy_or_default(df, first_existing_column(df, DATE_COLUMNS), "tweet_date", pd.NaT)
    _copy_or_default(df, first_existing_column(df, USER_COLUMNS), "username", "Unknown")
    _copy_or_default(df, first_existing_column(df, COUNTRY_COLUMNS), "country", "Unknown")
    _copy_or_default(df, first_existing_column(df, VERIFIED_COLUMNS), "is_verified", False)
    _copy_or_default(df, first_existing_column(df, LANGUAGE_COLUMNS), "language", "en")
    return df


def clean_tweets(df: pd.DataFrame, language_allowlist: Iterable[str] = LANGUAGE_ALLOWLIST) -> pd.DataFrame:
    """Clean raw tweets and return an analysis-ready dataframe."""
    LOGGER.info("Starting tweet cleaning for %s rows", len(df))
    download_nltk_assets()

    df = standardize_schema(df)
    df["tweet_text"] = df["tweet_text"].fillna("").astype(str)
    df["raw_tweet_text"] = df["tweet_text"]
    df["tweet_date"] = pd.to_datetime(df["tweet_date"], errors="coerce", utc=True)
    df["country"] = df["country"].apply(normalize_country)
    df["is_verified"] = df["is_verified"].apply(normalize_verified)
    df["language"] = df["language"].fillna("unknown").astype(str).str.lower()

    before_filter = len(df)
    df = df[df["language"].isin(set(language_allowlist))].copy()
    LOGGER.info("Language filtering removed %s rows", before_filter - len(df))

    df["hashtags"] = df["raw_tweet_text"].apply(extract_hashtags)
    df["mentions"] = df["raw_tweet_text"].apply(extract_mentions)
    df["clean_text"] = df["raw_tweet_text"].apply(remove_noise)

    df = df.dropna(subset=["tweet_date"])
    df = df[df["clean_text"].str.len() > 0]
    df = df.drop_duplicates(subset=["clean_text", "tweet_date", "username"])

    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    df["tokens"] = df["clean_text"].apply(lambda value: tokenize_and_lemmatize(value, stop_words, lemmatizer))
    df["lemmatized_text"] = df["tokens"].apply(" ".join)

    LOGGER.info("Finished cleaning. Output rows: %s", len(df))
    return df.reset_index(drop=True)

