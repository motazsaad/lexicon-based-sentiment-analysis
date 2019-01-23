#!/usr/bin/python
# -*- coding: utf-8 -*-
import xlsxwriter
import tweet_cleaner
import json
import argparse

parser = argparse.ArgumentParser(description='extract tweet from json and write them into xls file')
parser.add_argument('-f', '--filteringfile', type=argparse.FileType(mode='r', encoding='utf-8'),
                    help='lexicon for filtering spam tweets. Only one term should be per line',
                    required=True)
parser.add_argument('-i', '--json-file', type=argparse.FileType(mode='r', encoding='utf-8'), help='input json file.', required=True)
parser.add_argument('-o', '--out-file', type=str, help='the output file.', required=True)


def process_json(filters, json_file, xls_file):
    import preprocessor
    workbook = xlsxwriter.Workbook(xls_file)
    worksheet = workbook.add_worksheet()

    # Start from the first cell. Rows and columns are zero indexed.

    row = 0
    col = 0
    worksheet.write(row, 0, 'id')
    worksheet.write(row, 1, 'created_at')
    worksheet.write(row, 2, 'text')
    worksheet.write(row, 3, 'clean_text')
    row += 1

    lines = json_file.readlines()
    for line in lines:
        json_tweet = json.loads(line)
        if 'retweeted_status' in json_tweet:
            text = json_tweet['retweeted_status']['text']
        else:
            text = json_tweet['text']
        clean_text = tweet_cleaner.clean_tweet(text)
        clean_text = tweet_cleaner.normalize_arabic(clean_text)
        clean_text = tweet_cleaner.remove_repeating_char(clean_text)
        clean_text = tweet_cleaner.keep_only_arabic(clean_text.split())
        is_filtered = filter_tweet(filters, clean_text)
        if not is_filtered:  # print only if text is not filtered
            worksheet.write(row, col, json_tweet['id_str'])
            worksheet.write(row, col + 1, json_tweet['created_at'])
            worksheet.write(row, col + 2, text)
            worksheet.write(row, col + 3, clean_text)
            row += 1
    workbook.close()


def filter_tweet(filters, clean_text):
        for filter2 in filters:
            filter2 = filter2.strip()
            if filter2 in clean_text:
                return True
        return False


if __name__ == '__main__':
    args = parser.parse_args()
    filters = args.filteringfile.read().splitlines()
    json_file = args.json_file
    xls_file = args.out_file
    process_json(filters, json_file, xls_file)