var front_url = 'http://translate.google.com/translate_a/t?client=t&sl=auto&tl=ko&hl=en&sc=2&ie=UTF-8&oe=UTF-8&uptl=ko&ssel=0&tsel=0&q=';
front_url = 'http://translate.google.com/translate_a/t?client=t&sl=en&tl=ko&hl=en&sc=2&ie=UTF-8&oe=UTF-8&pc=1&oc=1&otf=1&ssel=0&tsel=0&q=';
front_url = 'https://translate.google.com/translate_a/t?client=t&sl=auto&tl=ko&hl=en&sc=2&ie=UTF-8&oe=UTF-8&prev=btn&rom=1&ssel=0&tsel=0&q=';
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
                var split_line = line.split(' ## ');
                var word = split_line[0];
                var replaced_word = word.replace(/\_/g, ' ');
                var line = split_line[1];
                var replaced_line = line.replace(/\_/g, ' ');
                setTimeout(function () {
                    callback(replaced_word, replaced_line);
                }, 200 * num);
            }
        });
    });
};

var translate = function (word, line) {
    if (line.length < 1) {
        line = word;
    }
    $.ajax({
        url: front_url + line,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            if (data.indexOf('-//W3C//DTD') > -1 ||
                data.indexOf('content-type') > -1) {
                translate(word, line);
            } else {
                var res = eval(data);
                var result = '';
                var origin = res[5];
                var index = -1;
                for (var i = 0; i < origin.length; i++) {
                    var origin_lower = origin[i][0].toLowerCase();
                    var word_lower = word.toLowerCase();
                    if (origin_lower.indexOf(word_lower) > -1 ||
                        word_lower.indexOf(origin_lower) > -1) {
                        index = i;
                        break;
                    }
                }
                if (index > -1) {
                    result = res[4][index][0].trim();
                }
                if (result.length < 1) {
                    $('body').append($('<div>').html(word + ': ' + word));
                } else {
                    $('body').append($('<div>').html(word + ': ' + result));
                }
            }
        },
        error: function (err, obj) {
            if (err.responseText.indexOf('-//W3C//DTD') > -1 ||
                err.responseText.indexOf('content-type') > -1) {
                translate(word, line);
            } else {
                var res = eval(err.responseText);
                var result = '';
                var origin = res[5];
                var index = -1;
                for (var i = 0; i < origin.length; i++) {
                    var origin_lower = origin[i][0].toLowerCase();
                    var word_lower = word.toLowerCase();
                    if (origin_lower.indexOf(word_lower) > -1 ||
                        word_lower.indexOf(origin_lower) > -1) {
                        index = i;
                        break;
                    }
                }
                if (index > -1) {
                    result = res[4][index][0].trim();
                }
                if (result.length < 1) {
                    $('body').append($('<div>').html(word + ': ' + word));
                } else {
                    $('body').append($('<div>').html(word + ': ' + result));
                }
            }
        }
    });
};