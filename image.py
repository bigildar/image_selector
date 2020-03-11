import cv2  # opencv-python
import difflib
import numpy as np
from PIL import Image

# Функция вычисления хэша. Взята с хабра


def CalcImageHash(FileName):
    image = cv2.imread(FileName)  # Прочитаем картинку
    sz1 = 32  # Уменьшим картинку
    resized = cv2.resize(image, (sz1, sz1), interpolation=cv2.INTER_AREA)
    # Переведем в черно-белый формат
    img = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    img = np.float32(img)  # float conversion/scale
    sz2 = 8
    img = cv2.resize(img, (sz2, sz2))  # Уменьшим картинку
    img = cv2.dct(img)  # the dct
    img = np.uint8(img)
    avg = img.mean()  # Среднее значение пикселя
    ret, threshold_image = cv2.threshold(
        img, avg, 255, 0)  # Бинаризация по порогу

    _hash = ""  # Рассчитаем хэш
    to_hash = threshold_image.ravel()
    for i in to_hash.tolist():
        _hash += str(int(i/255))
    return _hash


def CompareHash(hash1, hash2):  # сравнение хеша
    l = len(hash1)
    i = 0
    count = 0
    while i < l:
        if hash1[i] != hash2[i]:
            count = count+1
        i = i+1
    return count

# если больше 10 то это скорее всего разные картинки
# от 5 до 9 очень похожие
