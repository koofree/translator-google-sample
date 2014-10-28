var front_url = 'http://translate.google.com/translate_a/t?client=p&sl=auto&tl=ko&hl=en&sc=2&ie=UTF-8&oe=UTF-8&uptl=ko&ssel=0&tsel=0&q=';
front_url = 'http://translate.google.com/translate_a/t?client=p&sl=en&tl=ko&hl=en&sc=2&ie=UTF-8&oe=UTF-8&pc=1&oc=1&otf=1&ssel=0&tsel=0&q=';
front_url = 'https://translate.google.com/translate_a/t?client=t&sl=en&tl=ko&hl=en&sc=2&ie=UTF-8&oe=UTF-8&prev=btn&rom=1&ssel=0&tsel=0&q=';
var resource_file = 'writeVocabularyNameKey.txt';
var word_count = 1;

var divide_words = function (words, count) {
    var lines_modified = [];
    var temp_str = '';

    for (n in words) {
        temp_str += words[n] + ', ';
        if (n % count == 0) {
            temp_str = temp_str.substr(0, temp_str.length - 2);
            lines_modified.push(temp_str);
            temp_str = '';
        }
    }
    if (temp_str != '') {
        lines_modified.push(temp_str);
        temp_str = '';
    }
    return lines_modified;
};

var readFile = function (filename, callback) {
    $.get(filename, function (data) {
        var lines = data.split('\n');

        $.each(lines, function (num, line) {
            if (line != '') {
                setTimeout(function () {
                    callback(line);
                }, 200 * num);
            }
        });
    });
};

var translate = function (word) {
    var replaced_word = word.replace(/\_/g, ' ');
    $.ajax({
        url: front_url + replaced_word,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            console.log(data);
            var result = data.split('\"')[1];
            if (result.indexOf('-//W3C//DTD') > -1) {
                translate(replaced_word);
            } else {
                $('body').append($('<div>').html(word + ': ' + result));
            }
        },
        error: function (err, obj) {
            console.log(err.responseText);
            var result = err.responseText.split('\"')[1];
            if (result.indexOf('-//W3C//DTD') > -1) {
                translate(replaced_word);
            } else {
                $('body').append($('<div>').html(word + ': ' + result));
            }
        }
    });
};

readFile(resource_file, translate);