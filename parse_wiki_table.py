import html
import logging
import re


from kanji import JouyouKanji


def readline(file):
    val = file.readline()
    logging.debug(val)
    return val


def html_unescape(html_string):
    return None if html_string is None else html.unescape(html_string)


def parse_wiki_table():
    f = open('./wiki_page.html', encoding='utf-8')
    line = ''

    while line != '<td>1</td>\n':
        line = readline(f)

    kanji = list()

    while re.match('<td>\d+</td>', line):
        character = html_unescape(
            re.match('<td.*?>.*?<a.*?>(.*?)</a>.*</td>', readline(f)).group(1))
        kyujitai = html_unescape(
            re.match('<td.*?>(?:.*?<a.*?>(.*?)</a>.*)?</td>', readline(f)).group(1))
        radical = re.match('<td.*><a.*>(.)</a></td>', readline(f)).group(1)
        strokes = int(re.match('<td>(\d+)</td>', readline(f)).group(1))
        grade = re.match('<td>(.)</td>', readline(f)).group(1)
        year_added = re.match('<td>(\d*?)</td>', readline(f)).group(1)

        # English meaning: skipped because more extensive lists have this data.
        readline(f)

        # Readings: skipped because more extensive lists have this data.
        readline(f)

        kanji.append(
            JouyouKanji(character, radical, kyujitai, year_added, strokes, grade)
        )

        # Empty cell?
        readline(f)
        # TR
        readline(f)
        # Read an additional line into `line` so the while loop will eventually
        # break.
        line = readline(f)

    return kanji


if __name__ == '__main__':
    parse_wiki_table()
