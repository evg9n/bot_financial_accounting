from json import dump
from datetime import datetime
from os.path import abspath, join
from re import sub
from os import mkdir

from work_database.get import get_all_state, get_users, get_all_names_finance, get_all_finance_operations


def gener_list(list_data: list, state: bool = False, users: bool = False,
               finance_operations: bool = False, names_finance: bool = False) -> dict:

    if state:
        (id_, user_id, state, name_table, sum_operation, type_operation, finance_operations_id,
         categories_operation, message_id, date_, date2, max_sheet, current_sheet) = list_data
        return dict(id=id_, user_id=user_id, state=state, name_table=name_table, sum_operation=float(sum_operation),
                    type_operation=type_operation, finance_operations_id=finance_operations_id,
                    categories_operation=categories_operation, message_id=message_id,
                    date=str(date_), date2=str(date2), max_sheet=max_sheet, current_sheet=current_sheet)
    elif users:
        user_id, username, first_name, last_name, language_code, chat_id = list_data
        return dict(user_id=user_id, username=username, first_name=first_name, last_name=last_name,
                    language_code=language_code, chat_id=chat_id)

    elif finance_operations:
        (id_, user_id, name_table, sum_operation, type_operation,
         categories_operation, name_operation, date_) = list_data
        return dict(id=id_, user_id=user_id, name_table=name_table, sum_operation=float(sum_operation),
                    type_operation=type_operation, categories_operation=categories_operation,
                    name_operation=name_operation, date=str(date_))

    elif names_finance:
        id_, user_id, name_table = list_data
        return dict(id=id_, user_id=user_id, name_table=name_table)

    else:
        return dict()


def backup_db(user_id: int) -> bool:
    list_state = get_all_state()
    list_state = [gener_list(state, state=True) for state in list_state]

    list_users = get_users()
    list_users = [gener_list(user, users=True) for user in list_users]

    list_finance_operations = get_all_finance_operations()
    list_finance_operations = [gener_list(operation, finance_operations=True) for operation in list_finance_operations]

    list_names_finance = get_all_names_finance()
    list_names_finance = [gener_list(finance, names_finance=True) for finance in list_names_finance]

    result = dict(
        list_finance_operations=list_finance_operations,
        list_names_finance=list_names_finance,
        list_state=list_state,
        list_users=list_users
    )
    name_file = f'{user_id}_{datetime.now()}'
    name_file = sub(r'[\s\.]', '_', name_file)
    path_file = abspath(join('backups', f'{name_file}.json'))
    try:
        with open(path_file, mode='w', encoding='utf-8') as file:
            dump(result, file, indent=4, ensure_ascii=False)
    except FileNotFoundError:
        mkdir(abspath('backups'))
        with open(path_file, mode='w', encoding='utf-8') as file:
            dump(result, file, indent=4, ensure_ascii=False)

    return True
