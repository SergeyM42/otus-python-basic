import os
import json
global_result_search = 0
global_selected_file = ''
menu_1 = [
    """
    1. Открыть файл/показать список файлов
    2. Создать файл телефонной книги
    3. Показать все контакты
    4. Создать контакт
    5. Найти контакт
    6. Изменить контакт
    7. Удалить контакт
    8. Выход
    ---
    9. Удалить файл телефонной книги
    """
]


def chk_main_menu_selection():
    while True:
        choice = input('Выберите действие: ')
        if choice.isdigit() and 0 < int(choice) < 10:
            return choice
        print('Введена неверная опция')


def search_files_phone_books():
    results = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.json'):
                result = (os.path.join(root, file))
                results.append(result.strip('./'))
    return results


def create_file(file_path):
    if file_path == 'отмена':
        return run()
    if file_path.endswith('.json'):
        with open(file_path, 'x', encoding='UTF-8'):
            print(f'{file_path} файл успешно создан')
    else:
        file_path = file_path + '.json'
        with open(file_path, 'x', encoding='UTF-8'):
            print(f'{file_path} файл успешно создан')


def chk_open_file_menu_selection():
    while True:
        choice = input('Создать новую книгу? 1 - Да / 2 - Нет: ')
        if choice.isdigit() and 0 < int(choice) < 3:
            return choice
        print('Введена неверная опция')


def select_file():
    global global_selected_file
    results = search_files_phone_books()
    if not results:
        print('Телефонная книга не обнаружена')
        while True:
            choice = chk_open_file_menu_selection()
            if choice == '1':
                create_file(input('Введите имя файла: '))
                return False
            elif choice == '2':
                return False
    num_of_dir = len(results)
    if num_of_dir > 1:
        num = 0
        for dir_1 in results:
            num += 1
            print(f'{num}. {dir_1}')
        try:
            choice1 = int(input(f'Найдено {num_of_dir} файла, выберете нужный: '))
            if 1 <= choice1 <= num_of_dir:
                selected_file_path = results[choice1 - 1]
                print(f"Вы выбрали: {selected_file_path}")
                with open(selected_file_path, 'r') as file:
                    if file.readable() and file.read() == '':
                        print("Файл пустой")
                        global_selected_file = selected_file_path
                        return global_selected_file
                    global_selected_file = selected_file_path
                    return global_selected_file
            else:
                print("Неверный номер. Пожалуйста, выберите номер из списка.")
        except ValueError:
            print("Введена неверная опция")
    else:
        selected_file_path = results[0]
        print(f'Выбран файл {selected_file_path}')
        with open(selected_file_path, 'r') as file:
            if file.readable() and file.read() == '':
                print("Файл пустой")
                global_selected_file = selected_file_path
                return global_selected_file
            else:
                global_selected_file = selected_file_path
                return global_selected_file


def contact_id():
    data = open_file(global_selected_file)
    next_id = 1
    if not data:
        return next_id
    else:
        next_id = max(int(key) for key in data.keys()) + 1
        return next_id


def open_file(file):
    try:
        with open(file, 'r', encoding='UTF-8') as json_file:
            return json.load(json_file)
    except json.decoder.JSONDecodeError:
        return dict()


def save_file(contact_data, file):
    with open(file, 'w', encoding='UTF-8') as json_file:
        json.dump(contact_data, json_file)


def add_contact():
    data = open_file(global_selected_file)
    input_name = str(input('Введите имя: '))
    if input_name == 'отмена':
        return run()
    else:
        input_phone = int(input('Введите телефон: '))
        input_city = str(input('Введите город: '))
        data[contact_id()] = {'name': input_name.title(),
                              'phone': input_phone,
                              'city': input_city.title()
                              }
        save_file(data, global_selected_file)
        print('Контакт добавлен')


def count_decorations():
    max_length_deco = 1
    phone_db = open_file(global_selected_file)
    length_deco = []
    for key, value in phone_db.items():
        relative_len = len(f'{key}. {value["name"]} {value["phone"]} {value["city"]} ')
        length_deco.append(relative_len)
        max_length_deco = max(length_deco) + 45
    return max_length_deco


def show_contacts():
    if not open_file(global_selected_file):
        print('Список контактов пуст')
    else:
        phone_db = open_file(global_selected_file)
        print('=' * count_decorations())
        print('   id  name                           phone           city')
        print('=' * count_decorations())
        for key, value in phone_db.items():
            print(f'{key: >5}. {value["name"]: <30} {value["phone"]: <15} {value["city"]: <15} ')
        print('=' * count_decorations())


