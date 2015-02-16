__author__ = 'koo'

import urllib
import urllib2
import httplib
import codecs
import time
import os
import socket
from bs4 import BeautifulSoup

sleep_time = 20

write_file = codecs.open('na_korean_dictionary.txt', 'w', "utf8")

headers = {"Content-type": "application/x-www-form-urlencoded",
           "Accept": "text/html,application/xhtml+xml,application/xml"}


def cleaning(word):
    return word.replace(",", "").replace("(", "").replace(")", "").replace("*", "")


h = httplib.HTTPConnection('www.korean.go.kr:80')

for page in range(1, 5757):
    data = urllib.urlencode({'go': page, 'searchDiv': '0'})

    while True:
        try:
            h.request('POST', '/09_new/dic/rule/rule_foreign.jsp', data, headers)
            r = h.getresponse()
            soup = BeautifulSoup(r.read())
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
        except httplib.CannotSendRequest, e:
            print '[cannot send request] sleep waiting..', sleep_time
            time.sleep(sleep_time)
            h = httplib.HTTPConnection('www.korean.go.kr:80')
            continue

    tds = soup.find('table', 'list').find('tbody').find_all('td')

    for idx in range(0, len(tds), 3):
        print tds[idx].text
        values = tds[idx + 2].text.strip().split()
        keys = tds[idx + 1].find('a').text.strip().split()
        for _idx in range(0, len(values)):
            if len(keys) > _idx:
                write_file.write(cleaning(keys[_idx]) + ': ' + cleaning(values[_idx]) + '\n')

write_file.close()