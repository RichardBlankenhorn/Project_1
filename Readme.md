# Python Project 1 - Stock Twits Analysis

> In this project, twits regarding BAC (Bank of America) stock have been downloaded from StockTwits and stored in a JSON file.
> We need to conduct sentiment analysis of the tweets and show the result of the sentiment analysis using graphs

1. Read stock twits from the JSON file to obtain a list of dictionaries.
2. Extract the date/time, tweet content and user-assigned sentiment from each tweet.
3. Process tweet content: Remove punctuations, convert each tweet in to ASCII format and lower-case each word in the twee.
4. Convert timestamp in to a date/time string
5. User assigned sentiment is Bullish, Bearish or Null. Replace Null values with Unknown.
6. For each dictionary, create a list that includes the date/time, processed tweet content and user-assigned sentiment
Write the lists to a BAC.csv file.

7. Read data from BAC.csv file. If user assigned sentiment is Bullish or Bearish, no sentiment analysis is needed.
If user-assigned sentiment is Unknown, we need to conduct sentiment analysis for the tweet using the positive_words.txt
and negative_words.txt files.
8. Write date/time of tweet and sentiment to BAC2.csv file.

9. Read data from BAC2.csv and select tweets posted between the start_date and end_date.
Output a list of dictionaries that include positive_dict, negative_dict and neutral_dict. These three
dictionaries include the counts of positive, negative and neutral tweets on each day.

10. Draw pie charts and line charts using matplotlib.