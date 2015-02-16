import codecs

open_file_name = 'test.txt'
open_file = open(open_file_name)

result = str()
count = 1
for line in open_file:
    result = result + ' ' + line.split('<')[0]
    if count < 10:
        count += 1
    else:
        result += '\n'
        count = 1

write_file = codecs.open(open_file_name[:open_file_name.index('.')] + '_fixed.txt', 'w', "utf8")
write_file.write(result.decode('utf-8'))
write_file.close()