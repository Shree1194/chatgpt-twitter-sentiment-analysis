# Interview Preparation

## 50 Data Analyst Interview Questions

1. What business problem does this project solve?
2. Why is Twitter sentiment useful for AI product teams?
3. What are the limitations of social media data?
4. How did you handle missing values?
5. How did you detect duplicate tweets?
6. Why remove URLs, usernames, HTML, and emojis before NLP?
7. Why keep hashtags separately instead of deleting them completely?
8. What is the difference between tweet length and word count?
9. How did you normalize countries?
10. Why filter by language?
11. What is tokenization?
12. What is lemmatization?
13. Why remove stopwords?
14. What is VADER sentiment analysis?
15. Why is VADER useful for social media text?
16. What is TextBlob polarity?
17. How are VADER and TextBlob different?
18. How did you assign sentiment labels?
19. What does compound score mean?
20. How did you compare sentiment models without manually labeled data?
21. What is a weak-label baseline?
22. What does accuracy measure?
23. What does precision measure?
24. What does recall measure?
25. What does F1 score measure?
26. Why use a confusion matrix?
27. What are the most important KPIs in this project?
28. How would you explain sentiment over time to executives?
29. How would you identify spike events?
30. How would you prevent misleading country-level conclusions?
31. How did verified users differ from non-verified users?
32. Which hashtags were most associated with positive sentiment?
33. Which topics generated fear?
34. Which topics generated excitement?
35. What dashboard filters would business users need?
36. How would you optimize this pipeline for 5 million tweets?
37. How would you validate the data quality?
38. How would you handle sarcasm?
39. How would you handle multilingual tweets?
40. How would you deploy this project?
41. What SQL window functions did you use?
42. What is the difference between RANK and DENSE_RANK?
43. When would you use a CTE?
44. How would you design the Power BI data model?
45. Which DAX measures are most useful?
46. What are the risks of using Twitter data for public opinion?
47. What would you improve with more time?
48. How would this project help a product manager?
49. How would this project help a marketing team?
50. How would you summarize the project in 60 seconds?

## NLP Questions

- Explain VADER's positive, negative, neutral, and compound scores.
- Why can lexicon-based sentiment struggle with sarcasm?
- What is subjectivity in TextBlob?
- How would you build a supervised sentiment classifier?
- How would you evaluate a sentiment model with manually labeled data?
- How would you use topic modeling for this project?

## SQL Questions

- Write a query to find top countries by positive sentiment ratio.
- Write a CTE to identify spike days.
- Use LAG to calculate day-over-day tweet growth.
- Use ROW_NUMBER to find the most positive tweet per user.
- Explain HAVING versus WHERE.
- Explain PARTITION BY in a window function.

## Python Questions

- Why use functions and modules instead of one long notebook?
- How do Pandas groupby operations work?
- How would you process a CSV that is too large for memory?
- Why use logging in a data pipeline?
- What exceptions can happen while reading real-world CSV files?
- How would you profile slow preprocessing code?

## Statistics Questions

- What is a distribution?
- What is a ratio metric?
- Why can small sample sizes mislead country comparisons?
- What is a moving average?
- How would you detect an outlier day?
- What is sampling bias?

## Power BI Questions

- What pages would you include in the dashboard?
- What slicers are needed?
- What measures should become KPI cards?
- Why use a dark modern theme?
- How would you design drillthrough for country analysis?
- How would you make the dashboard executive-friendly?

## HR Questions

- Tell me about a challenging data cleaning problem.
- Tell me about a time you turned messy data into insights.
- How do you explain technical findings to non-technical stakeholders?
- How do you prioritize analysis when there are many possible charts?
- What would you do if stakeholders disagree with the data?

## 60-Second Project Explanation

I built a production-style sentiment analysis project on roughly 500K ChatGPT-related tweets from January to March 2023. I cleaned noisy social media text, extracted hashtags and mentions, normalized dates and countries, engineered text and time features, and used both VADER and TextBlob to classify sentiment. I then compared model outputs with accuracy, precision, recall, F1 score, and a confusion matrix. The analysis answers business questions around public opinion, country-level reaction, verified-user behavior, hashtag associations, AI fear topics, and excitement drivers. I also designed a Power BI dashboard and wrote 50 SQL queries to show how the dataset can support executive reporting and interview-level analytics.