def search_contact():
    global global_result_search
    show_contacts()
    data = open_file(global_selected_file)
    user_search = input('Введите запрос: ')
    if not user_search.strip():
        print('Некорректный запрос')
    elif user_search.strip().isdigit():
        user_search_num = int(user_search)
        print('=' * count_decorations())
        print('   id  name                           phone           city')
        print('=' * count_decorations())
        for key, value in data.items():
            if user_search_num in value.values() or user_search in value.values():
                global_result_search = value
                print(f'{key: >5}. {value["name"]: <30} {value["phone"]: <15} {value["city"]: <15} ')
        print('=' * count_decorations())
    else:
        search_lower = user_search.lower().strip()
        search_upper = user_search.upper().strip()
        search_title = user_search.title().strip()
        print('=' * count_decorations())
        print('   id  name                           phone           city')
        print('=' * count_decorations())
        for key, value in data.items():
            if search_lower in value.values() or search_upper in value.values() or search_title in value.values():
                global_result_search = value
                print(f'{key: >5}. {value["name"]: <30} {value["phone"]: <15} {value["city"]: <15} ')
        print('=' * count_decorations())
    if not global_result_search:
        print('Ничего не найдено')


def chk_main_menu_selection1111():
    while True:
        choice = input('Выберите действие: ')
        if choice.isdigit() and 0 < int(choice) < 10:
            return choice
        print('Введена неверная опция')


def change_contact():
    list_key = []
    show_contacts()
    choice = input('Выберете id контакта который желаете изменить: ')
    data = open_file(global_selected_file)
    list_id = []
    for key in data.keys():
        list_id.append(key)
    if choice in list_id:
        print('У выбранного контакта имеются следующие атрибуты: ')
        data = open_file(global_selected_file)
        for key in data[choice].keys():
            list_key.append(key)
        print(list_key)
        choice_attribute = input('Какой атрибут вы желаете изменить? ')
        if choice_attribute in list_key:
            if choice_attribute in data[choice].keys():
                new_name = input('Введи новое значение атрибута: ')
                data[choice][choice_attribute] = new_name
            save_file(data, global_selected_file)
            show_contacts()
        else:
            print('Введено неверное значение атрибута')
            run()
    else:
        print('Введён неверный id')
        run()


def delete_contact():
    show_contacts()
    choice = input('Выберете id контакта который желаете удалить: ')
    data = open_file(global_selected_file)
    list_id = []
    for key in data.keys():
        list_id.append(key)
    if choice in list_id:
        data = open_file(global_selected_file)
        del data[choice]
        save_file(data, global_selected_file)
        print(f'Контакт с id {choice} удалён')
        show_contacts()
    else:
        print('Введена неверная опция')


def delete_file():
    results = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.json'):
                result = (os.path.join(root, file))
                results.append(result)
    print('---')
    for result in results:
        print(result.split('./')[1])
    deleting_file = input('Введите имя файла который желаете удалить: ')
    if deleting_file == 'отмена':
        return run()
    else:
        if os.path.exists(deleting_file):
            choice = input(f'Вы действительно хотите удалить файл {deleting_file}, введите Да или Нет: ')
            if choice == 'Да':
                os.remove(deleting_file)
            elif choice == 'Нет':
                print('Удаление отменено')
                run()
            else:
                print('Неверная команда, используйте только Да или Нет')
                run()
            print('Выбранный файл удалён')
        else:
            print('Введено неверное имя файла')
        pass


def run():
    while True:
        for str_menu_1 in menu_1:
            print(str_menu_1)
        choice = chk_main_menu_selection()
        if choice == '1':
            select_file()
        elif choice == '2':
            print('Для отмены введите ключевое слово "отмена"')
            try:
                create_file(input('Введите имя файла: '))
            except FileExistsError:
                print('Файл с таким именем существует')
        elif choice == '3':
            if not global_selected_file:
                print('Файл не выбран')
            else:
                show_contacts()
        elif choice == '4':
            try:
                if not global_selected_file:
                    print('Файл не выбран')
                else:
                    print('Для отмены введите ключевое слово "отмена"')
                    add_contact()
            except ValueError:
                print('Телефонный номер не может содержать буквы')
        elif choice == '5':
            if not global_selected_file:
                print('Файл не выбран')
            else:
                search_contact()
        elif choice == '6':
            if not global_selected_file:
                print('Файл не выбран')
            else:
                change_contact()
        elif choice == '7':
            if not global_selected_file:
                print('Файл не выбран')
            else:
                delete_contact()
        elif choice == '8':
            break
        elif choice == '9':
            print('Для отмены введите ключевое слово "отмена"')
            delete_file()


if __name__ == '__main__':
    run()
