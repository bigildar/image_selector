import sqlite3
import random

__connection = None


def get_connection():
    global __connection
    if __connection is None:
        __connection = sqlite3.connect('bd_img.db')
    return __connection


def init_db(force: bool = False):
    """ Проверить что нужные таблицы существуют, иначе создать их
        Важно: миграции на такие таблицы вы должны производить самостоятельно!
        :param conn: подключение к СУБД
        :param force: явно пересоздать все таблицы
    """
    conn = get_connection()
    c = conn.cursor()
    # Информация о пользователе
    # TODO: создать при необходимости...
    # Сообщения от пользователей
    if force:
        c.execute('DROP TABLE IF EXISTS images')
        c.execute('DROP TABLE IF EXISTS albums')

    c.execute('''
            CREATE TABLE IF NOT EXISTS images (
            id          INTEGER PRIMARY KEY,
            name        TEXT NOT NULL,
            hash        TEXT NOT NULL,
            red         TEXT NOT NULL,
            green       TEXT NOT NULL,
            blue        TEXT NOT NULL
        )
    ''')
    c.execute('''
            CREATE TABLE IF NOT EXISTS albums (
            id          INTEGER PRIMARY KEY,
            list        TEXT NOT NULL
        )
    ''')
    # Сохранить изменения
    conn.commit()


def add_images(name: str, hash: str, red: str, green: str, blue: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO images (name, hash, red, green, blue) VALUES (?, ?, ?, ?, ?)',
              (name, hash, red, green, blue))
    conn.commit()


def add_list(list: str,):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO albums (list) VALUES (?)',
              (list,))
    conn.commit()


def get_images(name: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT red, green, blue FROM images WHERE name = ?',
              (name,))
    s = c.fetchall()
    return s[0]


def get_index(name: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT id FROM images WHERE name = ?',
              (name,))
    (s,) = c.fetchone()
    return s


def find_hash(hash: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT id FROM images WHERE hash = ?',
              (hash,))
    s = c.fetchone()
    if s:
        return False
    else:
        return True


def get_list(id: int,):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT list FROM albums WHERE id = ?',
              (id,))
    (s,) = c.fetchall()
    return s[0]


def count_id():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT COUNT (id) FROM albums')
    (n,) = c.fetchall()
    return n[0]


if __name__ == '__main__':
    init_db()
