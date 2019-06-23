import re
import sys
from urllib import request

import kanji


def parse_jisho_page(character):
    print('Parsing %s' % character, file=sys.stderr)
    url = 'http://www.jisho.org/search/{}%23kanji'.format(
        request.quote(character))
    page_lines = map(lambda line: line.decode('utf-8', errors='replace'),
                     (request.urlopen(url)))

    radical = ''
    parts = []

    breakout = False
    for line in page_lines:
        if '<div class="radicals">' in line:
            if not radical:
                for line in page_lines:
                    match = re.match('^\s*?([^<\s[A-z]).*$', line)
                    if match:
                        radical = match.group(1)
                        break
            else:
                for line in page_lines:
                    match = (re.match('^\s*?([^<\s])$', line) or
                             re.match('^\s*?<a.*>(.)</a>$', line))
                    if match:
                        parts.append(match.group(1))
                    if '</dl>' in line:
                        breakout = True
                        break
        if breakout:
            break

    return kanji.Kanji(character, radical, parts)


if __name__ == '__main__':
    val = parse_jisho_page('机')
    print(val)
