import logging
import random
import sys
import time

from ruamel.yaml import YAML

from parse_jisho_page import parse_jisho_page
from parse_wiki_table import parse_wiki_table

logging.basicConfig(level=logging.INFO)


def main():
    kanji_set = parse_wiki_table()

    yaml = YAML()

    stream = open('/home/markdr/Desktop/KanjiStuff/kanji.yaml', 'a+')
    yaml.explicit_start = True

    kanji_set = iter(kanji_set)

    for kanji in kanji_set:

        if kanji.character == '栄':
            break

    for kanji in kanji_set:

        if kanji.character == '宙':
            break

        jisho_kanji = parse_jisho_page(kanji.character)
        kanji.parts = jisho_kanji.parts
        kanji.dependencies = jisho_kanji.dependencies
        if kanji.radical != jisho_kanji.radical:
            logging.warning('Radical for %s: Wiki: %s, Jisho: %s' % (
                kanji.character, kanji.radical, jisho_kanji.radical
            ))

        yaml.dump(kanji.as_serializable(), stream=stream)
        time.sleep(random.random() * 3)
        # dumper.emit(kanji)
    # dumper.emit(yaml.DocumentEndEvent())
    # dumper.emit(yaml.StreamEndEvent())


if __name__ == '__main__':
    main()