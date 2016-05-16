__author__ = 'Richard'

import json
import sys
import matplotlib.pyplot as plt
import datetime
import time
import complete_project_1_util as util
import csv
import numpy as np


def read_stocktwits():

    f = open('BAC.json','r')
    json_txt = f.read()
    decoded = util.byteify(json.loads(json_txt))
    decoded_list = []
    for item in decoded:
        lis = []
        lis.append(str(int(item["created_at"]["$date"])/1000))
        lis.append(str(item["body"]))
        lis.append(item["entities"]["sentiment"])
        decoded_list.append(lis)

    length = len(decoded_list)
    count = 0
    values_list = []
    while count < length:
        items_list = []
        items_list.append(util.time_conversion(decoded_list[count][0]))
        items_list.append(util.to_lower(util.remove_puncuation(decoded_list[count][1])))
        items_list.append(util.sentiment(decoded_list[count][2]))
        values_list.append(items_list)
        count += 1

    util.csv_writer(values_list, 'ProjectBAC.csv')

    return

def sentiment_analysis():

    bac_list = util.csv_reader('ProjectBAC.csv')
    length = len(bac_list)

    p_lines_list = util.pos_or_neg_word_list(r'positive_words.txt')
    n_lines_list = util.pos_or_neg_word_list(r'negative_words.txt')

    positive_word_list = []
    negative_word_list = []
    for line in p_lines_list:
        positive_word_list.append(line.strip("\n"))
    for line in n_lines_list:
        negative_word_list.append((line.strip("\n")).strip('\r'))

    count = 0
    count_list = []
    while count < length:
        words = bac_list[count][1]
        splitted = str(words).split()

        pos_count = 0
        neg_count = 0
        words_list = []
        if bac_list[count][2] == 'Unknown':
            for value in splitted:
                if value in positive_word_list:
                    pos_count += 1
                elif value in negative_word_list:
                    neg_count += 1
            count += 1
            words_list.append(pos_count)
            words_list.append(neg_count)
            if pos_count > neg_count:
                count_list.append('Bullish')
            elif pos_count < neg_count:
                count_list.append('Bearish')
            elif pos_count == neg_count:
                count_list.append('Neutral')
        else:
            count_list.append(bac_list[count][2])
            count += 1

    list_count = 0
    final_sentiment_list = []
    while list_count < length:
        sentiment_list = []
        sentiment_list.append(bac_list[list_count][0])
        sentiment_list.append(count_list[list_count])
        final_sentiment_list.append(sentiment_list)
        list_count += 1

    util.csv_writer(final_sentiment_list, 'ProjectBAC2.csv')
    return

def get_sentiment_dates(start_date, end_date):

    BAC2_list = util.csv_reader('ProjectBAC2.csv')
    length = len(BAC2_list)

    new_BAC2_list = []
    count = 0
    while count < length:
        temp_list = []
        the_time = util.time_conversion_to_y_m_d_format(BAC2_list[count][0])
        temp_list.append(the_time)
        temp_list.append(BAC2_list[count][1])
        new_BAC2_list.append(temp_list)
        count += 1

    pos_count = 0
    neg_count = 0
    neutral_count = 0
    pos_list = []
    neg_list = []
    neutral_list = []
    for list in new_BAC2_list:
        if list[0] >= start_date and list[0] <= end_date:
            if list[1] == 'Bullish':
                pos_list.append(list)
                pos_count += 1
            elif list[1] == 'Bearish':
                neg_list.append(list)
                neg_count += 1
            elif list[1] == 'Neutral':
                neutral_list.append(list)
                neutral_count += 1

    pos_list = util.time_convert_datetime_date(pos_list)
    neg_list = util.time_convert_datetime_date(neg_list)
    neutral_list = util.time_convert_datetime_date(neutral_list)

    start_date = datetime.date(*time.strptime(start_date, "%Y-%m-%d")[0:3])
    end_date = datetime.date(*time.strptime(end_date, "%Y-%m-%d")[0:3])

    positive_dict = util.sentiment_dictionary(start_date, end_date, pos_list)
    negative_dict = util.sentiment_dictionary(start_date, end_date, neg_list)
    neutral_dict = util.sentiment_dictionary(start_date, end_date, neutral_list)

    return [positive_dict,negative_dict,neutral_dict]

def drawing_pie(start_date, end_date):
    sentiment_dictionary = get_sentiment_dates(start_date, end_date)

    sentiment_array = util.total_sentiment_array(sentiment_dictionary)

    positive_count = sentiment_array[0]
    negative_count = sentiment_array[1]
    neutral_count = sentiment_array[2]

    sentiment = ''
    if positive_count > negative_count or positive_count > neutral_count:
        sentiment = 'Sentiment is Positive'
    elif negative_count > positive_count or negative_count > neutral_count:
        sentiment = 'Sentiment is Negative'
    elif neutral_count > positive_count or neutral_count > negative_count:
        sentiment = 'Sentiment is Neutral'
    elif positive_count == neutral_count and positive_count > negative_count:
        sentiment = 'Sentiment is Positive'
    elif negative_count == neutral_count and negative_count > positive_count:
        sentiment = 'Sentiment is Negative'

    labels = ['Positive', 'Negative', 'Neutral']
    colors = ['blue', 'green', 'red']
    explode = (0, 0, 0)

    plt.pie(sentiment_array, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)

    plt.axis('equal')

    plt.title(sentiment)

    plt.show()

    return

def drawing_lines(start_date, end_date):

    sentiment_dictionary = get_sentiment_dates(start_date, end_date)
    positive = sentiment_dictionary[0]
    negative = sentiment_dictionary[1]
    neutral =  sentiment_dictionary[2]
    sorted_sentiment_dictionary_keys = sorted(sentiment_dictionary[0].keys())

    count = 0
    sorted_dictionary_list = []
    for value in sorted_sentiment_dictionary_keys:
        datetime_values_list = []
        sentiment_values = []
        datetime_values_list.append(value)
        sentiment_values.append(sentiment_dictionary[0][sorted_sentiment_dictionary_keys[count]])
        sentiment_values.append(sentiment_dictionary[1][sorted_sentiment_dictionary_keys[count]])
        sentiment_values.append(sentiment_dictionary[2][sorted_sentiment_dictionary_keys[count]])
        datetime_values_list.append(sentiment_values)
        sorted_dictionary_list.append(datetime_values_list)
        count += 1

    positive_list = []
    negative_list = []
    neutral_list = []
    for lis in sorted_dictionary_list:
        positive_list.append(lis[1][0])
        negative_list.append(lis[1][1])
        neutral_list.append(lis[1][2])

    fig, ax = plt.subplots()

    plt.plot(sorted(positive.keys()), positive_list, 's-', linestyle='-', color='blue', label='positive')
    plt.plot(sorted(negative.keys()), negative_list, 's-', linestyle='-', color='green', label='negative')
    plt.plot(sorted(neutral.keys()), neutral_list, 's-', linestyle='-', color='red', label='neutral')

    plt.legend()
    fig.autofmt_xdate()
    plt.title('Sentiment between ' + start_date + ' and ' + end_date)
    plt.show()

    return

def main():
    read_stocktwits()# output: BAC.csv
    sentiment_analysis() # output BAC2.csv
    #get_sentiment_dates('2013-01-02', '2013-01-31')
    drawing_pie('2013-01-02', '2013-01-31') #output: pie_sentiment.png
    drawing_lines('2013-01-02', '2013-01-31') # output: lines_sentiment.png
    return

if __name__ == '__main__':
    main()
