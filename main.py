import os
import json

GLOBAL_RESULT_SEARCH = 0
GLOBAL_SELECTED_FILE = ''
MENU_1 = [
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
    """
    Функция реализует проверку ввода выбора пунктов в главном меню.
    :return: Число от 1 до 9
    """
    while True:
        choice = input('Выберите действие: ')
        if choice.isdigit() and 0 < int(choice) < 10:
            return choice
        print('Введена неверная опция')


def search_files_phone_books():
    """
    Функция реализует поиск файлов с расширением json в корневой директории проекта
    :return: Список файлов
    """
    results = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.json'):
                result = (os.path.join(root, file))
                results.append(result.strip('./'))
    return results


def create_file(file_path):
    """
    Функция создаёт файл с расширением json
    :param file_path: Пусть до файла
    :return: Файл *.fson
    """
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
    """
    Функция проверки ввода в суб меню при создании новой телефонной книги
    :return: int(choice) от 1 до 2
    """
    while True:
        choice = input('Создать новую книгу? 1 - Да / 2 - Нет: ')
        if choice.isdigit() and 0 < int(choice) < 3:
            return choice
        print('Введена неверная опция')


def select_file():
    """
    Функция реализует выбор файла телефонной книги и
    если файл отсутствует в корневой директории программы, предлагает его создать
    :return:
    """
    global GLOBAL_SELECTED_FILE
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
            choice1 = int(input(f'Файлов найдено: {num_of_dir}\nВыберете нужный: '))
            if 1 <= choice1 <= num_of_dir:
                selected_file_path = results[choice1 - 1]
                print(f"Вы выбрали: {selected_file_path}")
                with open(selected_file_path, 'r') as file:
                    if file.readable() and file.read() == '':
                        print("Файл пустой")
                        GLOBAL_SELECTED_FILE = selected_file_path
                        return GLOBAL_SELECTED_FILE
                    GLOBAL_SELECTED_FILE = selected_file_path
                    return GLOBAL_SELECTED_FILE
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
                GLOBAL_SELECTED_FILE = selected_file_path
                return GLOBAL_SELECTED_FILE
            else:
                GLOBAL_SELECTED_FILE = selected_file_path
                return GLOBAL_SELECTED_FILE


def contact_id():
    """
    Функция создаёт id контакта, если файл телефонной книги пуст то id = 1, иначе находится
    максимальный доступный ключ контакта и к нему прибавляется единица
    :return: int(next_id)
    """
    data = open_file(GLOBAL_SELECTED_FILE)
    next_id = 1
    if not data:
        return next_id
    else:
        next_id = max(int(key) for key in data.keys()) + 1
        return next_id


def open_file(file):
    """
    Функция открывает выбранный json файл на чтение, возвращает файл телефонной книги,
    если словарь не был распознан как json файл то возвращает пустой словарь
    :param file: путь до файла
    :return: dict()
    """
    try:
        with open(file, 'r', encoding='UTF-8') as json_file:
            return json.load(json_file)
    except json.decoder.JSONDecodeError:
        return dict()


def save_file(contact_data, file):
    """
    Функция сохраняет выбранный файл
    :param contact_data: данные контакта для записи в файл
    :param file: путь до файла
    :return:
    """
    with open(file, 'w', encoding='UTF-8') as json_file:
        json.dump(contact_data, json_file)


def add_contact():
    """
    Функция добавляет новый контакт в файл телефонной книги
    :return:
    """
    data = open_file(GLOBAL_SELECTED_FILE)
    input_name = str(input('Введите имя: '))
    if input_name == 'отмена':
        return run()
    else:
        input_surname = str(input('Введите фамилию: '))
        input_phone = int(input('Введите телефон: '))
        input_city = str(input('Введите город: '))
        data[contact_id()] = {'name': input_name.title(),
                              'surname': input_surname.title(),
                              'phone': input_phone,
                              'city': input_city.title()
                              }
        save_file(data, GLOBAL_SELECTED_FILE)
        print('Контакт добавлен')


def count_decorations():
    """
    Функция выводи декоративные разделите для разграничения вывода контактов телефонной книги,
    количество зависит от максимальной длинны строки контакта, плюс статическая поправка на отступы
    :return:
    """
    max_length_deco = 1
    phone_db = open_file(GLOBAL_SELECTED_FILE)
    length_deco = []
    for key, value in phone_db.items():
        relative_len = len(f'{key}. {value["name"]} {value["surname"]} {value["phone"]} {value["city"]} ')
        length_deco.append(relative_len)
        max_length_deco = max(length_deco) + 45
    return max_length_deco


def show_contacts():
    """
    Функция отображает список контактов в телефонной книге
    :return:
    """
    if not open_file(GLOBAL_SELECTED_FILE):
        print('Список контактов пуст')
    else:
        phone_db = open_file(GLOBAL_SELECTED_FILE)
        print('=' * count_decorations())
        print('   id  name            surname         phone           city')
        print('=' * count_decorations())
        for key, value in phone_db.items():
            print(f'{key: >5}. {value["name"]: <15} {value["surname"]: <15} {value["phone"]: <15} {value["city"]: <15} ')
        print('=' * count_decorations())


def search_contact():
    """
    Функция поиска контактов в телефонной книге, ведёт поиск по полному совпадению любого значения без учёта регистра
    :return:
    """
    global GLOBAL_RESULT_SEARCH
    show_contacts()
    data = open_file(GLOBAL_SELECTED_FILE)
    user_search = input('Введите запрос: ')
    if not user_search.strip():
        print('Некорректный запрос')
    elif user_search.strip().isdigit():
        user_search_num = int(user_search)
        print('=' * count_decorations())
        print('   id  name            surname         phone           city')
        print('=' * count_decorations())
        for key, value in data.items():
            if user_search_num in value.values() or user_search in value.values():
                GLOBAL_RESULT_SEARCH = value
                print(f'{key: >5}. {value["name"]: <15} {value["surname"]: <15} {value["phone"]: <15} {value["city"]: <15} ')
        print('=' * count_decorations())
    else:
        search_lower = user_search.lower().strip()
        search_upper = user_search.upper().strip()
        search_title = user_search.title().strip()
        print('=' * count_decorations())
        print('   id  name            surname         phone           city')
        print('=' * count_decorations())
        for key, value in data.items():
            if search_lower in value.values() or search_upper in value.values() or search_title in value.values():
                GLOBAL_RESULT_SEARCH = value
                print(f'{key: >5}. {value["name"]: <15} {value["surname"]: <15} {value["phone"]: <15} {value["city"]: <15} ')
        print('=' * count_decorations())
    if not GLOBAL_RESULT_SEARCH:
        print('Ничего не найдено')


def change_contact():
    """
    Функция реализует изменение выбранного контакта
    :return:
    """
    list_key = []
    show_contacts()
    choice = input('Выберете id контакта который желаете изменить: ')
    data = open_file(GLOBAL_SELECTED_FILE)
    list_id = []
    for key in data.keys():
        list_id.append(key)
    if choice in list_id:
        print('У выбранного контакта имеются следующие атрибуты: ')
        data = open_file(GLOBAL_SELECTED_FILE)
        for key in data[choice].keys():
            list_key.append(key)
        print(list_key)
        choice_attribute = input('Какой атрибут вы желаете изменить? ')
        if choice_attribute in list_key:
            if choice_attribute in data[choice].keys():
                new_name = input('Введи новое значение атрибута: ')
                data[choice][choice_attribute] = new_name
            save_file(data, GLOBAL_SELECTED_FILE)
            show_contacts()
        else:
            print('Введено неверное значение атрибута')
            run()
    else:
        print('Введён неверный id')
        run()


def delete_contact():
    """
    Функция реализует удаление выбранного контакта по id контакта
    :return:
    """
    show_contacts()
    choice = input('Выберете id контакта который желаете удалить: ')
    data = open_file(GLOBAL_SELECTED_FILE)
    list_id = []
    for key in data.keys():
        list_id.append(key)
    if choice in list_id:
        data = open_file(GLOBAL_SELECTED_FILE)
        del data[choice]
        save_file(data, GLOBAL_SELECTED_FILE)
        print(f'Контакт с id {choice} удалён')
        show_contacts()
    else:
        print('Введена неверная опция')


def delete_file():
    """
    Функция реализует удаление выбранного файла телефонной книги по имени файла
    :return:
    """
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
    """
    Функция главного меню программы, отображает основное меню и реализует функционал выбора действий
    :return:
    """
    while True:
        for str_menu_1 in MENU_1:
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
            if not GLOBAL_SELECTED_FILE:
                print('Файл не выбран')
            else:
                show_contacts()
        elif choice == '4':
            try:
                if not GLOBAL_SELECTED_FILE:
                    print('Файл не выбран')
                else:
                    print('Для отмены введите ключевое слово "отмена"')
                    add_contact()
            except ValueError:
                print('Телефонный номер не может содержать буквы')
        elif choice == '5':
            if not GLOBAL_SELECTED_FILE:
                print('Файл не выбран')
            else:
                search_contact()
        elif choice == '6':
            if not GLOBAL_SELECTED_FILE:
                print('Файл не выбран')
            else:
                change_contact()
        elif choice == '7':
            if not GLOBAL_SELECTED_FILE:
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
