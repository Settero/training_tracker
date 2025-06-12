import pandas as pd
# import matplotlib as plt
import numpy as np
from datetime import datetime
import os

# Константы программы.
CSV_FILE = 'data/workouts.csv'
FORMAT = '%d.%m.%Y'
COLUMNS = ['Упражнение', 'Повторения', 'Подходы', 'Вес', 'Дата']
REQUIRED_INDEX = [0, 1, 2]


def input_get_working():
    ''' Функция получения данных об упражнении от пользователя. '''
    print(
        'Введите информацию об упражнении в формате: '
        'Название, Повторения, Подходы, Вес (по желанию), '
        'дату (оставьте поле пустым, чтобы поставилась сегодняшняя дата). \n'
        'Чтобы оставить поле пустым - укажите "-"'
    )
    ercise = input().split(', ')
    return ercise


def get_working(ercise: list, data: pd.DataFrame):
    ercise = [np.nan if cell == '-' else cell for cell in ercise]
    if data_check(ercise):
        add_row_data(ercise, data)
        return True
    return False


def add_row_data(ercise: list, data: pd.DataFrame):
    data.loc[len(data)] = ercise
    save_file(data)


def data_check(ercise: list):
    for index in REQUIRED_INDEX:
        if pd.isna(ercise[index]) or str(ercise[index]).strip() == '':
            validation_error(
                f'Обязательное поле {COLUMNS[index]} не заполнено')
            return False
    try:
        # Проверка на ввод даты
        if pd.isna(ercise[4]):
            ercise[4] = datetime.now().strftime(FORMAT)
        else:
            datetime.strptime(ercise[4], FORMAT)

        # Проверка на тип данных названия упражнения
        if str(ercise[0]).isdigit():
            raise ValueError("Поле 'Упражнение' должго быть текстом.")

        # Проверка на тип данных подходов
        ercise[2] = int(ercise[2])

        if not pd.isna(ercise[3]):
            ercise[3] = float(ercise[3])
        # Проверка на тип данных Повторений
        ercise[1] = int(ercise[1])

        return True

    except ValueError as error_type:
        validation_error(f'Ошибка в типах данных: {error_type}')
        return False


def validation_error(error_text):
    raise ValueError(error_text)


def read_file():
    '''
    Функция чтения файла БД. Если файла нет или он пустой,
    то создается новый файл.
    '''
    if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
        data = pd.read_csv(CSV_FILE)
    else:
        data = pd.DataFrame(columns=COLUMNS)
    return data


def save_file(data):
    ''' Функция сохранения файла БД. '''
    data.to_csv(CSV_FILE, index=False)


def ploter():
    ''' Функция построения графиков '''
    pass


def menu(data):
    while True:
        print(
            'Меню: \n '
            '1. Добавление упражнения \n '
            '2. Построение графика \n '
            '0. Выход')
        choice = int(input('Выберите функцию: '))
        if choice == 1:
            ercise = input_get_working()
            get_working(ercise, data)
        elif choice == 2:
            pass
        elif choice == 0:
            break
        else:
            print('Неверный выбор')


def main():
    data = read_file()
    menu(data)


main()
