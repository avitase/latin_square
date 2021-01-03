import warnings

import numpy as np
import png


def check(assumption, msg, pedantic):
    if pedantic:
        assert assumption, msg
    elif not assumption:
        warnings.warn(msg)


def all_colors():
    return 'robwgtynpd'


def get_color(c, *, scheme):
    schemes = [[
        (84,48,5),
        (140,81,10),
        (191,129,45),
        (223,194,125),
        (246,232,195),
        (199,234,229),
        (128,205,193),
        (53,151,143),
        (1,102,94),
        (0,60,48),
    ], [
        (142,1,82),
        (197,27,125),
        (222,119,174),
        (241,182,218),
        (253,224,239),
        (230,245,208),
        (184,225,134),
        (127,188,65),
        (77,146,33),
        (39,100,25),
    ], [
        (64,0,75),
        (118,42,131),
        (153,112,171),
        (194,165,207),
        (231,212,232),
        (217,240,211),
        (166,219,160),
        (90,174,97),
        (27,120,55),
        (0,68,27),
    ], [
        (127,59,8),
        (179,88,6),
        (224,130,20),
        (253,184,99),
        (254,224,182),
        (216,218,235),
        (178,171,210),
        (128,115,172),
        (84,39,136),
        (45,0,75),
    ], [
        (103,0,31),
        (178,24,43),
        (214,96,77),
        (244,165,130),
        (253,219,199),
        (209,229,240),
        (146,197,222),
        (67,147,195),
        (33,102,172),
        (5,48,97),
    ], [
        (165,0,38),
        (215,48,39),
        (244,109,67),
        (253,174,97),
        (254,224,144),
        (224,243,248),
        (171,217,233),
        (116,173,209),
        (69,117,180),
        (49,54,149),
    ]]

    assert scheme >= 0 and scheme < len(schemes)
    
    return schemes[scheme][c]


def fill(img, *, row, col, scale, margin, color):
    rs = scale
    cs = scale * 3
    for i in range(rs * row + margin, rs * row + rs - margin):
        for j in range(cs * col + 3 * margin, cs * col + cs - 3 * margin, 3):
            img[i, (j, j + 1, j + 2)] = color


def main(file_name, pedantic, style, color_scheme):
    n_colors = len(all_colors())
    latin_square = np.empty((n_colors, n_colors), dtype=np.int)

    cidx = dict()
    for i1, c1 in enumerate(all_colors()):
        for i2, c2 in enumerate(all_colors()):
            cidx[c1 + c2] = i1 * n_colors + i2

    with open(file_name, 'r') as f:
        rows = [line.strip().split() for line in f.readlines()]
        for i, row in enumerate(rows):
            latin_square[i] = np.array([cidx[xy] for xy in row])

    for i in np.arange(0, n_colors * n_colors):
        assert i in latin_square, f'{i}'

    for i in np.arange(0, n_colors):
        for j in np.arange(0, n_colors):
            check(i in latin_square[j] // 10, f'ec 1: row={j + 1}', pedantic)
            check(i in latin_square[j] % n_colors, f'ec 2: row={j + 1}', pedantic)
            check(i in latin_square[:, j] // 10, f'ec 3: col={j + 1}', pedantic)
            check(i in latin_square[:, j] % n_colors, f'ec 4: col={j + 1}', pedantic)

    scale = 200
    img = np.ones((scale * n_colors, scale * 3 * n_colors), dtype=np.uint8) * 255
    for i in range(n_colors):
        for j in range(n_colors):
            c = latin_square[i, j]
            c1 = get_color(c // 10, scheme=color_scheme)
            c2 = get_color(c % 10, scheme=color_scheme)

            fill(img, row=i, col=j, scale=scale, margin=0, color=c1)
            if style == 'tidy':
                fill(img, row=i, col=j, scale=scale, margin=int(scale * .3), color=c2)
            else:
                fill(img, row=i, col=j, scale=scale, margin=int(scale * .2), color=c2)

    f = open(f'latin_square_{style}_{color_scheme + 1}.png', 'wb')
    w = png.Writer(img.shape[0], img.shape[1] // 3, greyscale=False)
    w.write(f, img.tolist())
    f.close()


if __name__ == '__main__':
    for style in ['tidy', 'dirty']:
        for scheme in range(6):
            main('latin_square_10x10_wrong.txt', pedantic=False, style=style, color_scheme=scheme)
