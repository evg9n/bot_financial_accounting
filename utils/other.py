from datetime import date


def update_date(d: date) -> str:
    """преобразует из даты ГГГГ-ММ-ДД в ДД.ММ.ГГГГ"""
    d = str(d).split('-')
    return '.'.join(d[::-1])
