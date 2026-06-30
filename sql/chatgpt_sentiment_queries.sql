-- ChatGPT Twitter Sentiment Analysis: 50 interview-level SQL queries
-- Assumed table: chatgpt_tweets_featured

-- 1. Total tweet volume
SELECT COUNT(*) AS total_tweets FROM chatgpt_tweets_featured;

-- 2. Daily tweet volume
SELECT day, COUNT(*) AS tweet_count
FROM chatgpt_tweets_featured
GROUP BY day
ORDER BY day;

-- 3. Monthly tweet growth
SELECT month, COUNT(*) AS tweet_count
FROM chatgpt_tweets_featured
GROUP BY month
ORDER BY month;

-- 4. Sentiment distribution
SELECT sentiment_label, COUNT(*) AS tweet_count
FROM chatgpt_tweets_featured
GROUP BY sentiment_label
ORDER BY tweet_count DESC;

-- 5. Positive percentage
SELECT
    ROUND(100.0 * SUM(CASE WHEN sentiment_label = 'Positive' THEN 1 ELSE 0 END) / COUNT(*), 2) AS positive_pct
FROM chatgpt_tweets_featured;

-- 6. Negative percentage
SELECT
    ROUND(100.0 * SUM(CASE WHEN sentiment_label = 'Negative' THEN 1 ELSE 0 END) / COUNT(*), 2) AS negative_pct
FROM chatgpt_tweets_featured;

-- 7. Positive-to-negative ratio
SELECT
    SUM(CASE WHEN sentiment_label = 'Positive' THEN 1 ELSE 0 END) * 1.0 /
    NULLIF(SUM(CASE WHEN sentiment_label = 'Negative' THEN 1 ELSE 0 END), 0) AS positive_negative_ratio
FROM chatgpt_tweets_featured;

-- 8. Top 10 countries by volume
SELECT country, COUNT(*) AS tweet_count
FROM chatgpt_tweets_featured
GROUP BY country
ORDER BY tweet_count DESC
LIMIT 10;

-- 9. Countries with more than 1,000 tweets
SELECT country, COUNT(*) AS tweet_count
FROM chatgpt_tweets_featured
GROUP BY country
HAVING COUNT(*) > 1000
ORDER BY tweet_count DESC;

-- 10. Country sentiment ratio
SELECT
    country,
    COUNT(*) AS total_tweets,
    AVG(CASE WHEN sentiment_label = 'Positive' THEN 1.0 ELSE 0.0 END) AS positive_ratio,
    AVG(CASE WHEN sentiment_label = 'Negative' THEN 1.0 ELSE 0.0 END) AS negative_ratio
FROM chatgpt_tweets_featured
GROUP BY country
HAVING COUNT(*) >= 500
ORDER BY positive_ratio DESC;

-- 11. Top negative countries
SELECT country, COUNT(*) AS total_tweets,
       SUM(CASE WHEN sentiment_label = 'Negative' THEN 1 ELSE 0 END) AS negative_tweets
FROM chatgpt_tweets_featured
GROUP BY country
HAVING COUNT(*) >= 500
ORDER BY negative_tweets DESC;

-- 12. Verified vs non-verified volume
SELECT is_verified, COUNT(*) AS tweet_count
FROM chatgpt_tweets_featured
GROUP BY is_verified;

-- 13. Verified user sentiment
SELECT is_verified, sentiment_label, COUNT(*) AS tweet_count
FROM chatgpt_tweets_featured
GROUP BY is_verified, sentiment_label
ORDER BY is_verified, tweet_count DESC;

-- 14. Most active users
SELECT username, COUNT(*) AS tweet_count
FROM chatgpt_tweets_featured
GROUP BY username
ORDER BY tweet_count DESC
LIMIT 20;

-- 15. Most active verified users
SELECT username, COUNT(*) AS tweet_count
FROM chatgpt_tweets_featured
WHERE is_verified = TRUE
GROUP BY username
ORDER BY tweet_count DESC
LIMIT 20;

-- 16. Hourly tweet activity
SELECT hour, COUNT(*) AS tweet_count
FROM chatgpt_tweets_featured
GROUP BY hour
ORDER BY hour;

