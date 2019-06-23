import re
from urllib import request


class Kanji(object):
    def __init__(self, character, heisig_index, keyword):
        self.character = character
        self.heisig_index = heisig_index
        self.keyword = keyword


class ComponentNode(object):
    def __init__(self, keyword, kanji=None, dependencies=None):
        self.keyword = keyword
        self.kanji = kanji
        self.dependencies = dependencies or []


def parse_component_tree():
    URL = 'https://raw.githubusercontent.com/sdcr/heisig-kanjis/master/heisig-kanjis.csv'

    page_lines = map(lambda line: line.decode('utf-8', errors='replace'),
                     (request.urlopen(URL)))
    page_lines = iter(page_lines)

    # Ignore header.
    # kanji,id_5th_ed,id_6th_ed,keyword_5th_ed,keyword_6th_ed,components,on_reading,kun_reading
    next(page_lines)

    nodes = dict()

    for line in page_lines:
        character, _, heisig_index, _, keyword, components = line.split()
        components = re.split(';\s', components)

        kanji = Kanji(character, heisig_index, keyword)

        if keyword not in nodes:
            nodes[keyword] = ComponentNode(keyword, kanji, components)
        else:
            nodes[keyword].kanji = kanji
            nodes[keyword].dependencies = components

        for component in components:
            if component not in nodes:
                nodes[component] = ComponentNode(component)





if __name__ == '__main__':
    parse_component_tree()