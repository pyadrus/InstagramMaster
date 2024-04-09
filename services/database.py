import sqlite3


def get_instagram_posts(table):
    """Получение постов из базы данных"""
    with sqlite3.connect('instagram_posts.db') as conn:  # Подключаемся к базе данных SQLite
        cursor = conn.cursor()  # Создаем курсор
        cursor.execute(f'SELECT {table} FROM {table}')
        all_posts = cursor.fetchall()
    return all_posts


def database_for_instagram_posts(table):
    """Создание таблицы для базы данных постов instagram"""
    with sqlite3.connect('instagram_posts.db') as conn:  # Подключаемся к базе данных SQLite
        cursor = conn.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} ({table})")  # Создаем таблицу, если её нет
        conn.commit()

    return conn, cursor


def removing_duplicates_from_the_database(cursor, conn, table) -> None:
    """Удаление дубликатов с базы данных"""
    # После завершения парсинга и вставки данных
    # Шаг 1: Считать данные из базы данных
    cursor.execute(f'SELECT DISTINCT {table} FROM {table}')
    all_posts = cursor.fetchall()
    # Шаг 2: Удалить дубликаты
    # Создать множество для хранения уникальных значений
    unique_posts = set()
    # Итерироваться по всем данным и добавлять их в множество
    for post in all_posts:
        unique_posts.add(post[0])
    # Шаг 3: Записать очищенные данные обратно в базу данных
    # Очистить таблицу перед вставкой обновленных данных
    cursor.execute(f'DELETE FROM {table}')
    # Вставить уникальные посты обратно в базу данных
    for post_url in unique_posts:
        cursor.execute(f'INSERT INTO {table} ({table}) VALUES (?)', (post_url,))
    # Завершить транзакцию
    conn.commit()
    conn.close()  # Закрываем соединение с базой данных