-- 17. Weekend vs weekday sentiment
SELECT weekend_flag, sentiment_label, COUNT(*) AS tweet_count
FROM chatgpt_tweets_featured
GROUP BY weekend_flag, sentiment_label
ORDER BY weekend_flag, tweet_count DESC;

-- 18. Average tweet length by sentiment
SELECT sentiment_label, AVG(tweet_length) AS avg_tweet_length
FROM chatgpt_tweets_featured
GROUP BY sentiment_label
ORDER BY avg_tweet_length DESC;

-- 19. Average word count by sentiment
SELECT sentiment_label, AVG(word_count) AS avg_word_count
FROM chatgpt_tweets_featured
GROUP BY sentiment_label
ORDER BY avg_word_count DESC;

-- 20. Long tweets with strong negative sentiment
SELECT username, tweet_date, raw_tweet_text, compound_score
FROM chatgpt_tweets_featured
WHERE word_count >= 30 AND compound_score <= -0.5
ORDER BY compound_score ASC
LIMIT 50;

-- 21. Strongly positive tweets
SELECT username, tweet_date, raw_tweet_text, compound_score
FROM chatgpt_tweets_featured
WHERE compound_score >= 0.75
ORDER BY compound_score DESC
LIMIT 50;

-- 22. Daily sentiment with window total
SELECT
    day,
    sentiment_label,
    COUNT(*) AS tweets,
    SUM(COUNT(*)) OVER (PARTITION BY day) AS daily_total
FROM chatgpt_tweets_featured
GROUP BY day, sentiment_label
ORDER BY day, sentiment_label;

-- 23. Daily positive share
WITH daily AS (
    SELECT day,
           COUNT(*) AS total_tweets,
           SUM(CASE WHEN sentiment_label = 'Positive' THEN 1 ELSE 0 END) AS positive_tweets
    FROM chatgpt_tweets_featured
    GROUP BY day
)
SELECT day, total_tweets, positive_tweets,
       positive_tweets * 1.0 / NULLIF(total_tweets, 0) AS positive_share
FROM daily
ORDER BY day;

-- 24. Rank days by tweet volume
SELECT day, COUNT(*) AS tweet_count,
       RANK() OVER (ORDER BY COUNT(*) DESC) AS volume_rank
FROM chatgpt_tweets_featured
GROUP BY day
ORDER BY volume_rank;

-- 25. Dense rank countries by positive tweets
SELECT country,
       SUM(CASE WHEN sentiment_label = 'Positive' THEN 1 ELSE 0 END) AS positive_tweets,
       DENSE_RANK() OVER (ORDER BY SUM(CASE WHEN sentiment_label = 'Positive' THEN 1 ELSE 0 END) DESC) AS positive_rank
FROM chatgpt_tweets_featured
GROUP BY country;

-- 26. Row number top tweet per user by compound score
WITH ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY username ORDER BY compound_score DESC) AS rn
    FROM chatgpt_tweets_featured
)
SELECT username, tweet_date, raw_tweet_text, compound_score
FROM ranked
WHERE rn = 1;

-- 27. Lag daily tweet volume
WITH daily AS (
    SELECT day, COUNT(*) AS tweet_count
    FROM chatgpt_tweets_featured
    GROUP BY day
)
SELECT day, tweet_count,
       LAG(tweet_count) OVER (ORDER BY day) AS previous_day_tweets,
       tweet_count - LAG(tweet_count) OVER (ORDER BY day) AS day_over_day_change
FROM daily
ORDER BY day;

-- 28. Lead next day sentiment volume
WITH daily_sentiment AS (
    SELECT day, sentiment_label, COUNT(*) AS tweets
    FROM chatgpt_tweets_featured
    GROUP BY day, sentiment_label
)
SELECT day, sentiment_label, tweets,
       LEAD(tweets) OVER (PARTITION BY sentiment_label ORDER BY day) AS next_day_tweets
FROM daily_sentiment;

-- 29. Seven-day moving average
WITH daily AS (
    SELECT day, COUNT(*) AS tweet_count
    FROM chatgpt_tweets_featured
    GROUP BY day
)
SELECT day, tweet_count,
       AVG(tweet_count) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS seven_day_avg
FROM daily;

