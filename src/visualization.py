"""Generate portfolio-quality EDA visuals for the project."""

from __future__ import annotations

from collections import Counter
from itertools import chain
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
from nltk import ngrams
from wordcloud import WordCloud


sns.set_theme(style="whitegrid")


def _save_matplotlib(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()


def _bar(series: pd.Series, title: str, xlabel: str, ylabel: str, path: Path, top_n: int = 20) -> None:
    plt.figure(figsize=(12, 7))
    series.head(top_n).sort_values().plot(kind="barh", color="#2d7dd2")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    _save_matplotlib(path)


def _count_terms(values: pd.Series, top_n: int = 25) -> pd.Series:
    return pd.Series(Counter(chain.from_iterable(values.dropna()))).sort_values(ascending=False).head(top_n)


def _keyword_flag(df: pd.DataFrame, terms: list[str]) -> pd.Series:
    pattern = "|".join(terms)
    return df["clean_text"].str.contains(pattern, case=False, na=False, regex=True)


def generate_core_visualizations(df: pd.DataFrame, output_dir: Path) -> list[Path]:
    """Generate 30+ EDA visualizations requested for the portfolio."""
    output_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []

    daily = df.groupby("day").size()
    plt.figure(figsize=(14, 6)); daily.plot(color="#134074"); plt.title("Daily Tweet Volume"); plt.ylabel("Tweets")
    paths.append(output_dir / "01_daily_tweet_volume.png"); _save_matplotlib(paths[-1])

    monthly = df.groupby("month").size()
    _bar(monthly.sort_values(ascending=False), "Monthly Tweet Growth", "Tweets", "Month", output_dir / "02_monthly_tweet_growth.png", 12); paths.append(output_dir / "02_monthly_tweet_growth.png")

    hourly = df.groupby("hour").size()
    plt.figure(figsize=(12, 6)); hourly.plot(kind="bar", color="#f45b69"); plt.title("Hourly Tweet Activity")
    paths.append(output_dir / "03_hourly_tweet_activity.png"); _save_matplotlib(paths[-1])

    _bar(df["country"].value_counts(), "Top Countries by Tweet Volume", "Tweets", "Country", output_dir / "04_top_countries.png"); paths.append(output_dir / "04_top_countries.png")
    _bar(df["is_verified"].map({True: "Verified", False: "Non-Verified"}).value_counts(), "Verified vs Non-Verified Users", "Tweets", "Account Type", output_dir / "05_verified_vs_non_verified.png", 2); paths.append(output_dir / "05_verified_vs_non_verified.png")
    _bar(df["sentiment_label"].value_counts(), "Sentiment Distribution", "Tweets", "Sentiment", output_dir / "06_sentiment_distribution.png", 3); paths.append(output_dir / "06_sentiment_distribution.png")

    _bar(df["username"].value_counts(), "Most Active Users", "Tweets", "User", output_dir / "07_most_active_users.png"); paths.append(output_dir / "07_most_active_users.png")
    _bar(_count_terms(df["hashtags"]), "Most Used Hashtags", "Mentions", "Hashtag", output_dir / "08_most_used_hashtags.png"); paths.append(output_dir / "08_most_used_hashtags.png")
    _bar(_count_terms(df["mentions"]), "Most Mentioned Accounts", "Mentions", "Account", output_dir / "09_most_mentioned_accounts.png"); paths.append(output_dir / "09_most_mentioned_accounts.png")

    plt.figure(figsize=(12, 6)); sns.histplot(df["tweet_length"], bins=50, color="#23ce6b"); plt.title("Tweet Length Distribution")
    paths.append(output_dir / "10_tweet_length_distribution.png"); _save_matplotlib(paths[-1])

    words = pd.Series(Counter(chain.from_iterable(df["tokens"]))).sort_values(ascending=False)
    _bar(words, "Word Frequency", "Count", "Word", output_dir / "11_word_frequency.png"); paths.append(output_dir / "11_word_frequency.png")

    bigrams = Counter(chain.from_iterable(ngrams(tokens, 2) for tokens in df["tokens"] if len(tokens) >= 2))
    _bar(pd.Series({" ".join(k): v for k, v in bigrams.items()}).sort_values(ascending=False), "Bigram Analysis", "Count", "Bigram", output_dir / "12_bigram_analysis.png"); paths.append(output_dir / "12_bigram_analysis.png")

    trigrams = Counter(chain.from_iterable(ngrams(tokens, 3) for tokens in df["tokens"] if len(tokens) >= 3))
    _bar(pd.Series({" ".join(k): v for k, v in trigrams.items()}).sort_values(ascending=False), "Trigram Analysis", "Count", "Trigram", output_dir / "13_trigram_analysis.png"); paths.append(output_dir / "13_trigram_analysis.png")

    sentiment_time = df.pivot_table(index="day", columns="sentiment_label", values="clean_text", aggfunc="count").fillna(0)
    plt.figure(figsize=(14, 7)); sentiment_time.plot(ax=plt.gca()); plt.title("Sentiment Over Time"); plt.ylabel("Tweets")
    paths.append(output_dir / "14_sentiment_over_time.png"); _save_matplotlib(paths[-1])

    country_sentiment = df.pivot_table(index="country", columns="sentiment_label", values="clean_text", aggfunc="count").fillna(0)
    country_sentiment["total"] = country_sentiment.sum(axis=1)
    country_sentiment.sort_values("total", ascending=False).head(15).drop(columns="total").plot(kind="bar", stacked=True, figsize=(14, 7))
    plt.title("Sentiment by Country"); paths.append(output_dir / "15_sentiment_by_country.png"); _save_matplotlib(paths[-1])

    df.pivot_table(index="is_verified", columns="sentiment_label", values="clean_text", aggfunc="count").fillna(0).plot(kind="bar", stacked=True, figsize=(10, 6))
    plt.title("Verified User Sentiment"); paths.append(output_dir / "16_verified_user_sentiment.png"); _save_matplotlib(paths[-1])

    for label, file_name in [("Positive", "17_positive_wordcloud.png"), ("Negative", "18_negative_wordcloud.png"), ("Neutral", "19_neutral_wordcloud.png")]:
        text = " ".join(df.loc[df["sentiment_label"] == label, "lemmatized_text"].dropna())
        wc = WordCloud(width=1400, height=700, background_color="white", colormap="viridis").generate(text or "chatgpt")
        plt.figure(figsize=(14, 7)); plt.imshow(wc); plt.axis("off"); plt.title(f"{label} Word Cloud")
        paths.append(output_dir / file_name); _save_matplotlib(paths[-1])

    for label, file_name in [("Positive", "20_top_positive_words.png"), ("Negative", "21_top_negative_words.png")]:
        subset_words = pd.Series(Counter(chain.from_iterable(df.loc[df["sentiment_label"] == label, "tokens"]))).sort_values(ascending=False)
        _bar(subset_words, f"Top {label} Words", "Count", "Word", output_dir / file_name); paths.append(output_dir / file_name)

    _bar(daily.sort_values(ascending=False), "Peak Tweet Days", "Tweets", "Day", output_dir / "22_peak_tweet_days.png", 15); paths.append(output_dir / "22_peak_tweet_days.png")

    topic_map = {
        "23_ai_concern_trends.png": ["risk", "concern", "danger", "bias", "misinformation", "regulation"],
        "24_privacy_discussions.png": ["privacy", "data", "security", "surveillance"],
        "25_job_loss_discussions.png": ["job", "jobs", "layoff", "automation", "replace"],
        "26_education_mentions.png": ["school", "student", "teacher", "education", "homework"],
        "27_coding_mentions.png": ["code", "coding", "python", "developer", "programming"],
        "28_developer_mentions.png": ["developer", "engineer", "software", "github", "api"],
    }
    for file_name, terms in topic_map.items():
        topic_df = df[_keyword_flag(df, terms)].groupby("day").size()
        plt.figure(figsize=(14, 6)); topic_df.plot(color="#7b2cbf"); plt.title(file_name.replace(".png", "").replace("_", " ").title())
        paths.append(output_dir / file_name); _save_matplotlib(paths[-1])

    comparison_topics = {
        "29_chatgpt_vs_bard_mentions.png": ["chatgpt", "bard"],
        "30_chatgpt_vs_gemini_mentions.png": ["chatgpt", "gemini"],
        "31_chatgpt_vs_claude_mentions.png": ["chatgpt", "claude"],
        "32_most_mentioned_ai_models.png": ["chatgpt", "gpt", "bard", "gemini", "claude", "llama"],
        "33_most_mentioned_companies.png": ["openai", "google", "microsoft", "meta", "amazon"],
    }
    for file_name, terms in comparison_topics.items():
        counts = {term: int(df["clean_text"].str.contains(term, case=False, na=False).sum()) for term in terms}
        _bar(pd.Series(counts).sort_values(ascending=False), file_name.replace(".png", "").replace("_", " ").title(), "Tweets", "Keyword", output_dir / file_name, len(terms))
        paths.append(output_dir / file_name)

    positive_ratio = df.assign(is_positive=df["sentiment_label"].eq("Positive")).groupby("country")["is_positive"].mean().sort_values(ascending=False)
    _bar(positive_ratio, "Positive Sentiment Ratio by Country", "Positive Ratio", "Country", output_dir / "34_positive_ratio_by_country.png"); paths.append(output_dir / "34_positive_ratio_by_country.png")

    fig = px.choropleth(df.groupby("country").size().reset_index(name="tweets"), locations="country", locationmode="country names", color="tweets", title="Country-wise Tweets")
    html_path = output_dir / "35_country_wise_tweets_map.html"; fig.write_html(html_path); paths.append(html_path)

    return paths

