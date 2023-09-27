from datetime import date
from typing import Union


def update_date(d: date) -> str:
    """преобразует из даты ГГГГ-ММ-ДД в ДД.ММ.ГГГГ"""
    d = str(d).split('-')
    return '.'.join(d[::-1])


def break_ranks(number: Union[float, int]) -> str:
    """
    Разбить число на разряды
    :param number: число
    :return: Возращает число разбитое на разряды в виде стоки
    """
    return '{0:,}'.format(round(number, 2)).replace(',', ' ')
