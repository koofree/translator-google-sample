__author__ = 'koo'

import urllib2
import codecs
import time
import os
import socket
from bs4 import BeautifulSoup

open_file_name = 'translate_line3.txt'
open_file = open(open_file_name)

write_file = codecs.open(open_file_name[:open_file_name.index('.')] + '_dictionary.txt', 'w', "utf8")

total_count = 0
translated_count = 0
constant_count = 0

dictionary = {}
duplicated_count = 0


def isProperNoun(word):
    return word.isupper() or '.com' in word


def isAlphabet(word):
    return all(ord(c) < 128 for c in word)


def adjust(word):
    return word.split('(')[0].replace(" ", "").replace(",", "")


for line in open_file:
    split_line = line.split(':')
    translated_word = split_line[1].strip()
    if dictionary.has_key(translated_word):
        duplicated_count += 1
        dictionary[translated_word] += 1
    else:
        dictionary[translated_word] = 1

    if isProperNoun(translated_word):
        constant_count += 1
        translated_count += 1
    elif not isAlphabet(translated_word):
        translated_count += 1

    total_count += 1

print translated_count, '(', constant_count, duplicated_count, ')', '/', total_count, str(
    (float(translated_count) / float(total_count) * 100))

for word in dictionary.keys():
    if not isAlphabet(word):
        write_file.write(adjust(word).strip().decode('utf8') + ',100000000X' + '\n')