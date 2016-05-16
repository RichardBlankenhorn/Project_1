__author__ = 'Richard'

import datetime
import csv
import time

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('ascii', 'ignore')
    else:
        return input

def remove_puncuation(list):
    no_punc_list = []
    for char in str(list):
        if char.isalnum() == True or char == ' ':
            no_punc_list.append(char)
    return ''.join(no_punc_list)

def to_lower(list):
    lower_list = []
    for char in list:
        lower_list.append(char.lower())
    return ''.join(lower_list)

def time_conversion(epoch_seconds):
    time = datetime.datetime.fromtimestamp(float(epoch_seconds)).strftime('%m/%d/%Y %H:%M')
    return time

def time_conversion_to_y_m_d_format(list):
    pattern = '%m/%d/%Y %H:%M'
    epoch = int(time.mktime(time.strptime(list, pattern)))
    the_time = datetime.datetime.fromtimestamp(float(epoch)).strftime('%Y-%m-%d')
    return the_time

def time_convert_datetime_date(list_1):
    list = list_1
    for item in list:
        now = datetime.date(*time.strptime(item[0], "%Y-%m-%d")[0:3])
        item[0] = now
    return list

def sentiment(sentiment):
    if sentiment == None:
        return 'Unknown'
    else:
        return sentiment['basic']

def csv_writer(list, filename):
    result_file = open(filename, "wb")
    wr = csv.writer(result_file, dialect='excel')
    for item in list:
        wr.writerow(item)
    result_file.close()

def csv_reader(filename):
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        target_list = list(reader)

    return target_list

def pos_or_neg_word_list(filename):
    word_file = open(filename, 'r')
    words = word_file.readlines()
    p_or_n_words_list = list(words)
    word_file.close()

    return p_or_n_words_list

def sentiment_dictionary(start_date, end_date, pos_list):
    difference = datetime.timedelta(days=1)
    target_date = start_date
    sentiment_count = 0
    sentiment_dict = {}
    while target_date <= end_date:
        for value in pos_list:
            if value[0] == target_date:
                sentiment_count += 1
        sentiment_dict[target_date] = sentiment_count
        target_date += difference
        sentiment_count = 0
    return sentiment_dict

def total_sentiment_array(sentiment_dictionary):

    total_positive = 0
    total_negative = 0
    total_neutral = 0
    sentiment_array = []
    for v in sentiment_dictionary:
        if v == sentiment_dictionary[0]:
            for value in v.values():
                total_positive += value
            sentiment_array.append(total_positive)
        elif v == sentiment_dictionary[1]:
            for value in v.values():
                total_negative += value
            sentiment_array.append(total_negative)
        elif v == sentiment_dictionary[2]:
            for value in v.values():
                total_neutral += value
            sentiment_array.append(total_neutral)

    return sentiment_array