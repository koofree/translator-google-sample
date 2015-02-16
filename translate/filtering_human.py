__author__ = 'Koo Lee'

import codecs

open_file_name = 'writeVocabularyName_notMorpheme_naver_checked_human.txt'
write_file = codecs.open(open_file_name[:open_file_name.index('.')] + '_filtered.txt', 'w', "utf8")
open_file = open(open_file_name)


def write(write_file, word1, word2):
    write_file.write(word1.strip().decode('utf8') + ': ' + word2.strip().decode('utf8') + '\n')


for line in open_file:
    number = line[0:1]
    split_line = line[2:].split(': ')
    original_word = split_line[0].strip().replace(' ', '')
    translated_word = split_line[1].strip().replace(' ', '')
    if int(number) is 1:
        print translated_word
        write(write_file, original_word, translated_word)