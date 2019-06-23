import json


class Kanji(object):

    def __init__(self, character='', radical='', parts=None):
        self.character = character
        self.radical = radical

        # The full list of primitives used to build the character.
        # Duplicates are kept.
        self.parts = parts or []

        # Different from parts as it may contain groups/kanji.
        self.dependencies = []

        # Useful for searching in English.
        self.keyword = ''

    def __str__(self):
        return json.dumps(
            self.as_serializable(),
            indent=4
        )

    def as_serializable(self):
        return {
            'character': self.character,
            'radical': self.radical,
            'parts': self.parts,
            'dependencies': self.dependencies,
            'keyword': self.keyword,
        }


class JouyouKanji(Kanji):

    def __init__(self,
                 character='',
                 radical='',
                 kyujitai=None,
                 year_added='',
                 strokes=0,
                 grade=''):
        super().__init__(character=character, radical=radical, parts=None)

        self.character = character

        # An old alternate form of the character.
        self.kyujitai = kyujitai

        # When no year is specified, 1946 or earlier should be assumed.
        # https://en.wikipedia.org/wiki/J%C5%8Dy%C5%8D_kanji#History
        self.year_added = year_added

        self.radical = radical
        self.strokes = strokes
        self.grade = grade

    def as_serializable(self):
        data = super().as_serializable()
        data.update({
            'kyujitai': self.kyujitai,
            'strokes': self.strokes,
            'jouyou': {
                'grade': self.grade,
                'year_added': self.year_added
            }
        })
        return data