-- 30. Top country per sentiment using row number
WITH country_sentiment AS (
    SELECT country, sentiment_label, COUNT(*) AS tweet_count
    FROM chatgpt_tweets_featured
    GROUP BY country, sentiment_label
),
ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY sentiment_label ORDER BY tweet_count DESC) AS rn
    FROM country_sentiment
)
SELECT sentiment_label, country, tweet_count
FROM ranked
WHERE rn = 1;

-- 31. Privacy discussions
SELECT day, COUNT(*) AS privacy_tweets
FROM chatgpt_tweets_featured
WHERE clean_text LIKE '%privacy%' OR clean_text LIKE '%data security%'
GROUP BY day
ORDER BY day;

-- 32. Job loss discussions
SELECT day, COUNT(*) AS job_loss_tweets
FROM chatgpt_tweets_featured
WHERE clean_text LIKE '%job%' OR clean_text LIKE '%automation%' OR clean_text LIKE '%replace%'
GROUP BY day
ORDER BY day;

-- 33. Education mentions
SELECT day, COUNT(*) AS education_tweets
FROM chatgpt_tweets_featured
WHERE clean_text LIKE '%student%' OR clean_text LIKE '%teacher%' OR clean_text LIKE '%school%'
GROUP BY day
ORDER BY day;

-- 34. Coding mentions
SELECT day, COUNT(*) AS coding_tweets
FROM chatgpt_tweets_featured
WHERE clean_text LIKE '%code%' OR clean_text LIKE '%python%' OR clean_text LIKE '%programming%'
GROUP BY day
ORDER BY day;

-- 35. Company mentions
SELECT
    SUM(CASE WHEN clean_text LIKE '%openai%' THEN 1 ELSE 0 END) AS openai_mentions,
    SUM(CASE WHEN clean_text LIKE '%microsoft%' THEN 1 ELSE 0 END) AS microsoft_mentions,
    SUM(CASE WHEN clean_text LIKE '%google%' THEN 1 ELSE 0 END) AS google_mentions,
    SUM(CASE WHEN clean_text LIKE '%meta%' THEN 1 ELSE 0 END) AS meta_mentions,
    SUM(CASE WHEN clean_text LIKE '%amazon%' THEN 1 ELSE 0 END) AS amazon_mentions
FROM chatgpt_tweets_featured;

-- 36. AI model mentions
SELECT
    SUM(CASE WHEN clean_text LIKE '%chatgpt%' THEN 1 ELSE 0 END) AS chatgpt_mentions,
    SUM(CASE WHEN clean_text LIKE '%bard%' THEN 1 ELSE 0 END) AS bard_mentions,
    SUM(CASE WHEN clean_text LIKE '%gemini%' THEN 1 ELSE 0 END) AS gemini_mentions,
    SUM(CASE WHEN clean_text LIKE '%claude%' THEN 1 ELSE 0 END) AS claude_mentions
FROM chatgpt_tweets_featured;

-- 37. VADER and TextBlob agreement
SELECT
    AVG(CASE WHEN sentiment_label = textblob_label THEN 1.0 ELSE 0.0 END) AS agreement_rate
FROM chatgpt_tweets_featured;

-- 38. Confusion matrix counts
SELECT sentiment_label AS vader_label, textblob_label, COUNT(*) AS tweet_count
FROM chatgpt_tweets_featured
GROUP BY sentiment_label, textblob_label
ORDER BY vader_label, textblob_label;

-- 39. Create analytical view
CREATE VIEW vw_daily_sentiment AS
SELECT day, sentiment_label, COUNT(*) AS tweets, AVG(compound_score) AS avg_compound
FROM chatgpt_tweets_featured
GROUP BY day, sentiment_label;

-- 40. Query daily sentiment view
SELECT * FROM vw_daily_sentiment ORDER BY day, sentiment_label;

-- 41. Subquery for above-average activity countries
SELECT country, COUNT(*) AS tweet_count
FROM chatgpt_tweets_featured
GROUP BY country
HAVING COUNT(*) > (
    SELECT AVG(country_count)
    FROM (
        SELECT country, COUNT(*) AS country_count
        FROM chatgpt_tweets_featured
        GROUP BY country
    ) country_counts
);

