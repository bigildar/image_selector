import os
import shutil
import numpy as np
from base import init_db
from base import get_index
from base import get_images


def comparison(img1, img2):
    init_db()
    color1 = get_images(img1)
    color2 = get_images(img2)
    c1 = sorted([
        [int(color1[0][1:3], 16), int(color1[0][3:5], 16), int(color1[0][5:7], 16)],
        [int(color1[1][1:3], 16), int(color1[1][3:5], 16), int(color1[1][5:7], 16)],
        [int(color1[2][1:3], 16), int(color1[2][3:5], 16), int(color1[2][5:7], 16)],
    ])

    c2 = sorted([
        [int(color2[0][1:3], 16), int(color2[0][3:5], 16), int(color2[0][5:7], 16)],
        [int(color2[1][1:3], 16), int(color2[1][3:5], 16), int(color2[1][5:7], 16)],
        [int(color2[2][1:3], 16), int(color2[2][3:5], 16), int(color2[2][5:7], 16)],
    ])
# np.linalg.norm это функция вычисления дистанции между векторами
    res = [
        np.linalg.norm(np.asarray(c1[0]) - np.asarray(c2[0])),
        np.linalg.norm(np.asarray(c1[1]) - np.asarray(c2[1])),
        np.linalg.norm(np.asarray(c1[2]) - np.asarray(c2[2])),
    ]

    n_c = get_index(img1)
    n_f = get_index(img2)

    if np.linalg.norm(res) < 56 and n_f >= n_c and n_f-n_c <= 3:
        return True
    else:
        False
