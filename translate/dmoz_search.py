# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'koo'

import urllib2
import codecs
import time
import os
import socket
from bs4 import BeautifulSoup

url = 'http://www.dmoz.org/search?all=no'
CATEGORY_PARAM_NAME = '&cat='
QUERY_PARAM_NAME = '&q='
open_file_name = 'term_cate2_source.txt'
sleep_time = 20


def search(query, category):
    result = str()
    sum_url = url + CATEGORY_PARAM_NAME + category + QUERY_PARAM_NAME + query
    while True:
        try:
            soup = BeautifulSoup(
                urllib2.urlopen(sum_url).read())
            break
        except urllib2.HTTPError, e:
            print 'sleep waiting..', sleep_time
            time.sleep(sleep_time)
            continue
        except urllib2.URLError, e:
            print 'sleep waiting..', sleep_time
            time.sleep(sleep_time)
            continue
        except socket.error, e:
            print 'sleep waiting..', sleep_time
            time.sleep(sleep_time)
            continue

    isFirst = True
    site_ol = soup.find('ol', 'site')
    if site_ol:
        a = site_ol.find('li')
        a.find('div', 'ref').clear()
        result = a.get_text().strip()

    try:
        decoded_result = result.encode('utf8')
        return decoded_result
    except UnicodeEncodeError:
        return result


open_file = open(open_file_name)
write_file = codecs.open(open_file_name[:open_file_name.index('.')] + '_dmoz.txt', 'w', "utf8")
whole_time = 0
progress = 1

whole_count = 0
for line in open_file:
    whole_count += 1

open_file.close()
open_file = open(open_file_name)

for line in open_file:
    split_line = line.split(' ')
    word = split_line[0]
    categories = map(str.strip, split_line[1:])

    start_time = time.time()

    search_result = str()
    for category in categories:
        site_text = search(word, category)
        if word in site_text.lower():
            search_result = site_text
            break

    write_file.write(word.decode('utf8') + ' ## ' + search_result.decode('utf8') + '\n')

    finish_time = time.time()

    during_time = finish_time - start_time
    whole_time += during_time
    rest_time = (whole_time / progress) * (whole_count - progress)
    if rest_time < 60:
        cal_time = str(round(rest_time)).split('.')[0] + 's'
    else:
        cal_time = str(round(rest_time / 60)).split('.')[0] + 'm'

    # cls()
    print progress, '/', whole_count, '( rest time : ', cal_time, ')'

    progress += 1

write_file.close()