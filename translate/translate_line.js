$(function () {
    var resource_file = 'output.txt';
    var before_file = 'translate_line3.txt';
    var $progressbar = $("#progressbar");
    var $result = $('.result');
    var number = 0;

    var front_url = 'http://translate.google.com/translate_a/t?client=t&sl=auto&tl=ko&hl=en&sc=2&ie=UTF-8&oe=UTF-8&uptl=ko&ssel=0&tsel=0&q=';
    front_url = 'http://translate.google.com/translate_a/t?client=t&sl=en&tl=ko&hl=en&sc=2&ie=UTF-8&oe=UTF-8&pc=1&oc=1&otf=1&ssel=0&tsel=0&q=';
    front_url = 'https://translate.google.com/translate_a/t?client=t&sl=auto&tl=ko&hl=en&sc=2&ie=UTF-8&oe=UTF-8&prev=btn&rom=1&ssel=0&tsel=0&q=';

    var library = {};

    var readFile = function (filename, before_file, callback) {
        if (before_file) {
            $.get(before_file, function (data) {
                var lines = data.split('\n');

                for (var i = 0; i < lines.length; i++) {
                    var line = lines[i];
                    var split_line = line.split(': ');
                    library[split_line[0]] = split_line[1];
                }

                startFile(filename, callback);
            });
        } else {
            startFile(filename, callback);
        }
    };

    var startFile = function (filename, callback) {
        $.get(filename, function (data) {
            var lines = data.split('\n');
            var total = lines.length;

            $.each(lines, function (num, line) {
                if (line) {
                    var split_line = line.split(' ## ');
                    var word = split_line[0];
                    var replaced_word = word.replace(/\_/g, ' ');
                    var line = split_line[1];
                    var replaced_line = line.replace(/\_/g, ' ');
                    var status = {num: num, total: total};
                    if (library.hasOwnProperty(replaced_word)) {
                        callback(word + ': ' + library[word], status);
                    } else {
                        var start_count = num;
                        setTimeout(function () {
                            translate(replaced_word, replaced_line, function (result) {
                                callback(result, status);
                            });
                        }, 200 * start_count);
                    }
                }
            });
        });
    };

    var translate = function (word, line, callback) {
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
                    var origin = res[5];
                    var target = res[4];
                    if (origin) {
                        var result = '';
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
                            result = target[index][0].trim();
                        }
                        if (result.length < 1) {
                            callback(word + ': ' + word);
                        } else {
                            callback(word + ': ' + result);
                        }
                    } else {
                        callback(word + ': ' + word);
                    }
                }
            },
            error: function (err, obj) {
                if (err.responseText.indexOf('-//W3C//DTD') > -1 ||
                    err.responseText.indexOf('content-type') > -1) {
                    translate(word, line);
                } else {
                    var res = eval(err.responseText);
                    var origin = res[5];
                    var target = res[4];
                    if (origin && target) {
                        var result = '';
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
                            result = target[index][0].trim();
                        }
                        if (result.length < 1) {
                            callback(word + ': ' + word);
                        } else {
                            callback(word + ': ' + result);
                        }
                    } else {
                        callback(word + ': ' + word);
                    }
                }
            }
        });
    };

    readFile(resource_file, before_file, function (result, status) {
        var progress = Math.round(status.num / status.total * 100);
        if (progress > number) {
            $progressbar.progressbar({
                value: progress
            });
            number = progress;
        }
        $result.append(result + '\n');
    });
});