import os
import shutil
import random
import numpy as np
from image import CalcImageHash  # Функция вычисления хеша картинок
from color import colorz  # Функция поиск доминирующих цветов
from base import init_db  # Бза данных
from base import add_images  # Функция БД. Добавление картинки в базу
from base import get_images  # Функция БД. Взятие картинки из базы
from base import get_index  # Функция БД. Взятие индекса картинки из базы
from base import find_hash  # Функция БД. Поиск хеша картинки в базе
from base import add_list  # Функция БД. Добавление списка картинок в альбоме
from base import get_list  # Функция БД. Взяие списка картинок в альбоме
from base import count_id  # Функция БД. Счетчик записей в базе
from comparison_color import comparison  # Функция сравнения цвета

init_db(True)

path = ""  # Путь откуда берем картинки
path_to = ""  # Путь куда кдалем их после обработки

##############################################
# # В этой части берем картинки из дериктории, находим хеш и доминирующие цвета и заносим в базу
a = os.listdir(path)
dublikat = 0
for i in a:
    hash = CalcImageHash(path+i)
    if find_hash(hash):
        c = colorz(path+i, n=3)
        c = list(c)
        add_images(i, hash, c[0], c[1], c[2])
        print(i)
    else:
        dublikat = dublikat+1
        os.remove(path+i)
print(f"Тут {dublikat} дубликатов")
##################################################
# В этой части на основе данных по цветам, мы сравниваем картинки и формируем списки картинок для альбомов
# и заносим в отдельную тацлицу в базе
a = os.listdir(path)
for img1 in a:
    h = []
    if os.path.isfile(path+img1):
        for img2 in a:
            if os.path.isfile(path+img2):
                if comparison(img1, img2):
                    h.append(img2)
        for i in h:
            if h.index(i) != (get_index(i)-get_index(h[0])):
                h = h[0:h.index(i)]
                break
        slist = ' '.join(h)
        add_list(slist)
#####################################################
# # По сформированные спискам для альбомов формируем собственно альбомы и переносим в целевую дерикторию
# Одиночные картинки тоже переносим.
n = count_id()
for i in range(1, n+1):

    a = get_list(i).split(' ')
    for j in range(1, n+1):
        b = get_list(j).split(' ')
        if set(a) & set(b):
            a = sorted(list(set(a) | set(b)))

    if len(a) == 1 and os.path.isfile(path+a[0]):
        print(a)
        shutil.move(path+a[0], path_to)
    elif len(a) > 1:
        print(a)
        path_al = path_to+str(random.randint(1, 10000))
        if os.path.isfile(path+a[0]):
            while os.path.exists(path_al) is True:
                path_al = path_to+str(random.randint(1, 10000))
            os.mkdir(path_al)
            for i in a:
                print(i)
                shutil.move(path+i, path_al)

# init_db(True)
