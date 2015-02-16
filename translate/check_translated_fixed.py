__author__ = 'koo'

import codecs

open_file_name = 'writeVocabularyName_notMorpheme_naver.txt'
write_file = codecs.open(open_file_name[:open_file_name.index('.')] + '_checked.txt', 'w', "utf8")
open_file = open(open_file_name)
dictionary_file_name = 'na_korean_dictionary.txt'
korean_dictionary = {}

total_count = 0
translated_count = 0
constant_count = 0

dictionary_file = open(dictionary_file_name)

for line in dictionary_file:
    split_line = line.split(': ')
    lower = split_line[0].lower()
    korean_dictionary[lower] = split_line[1].strip()


def isProperNoun(word):
    return word.isupper() or "." in word or word.isdigit()


def isAlphabet(word):
    return all(ord(c) < 128 for c in word)


def write(write_file, word1, word2):
    write_file.write(word1.strip().decode('utf8') + ': ' + word2.strip().decode('utf8') + '\n')


index = 0
for line in open_file:
    split_line = line.split(':')
    original_word = split_line[0].strip()
    translated_word = split_line[1].strip().split('.')[0]
    if isProperNoun(original_word):
        constant_count += 1
        # translated_count += 1
        # index += 1
        # print index, split_line[0], ':', translated_word
        # write(write_file, split_line[0], split_line[0])
    elif korean_dictionary.has_key(original_word.lower()):
        print 'dictionary', original_word
    elif not isAlphabet(translated_word):
        translated_count += 1
        index += 1
        print index, split_line[0], ':', translated_word
        write(write_file, split_line[0], translated_word)

    total_count += 1

print translated_count, '(', constant_count, ')', '/', total_count, str(
    (float(translated_count) / float(total_count) * 100))

write_file.close()
