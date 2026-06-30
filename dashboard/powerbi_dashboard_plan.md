# Power BI Dashboard Plan

## Theme

Dark modern executive theme with high contrast KPI cards, muted gridlines, and accent colors:

- Positive: green
- Negative: red
- Neutral: gray
- ChatGPT/OpenAI accent: teal
- Background: near-black

## Data Model

- Fact table: `chatgpt_tweets_featured`
- Date dimension: derived from `tweet_date`, `day`, `month`, `week`, `hour`
- Geography dimension: `country`
- Account dimension: `username`, `is_verified`
- NLP dimensions: `sentiment_label`, `textblob_label`, hashtags, mentions, topic flags

## Page 1: Executive Summary

KPIs:

- Total Tweets
- Positive %
- Negative %
- Neutral %
- Positive-to-Negative Ratio
- Verified Tweet %
- Top Country
- Peak Tweet Day

Visuals:

- Sentiment donut chart
- Daily tweet volume line chart
- Top 10 countries bar chart
- Topic trend small multiples

## Page 2: Tweet Activity

Visuals:

- Daily tweet volume
- Monthly tweet growth
- Hourly tweet activity heatmap
- Weekend vs weekday comparison
- Peak tweet days table

Filters:

- Date range
- Country
- Verified flag
- Sentiment label

## Page 3: Sentiment Dashboard

Visuals:

- Sentiment over time
- VADER compound score distribution
- TextBlob polarity distribution
- Positive vs negative ratio by week
- Confusion matrix image from model comparison

Cards:

- Average compound score
- Average TextBlob polarity
- VADER/TextBlob agreement rate

## Page 4: Country Dashboard

Visuals:

- Filled map by tweet count
- Country-wise positive ratio
- Country-wise negative ratio
- Country sentiment stacked bar
- Country drillthrough table

## Page 5: Verified Users Dashboard

Visuals:

- Verified vs non-verified tweet volume
- Verified user sentiment distribution
- Top verified users
- Verified account sentiment over time
- Topic distribution by verified flag

## Page 6: Keyword Dashboard

Visuals:

- AI concern trend
- Privacy discussion trend
- Job loss discussion trend
- Education mentions
- Coding and developer mentions
- ChatGPT vs Bard/Gemini/Claude comparison

## Page 7: Hashtag Dashboard

Visuals:

- Top hashtags
- Hashtags by sentiment
- Positive hashtag associations
- Negative hashtag associations
- Hashtag trend over time

## Page 8: Trend Dashboard

Visuals:

- Daily volume with spike annotation
- Sentiment spike decomposition
- Top words during spike days
- Top users during spike days
- Company and AI model mention trends

## Interactive Filters

- Date
- Month
- Week
- Hour
- Country
- Sentiment
- Verified account
- Hashtag
- Mentioned company
- Topic category

## Recommended DAX Measures

```DAX
Total Tweets = COUNTROWS(chatgpt_tweets_featured)

Positive Tweets =
CALCULATE([Total Tweets], chatgpt_tweets_featured[sentiment_label] = "Positive")

Negative Tweets =
CALCULATE([Total Tweets], chatgpt_tweets_featured[sentiment_label] = "Negative")

Positive % = DIVIDE([Positive Tweets], [Total Tweets])

Negative % = DIVIDE([Negative Tweets], [Total Tweets])

Positive Negative Ratio = DIVIDE([Positive Tweets], [Negative Tweets])

Verified Tweet % =
DIVIDE(
    CALCULATE([Total Tweets], chatgpt_tweets_featured[is_verified] = TRUE()),
    [Total Tweets]
)

Average Compound Score = AVERAGE(chatgpt_tweets_featured[compound_score])
```

