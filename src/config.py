"""Central project configuration."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
CLEANED_DATA_DIR = DATA_DIR / "cleaned"
IMAGE_DIR = PROJECT_ROOT / "images"
REPORT_DIR = PROJECT_ROOT / "reports"

RAW_FILE_NAME = "chatgpt_tweets.csv"
CLEANED_FILE_NAME = "chatgpt_tweets_cleaned.csv"
FEATURED_FILE_NAME = "chatgpt_tweets_featured.csv"

RAW_DATA_PATH = RAW_DATA_DIR / RAW_FILE_NAME
CLEANED_DATA_PATH = CLEANED_DATA_DIR / CLEANED_FILE_NAME
FEATURED_DATA_PATH = CLEANED_DATA_DIR / FEATURED_FILE_NAME

LANGUAGE_ALLOWLIST = {"en"}

COUNTRY_REPLACEMENTS = {
    "usa": "United States",
    "us": "United States",
    "u.s.": "United States",
    "u.s.a.": "United States",
    "united states of america": "United States",
    "uk": "United Kingdom",
    "u.k.": "United Kingdom",
    "england": "United Kingdom",
    "uae": "United Arab Emirates",
}

TEXT_COLUMNS = ("tweet", "text", "content", "full_text")
DATE_COLUMNS = ("date", "created_at", "tweet_created", "timestamp")
USER_COLUMNS = ("user", "username", "screen_name", "author")
COUNTRY_COLUMNS = ("country", "user_location", "location")
VERIFIED_COLUMNS = ("verified", "user_verified", "is_verified")
LANGUAGE_COLUMNS = ("language", "lang")

