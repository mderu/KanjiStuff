import json


class BackgroundColors:
    RED     = '\033[41m'
    GREEN   = '\033[42m'
    YELLOW  = '\033[43m'
    BLUE    = '\033[44m'
    MAGENTA = '\033[45m'
    CYAN    = '\033[46m'
    WHITE   = '\033[47m'
    RESET   = '\033[49m'


BACKGROUND_COLORS = [
    BackgroundColors.RED,
    BackgroundColors.GREEN,
    BackgroundColors.YELLOW,
    BackgroundColors.BLUE,
    BackgroundColors.MAGENTA,
    BackgroundColors.CYAN,
    BackgroundColors.WHITE,
]


class Bounds(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0


class Component(object):
    def __init__(self, bounds, character):
        self.bounds = bounds
        self.character = character
        self.component_type = None


def break_square(size, internal_data):
    components = []

    if isinstance(internal_data, str):
        return [Component(size, internal_data)]

    for key, values in internal_data.items():
        if key == 'horizontal':
            for index, value in enumerate(values):
                bounds = Bounds()
                bounds.x = size.x + index * size.width / len(values)
                bounds.y = size.y
                bounds.width = size.width / len(values)
                bounds.height = size.height
                components += break_square(bounds, value)

        if key == 'vertical':
            for index, value in enumerate(values):
                bounds = Bounds()
                bounds.x = size.x
                bounds.y = size.y + index * size.height / len(values)
                bounds.width = size.width
                bounds.height = size.height / len(values)
                components += break_square(bounds, value)

        # Note: this includes overlapping
        if key == 'bound':
            component = Component(size, values[0])
            component.component_type = 'encompass'
            components = [component]
            inner_bounds = Bounds()
            inner_bounds.x = size.x + size.width / 5
            inner_bounds.y = size.y + size.height / 5
            inner_bounds.width = size.width * 3 / 5
            inner_bounds.height = size.height * 3 / 5
            components += break_square(inner_bounds, values[1])

    return components


def visualize(data):
    full_width = '  '
    bounds = Bounds()
    bounds.width = 40
    bounds.height = 40
    components = break_square(bounds, data)

    out_data = [[full_width for _ in range(40)] for _ in range(40)]

    for color_index, component in enumerate(components):
        color_index = color_index % len(BACKGROUND_COLORS)
        bounds = component.bounds
        for y in range(round(bounds.y), round(bounds.y + bounds.height)):
            for x in range(round(bounds.x), round(bounds.x + bounds.width)):
                out_data[y][x] = BACKGROUND_COLORS[color_index] + '  ' + BackgroundColors.RESET

        if component.component_type == 'encompass':
            center_height = round(bounds.y + bounds.height / 10)
        else:
            center_height = round(bounds.y + bounds.height / 2)
        begin_width = round(bounds.x + bounds.width / 2 - len(component.character) / 2)

        for offset, character in enumerate(component.character):
            character = character
            # if offset == 0:
            #     character = ' ' * int(len(component.character) / 2) + character
            # if offset == len(component.character) - 1:
            #     character = character + ' ' * (len(component.character) -
            #                                    int(len(component.character) / 2))
            out_data[center_height][begin_width + offset] = (
                    '\033[30m' +
                    BACKGROUND_COLORS[color_index] +
                    character +
                    BackgroundColors.RESET +
                    '\033[39m'
            )

    for line in out_data:
        out_line = ''
        for char in line:
            out_line += char
        print(out_line)


if __name__ == '__main__':
    char_data = {
        '一'
    }
    visualize(char_data)
    print(json.dumps(char_data))

'人亻 小 水 ⼂⼃⼅⼁⼘ 火灬 巛 巜'
'⼧宀冖𠆢  ⺾艹  ⺌⺍ 亠'
'⺡氵冫  犭  扌 衤'
'夂攵欠又'
'儿'

'工 匕 寸 己 土 也 貝 隹'

'广 ⼚ 勹 冂 ⼏ 几 辶 ⻌ ⻍ 廴 弋 戈 𠂇'
'⿸ ⿸ ⿹ ⿵ ⿵ ⿵ ⿺ ⿺ ⿺ ⿺ ⿹ ⿹ ⿸'

'⿰ ⿱ ⿲ ⿳ ⿴ ⿵ ⿶ ⿷ ⿸ ⿹ ⿺ ⿻'
