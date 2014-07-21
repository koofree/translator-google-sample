# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'koo'

import urllib2
import codecs
import time
import os
import socket
from bs4 import BeautifulSoup


def cls():
    os.system(['clear', 'cls'][os.name == 'nt'])


url = 'http://endic.naver.com/search.nhn?sLn=en&searchOption=entry_idiom&query='
open_file_name = 'finalTranslatorVocabulary.txt'
sleep_time = 20
translate_all = True


def isProperNoun(word):
    return word.isupper() or '.com' in word


def isAlphabet(word):
    return all(ord(c) < 128 for c in word)


def search(query):
    result = str()
    while True:
        try:
            soup = BeautifulSoup(urllib2.urlopen(url + query).read())
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
    for span in soup.find_all('span', 'fnt_k05'):
        isNoun = False
        if '명사'.decode('utf8') in span.parent.text:
            isNoun = True

        if isNoun:
            result = span.text
            break
        elif isFirst:
            result = span.text
            isFirst = False

    return result


def err():
    print err


open_file = open(open_file_name)
write_file = codecs.open(open_file_name[:open_file_name.index('.')] + '_naver.txt', 'w', "utf-8")

progress = 1

whole_count = 0
for line in open_file:
    whole_count += 1

fixed_count = 0

open_file.close()
open_file = open(open_file_name)

whole_time = 0
for line in open_file:
    pass_word = False
    if ':' in line:
        split_line = line.split(':')
        translated_word = split_line[1].strip()
        if isProperNoun(translated_word) or ((not isAlphabet(translated_word)) and (translate_all == False)):
            pass_word = True
        word = split_line[0]
        final_word = split_line[1].strip()
    else:
        word = line.strip()
        final_word = split_line[1].strip()

    start_time = time.time()
    if pass_word == False:
        word_translated = search(word.strip())
        # time.sleep(1)
        if word_translated.strip() == '':
            write_file.write(word.decode('utf8') + ': ' + final_word.decode('utf8') + '\n')
        else:
            split_word = word_translated.split(';')[0].split(':')[0].split(',')[0]
            final_word = ''
            in_bracket_count = 0
            for ch in split_word:
                if ch in '({[':
                    in_bracket_count += 1
                    continue
                if ch in ')}]':
                    in_bracket_count -= 1
                    continue
                if in_bracket_count is 0:
                    final_word += ch

            write_word = final_word.strip()
            if write_word != '' and isProperNoun(write_word):
                write_file.write(word.strip() + ': ' + write_word + '\n')
            else:
                write_file.write(word.strip() + ': ' + final_word + '\n')
            fixed_count += 1
    else:
        write_file.write(word.strip().decode('utf8') + ': ' + final_word.decode('utf8') + '\n')

    finish_time = time.time()

    during_time = finish_time - start_time
    whole_time += during_time
    rest_time = (whole_time / progress) * (whole_count - progress)
    if rest_time < 60:
        cal_time = str(round(rest_time)).split('.')[0] + 's'
    else:
        cal_time = str(round(rest_time / 60)).split('.')[0] + 'm'

    # cls()
    print progress, '(', fixed_count, ')', '/', whole_count, '( rest time : ', cal_time, ')'

    progress += 1

print 'whole time :', str(whole_time / 60), 'm', str(whole_time % 60), 's'
print 'fixed count :', str(fixed_count)
open_file.close()
write_file.close()