-- 42. Countries where negative share exceeds global negative share
WITH global_rate AS (
    SELECT AVG(CASE WHEN sentiment_label = 'Negative' THEN 1.0 ELSE 0.0 END) AS global_negative_rate
    FROM chatgpt_tweets_featured
),
country_rate AS (
    SELECT country,
           COUNT(*) AS tweets,
           AVG(CASE WHEN sentiment_label = 'Negative' THEN 1.0 ELSE 0.0 END) AS country_negative_rate
    FROM chatgpt_tweets_featured
    GROUP BY country
)
SELECT country, tweets, country_negative_rate
FROM country_rate
CROSS JOIN global_rate
WHERE tweets >= 500 AND country_negative_rate > global_negative_rate
ORDER BY country_negative_rate DESC;

-- 43. Hashtag exploded table example
-- Use this if hashtags are normalized into tweet_hashtags(tweet_id, hashtag).
SELECT hashtag, COUNT(*) AS usage_count
FROM tweet_hashtags
GROUP BY hashtag
ORDER BY usage_count DESC
LIMIT 25;

-- 44. Join tweets to hashtags
SELECT h.hashtag, t.sentiment_label, COUNT(*) AS tweet_count
FROM chatgpt_tweets_featured t
JOIN tweet_hashtags h ON t.tweet_id = h.tweet_id
GROUP BY h.hashtag, t.sentiment_label
ORDER BY tweet_count DESC;

-- 45. Positive hashtags with minimum support
SELECT h.hashtag,
       COUNT(*) AS total_uses,
       AVG(CASE WHEN t.sentiment_label = 'Positive' THEN 1.0 ELSE 0.0 END) AS positive_rate
FROM chatgpt_tweets_featured t
JOIN tweet_hashtags h ON t.tweet_id = h.tweet_id
GROUP BY h.hashtag
HAVING COUNT(*) >= 100
ORDER BY positive_rate DESC;

-- 46. Negative hashtags with minimum support
SELECT h.hashtag,
       COUNT(*) AS total_uses,
       AVG(CASE WHEN t.sentiment_label = 'Negative' THEN 1.0 ELSE 0.0 END) AS negative_rate
FROM chatgpt_tweets_featured t
JOIN tweet_hashtags h ON t.tweet_id = h.tweet_id
GROUP BY h.hashtag
HAVING COUNT(*) >= 100
ORDER BY negative_rate DESC;

-- 47. User-level sentiment profile
SELECT username,
       COUNT(*) AS total_tweets,
       AVG(compound_score) AS avg_compound,
       SUM(CASE WHEN sentiment_label = 'Positive' THEN 1 ELSE 0 END) AS positive_tweets,
       SUM(CASE WHEN sentiment_label = 'Negative' THEN 1 ELSE 0 END) AS negative_tweets
FROM chatgpt_tweets_featured
GROUP BY username
HAVING COUNT(*) >= 10
ORDER BY avg_compound DESC;

-- 48. Country-hour activity pattern
SELECT country, hour, COUNT(*) AS tweets
FROM chatgpt_tweets_featured
GROUP BY country, hour
ORDER BY country, hour;

-- 49. Spike days above moving average
WITH daily AS (
    SELECT day, COUNT(*) AS tweet_count
    FROM chatgpt_tweets_featured
    GROUP BY day
),
moving AS (
    SELECT day, tweet_count,
           AVG(tweet_count) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS seven_day_avg
    FROM daily
)
SELECT day, tweet_count, seven_day_avg
FROM moving
WHERE tweet_count > seven_day_avg * 1.5
ORDER BY tweet_count DESC;

-- 50. Weekly sentiment change
WITH weekly AS (
    SELECT week,
           AVG(CASE WHEN sentiment_label = 'Positive' THEN 1.0 ELSE 0.0 END) AS positive_share,
           AVG(CASE WHEN sentiment_label = 'Negative' THEN 1.0 ELSE 0.0 END) AS negative_share
    FROM chatgpt_tweets_featured
    GROUP BY week
)
SELECT week,
       positive_share,
       positive_share - LAG(positive_share) OVER (ORDER BY week) AS positive_share_change,
       negative_share,
       negative_share - LAG(negative_share) OVER (ORDER BY week) AS negative_share_change
FROM weekly
ORDER BY week;

