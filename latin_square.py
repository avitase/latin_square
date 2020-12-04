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


def get_color(c):
    return [
        (214, 39, 40),  # red
        (255, 127, 14),  # orange
        (31, 119, 180),  # blue
        (148, 103, 189),  # purple
        (44, 160, 44),  # green
        (140, 86, 75),  # brown
        (188, 189, 34),  # yellow
        (23, 190, 207),  # cyan
        (227, 119, 194),  # pink
        # (127, 127, 127),  # grey
        (255, 255, 0),  # grey
    ][c]


def fill(img, *, row, col, scale, margin, color):
    rs = scale
    cs = scale * 3
    for i in range(rs * row + margin, rs * row + rs - margin):
        for j in range(cs * col + 3 * margin, cs * col + cs - 3 * margin, 3):
            img[i, (j, j + 1, j + 2)] = color


def main(file_name, pedantic):
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
            c1 = get_color(c // 10)
            c2 = get_color(c % 10)

            # fill(img, row=i, col=j, scale=scale, margin=int(scale * .1), color=c1)
            # fill(img, row=i, col=j, scale=scale, margin=int(scale * .3), color=c2)
            fill(img, row=i, col=j, scale=scale, margin=0, color=c1)
            fill(img, row=i, col=j, scale=scale, margin=int(scale * .2), color=c2)

    f = open('latin_square.png', 'wb')
    w = png.Writer(img.shape[0], img.shape[1] // 3, greyscale=False)
    w.write(f, img.tolist())
    f.close()


if __name__ == '__main__':
    main('latin_square_10x10_wrong.txt', pedantic=False)
